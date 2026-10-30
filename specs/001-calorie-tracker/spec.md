# Feature Specification: Calorie and Nutrition Tracker

**Feature Branch:** Not created (no branch hook is configured)

**Created:** 2026-10-27

**Status:** Reviewed by project owner; planning baseline accepted

**Input:** Build a simple, locally runnable application for one local user to record meals,
track daily calories and protein, configure daily targets, and view progress, including previous
dates.

## Problem

A user needs a simple way to keep a personal meal record and understand daily calorie and
protein intake relative to configurable targets. Without reliable entry validation and
consistent daily calculations, summaries can be misleading. The application must support
manual tracking without requiring an account, nutrition service, or cloud account.

## Goals

- Record meals and manually entered calorie and protein values.
- Show daily intake, targets, remaining or excess amounts, and progress.
- Allow the user to correct entries and inspect previous dates.
- Keep records and targets available locally after the application is closed and reopened.

## Scope

The initial version supports one local user; manual meal-entry creation, editing, and deletion;
Breakfast, Lunch, Dinner, and Snack categories; calorie tracking in kcal; protein tracking in
grams; configurable daily targets; daily summaries; and viewing dates up to and including today.
Meal data and targets persist locally.

The initial version does not include registration or login, multiple users, external nutrition
services, barcode scanning, image recognition, AI features or recommendations, additional
nutrients, medical advice, social features, cloud synchronization, or weekly and monthly
analytics. It does not provide target history or recovery/undo for deleted entries.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record and Correct Meals (Priority: P1)

As the local user, I want to record meals and correct or remove entries so that each day's
calorie and protein totals reflect the meals I chose to record.

**Why this priority**: Accurate meal records are the foundation for every summary and progress
comparison.

**Independent Test**: Add one meal with known per-serving nutrition and quantity, verify the
resulting daily totals, then edit and delete it and verify each resulting total.

**Acceptance Scenarios**:

1. **AC-001 (FR-001, FR-002, FR-008, FR-010)** Given a date on or before today is selected, when the user saves a valid meal with a name, category, quantity, calories per serving, and protein per serving, then exactly one entry appears on that date and remains available after reopening the application.
2. **AC-002 (FR-003)** Given a day with no entries, when the user adds 2.50 servings at 72.00 kcal and 6.30 g protein per serving, then that entry contributes 180.00 kcal and 15.75 g protein to the day's totals.
3. **AC-003 (FR-004)** Given an entry contributes 180.00 kcal and 15.75 g protein, when the user edits its quantity to 3.00 servings, then the original day's totals include 216.00 kcal and 18.90 g protein for that entry, with no contribution from its previous values.
4. **AC-004 (FR-004, FR-003)** Given an entry contributes 100.00 kcal and 5.00 g protein to date A, when the user edits its date to date B, then date A no longer includes that entry and date B includes exactly 100.00 kcal and 5.00 g protein from it.
5. **AC-005 (FR-005, FR-003, FR-009)** Given an entry is included in a day's totals, when the user deletes it, then its calorie and protein contributions are removed; when it was the last entry, the day displays the no-entry state and zero intake.
6. **AC-006 (FR-002)** Given the user creates or edits an entry, when the category choices are shown, then the available categories are exactly Breakfast, Lunch, Dinner, and Snack.

### User Story 2 - Set Targets and Read Progress (Priority: P1)

As the local user, I want to set daily calorie and protein targets and compare intake with them
so that I can see the amount remaining or the amount over each target.

**Why this priority**: Target comparison is the main way the application turns recorded meals
into a useful daily summary.

**Independent Test**: Set known targets, create entries below, at, and above those targets, and
compare each displayed total, difference, and progress value with the defined rules.

**Acceptance Scenarios**:

