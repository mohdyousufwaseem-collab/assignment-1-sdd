---
description: "Implementation task list for Calorie and Nutrition Tracker"
---

# Tasks: Calorie and Nutrition Tracker

**Input**: Design documents from `specs/001-calorie-tracker/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Tests**: Test tasks are included because the specification has a mandatory User Scenarios & Testing section with independently verifiable acceptance criteria, and the quickstart defines automated checks. They verify implemented behavior; there is no requirement to write failing tests before implementation.

**Organization**: Tasks are grouped by user story in priority order: US1 (P1), US2 (P1), US4 (P1), then US3 (P2). Every story task identifies its specification coverage and exact implementation/test paths.

## Phase 1: Setup

**Purpose**: Create the frontend/backend project skeleton and installable dependency manifests.

- [X] T001 Create folders `src/backend/app/api`, `src/backend/app/domain`, `src/backend/app/storage`, `src/backend/app/static`, `src/frontend/src/api`, `src/frontend/src/features`, `tests/backend/unit`, `tests/backend/integration`, and `tests/frontend` per `specs/001-calorie-tracker/plan.md`
- [X] T002 [P] Create `src/backend/requirements.txt` with the planned FastAPI, Pydantic 2, Uvicorn, pytest, and httpx dependencies
- [X] T003 [P] Create `src/frontend/package.json` with the planned React 19, TypeScript, Vite, Vitest, and React Testing Library dependencies and development/build/test/typecheck scripts
- [X] T004 Configure `src/frontend/vite.config.ts` to proxy `/api` to `127.0.0.1:8000`, build assets into `src/backend/app/static`, and include `../../tests/frontend/**/*.{test,spec}.{ts,tsx}` in Vitest discovery
- [X] T005 Create `src/frontend/index.html`, `src/frontend/src/main.tsx`, `src/frontend/src/App.tsx`, `src/frontend/tsconfig.json`, and `src/frontend/tsconfig.app.json`; configure the React root mount and strict JSX/type checking. Completion criteria: `npm --prefix src/frontend run typecheck` and `npm --prefix src/frontend run build` both succeed, and the build writes assets to `src/backend/app/static` (depends on T003, T004)

---

## Phase 2: Foundational
- [X] T006 [P] Implement `src/backend/app/config.py` to use `%LOCALAPPDATA%\CalorieTracker` by default, allow `CALORIE_TRACKER_DATA_DIR` override, create the selected directory, and keep the SQLite file outside the repository
- [X] T007 [P] Create `src/backend/app/storage/schema.sql` with meal-entry and singleton-target tables; enforce the category set `Breakfast`, `Lunch`, `Dinner`, `Snack`, local calendar date format, quantity `0.01-100.00`, calories per serving `0.00-10000.00`, protein per serving `0.00-1000.00`, calorie target `1.00-100000.00`, and protein target `0.01-10000.00` as inclusive bounds
- [X] T008 Implement `src/backend/app/storage/database.py` to initialize the schema from T007, use the data path from T006, seed current targets to `2000.00` kcal and `50.00` g once, and provide transaction commit/rollback boundaries (depends on T006, T007)
- [X] T009 [P] Implement `src/backend/app/domain/numeric.py` to parse unsigned decimal strings with at most two fractional digits into integer hundredths, reject malformed or out-of-range values without float conversion, calculate unrounded totals, and format two-decimal amounts and one-decimal half-up progress
- [X] T010 [P] Define request/response schemas and shared error helpers in `src/backend/app/api/schemas.py` and `src/backend/app/api/errors.py` to match `specs/001-calorie-tracker/contracts/openapi.yaml`, including field-level `validation_failed`, `not_found`, and `persistence_failed` envelopes
- [X] T011 Compose the FastAPI application in `src/backend/app/main.py` and `src/backend/app/api/router.py`; include API routes, serve `src/backend/app/static`, bind only to `127.0.0.1`, and reject state-changing requests with an unexpected Host/Origin (depends on T008, T010)
- [X] T012 [P] Implement same-origin typed request helpers in `src/frontend/src/api/client.ts` for the operations and decimal-string contracts in `specs/001-calorie-tracker/contracts/openapi.yaml` (depends on T003, T004, T005)

**Checkpoint**: Backend storage, numeric rules, schemas, API composition, React bootstrap, frontend client, and build configuration are ready before story work begins.

---

### Implementation for User Story 1

- [X] T013 [US1] Implement meal persistence operations in `src/backend/app/storage/meals.py` for insert, lookup, full replacement, delete, and date-filtered reads using one transaction per mutation (depends on T008)
- [X] T014 [US1] Implement `src/backend/app/domain/meals.py` to validate and convert meal fields, calculate each contribution as quantity multiplied by per-serving values, and derive totals from saved entries without intermediate rounding (depends on T009, T013)
- [X] T015 [US1] Implement `POST /api/meals`, `PUT /api/meals/{mealId}`, and `DELETE /api/meals/{mealId}` in `src/backend/app/api/meals.py`, plus `GET /api/days/{date}` in `src/backend/app/api/days.py` to return selected-day meals and totals using the seeded current targets and the contract schemas (depends on T010, T011, T014)
- [X] T016 [P] [US1] Create the add/edit form in `src/frontend/src/features/meals/MealForm.tsx` with name, category, local date, quantity, kcal per serving, and protein per serving fields; submit decimal values as strings (depends on T005, T012)
- [X] T017 [US1] Create `src/frontend/src/features/meals/MealList.tsx` and `src/frontend/src/features/summary/DailyIntake.tsx` to show selected-day meals, actual totals, and zero intake with a no-entry state; expose edit/delete actions that refresh the confirmed day after successful API responses (depends on T012, T015, T016)
- [X] T018 [US1] Connect the meal form and list in `src/frontend/src/App.tsx` and load the selected day's meals through the API client (depends on T015, T017)

### Verification for User Story 1

- [X] T019 [P] [US1] Add API integration coverage for create, full edit, date change, delete, category values, committed responses, and entry visibility after reopening the same database per AC-001, AC-003-006 in `tests/backend/integration/test_meals.py` (depends on T015)
- [X] T020 [P] [US1] Add exact contribution and recomputation unit cases for 2.50 servings, quantity edits, date moves, and deletion per FR-003 and AC-002-005 in `tests/backend/unit/test_meal_totals.py` (depends on T014)

**Checkpoint**: AC-001-006 pass independently for creating, recalculating, moving, and deleting meal entries.

---

## Phase 4: User Story 2 - Set Targets and Read Progress (Priority: P1)

**Goal**: Configure current calorie/protein targets and display intake, remaining/excess amounts, and uncapped progress.

**Independent Test**: Set targets and compare below-target, exact-target, and above-target summaries; verify defaults and that a saved target change applies to historical dates.

### Implementation for User Story 2

- [X] T021 [US2] Implement singleton target read/update transactions in `src/backend/app/storage/targets.py`, replacing calorie and protein values atomically (depends on T008)
- [X] T022 [US2] Implement `src/backend/app/domain/targets.py` and extend `src/backend/app/domain/meals.py` to apply current targets to every selected date and calculate remaining, excess, and progress from unrounded totals (depends on T014, T021)
- [X] T023 [US2] Implement `GET /api/targets` and `PUT /api/targets` in `src/backend/app/api/targets.py`, returning current defaults or saved targets and reporting success only after commit (depends on T010, T011, T021, T022)
- [X] T024 [P] [US2] Create target inputs and nutrient progress presentation in `src/frontend/src/features/targets/TargetForm.tsx` and `src/frontend/src/features/summary/NutrientSummary.tsx` using decimal-string API values (depends on T012, T018)
- [X] T025 [US2] Connect targets and daily summary into `src/frontend/src/features/summary/DailySummary.tsx` and `src/frontend/src/App.tsx`; display actual intake, target, remaining or excess, and uncapped percentage (depends on T023, T024)

### Verification for User Story 2

These tests verify completed behavior; no test-first workflow is required.

- [X] T026 [P] [US2] Add API integration tests for default targets, atomic target replacement, and saved target values after reopening the same database per FR-006, FR-010, FR-017, AC-007-008 in `tests/backend/integration/test_targets.py` (depends on T023)
- [X] T027 [P] [US2] Add unit cases for below/equal/above comparisons, remaining/excess, uncapped progress, and half-up boundaries per FR-007, AC-009-011, SC-001, and SC-003 in `tests/backend/unit/test_progress.py` (depends on T022, T025)

**Checkpoint**: AC-007-011 pass independently for default/saved targets and below/equal/above progress states.

---

## Phase 5: User Story 4 - Keep Records Valid and Local (Priority: P1)

**Goal**: Reject invalid inputs with field-specific feedback, preserve confirmed data on failed writes, and keep all user data local.

**Independent Test**: Exercise every proposed field boundary and malformed input; inject failed create, edit, delete, and target writes; verify errors are clear, no failed operation is reported as saved, and the prior persisted view remains authoritative.

### Implementation for User Story 4

- [X] T028 [US4] Implement strict field validation in `src/backend/app/domain/validation.py`; trim names then require 1-80 characters, accept only the four specified categories and real local ISO dates through today, enforce each inclusive numeric range, and reject malformed strings before any write (depends on T009, T010)
- [X] T029 [US4] Map validation and missing-entry outcomes in `src/backend/app/api/errors.py` and `src/backend/app/api/meals.py`/`src/backend/app/api/targets.py` to field-specific 422 and not-found 404 responses without exposing database internals (depends on T028)
- [X] T030 [US4] Ensure write paths in `src/backend/app/storage/meals.py`, `src/backend/app/storage/targets.py`, and `src/backend/app/storage/database.py` roll back failed create/edit/delete/target operations and expose success only after commit (depends on T013, T021)
- [X] T031 [US4] Update `src/frontend/src/api/client.ts`, `src/frontend/src/features/meals/MealForm.tsx`, and `src/frontend/src/features/targets/TargetForm.tsx` to display field/persistence errors and preserve last-confirmed UI state without optimistic success (depends on T012, T016, T024, T029, T030)
- [X] T032 [US4] Enforce local-only delivery in `src/backend/app/main.py`, `src/frontend/vite.config.ts`, and `src/frontend/index.html`: loopback runtime, same-origin API/assets, no remote scripts/fonts/telemetry, and no permissive cross-origin access per FR-016, NFR-001/002, and AC-023-025 (depends on T011, T004, T005)

### Verification for User Story 4

These tests verify completed behavior and follow the relevant implementation tasks; they do not impose a test-first workflow.

- [X] T033 [P] [US4] Add parameterized API tests in `tests/backend/integration/test_validation.py`: accept trimmed names of 1/80 characters, categories Breakfast/Lunch/Dinner/Snack, real dates through today, quantity 0.01/100.00, kcal 0.00/10000.00, protein 0.00/1000.00, calorie target 1.00/100000.00, and protein target 0.01/10000.00; reject blank/81-character names, invalid category/date/future dates, values immediately outside every numeric bound, zero quantity/targets, negatives, signs, commas, exponent notation, malformed text, and excess precision per FR-012-015 and AC-019-022 (depends on T028, T029)
- [X] T034 [P] [US4] Inject storage/commit failures for create, edit, delete, and target update in `tests/backend/integration/test_persistence_failures.py`; assert error codes, no success response, rollback, and unchanged saved data per FR-011, NFR-003, AC-015-018, and SC-005 (depends on T015, T023, T030)
- [X] T035 [P] [US4] Test field-specific API errors and retention of last-confirmed meal/target state after failed requests in `tests/frontend/validation_and_failures.test.tsx` per FR-011, FR-015, AC-022, and SC-002 (depends on T031)

**Checkpoint**: AC-015-025, NFR-001-003, and SC-002/SC-005 pass for validation, failures, local use, and privacy.

---

## Phase 6: User Story 3 - Review Previous Days (Priority: P2)

**Goal**: Select a previous local date and inspect only its entries and summary, including the empty-day state.

**Independent Test**: Record meals on two dates, select each date and an empty past date, and verify date-specific entries, current targets, zero/remaining values, and no future-date selection.

### Implementation for User Story 3

- [X] T036 [US3] Extend `src/backend/app/storage/meals.py` with date-scoped meal reads and ensure date changes are visible only under the committed new date per FR-003, FR-004, and FR-008 (depends on T013)
- [X] T037 [US3] Extend `src/backend/app/domain/days.py` and `src/backend/app/api/days.py` to serve any valid historical date through today, reject future dates, and combine that date's entries with current global targets (depends on T015, T022, T036)
- [X] T038 [US3] Create `src/frontend/src/features/summary/CalendarDateControl.tsx` to select today or earlier dates and connect selection to `src/frontend/src/App.tsx`; show each selected date's entries and the existing empty state (depends on T025, T037)

### Verification for User Story 3

These tests verify completed behavior; no test-first workflow is required.

- [X] T039 [P] [US3] Add API tests for two-date isolation, past/today acceptance, future-date rejection, and empty-day summaries with current targets per FR-008/009, AC-012-014 in `tests/backend/integration/test_days.py` (depends on T036, T037)
- [X] T040 [P] [US3] Test date selection, future-date disabling, historical summary refresh, and empty-state display per AC-012-014 in `tests/frontend/history.test.tsx` (depends on T038)

**Checkpoint**: AC-012-014 pass independently for historical dates, date isolation, and empty days.

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Reproduce the setup and verify end-to-end behavior without adding scope.

- [X] T041 Review `specs/001-calorie-tracker/quickstart.md` against the implemented setup, build output, test commands, and offline smoke procedure; correct only commands or paths that differ from the implementation
- [X] T042 Run the backend and frontend suites plus the quickstart offline acceptance smoke test, then record actual commands, outcomes, and any unverified criteria in `docs/verification-results.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; T002 and T003 can run in parallel after T001; T004 follows T003; T005 follows T003/T004.
- **Phase 2 Foundational**: Begins after setup. T006, T007, T009, and T010 can proceed in parallel; T008 depends on T006/T007; T011 depends on T008/T010; T012 depends on T003/T004/T005.
- **Phase 3 US1**: Begins after the full foundation; delivers meal entry CRUD and the first usable tracking increment.
- **Phase 4 US2**: Depends on US1's meal-derived daily totals; adds target comparison and progress.
- **Phase 5 US4**: Depends on US1 and US2 mutation paths so validation, transaction failure, and confirmed-state behavior cover every operation.
- **Phase 6 US3**: Depends on US1 entries and US2 summaries/targets; adds previous-date navigation and empty history states.
- **Phase 7 Polish**: Depends on all desired stories being complete.

