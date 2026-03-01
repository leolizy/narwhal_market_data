# MVP-0001: MVP Delivery Task List — Policy & Guidelines

## Document Overview

### What is this document?

The MVP Delivery Task List is a lightweight, actionable document that tracks every work item required to deliver a
Minimum Viable Product (MVP) within a single release or sprint cycle. It serves as the single source of truth for what
needs to be built, who owns it, and where things stand.

### Function in the SDLC

This document bridges the gap between requirements (PC/FRD) and execution. Once requirements are defined and scope is
agreed upon, the MVP Task List translates that scope into discrete, trackable work items with owners, priorities,
estimates, and acceptance criteria. It is the operational backbone of MVP delivery.

### Document Hierarchy

```
PC / FRD / SRS (Requirements)
       │
       ▼
  MVP Delivery Task List  ◄── You are here
       │
       ├──▶ HLD / LLD (Design, if needed)
       ├──▶ Test Plan / Test Cases (QA)
       └──▶ Release Notes (Post-delivery)

```

The MVP Task List consumes requirements documents as input and produces delivery artifacts (code, tests, documentation)
as output.

---

## Document Dependencies

### Upstream Documents (Dependencies)

- All other documents (PC-0001, FRD-0001, NFR-0001, PSD-0001, AEC-0001, API-0001, DBC-0001, DC-0001, CICD-0001,
  DBAD-0001, TSI-0001, UT-0001, NFRAR-0001)

### Downstream Documents (Depend on This)

- RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

### Document ID Format

```
MVP-[NNNN]

```

- **Prefix**: `MVP`
- **Numbering**: Four-digit sequential, scoped per project (e.g., MVP-0001, MVP-0002)
- **Reset**: Numbering does NOT reset between sprints — it is a running sequence per project

### File Naming Convention

```
MVP-[NNNN]_[ShortTitle]_v[X.Y].[ext]

```

**Examples:**
- `MVP-0001_UserAuth_v1.0.yaml`
- `MVP-0001_UserAuth_v1.0.md`
- `MVP-0012_PaymentGateway_v2.1.md`

### Version Numbering

Semantic versioning with two levels: **Major.Minor**

- **Major** (X.0): Structural changes — sections added/removed, scope fundamentally changed
- **Minor** (X.Y): Content updates — tasks added/modified, status updates, estimates revised

---

## Scope & Granularity

### What does one document instance cover?

One MVP Task List covers **one release or sprint cycle** for a defined scope of MVP work. If an MVP spans multiple
sprints, each sprint gets its own task list document.

### When to create a new document vs. update an existing one

| Scenario | Action |
|----------|--------|
| New sprint starts for the same MVP | Create a new document (MVP-NNNN+1) |
| Tasks are added mid-sprint | Update the existing document (bump minor version) |
| Scope fundamentally changes mid-sprint | Create a new document, retire the old one |
| Bug fix sprint for the same MVP | Create a new document scoped to the fix cycle |

### Relationship to parent/child documents

- **Parent**: PC, FRD, or equivalent requirements document that defines the MVP scope
- **Children**: None directly, but tasks in this list may reference HLD/LLD sections, test cases (TC-NNNN), or
  deployment guides (DG-NNNN)

---

## Section-by-Section Explanation

### Section 1: MVP Objective

- **Purpose**: Provides a one-sentence north star that every task aligns to. Prevents drift.
- **What to include**: A concise statement of what this MVP cycle delivers and why it matters.
- **What NOT to include**: Multiple goals, technical implementation details, or feature lists.
- **Example**: "Deliver a functional user registration and login flow to enable beta user onboarding by Sprint 12."
- **Required**: Yes

### Section 2: Success Criteria

- **Purpose**: Defines measurable pass/fail conditions for the MVP.
- **What to include**: Quantifiable metrics with specific targets (response time, error rate, coverage %).
- **What NOT to include**: Vague statements like "works well" or "users are happy."
- **Example**: Criterion: "Login response time" | Metric: "p95 latency" | Target: "< 2 seconds"
- **Required**: Yes

### Section 3: Scope Definition

- **Purpose**: Draws a clear boundary around what is and isn't being delivered.
- **What to include**: Specific features/capabilities in scope, explicit exclusions, and assumptions.
- **What NOT to include**: Task-level detail (that goes in Section 4).
- **Example**: In Scope: "Email-based registration" | Out of Scope: "Social login (OAuth)"
- **Required**: Yes

### Section 4: Task Breakdown