1. **AC-007 (FR-006)** Given a first run with no saved targets, when the daily summary is displayed, then the proposed initial targets are 2,000.00 kcal and 50.00 g protein and are identified as generic defaults, not personalized advice.
2. **AC-008 (FR-006, FR-017, FR-010)** Given targets of 2,000.00 kcal and 50.00 g, when the user saves targets of 1,800.00 kcal and 60.00 g, then the new targets appear for today and every historical date, and remain saved after reopening the application.
3. **AC-009 (FR-007)** Given targets of 2,000.00 kcal and 50.00 g and intake of 1,200.00 kcal and 40.00 g, when the summary is displayed, then it shows 800.00 kcal and 10.00 g remaining, zero excess, and progress of 60.0% and 80.0%, respectively.
4. **AC-010 (FR-007)** Given targets of 2,000.00 kcal and 50.00 g and intake equal to both targets, when the summary is displayed, then it shows 100.0% progress for both nutrients and zero remaining and excess.
5. **AC-011 (FR-007)** Given targets of 2,000.00 kcal and 50.00 g and intake of 2,200.00 kcal and 65.00 g, when the summary is displayed, then it shows the full intake, excess of 200.00 kcal and 15.00 g, zero remaining, and progress of 110.0% and 130.0%; neither intake nor progress is capped at the target.

### User Story 3 - Review Previous Days (Priority: P2)

As the local user, I want to select a previous date and see the entries and summary for that
date so that I can review what I recorded earlier.

**Why this priority**: Historical review makes daily tracking useful beyond the current day while
remaining within the requested scope.

**Independent Test**: Record entries on two dates, select each date in turn, and verify that the
displayed entries and totals belong only to the selected date.

**Acceptance Scenarios**:

1. **AC-012 (FR-008, FR-003)** Given entries exist on two different dates, when the user selects either date, then only that date's entries and corresponding calorie and protein totals are displayed.
2. **AC-013 (FR-009, FR-006, FR-007)** Given a date on or before today has no entries, when the user selects it, then the summary shows zero calorie and protein intake, the current targets, the full target amounts remaining, zero excess, zero progress, and a clear no-entry message.
3. **AC-014 (FR-008)** Given the computer's local date is today, when the user starts a new entry, then today's date is selected by default; the user can select any earlier calendar date but cannot select a future date.

### User Story 4 - Keep Records Valid and Local (Priority: P1)

As the local user, I want invalid values and failed changes handled clearly so that my saved
records and totals remain trustworthy without requiring an account or external service.

**Why this priority**: Validation and reliable local persistence protect the accuracy of the
tracking experience and are required for responsible use of its summaries.

**Independent Test**: Exercise each field's valid and invalid boundaries, then simulate failed
create, edit, delete, and target-update operations and verify the last saved state remains intact.

**Acceptance Scenarios**:

1. **AC-015 (FR-011, NFR-003)** Given no entry exists, when creating an entry fails to persist, then the application shows an error without a success confirmation and the entry is absent from the list and totals.
2. **AC-016 (FR-011, NFR-003)** Given an entry has saved values, when editing it fails to persist, then the application shows an error without a success confirmation and the original entry and totals remain displayed.
3. **AC-017 (FR-011, NFR-003)** Given an entry has saved values, when deleting it fails to persist, then the application shows an error without a success confirmation and the entry and its original contribution remain displayed.
4. **AC-018 (FR-011, NFR-003)** Given saved targets exist, when changing them fails to persist, then the application shows an error without a success confirmation and the original targets and comparisons remain displayed.
5. **AC-019 (FR-012)** Given a food name containing only spaces or a trimmed name of 81 characters, when the user saves the entry, then the application rejects it; names containing 1 or 80 characters after trimming are accepted.
6. **AC-020 (FR-013)** Given entry numeric fields, when the user enters quantity 0.01 or 100.00 servings, calories 0.00 or 10,000.00 kcal per serving, or protein 0.00 or 1,000.00 g per serving, then the application accepts those boundary values; when the user enters zero quantity, any negative value, a value above a maximum, more than two fractional digits, comma-formatted text, exponent notation, a leading sign, or nonnumeric text, then the application rejects the entry without changing saved totals.
7. **AC-021 (FR-014)** Given calorie and protein targets, when the user enters calorie values of 1.00 or 100,000.00 kcal and protein values of 0.01 or 10,000.00 g, then the application accepts those boundary values; when the user enters zero, a negative value, a value outside either range, malformed numeric text, or more than two fractional digits, then the application rejects the target change.
8. **AC-022 (FR-015)** Given any invalid entry or target value, when validation rejects it, then the feedback names the invalid field and reason, and the last successfully saved entries, targets, and totals remain unchanged.
9. **AC-023 (FR-016)** Given a new local user opens the application for the first time, when the user records a meal and views its summary, then those actions are available without creating an account or logging in.
10. **AC-024 (FR-016, FR-010, NFR-001)** Given the application has been set up and the computer is offline, when the user creates, views, edits, and deletes entries and changes targets, then each workflow is available without an internet connection or external service; after closing and reopening the application, the successfully saved changes remain available.
11. **AC-025 (FR-016, NFR-002)** Given internet access is available, when the user records or views meal data, then the application does not transmit that data to an external service.

