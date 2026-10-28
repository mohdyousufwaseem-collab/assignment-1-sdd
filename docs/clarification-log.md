# Clarification Log — Calorie and Nutrition Tracker

**Assignment:** Assignment 1 — Spec-Driven Development  
**Document version:** 1.0  
**Status:** Independently clarified; pending consistency review  
**Decision owner:** Project owner  
**Business-owner consultation:** Not conducted; decisions below are independent proposals based on the supplied business request.

## 1. Purpose

The original business request describes the need to record meals, track calories and protein, set daily targets, and display progress. It does not define all business rules.

This log identifies the unanswered questions, documents the decisions selected for this fundamentals assignment, explains the rationale, and records unresolved assumptions. These decisions will guide the initial specification and may be revised if new evidence or requirements emerge.

## 2. Clarification Questions and Decisions

| ID | Clarification question | Independent decision | Rationale | Unresolved item / assumption |
|---|---|---|---|---|
| Q-01 | Who will use the application? | Support one local user without registration or login in the initial version. | Keeps the project small and avoids unnecessary authentication complexity. | Multi-user access is out of scope unless later required. |
| Q-02 | How will users enter food? | Users manually enter a food name, calories, and protein. | Avoids external API dependencies and keeps nutrition data under the user's control. | Automated food lookup is not included. |
| Q-03 | Which nutrients are tracked? | Track calories in kcal and protein in grams only. | These are the two nutrients explicitly requested. | Other nutrients are out of scope. |
| Q-04 | Which meal categories are supported? | Provide Breakfast, Lunch, Dinner, and Snack categories. | These common categories make the diary easy to organize. | Custom categories are not supported initially. |
| Q-05 | Can users set daily targets? | Allow users to configure daily calorie and protein targets. Require valid positive target values. | Custom targets are explicitly requested. | Default targets and target-change history are not required initially; initial values must be defined in the specification. |
| Q-06 | Can meal entries be edited or deleted? | Allow users to edit and delete their own entries. | Supports correction of mistakes and prevents incorrect records from remaining in totals. | No recovery or undo feature is planned. |
| Q-07 | How are daily totals calculated? | Sum the calorie and protein values of all valid entries assigned to the selected date. Recalculate totals after additions, edits, and deletions. | Provides deterministic and testable results. | Numeric precision and rounding rules will be defined in the specification. |
| Q-08 | How should daily progress be displayed? | Show calorie and protein totals, targets, remaining amounts or excess amounts, and progress indicators. | Makes the comparison with goals understandable. | The exact visual design will be decided during planning. |
| Q-09 | Is historical tracking needed? | Allow users to select a previous date and view its entries and totals. | Daily tracking is more useful when users can inspect earlier days. | Weekly and monthly analytics are out of scope. |
| Q-10 | What inputs are valid? | Reject blank food names, negative calorie or protein values, non-numeric values, and invalid targets. Define quantity and decimal rules in the specification. | Prevents invalid records from corrupting calculations. | Maximum values and decimal precision must be explicitly set in the specification. |
| Q-11 | What happens when a target is exceeded? | Display the amount consumed, the target, and the amount exceeding the target. Do not cap totals at the target. | Preserves accurate intake data. | No health warnings or medical recommendations are included. |
| Q-12 | Which timezone determines a day? | Use the application's configured local timezone for assigning entries to calendar dates. For the initial local application, use the computer's local date. | Keeps daily summaries consistent with the user's local tracking day. | Cross-timezone travel behavior is out of scope. |
| Q-13 | Should data persist? | Store food entries and targets persistently using a local database. | Records should remain available after the application restarts. | Cloud synchronization and backup are not included. |
| Q-14 | Are technology or deployment constraints specified? | Use a simple, locally runnable web application. The proposed stack is React, FastAPI, and SQLite, subject to the technical plan. | Uses familiar technologies and keeps deployment costs low. | No cloud deployment or paid services are required by the supplied request. |
| Q-15 | What happens when no meals are recorded? | Show zero intake and the configured targets, with an empty-state message. | Makes the dashboard understandable on a new day. | None identified for the initial version. |
| Q-16 | What happens if saving a meal fails? | Show a clear error and do not report the entry as saved. Do not include an unpersisted entry in confirmed totals. | Prevents misleading success messages and inconsistent data. | Detailed recovery and retry behavior will be defined in the technical plan. |

## 3. Scope Decisions

### Included in the initial version

- Manually add food entries.
- Categorize entries by meal.
- Record calories and protein.
- Edit and delete entries.
- Configure daily calorie and protein targets.
- Display daily totals and progress.
- View previous dates.
- Validate inputs and handle storage errors.
- Persist entries and targets locally.

### Excluded from the initial version

- User registration and authentication.
- Barcode scanning or image-based food recognition.
- External nutrition APIs.
- Tracking additional nutrients.
- AI-generated diet recommendations.
- Social features, multi-user sharing, and cloud synchronization.
- Medical advice or disease-specific dietary recommendations.

## 4. Unresolved Assumptions and Risks

1. The proposed scope and technology choices have not been confirmed by a business owner; they are independent decisions made for this assignment.
2. The maximum allowed calorie, protein, and target values, along with decimal precision, must be specified before implementation.
3. The initial target values and behavior when targets are changed need explicit rules in the specification.
4. The intended local timezone behavior should be verified through tests.
5. If new requirements emerge, the specification, plan, task breakdown, and validation plan must be updated consistently.

## 5. Decision and Review Record

- Decisions documented by: Project owner
- Decision date: 2026-10-27
- Review status: Initial independent review pending
- External mentor approval: Not obtained
- Specification baseline: Not yet established

## 6. Change Control

Any changed decision must be recorded here with the affected question ID, previous decision, revised decision, reason for change, and date. Changes affecting the specification must be reflected in the corresponding requirements and acceptance criteria before the planning baseline is established.