# Data Model: Calorie and Nutrition Tracker

This design supports the entities and rules in [spec.md](spec.md). It is a proposed design, not
implementation code. Quantity, numeric boundaries, and target defaults are based on the
project-author self-review in `docs/clarification-log.md`; no mentor approval is claimed.

## Meal Entry

One manually entered food record assigned to one local calendar date.

| Field | Stored representation | Validation and behavior | Spec coverage |
|---|---|---|---|
| `id` | SQLite integer primary key | Generated locally; stable for editing/deletion. | FR-001, FR-004, FR-005 |
| `name` | Text | Trim surrounding whitespace; 1-80 characters after trimming. | FR-012, AC-019 |
| `category` | Text constrained to `Breakfast`, `Lunch`, `Dinner`, `Snack` | No custom categories. | FR-002, AC-006 |
| `entry_date` | ISO date text, `YYYY-MM-DD` | Computer-local date; may be today or earlier, never future. | FR-008, AC-012, AC-014 |
| `quantity_hundredths` | Integer, scale 100 | 1-10,000 inclusive, representing 0.01-100.00 servings. | FR-001, FR-013, AC-020 |
| `calories_per_serving_hundredths` | Integer, scale 100 | 0-1,000,000 inclusive, representing 0.00-10,000.00 kcal. | FR-001, FR-013, AC-020 |
| `protein_per_serving_hundredths` | Integer, scale 100 | 0-100,000 inclusive, representing 0.00-1,000.00 g. | FR-001, FR-013, AC-020 |

The API accepts these numeric inputs as decimal strings matching digits with an optional
decimal point and one or two fractional digits. Parse directly to integer hundredths. Reject
signs, exponent notation, commas, malformed text, excess fractional digits, zero quantity,
negative values, and out-of-range values before opening a write transaction. Nutrition values
may be zero.

An edit replaces the entire entry in one transaction. If its date changes, summaries for both
the former and new dates are derived from the committed entry set. A delete removes the row in
one transaction; there is no undo/recovery entity.

## Daily Targets

One singleton record for the current local user. It is not keyed by date; no historical target
versions are retained.

| Field | Stored representation | Validation and behavior | Spec coverage |
|---|---|---|---|
| `id` | Integer constrained to `1` | Enforces at most one target record. | FR-006, FR-017 |
| `calorie_target_hundredths` | Integer, scale 100 | 100-10,000,000 inclusive, representing 1.00-100,000.00 kcal. | FR-006, FR-014, AC-021 |
| `protein_target_hundredths` | Integer, scale 100 | 1-1,000,000 inclusive, representing 0.01-10,000.00 g. | FR-006, FR-014, AC-021 |

When storage is initialized, create the singleton row with the proposed generic defaults of
2,000.00 kcal (`200000`) and 50.00 g (`5000`). Changing targets replaces both values
atomically. The current row is used for every selected historical date.

## Daily Summary (Derived)

Not persisted. Build it by selecting meal records for one `entry_date`, summing each scaled
quantity/per-serving product in Python integers, and comparing against the singleton targets.
For each nutrient:

- Raw intake numerator: `sum(quantity_hundredths * nutrient_per_serving_hundredths)`, scale 10,000.
- Target numerator: `target_hundredths * 100`, scale 10,000.
- Compare raw values before rounding. Intake equal to target has `remaining = 0.00` and `excess = 0.00`. Below target has positive remaining and zero excess; above target has zero remaining and positive excess.
- Displayed amounts in hundredths use positive half-up rounding: `(numerator + 50) // 100`.
- Progress in tenths of a percent uses positive half-up rounding: `(20 * raw_intake + target_hundredths) // (2 * target_hundredths)`.
- Format amounts with exactly two fractional digits and progress with exactly one. Intake and progress are never capped.
- Remaining numerator: `max(target_hundredths * 100 - raw_intake_numerator, 0)`.
- Excess numerator: `max(raw_intake_numerator - target_hundredths * 100, 0)`.
- Round remaining and excess using the same positive half-up amount formula as intake: `(numerator + 50) // 100`. Determine whether an amount is remaining or excess using unrounded values before display rounding.
For no entries, raw intake is zero; current targets remain visible, remaining equals each
target, excess is zero, progress is `0.0`, and `has_entries` is false. A small positive
remaining/excess may round to `0.00`; target comparison still follows the unrounded numerator.

## Persistence Invariants

- SQLite is the source of truth; the browser is not authoritative for saved records.
- Every create, full edit, delete, or target replacement is a transaction. Success is returned
  only after commit.
- Failed writes do not produce success confirmation. The UI keeps the last confirmed view and
  refreshes from storage if transaction outcome is uncertain.
- Daily summaries are derived on read; no stored total can drift from meal records.
- Store only the fields listed here. Do not store account credentials, health profile data,
  unneeded timestamps, or remote synchronization metadata.