### Edge Cases

- Whitespace-only names and names longer than 80 characters are rejected.
- Numeric values containing letters, commas, scientific notation, a leading sign, or more than two fractional digits are rejected without changing saved data or totals.
- Zero calories and zero protein per serving are valid; zero quantity and zero targets are invalid.
- Values at each stated minimum and maximum are accepted; values outside the range are rejected.
- An entry at the maximum quantity or nutrition value is still multiplied by its quantity and included in the uncapped daily total.
- A target change applies to historical summaries because target history is not part of the initial version.
- If a save, edit, or delete cannot be persisted, the last confirmed entry or target state remains authoritative and the failed change is not reported as saved.
- Dates use the computer's local calendar date; travel and cross-timezone reinterpretation are not supported.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST let the local user create a meal entry with a food name, category, date, quantity in servings, calories per serving in kcal, and protein per serving in grams.
- **FR-002**: The application MUST limit meal categories to Breakfast, Lunch, Dinner, and Snack.
- **FR-003**: The application MUST calculate each entry's calorie and protein contribution as per-serving value multiplied by quantity, then sum contributions for the selected date.
- **FR-004**: The application MUST let the user edit an entry's name, category, date, quantity, calories per serving, and protein per serving; a successful edit MUST replace the old contribution and update the correct date or dates.
- **FR-005**: The application MUST let the user delete an entry; a successful deletion MUST remove its contribution from that date's totals.
- **FR-006**: The application MUST provide editable daily calorie and protein targets and MUST initialize them to the proposed generic defaults of 2,000.00 kcal and 50.00 g when no targets have been saved.
- **FR-007**: For each nutrient, the daily summary MUST show actual intake, target, remaining amount when below target or excess amount when above target, and progress as a percentage; actual intake and progress MUST NOT be capped at the target.
- **FR-008**: The application MUST assign new entries to the selected calendar date, default that selection to the computer's local date, allow dates before or equal to today, and disallow future dates.
- **FR-009**: For a date with no entries, the application MUST show zero intake, the current targets, the remaining target amounts, zero excess and progress, and a clear no-entry message.
- **FR-010**: The application MUST persist entries and targets locally and restore the last successfully saved values after it is reopened.
- **FR-011**: If an entry or target change cannot be saved, the application MUST show a clear error, MUST NOT report success, and MUST preserve the last confirmed state in displayed entries and totals.
- **FR-012**: The application MUST trim surrounding whitespace from a food name and reject a name that is empty after trimming or longer than 80 characters.
- **FR-013**: The application MUST validate quantity, calorie, and protein inputs using the proposed formats, precision, and ranges in Assumptions; it MUST permit zero nutrition values but reject zero quantity, negative values, malformed numbers, and out-of-range values.
- **FR-014**: The application MUST validate calorie and protein targets using the proposed formats, precision, and ranges in Assumptions; targets MUST be greater than zero.
- **FR-015**: For every rejected entry or target value, the application MUST identify the invalid field and give a clear reason; rejection MUST leave saved data and totals unchanged.
- **FR-016**: The application MUST support one local user without registration or login.
- **FR-017**: The current saved targets MUST be used when displaying any selected date; the initial version MUST NOT keep historical target versions.