- **Purpose**: The operational core. Every work item needed to deliver the MVP.
- **What to include**: Tasks grouped by workstream, each with ID, title, owner, priority (P0–P3), estimate, status,
  blockers, and acceptance criteria.
- **What NOT to include**: Tasks belonging to future sprints, aspirational "nice to haves" not committed to this cycle.
- **Priority levels**:
  - **P0-Critical**: MVP cannot ship without this. Drop everything if blocked.
  - **P1-High**: Core functionality. Must be done this cycle.
  - **P2-Medium**: Important but MVP can technically ship without it.
  - **P3-Low**: Nice to have. Defer if time runs out.
- **Status values**: Not Started | In Progress | Blocked | Done | Deferred
- **Required**: Yes

### Section 5: Dependencies & Risks

- **Purpose**: Surfaces things outside the team's direct control that could derail delivery.
- **What to include**: External API availability, cross-team handoffs, vendor timelines, technical risks with
  likelihood/impact/mitigation.
- **What NOT to include**: Internal task dependencies (those are captured via "Blocked By" in Section 4).
- **Required**: Yes

### Section 6: Timeline & Milestones

- **Purpose**: Provides a high-level view of key dates and checkpoints.
- **What to include**: 3–6 milestones with target dates, owners, and status.
- **What NOT to include**: Day-by-day schedules or Gantt-level detail.
- **Example**: "Feature freeze" | 2026-03-10 | Tech Lead | On Track
- **Required**: Yes

### Section 7: Definition of Done

- **Purpose**: Ensures every task meets a consistent quality bar before being marked complete.
- **What to include**: A checklist of conditions (code review, tests, acceptance criteria, no critical bugs).
- **What NOT to include**: Task-specific criteria (those go in each task's acceptance criteria).
- **Required**: Yes

### Section 8: Communication & Reporting

- **Purpose**: Sets expectations for how progress is shared.
- **What to include**: Standup cadence, status report frequency, escalation path.
- **What NOT to include**: Meeting agendas, detailed RACI matrices.
- **Required**: No (optional, but recommended)

### Section 9: Attachments

- **Purpose**: Central reference for supporting materials.
- **What to include**: Links to wireframes, architecture diagrams, Figma files, data models.
- **What NOT to include**: Inline content — keep attachments as links/references.
- **Required**: No

---

## Update Triggers

### Creation Triggers

- A new sprint or release cycle begins for an MVP initiative
- A new MVP initiative is kicked off
- An existing MVP Task List is retired due to fundamental scope change

### Update Triggers (bump minor version)

- New task added or existing task modified
- Task status changes (daily/weekly updates)
- Estimate revised after discovery work
- Dependency status changes
- Risk materializes or is mitigated
- Milestone date adjusted

### Review Triggers (re-review without changes)

- Mid-sprint health check (halfway through the sprint)
- Escalation event (blocked task, missed milestone)
- Stakeholder requests progress review

### Retirement Triggers

- Sprint/release cycle completes — mark status as "Complete"
- MVP initiative cancelled — mark status as "Cancelled"
- Scope fundamentally changed — retire and create replacement document

---

## Roles & Responsibilities

| Role | Responsibility |
|------|---------------|
| **Author** (typically Tech Lead or PM) | Creates the document, breaks down tasks, assigns owners, maintains updates |
| **Product Owner / PM** | Defines MVP objective, success criteria, and scope; approves scope changes |
| **Tech Lead** | Validates estimates, reviews task breakdown, owns technical dependencies |
| **Task Owners** (Developers) | Update their task statuses, flag blockers promptly |
| **Reviewer** (PM or Tech Lead, cross-review) | Reviews document for completeness and accuracy before sprint start |
| **Approver** (PM or Engineering Manager) | Signs off that the task list is ready to execute |

---

## Quality Checklist

Before submitting this document for review, verify:

- [ ] Document ID follows `MVP-[NNNN]` convention
- [ ] MVP Objective is a single, clear sentence
- [ ] Success Criteria are measurable with specific targets
- [ ] In Scope and Out of Scope are explicitly listed
- [ ] Every task has: ID, title, owner, priority, estimate, status, acceptance criteria
- [ ] All P0 and P1 tasks have owners assigned
- [ ] Dependencies are listed with owners and expected resolution dates
- [ ] Risks have likelihood, impact, and mitigation defined
- [ ] Milestones have target dates and owners
- [ ] Definition of Done checklist is agreed upon by the team
- [ ] Related documents are linked in metadata
- [ ] Change Log is updated with current version entry
- [ ] Reviewed by at least one person other than the author
