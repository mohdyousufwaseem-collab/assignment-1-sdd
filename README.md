# Calorie and Nutrition Tracker

A locally runnable, single-user meal diary for recording foods and tracking daily calorie and
protein intake against editable targets. Meal data and targets are stored in a local SQLite
database. The browser app and API are served locally; no account or external nutrition service
is required.

This is Assignment 1 for a fundamentals project. The documented v1 target is Windows 10/11.

## Features

- Add, edit, and delete manually entered meals.
- Categorize meals as Breakfast, Lunch, Dinner, or Snack.
- Record serving quantity, calories per serving in kcal, and protein per serving in grams.
- View a selected date's entries, totals, current targets, remaining or excess amounts, and
  progress; select today or a previous date.
- Configure daily calorie and protein targets. First-run defaults are 2,000 kcal and 50 g;
  these are generic defaults, not personalized nutrition advice.
- Retain meals and targets between application restarts.
- Validate input and report field-specific errors. Failed writes are not reported as saved.

## Technology Stack

- **Frontend:** React 19, TypeScript, Vite, Vitest, React Testing Library.
- **Backend:** Python 3.12 or later, FastAPI, Pydantic 2, Uvicorn.
- **Storage:** SQLite through Python's standard `sqlite3` module.
- **Runtime:** One FastAPI process serves the built React files and same-origin API on loopback.
  Vite is used for frontend development.

## Project Structure

```text
assignment-1-sdd/
├── .gitignore
├── docs/
│   ├── clarification-log.md
│   └── verification-results.md
├── specs/
│   └── 001-calorie-tracker/
│       ├── checklists/requirements.md
│       ├── contracts/openapi.yaml
│       ├── data-model.md
│       ├── plan.md
│       ├── quickstart.md
│       ├── research.md
│       ├── spec.md
│       └── tasks.md
├── src/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/       # FastAPI routers, schemas, and error mapping
│   │   │   ├── domain/    # Validation, meal rules, and exact calculations
│   │   │   ├── storage/   # SQLite schema and persistence operations
│   │   │   ├── config.py  # Local database directory
│   │   │   └── main.py    # FastAPI entry point and static frontend serving
│   │   └── requirements.txt
│   └── frontend/
│       ├── src/
│       │   ├── api/       # Same-origin typed API client
│       │   ├── features/  # Meals, targets, daily summary, date control
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── package-lock.json
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       └── vite.config.ts
└── tests/
    ├── backend/
    │   ├── integration/
    │   └── unit/
    └── frontend/
```

The production frontend build is written to `src/backend/app/static/`. That directory is generated
and ignored by Git; build it before importing/starting the FastAPI application on a fresh checkout.

## Prerequisites

- Windows 10/11 and PowerShell.
- Python 3.12 or later. Python 3.14.7 was available in the current environment.
- Node.js 22 or later. `package.json` requires Node `>=22`; Node 24.21.0 was available here.
- npm. npm 11.19.0 was available here.
- Internet access for the initial package installation. The app's runtime workflows use loopback
  and local storage after setup.

The dependency files use compatible version ranges rather than pinning every Python package:
`src/backend/requirements.txt`, `src/frontend/package.json`, and the committed npm lockfile.

## Initial Setup

Run these commands from the repository root in PowerShell:

```powershell
python --version
node --version
npm --version

python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r src\backend\requirements.txt
npm --prefix src\frontend ci
```

Build the frontend at least once before starting FastAPI. This creates the ignored static
asset directory that FastAPI mounts at startup:

```powershell
npm --prefix src\frontend run build
```

## Run the Application

### Local Production Build

From the repository root, start the FastAPI process after building the frontend:

```powershell
$env:PYTHONPATH = "src\backend"
& .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000**. FastAPI serves the built React application and `/api` endpoints
from this same origin. FastAPI's interactive API documentation is available at
**http://127.0.0.1:8000/docs**.

### Development Mode

Keep the backend running as above. In a second PowerShell terminal, run:

```powershell
npm --prefix src\frontend run dev
```

Open **http://127.0.0.1:5173** (or the address Vite prints if that port is occupied). Vite proxies
`/api` requests to `http://127.0.0.1:8000`. The FastAPI process still needs the initial static
build so its static-file mount exists.

## API Overview