### User Story Dependencies

```text
Setup -> Foundational -> US1 (P1) -> US2 (P1) -> US4 (P1) -> US3 (P2) -> Polish
```

US2 requires saved meal totals for below/equal/above comparisons. US4 covers both meal and target writes, so it follows both. US3 uses the completed date-specific meal and summary behavior. The order follows the spec's priorities while respecting these data dependencies.

### Parallel Opportunities

- Setup: T002 and T003 initialize independent backend/frontend manifests; T004 follows T003 and T005 follows T004.
- Foundation: T006, T007, T009, and T010 can proceed in parallel after setup; T008 follows T006/T007, T011 follows T008/T010, and T012 follows the frontend setup.
- US1: T013 backend storage can proceed alongside T016 frontend form after the foundation; T019 and T020 verification tasks follow the story implementation and can run in parallel.
- US2: T021 target storage can proceed alongside T024 target UI after US1; T026 and T027 verification tasks follow story implementation and can run in parallel.
- US4: T033, T034, and T035 operate on separate verification files after their listed implementations; they can then run in parallel.
- US3: T039 and T040 operate on separate backend/frontend test files after implementation.

### Parallel Execution Examples

```text
US1 after the foundation:
- T013 meal persistence in src/backend/app/storage/meals.py
- T016 meal form in src/frontend/src/features/meals/MealForm.tsx

US1 verification after implementation:
- T019 API acceptance tests in tests/backend/integration/test_meals.py
- T020 arithmetic tests in tests/backend/unit/test_meal_totals.py

US4 verification after implementation:
- T033 validation boundary tests in tests/backend/integration/test_validation.py
- T034 transaction failure tests in tests/backend/integration/test_persistence_failures.py
- T035 client failure-state tests in tests/frontend/validation_and_failures.test.tsx
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 Setup and Phase 2 Foundational.
2. Complete Phase 3 US1 only: add, view, edit, and delete meals with correctly recomputed totals.
3. Stop and validate US1 against AC-001-006 before extending the product.

US1 is the suggested MVP because it is the highest-priority standalone user outcome. The app still needs the shared local foundation, but targets, historical navigation, and additional reliability polish are not prerequisites for demonstrating the first meal-entry increment.

### Incremental Delivery

1. Setup and foundation establish the local run path and data rules.
2. US1 delivers a meal diary and exact meal contributions.
3. US2 adds current targets, remaining/excess, and uncapped progress.
4. US4 completes exhaustive validation, failure-state handling, and offline/privacy requirements across writes.
5. US3 adds historical date selection and empty historical-day behavior.
6. Run cross-story checks and record actual verification results.
