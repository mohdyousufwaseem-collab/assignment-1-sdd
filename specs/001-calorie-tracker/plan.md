# Implementation Plan: Calorie and Nutrition Tracker

**Branch**: `001-calorie-tracker` | **Date**: 2026-10-28 | **Spec**: [spec.md](spec.md)

**Status**: Draft technical design for project-owner review; no mentor approval is represented.

**Input**: Existing feature specification, clarification log, requirements checklist, and project constitution.

## Summary

Build a locally runnable, single-user meal tracker with a React client, a Python FastAPI local
service, and a SQLite file. At runtime, FastAPI serves the built client and same-origin API from
loopback, so the app has no external runtime dependency. The backend owns validation, exact
calculations, and persistence. Store input values as scaled integer hundredths, aggregate using
Python integers, and round only for display. Write mutations in SQLite transactions and return
success only after commit.

## Technical Context

**Language/Version**: Python 3.12+; TypeScript 5+ for the React client; Node.js 22 LTS for development/build only.

**Primary Dependencies**: FastAPI, Pydantic 2, Uvicorn, React 19, Vite, SQLite via Python `sqlite3`; pytest/httpx, Vitest, and React Testing Library for verification.

**Storage**: One local SQLite database in the current user's application-data directory; Windows default `%LOCALAPPDATA%\CalorieTracker\tracker.sqlite3`, overridable by `CALORIE_TRACKER_DATA_DIR`.

**Testing**: pytest and FastAPI test client/httpx; Vitest and React Testing Library; documented end-to-end offline smoke test.

**Target Platform**: Windows 10/11 for the current assignment environment. Other operating-system support is not established by the input and remains an open portability question.

**Project Type**: Locally hosted web application with a browser client and local service.

**Performance Goals**: The specification defines no numeric latency or scale SLA. Keep local single-user reads and writes synchronous from the user's perspective; do not introduce a benchmark target absent a requirement.

**Constraints**: No login, external APIs, cloud sync, telemetry, remote fonts, or runtime network calls. Bind the service to `127.0.0.1`; after dependencies and assets are installed/built, core workflows work without internet. Persist every confirmed mutation before returning success. Treat user input and API responses as decimal strings at the boundary.

**Scale/Scope**: One local user, four fixed meal categories, two nutrients, current global targets, arbitrary retained local dates up to today; no multi-user concurrency or server deployment requirement.

## Constitution Check

### Pre-Design Gate

| Principle | Gate | Result |
|---|---|---|
| I. Simplicity and Appropriate Scope | Keep one client, one local service, and one embedded database; justify any additional dependency by a stated requirement. | Pass: React, FastAPI, and SQLite are the requested proposed stack; no added service. |
| II. Calculation Correctness | Define deterministic aggregation, comparison, and rounding without silent loss. | Pass: fixed-scale integers and explicit half-up display rules are in [data-model.md](data-model.md). |
| III. Input Validation | Validate all entry and target fields against the spec and reject invalid values before persistence. | Pass: contract and data model carry the spec's proposed accepted ranges and decimal format. |
| IV. Requirements Traceability | Design contracts, entities, and tests retain unique spec identifiers. | Pass: traceability is recorded below and in supporting artifacts. |
| V. Human Review | Generated design remains a draft; no review or approval is invented. | Pass: clarification log records project-author self-review of business assumptions and explicitly says no mentor/business-owner review. This technical plan still requires owner review. |
| VI. Privacy and Security | Store only scoped data locally; never send it externally or commit secrets. | Pass: loopback-only service, local database, no external runtime calls or secrets. |
| VII. Verification and Testing | Cover normal, invalid, boundary, edge, persistence, and failure cases and record results when executed. | Pass as a plan: [quickstart.md](quickstart.md) describes the verification gates; no implementation tests are claimed as run. |
| VIII. Maintainability | Use clear module boundaries and reproducible setup instructions. | Pass: proposed layout and quickstart provide both. |
| IX. Scope Control | Do not add unrequested features or deployment infrastructure. | Pass: no authentication, external services, extra nutrients, cloud, or deployment target. |

No constitution violations or unjustified complexity were identified. The proposed three-part
stack follows the explicitly requested evaluation and is kept local; no repository/service
pattern or separate database service is proposed.

## Architecture

At runtime, a single Uvicorn/FastAPI process binds to loopback, serves the built React files, and
exposes `/api` endpoints on the same origin. React owns input forms, date selection, summary
presentation, and transient request/error state. FastAPI owns request parsing, domain validation,
date rules, calculations, and transaction boundaries. A small storage module owns SQLite
connection setup and SQL; domain calculations do not depend on UI code. The browser never opens
the database directly.

During development, Vite serves the client and proxies `/api` to FastAPI. For normal use, the
client is built into `src/backend/app/static` and served by FastAPI, including the SPA entry
point for client-side routes; Node.js is not needed at runtime. The browser uses relative
same-origin URLs. Do not load scripts, fonts, analytics, nutrition data, or other resources from
remote origins. No CORS allowance is needed for the same-origin deployment.

