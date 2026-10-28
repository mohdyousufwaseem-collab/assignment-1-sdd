# Research: Calorie and Nutrition Tracker

**Date:** 2026-10-28  
**Status:** Technical recommendations for the draft plan; no mentor approval is represented.

## Stack and Runtime Architecture

**Decision**: Use React 19 with TypeScript and Vite for the browser client, Python 3.12+ with
FastAPI/Pydantic 2 and Uvicorn for the local service, and SQLite through Python's standard
`sqlite3` module. At runtime, FastAPI serves the built frontend and same-origin `/api` routes
from one process bound to `127.0.0.1`. During development, Vite serves the client and proxies
`/api` to FastAPI.

**Rationale**: This matches the proposed stack in clarification Q-14 and the request to evaluate
it. A same-origin local deployment has one launch process, avoids production CORS configuration,
and needs no separate database service. Node is needed to build/develop the client, not to run
the built application.

**Alternatives considered**: A separately hosted frontend and API add a production process and
cross-origin configuration without a requirement. A desktop shell adds a platform dependency.
A CLI does not satisfy the requested browser-based tracker experience.

## Exact Numeric Representation

**Decision**: Parse accepted decimal strings into integer hundredths at the API boundary. Persist
quantity, per-serving nutrition values, and targets as SQLite `INTEGER` hundredths. Calculate
products and sums using Python integers; do not use binary floating point or SQLite floating
point aggregation.

**Rationale**: Inputs have at most two fractional digits and the spec defines half-up display
rounding. Fixed-scale integers preserve inputs exactly and make range checks, equality, target
comparisons, and summation deterministic. A product of quantity-hundredths and nutrient-
hundredths has scale 10,000. Accumulate in Python integers rather than relying on SQLite `SUM`,
whose integer accumulator is bounded.

For nutrient intake numerator `S = sum(quantity_hundredths * nutrient_per_serving_hundredths)`,
`S` is scaled by 10,000. For target `T` in hundredths, compare `S` with `100*T` before rounding.
The displayed amount in hundredths is half-up rounding of `S/100`, computed for nonnegative
integers as `(S + 50) // 100`. Remaining/excess use the positive raw difference and the same
conversion. Progress in tenths of a percent is half-up rounding of `10*S/T`, computed as
`(20*S + T) // (2*T)`. Format amounts with exactly two decimal places and progress with one.

**Alternatives considered**: `Decimal` parsed from strings and stored as canonical text can also
be exact, but requires careful context/rounding management and makes SQL-side validation and
aggregation less direct. SQLite `REAL` and JavaScript `Number` are rejected for authoritative
nutrition arithmetic because binary floating-point representation can make decimal boundaries
unreliable.

## Persistence and Failure Semantics

**Decision**: Use one local per-user SQLite database, with one transaction per create, edit,
delete, or target replacement. Send success only after commit. Derive day summaries from saved
meal rows rather than maintaining cached totals.

**Rationale**: SQLite is a small embedded store suitable for one local user. Transactions make
each mutation atomic. Derived summaries avoid stale aggregates after date edits or deletes.
Failed writes must preserve the last confirmed state as required by FR-011 and NFR-003.

**Alternatives considered**: Browser local storage would put persistence and validation in the
client. A server database adds an unneeded service. Stored aggregate rows add synchronization
risk without improving this scope.

## API Contract and Error Handling

**Decision**: Expose a small JSON API for selected-day summary, meal CRUD, and current targets.
Represent numeric request and response values as decimal strings. Use ISO dates. Return field
validation errors with HTTP 422, unknown meal IDs with 404, and persistence failures with a
distinct error code and no internal database details. See
[`contracts/openapi.yaml`](contracts/openapi.yaml).

**Rationale**: Decimal strings preserve accepted lexical precision across JavaScript and Python
boundaries. The summary endpoint returns entries and computed totals together for one date,
avoiding duplicated client calculations. Explicit error codes let the UI retain the last
confirmed state and distinguish rejected input from a failed persistence operation.

**Alternatives considered**: Numeric JSON values may be parsed as binary floating point in the
browser. Separate totals endpoints increase calls and risk inconsistent views. Optimistic
mutation success is rejected because the specification requires persistence confirmation.

## Date, Offline, and Privacy Boundaries

**Decision**: Store a calendar date as `YYYY-MM-DD`, with no timestamp or timezone conversion.
Use the local date of the computer running the service to reject future dates. Build frontend
assets into the local app and make no runtime calls to external origins. Bind the API to
loopback, use no permissive CORS, and validate the expected local Host/Origin for mutations.

**Rationale**: This follows FR-008, NFR-001/002, and clarification Q-12. The local browser and
service use the same local calendar and need no cross-timezone semantics. Offline means internet
is unnecessary after dependencies and assets are installed.

**Alternatives considered**: UTC timestamps can shift a meal between calendar dates and are not
needed for date-only records. Cloud persistence, external nutrition lookup, and remote assets
are out of scope.

## Testing Strategy

**Decision**: Use pytest/httpx for backend unit and API/database integration tests, Vitest with
React Testing Library for client validation and confirmed-state behavior, and a documented
browser smoke test with internet disabled.

**Rationale**: This covers deterministic calculation, accepted/rejected boundaries, all
mutations, database restart persistence, and the offline/privacy promise without requiring a
production service. See [`quickstart.md`](quickstart.md).

## Open Technical Question

The current environment is Windows. The plan proposes Windows 10/11 and `%LOCALAPPDATA%` for the
default database location. Confirm whether other operating systems are required before
implementation; if so, add platform-specific data-directory resolution and verification. This
does not change the business scope or require a stakeholder decision about nutrition behavior.
