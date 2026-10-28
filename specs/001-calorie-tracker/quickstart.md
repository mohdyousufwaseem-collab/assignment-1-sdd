# Quickstart: Calorie and Nutrition Tracker

This is the planned local setup and validation guide. The repository currently has no
application source, dependency manifests, or tests, so these commands become executable after
the implementation phase creates the planned files. No tests were run while preparing this plan.

## Prerequisites

- Windows 10/11 for the current assignment setup.
- Python 3.12 or later.
- Node.js 22 LTS and npm for frontend development and asset builds only.
- Internet access for the initial dependency installation; the built application must not
  require internet at runtime.

The SQLite database is stored under `%LOCALAPPDATA%\CalorieTracker\tracker.sqlite3` by default
and can be relocated with `CALORIE_TRACKER_DATA_DIR`. It must not be stored in the repository.

## Development Setup

After the planned dependency manifests exist:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r src\backend\requirements.txt
npm --prefix src\frontend ci
```

Run the API and frontend development server in separate terminals:

```powershell
$env:PYTHONPATH = "src\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```powershell
npm --prefix src\frontend run dev
```

The Vite development server proxies `/api` to the loopback API. The frontend must not call
external origins.

## Automated Checks

```powershell
$env:PYTHONPATH = "src\backend"
python -m pytest tests\backend
npm --prefix src\frontend test -- --run
```

Expected results: all backend validation, arithmetic, date, API, transaction, and persistence
tests pass; all client input-error and last-confirmed-state tests pass. Boundary suites must
include each inclusive minimum/maximum and values immediately outside them. Calculation tests
must verify multiplication, sum, exact-target/below/above comparisons, positive half-up
midpoints, uncapped progress, and the documented small-difference display case.

## Local Runtime and Acceptance Smoke Test

Build and run the single-process local application:

```powershell
npm --prefix src\frontend run build
$env:PYTHONPATH = "src\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The frontend build is configured to write into `src/backend/app/static`, which the local API
serves with the application entry point as the fallback for client-side routes. Open
`http://127.0.0.1:8000`. With internet disabled after setup, verify the following:

1. Add an entry with quantity `2.50`, `72.00` kcal, and `6.30` g protein per serving; confirm
   its contribution is `180.00` kcal and `15.75` g.
2. Edit the quantity to `3.00`; confirm contribution becomes `216.00` kcal and `18.90` g, with
   no old contribution remaining. Move the date and confirm only the new date contains it.
3. Delete the entry; confirm its contribution disappears and an empty day shows zero intake,
   current targets, full remaining amounts, zero excess/progress, and a no-entry message.
4. Save targets, close and reopen the app, and verify entries and targets remain. Change targets
   and confirm the new current targets are used for previous dates.
5. Test values below, at, and above each target. Confirm actual intake and progress are not
   capped and that remaining/excess reflect unrounded comparisons.
6. Submit blank/overlong names, malformed numeric text, signs, exponent notation, more than two
   fractional digits, zero quantity/targets, negatives, and values beyond every maximum. Confirm
   field-specific errors and unchanged saved data/totals.
7. Exercise failed create, edit, delete, and target writes using injected storage failures.
   Confirm an error is shown, no success is reported, and the last confirmed state remains.
8. Inspect browser network activity and confirm there are no requests to external origins.

This smoke test covers AC-001-AC-025, NFR-001/NFR-002, and SC-001-SC-005. Report actual results
when executed; this plan does not claim that they have passed.