### Non-Functional Requirements

- **NFR-001**: After local setup, all core workflows MUST be usable on the user's computer without requiring an account, internet connection, or external service.
- **NFR-002**: Meal entries and targets MUST remain local to the user's computer and MUST NOT be transmitted to an external service.
- **NFR-003**: Confirmation of a successful change MUST correspond to data that has been persisted; an unsuccessful persistence operation MUST be distinguishable from success.

### Key Entities *(include if data involved)*

- **Meal Entry**: A manually recorded food item with a name, meal category, calendar date, serving quantity, calories per serving, and protein per serving.
- **Daily Targets**: The current calorie and protein goals used for comparisons on all dates.
- **Daily Summary**: The selected date's summed calorie and protein intake, current targets, remaining or excess amounts, and progress percentages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For every valid calculation case in the acceptance scenarios, each displayed calorie and protein total equals the sum of each entry's per-serving value multiplied by its quantity, rounded once to two decimal places using round-half-up.
- **SC-002**: 100% of invalid inputs covered by FR-012-FR-015, AC-019-AC-022, and the food-name and numeric rules in Assumptions are rejected with the invalid field identified, while leaving the last confirmed totals unchanged.
- **SC-003**: In below-target, exact-target, and above-target cases, 100% of displayed remaining, excess, and progress values match the specified comparison rules, with above-target intake uncapped.
- **SC-004**: After a successful close-and-reopen cycle, 100% of saved entries and current targets retain their previously confirmed values.
- **SC-005**: For every simulated failed save in the acceptance scenarios, no failed change is shown as saved and the displayed state matches the last successfully saved state.

## Assumptions

The following are project decisions accepted by the project owner as the planning baseline.
They are not business-owner approvals and may be revised if requirements change:

- **Entry fields and quantity**: The clarification log's Q-10 mentions quantity, while Q-02 lists only a food name, calories, and protein. For the initial version, an entry includes quantity in servings, calories per serving, and protein per serving. This makes quantity meaningful and defines how it affects totals.
- **Food name**: Trim surrounding whitespace; accept 1 through 80 characters after trimming.
- **Numeric format and precision**: Accept unsigned decimal values written with digits and an optional decimal point followed by one or two digits. Reject commas, exponent notation, leading signs, nonnumeric text, and more than two fractional digits. Do not silently round or truncate entered values.
- **Entry numeric ranges**: Quantity is 0.01 through 100.00 servings; calories are 0.00 through 10,000.00 kcal per serving; protein is 0.00 through 1,000.00 g per serving. Minimum and maximum values are inclusive. Zero nutrition values are allowed; quantity must be positive.
- **Target numeric ranges**: Calorie target is 1.00 through 100,000.00 kcal; protein target is 0.01 through 10,000.00 g. Minimum and maximum values are inclusive; zero targets are invalid.
- **Calculation and display precision**: Multiply and sum without intermediate rounding. Determine whether intake is below, equal to, or above its target using the unrounded total. Round displayed calorie, protein, remaining, and excess amounts to two decimal places using round-half-up. Display progress to one decimal place using round-half-up. Progress is actual intake divided by target, multiplied by 100. Because comparisons use unrounded totals, a positive remaining or excess amount smaller than 0.005 may display as 0.00; progress may likewise display as 100.0% near the target.
- **Initial targets**: Use generic defaults of 2,000.00 kcal and 50.00 g protein until the user changes them. These values are not personalized recommendations or medical advice.
- **Date behavior**: Use the computer's local calendar date. A new entry uses the currently selected date, initially today; the user may select a past date. Editing may move an entry to another date on or before today.
- **Target history**: Targets are global current settings, not date-specific. Changing a target changes the comparison shown for historical dates as well.
- **Failed changes**: For a failed create, edit, delete, or target update, retain and display the last successfully persisted state. Exact recovery or retry interaction is left to planning.
- **Local persistence**: Data is retained on the same computer between application sessions; cloud backup and cross-device synchronization are not required.