The API is local and same-origin in production. Numeric request/response values are decimal
strings, not JSON floating-point numbers.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/days/{entry_date}` | Get meals and derived calorie/protein summary for an ISO date on or before today. |
| `POST` | `/api/meals` | Create and persist a meal; returns the saved meal after commit. |
| `PUT` | `/api/meals/{meal_id}` | Replace a meal's editable fields; returns the saved meal after commit. |
| `DELETE` | `/api/meals/{meal_id}` | Delete a meal; returns `204` after commit. |
| `GET` | `/api/targets` | Get current targets, initially 2,000.00 kcal and 50.00 g. |
| `PUT` | `/api/targets` | Atomically replace current calorie and protein targets. |

The runtime FastAPI route parameter is named `entry_date`; the checked-in OpenAPI contract uses
`{date}` for the same path position. Dates use `YYYY-MM-DD`. Validation errors return `422`,
missing meal IDs return `404`, and persistence failures return `500` with a structured error.
Mutation success responses are sent only after the SQLite transaction commits.

## Input Validation and Calculations

- Food names are trimmed and must contain 1-80 characters after trimming.
- Categories are limited to Breakfast, Lunch, Dinner, and Snack.
- Entries can use a valid computer-local calendar date up to and including today; future dates
  are rejected.
- Numeric input must be an unsigned decimal string with at most two fractional digits. Signs,
  commas, exponent notation, malformed values, excess fractional digits, and out-of-range values
  are rejected.
- Quantity is 0.01-100.00 servings. Calories per serving are 0.00-10,000.00 kcal; protein per
  serving is 0.00-1,000.00 g. Zero nutrition values are allowed; zero quantity is not.
- Calorie targets are 1.00-100,000.00 kcal; protein targets are 0.01-10,000.00 g. Targets must
  be positive.

The backend stores numeric values as integer hundredths and computes contribution as quantity
multiplied by the per-serving value, summing without intermediate rounding. It compares unrounded
totals to targets, then formats amounts to two decimal places and progress to one decimal place
using round-half-up. Actual intake and progress are not capped at the target. Current targets
apply to historical dates; the v1 application does not keep target history.

An empty day has zero intake, current targets, the full target remaining, zero excess, zero
progress, and a no-meal state. If a create, edit, delete, or target update fails to persist, the
client does not claim success and continues to show the last confirmed state.

## Data and Privacy

By default, the SQLite database is stored at:

```text
%LOCALAPPDATA%\CalorieTracker\tracker.sqlite3
```

The directory is created and default targets are seeded on application startup. Data persists
between runs. To choose another directory, set `CALORIE_TRACKER_DATA_DIR` before starting the
backend, for example:

```powershell
$env:CALORIE_TRACKER_DATA_DIR = Join-Path $env:LOCALAPPDATA 'CalorieTracker'
```

The database should remain outside the repository. The app is designed for one local user, binds
to `127.0.0.1`, and does not send meal data to external services. It does not implement
application-level database encryption; access is governed by the local account and file
permissions. No authentication, cloud synchronization, or backup feature is included.

## Run Tests and Checks

Run from the repository root.

### Backend

The backend package is under `src/backend`, so set `PYTHONPATH` before running pytest:

```powershell
$env:PYTHONPATH = "src\backend"
& .\.venv\Scripts\python.exe -m pytest tests\backend -q
```

### Frontend

```powershell
npm --prefix src\frontend test -- --run
npm --prefix src\frontend run typecheck
npm --prefix src\frontend run build
```

## Existing Project Documentation

- [Prompt log](docs/prompt-log.md): recorded prompts, project decisions, AI contributions, and
  verification history.
- [Clarification log](docs/clarification-log.md): scope decisions and review record.
- [Verification results](docs/verification-results.md): recorded test, build, audit, and browser
  smoke outcomes, including the offline-test limitation.
- [Feature specification](specs/001-calorie-tracker/spec.md)
- [Implementation plan](specs/001-calorie-tracker/plan.md)
- [Data model](specs/001-calorie-tracker/data-model.md)
- [API contract](specs/001-calorie-tracker/contracts/openapi.yaml)
- [Task breakdown](specs/001-calorie-tracker/tasks.md)
- [Requirements checklist](specs/001-calorie-tracker/checklists/requirements.md)

## Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

Run commands from the repository root and set `PYTHONPATH` to `src\backend` in the same
PowerShell session before starting Uvicorn or pytest:

```powershell
$env:PYTHONPATH = "src\backend"
```

### FastAPI reports that the static directory does not exist

Build the frontend before starting the backend:

```powershell
npm --prefix src\frontend run build
```

The generated `src/backend/app/static/` directory is ignored by Git and is not included in a
fresh checkout until the build creates it.

### Database directory configuration fails

On Windows, `LOCALAPPDATA` is required unless `CALORIE_TRACKER_DATA_DIR` is set. Set the override
before starting Uvicorn and verify that the current user can create files in the chosen folder.

### Port 8000 is already in use

Stop the process using port 8000. The Vite development proxy is configured for
`127.0.0.1:8000`; if you change the backend port, update `src/frontend/vite.config.ts` to match.
Vite uses port 5173 by default and may select another port if it is occupied.

### npm reports an audit or install warning

At README preparation, `npm audit` reported zero vulnerabilities. The test run may emit deprecation
warnings from FastAPI's `on_event` startup hook and Starlette's TestClient/httpx integration; these
were warnings, not test failures, in the recorded run.

## Current Limitations and Verification Notes

- Windows 10/11 is the documented v1 target; macOS/Linux are out of scope unless the project
  scope is explicitly expanded.
- The application supports one local user, calories and protein only, and current global targets.
  It has no login, nutrition lookup, barcode scanning, medical advice, target history, undo,
  cloud sync, or backup.
- “Offline” means internet-independent after setup while the local backend is running. The
  recorded browser smoke blocked external-origin requests but did not physically disconnect the
  computer from the internet.
- **Previously recorded verification** is in [docs/verification-results.md](docs/verification-results.md):
  58 backend tests and 5 frontend tests passed; typecheck, build, and dependency audit passed.
- **Checked while preparing this README:** Python 3.14.7, Node 24.21.0, npm 11.19.0 are installed;
  the backend import-path command succeeds and `npm audit` reports zero vulnerabilities. The
  full test suites are recorded above as prior verification, not rerun specifically for this
  README edit.
