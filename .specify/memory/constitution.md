<!--
Sync Impact Report
Version change: uninitialized -> 1.0.0 (initial project constitution)
Modified principles: none; defined nine project-specific principles
Added sections: Project Context and Decision Records; Development and Quality Workflow
Removed sections: none
Follow-up TODO: confirm the original ratification date and replace TODO(RATIFICATION_DATE)
-->

# Assignment 1: Calorie and Nutrition Tracker Constitution

## Core Principles

### I. Simplicity and Appropriate Scope
The application MUST remain understandable and appropriate for a fundamentals assignment.
Implementations MUST prefer the simplest design that satisfies an agreed requirement; added
complexity MUST have a documented requirement-based justification. This keeps the project
learnable, reviewable, and feasible within its assignment scope.

### II. Calculation Correctness
Daily calorie and protein totals MUST follow deterministic, documented rules approved in the
specification. The implementation and tests MUST use the same defined rules, including how
quantities and numeric precision affect totals. The application MUST NOT silently report an
incorrect or incomplete total. This makes nutrition summaries reproducible and verifiable.

### III. Input Validation
The application MUST validate food names, quantities, calorie values, protein values, and daily
targets against the approved specification. Invalid values MUST be rejected with clear feedback
and MUST NOT be included in stored entries or calculated totals. This prevents malformed data
from corrupting user-visible results.

### IV. Requirements Traceability
Functional requirements and acceptance criteria MUST have unique, stable identifiers. Planning,
implementation, and testing tasks MUST link to the relevant criteria or constraints. This lets
reviewers verify that agreed behavior is implemented and tested without adding unrequested work.

### V. Human Review
AI-generated specifications, plans, tasks, and code MUST be treated as drafts until reviewed by
the project owner. Review corrections MUST be recorded, and unresolved assumptions MUST remain
visible in the relevant project artifact. This preserves human accountability for decisions and
prevents generated content from being mistaken for approval.

### VI. Privacy and Security
The project MUST NOT commit passwords, API keys, access tokens, or other secrets. It MUST collect
and store only data necessary for the agreed application scope. This limits avoidable exposure
and keeps data handling proportionate to a fundamentals assignment.

### VII. Verification and Testing
Requirements and acceptance criteria MUST define expected outcomes for normal, invalid, boundary,
and relevant edge-case inputs. Appropriate tests MUST be run, and actual verification results
MUST be recorded. This provides evidence that calculations, validation, and user-visible behavior
match the approved requirements.

### VIII. Maintainability
Code MUST use clear names, modular organization, and readable structure. Setup instructions MUST
allow the project to be reproduced in the intended environment. This makes the work practical to
understand, review, test, and continue.

### IX. Scope Control
Implementation MUST be limited to agreed requirements and justified supporting functionality.
AI features, external APIs, and deployment infrastructure MUST NOT be added without a documented
need and approval. This protects the assignment from unnecessary dependencies and scope growth.

## Project Context and Decision Records

This project is Assignment 1: Calorie and Nutrition Tracker, a fundamentals assignment. Business
questions not answered by the requirements MUST be resolved through reasonable decisions that
are explicitly documented. Generated artifacts and those decisions remain subject to human
review under Principle V; unresolved assumptions MUST be identified rather than silently treated
as requirements.

## Development and Quality Workflow

During specification review, verify that requirements and acceptance criteria have unique IDs,
that assumptions are recorded, and that expected normal, invalid, boundary, and edge-case
outcomes are defined. During planning, link each implementation and testing task to its relevant
requirement or constraint, and justify work that does not map directly to one. During
implementation, review scope, validation, calculation rules, privacy, and maintainability
against this constitution. During testing, run the tests appropriate to the changed behavior and
record the actual results; unresolved failures or unverified criteria MUST be reported rather
than represented as passing.

## Governance
The project owner may propose amendments. An amendment MUST update this file, state its rationale,
and identify affected principles or workflow requirements. Changes MUST be reviewed for effects
on existing requirements, plans, implementation, and tests before they are treated as governing
policy.

Constitution versions use `MAJOR.MINOR.PATCH`. Increment MAJOR for backward-incompatible removal
or redefinition of governance; MINOR for a new principle or section or materially expanded
guidance; and PATCH for clarifications, wording corrections, or other non-semantic refinements.
Every amendment MUST update the last-amended date. The ratified date records the original
adoption date and MUST remain unchanged by later amendments.

Compliance MUST be checked at specification review, planning, implementation, and testing as
defined in Development and Quality Workflow. Reviewers MUST record identified deviations,
corrections, and unresolved assumptions in the relevant artifact. Work that conflicts with a
principle MUST be corrected or explicitly resolved through an approved constitution amendment;
unreviewed deviations MUST NOT be treated as compliant.

**Version**: 1.0.0 | **Ratified**: 27-10-2026 | **Last Amended**: 2026-10-27