Bind only to `127.0.0.1`, validate the expected local Host/Origin for state-changing requests,
and avoid permissive CORS. This limits network exposure but is not authentication: the intended
privacy boundary is the local OS account, not protection from other processes running as that
user or a person with access to the database file. Store no personal data beyond meal entries
and current targets; do not claim encryption.

## Persistence, Validation, and Failure Handling

Persist entry numeric values and targets as integer hundredths. Convert validated decimal input
strings directly to integers without binary floating point. Each create, edit, delete, or target
update is one SQLite transaction. Seed the single current-target row with the generic spec
defaults when the local database is first initialized. Keep no separately stored daily totals;
derive summaries from saved entries so edits/deletions cannot leave stale aggregates.

For writes, do not update confirmed client state optimistically. Return a success response only
after commit. On a database error, roll back where possible, return a `persistence_failed`
response without database details, and have the client keep the last confirmed state and show
the error. If persistence state is uncertain, reload the day/targets before displaying a state
as confirmed. Validation failures return field-specific errors and do not write. Full contracts
are in [contracts/openapi.yaml](contracts/openapi.yaml).

Represent dates as ISO calendar dates (`YYYY-MM-DD`), not timestamps. Use the local date of the
computer running the service, accept dates through today, reject future dates, and keep an
entry's date unchanged when viewing another day. Editing a date moves its contribution between
the old and new date summaries. Changing the single current target row intentionally changes
the comparison for all historical dates; no target history is stored.

## Traceability and Verification Strategy

| Design/test area | Specification coverage |
|---|---|
| Entry contract, categories, CRUD, date moves, persistence | FR-001–005, FR-008, FR-010; AC-001–006, AC-012, AC-014; SC-004 |
| Targets and daily comparison | FR-006–007, FR-017; AC-007–011, AC-013; SC-003 |
| Validation and error feedback | FR-012–015; AC-019–022; SC-002 |
| Local-only use and privacy | FR-016, NFR-001–002; AC-023–025 |
| Persistence failure/confirmed state | FR-011, NFR-003; AC-015–018; SC-005 |
| Exact arithmetic and rounding | FR-003, FR-007; AC-002–005, AC-009–011; SC-001, SC-003 |

Use unit tests for input parsing, range checks, fixed-scale arithmetic, half-up boundaries,
target comparisons, and date rules. Use API integration tests with a temporary SQLite file for
create/edit/delete/target transactions, restart persistence, empty days, historical summaries,
and injected write/commit failures. Use React tests for field-specific errors and retention of
the last confirmed state. Finish with a browser smoke test with internet disabled, checking that
all core workflows operate locally and that no external requests are made. Test valid values at
each inclusive minimum/maximum and invalid values immediately outside each boundary. No tests
have been executed in this planning step.

## Project Structure

### Documentation (this feature)

```text
specs/001-calorie-tracker/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── openapi.yaml
```

### Proposed Source Code (not created in this planning step)

```text
src/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── storage/
│   │   ├── static/      # Built frontend assets; generated during build
│   │   └── main.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── features/
    │   └── main.tsx
    └── package.json
tests/
├── backend/
│   ├── unit/
│   └── integration/
└── frontend/
```

**Structure Decision**: The existing `src/` and `tests/` directories are empty. Use one
repository with a frontend and backend subproject; keep backend domain logic and SQLite access
separate, and organize React by feature. This avoids separate repositories or deployable
services while allowing focused tests.

## Open Technical Question

The current environment is Windows, so the proposed default database path uses
`%LOCALAPPDATA%`. Confirm whether macOS/Linux support is required before implementation. If it
is, select platform-specific user-data paths and add setup/verification coverage for those
platforms. This is a portability question, not an unresolved business rule or stakeholder
decision.

## Post-Design Constitution Check

| Gate | Result after design |
|---|---|
| Scope and simplicity | Pass: one local browser app, one local API process, and SQLite; no external runtime service or extra product feature. |
| Correctness and validation | Pass: integer scaled storage, exact aggregation, unrounded comparisons, explicit display rounding, strict input parsing, and field-level errors are specified. |
| Traceability and verification | Pass: FR/NFR/AC/SC identifiers are retained in the plan and coverage matrix; quickstart links concrete checks. |
| Privacy and security | Pass: loopback binding, local-only storage/assets, no data transmission, and no secret storage are specified. |
| Maintainability and human review | Pass as design: modular layout and reproducible commands are documented; plan remains a draft for owner review, and no mentor approval is claimed. |

No post-design gate failures remain. The only open technical question is supported operating
systems, documented above; Windows is the plan's current target and does not block the proposed
local architecture.

## Complexity Tracking

No constitution violations. The React/FastAPI split is retained because it is the stack the user
asked to evaluate; serving both from one local process and using SQLite avoids additional runtime
services.
