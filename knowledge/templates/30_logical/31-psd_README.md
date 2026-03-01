# PSD-0001: Product Specification Document (PSD) — Policy & Governance

## Document Overview

### What is a PSD?

A Product Specification Document (PSD) defines a single, testable function within a system. It bridges the gap between
high-level functional requirements (FRD) and low-level design (LLD) by providing a complete, implementation-ready
specification that is directly testable by QA.

### Function in the SDLC

The PSD sits in the **Requirements → Design** transition zone:

```
BRD (Business Need)
 └─ FRD (Feature Group)
     └─ PSD (Single Testable Function)   ← YOU ARE HERE
         └─ LLD (Module/Component Design)
             └─ TC (Test Cases)

```

The PSD receives input from the FRD (what the feature group requires) and produces output consumed by:

- **LLD authors** — to design the technical implementation
- **QA engineers** — to derive test cases directly from acceptance criteria
- **Developers** — to understand exact behavior, validations, and edge cases

### Three Function Archetypes

Every PSD instance describes exactly one of three function archetypes:

| Archetype | Description | Example |
|-----------|-------------|---------|
| **DATA PAGE (CRUD)** | A page managing a dataset with Create, Read, Update, Delete operations | Customer list page, Product catalog |
| **PROCESS FLOW** | A triggered process with defined inputs, steps, decisions, and outputs | Order approval workflow, Payment processing |
| **STATUS GROUP** | A set of mutually exclusive statuses with defined transitions and per-status processing | Account status management, Ticket lifecycle |

The archetype determines which specification section (Section 4, 5, or 6 in the template) must be completed. The
remaining archetype sections are skipped.

---

## Document Dependencies

### Upstream Documents (Dependencies)

- FRD-0001

### Downstream Documents (Depend on This)

- AEC-0001, API-0001, DBC-0001, DC-0001, UT-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

### ID Format

```
PSD-[NNNN]

```

- **Prefix:** `PSD` — Product Specification Document
- **Separator:** Hyphen (`-`)
- **Number:** 4-digit sequential, zero-padded (0001–9999)
- **Scope:** Global sequential across the project. Do not reset numbering per module.

**Examples:** PSD-0001, PSD-0042, PSD-0315

### File Naming

```
PSD-[NNNN]_[ShortTitle]_v[X.Y].[ext]

```

- **ShortTitle:** PascalCase, max 50 characters, no spaces or special characters
- **Version:** Major.Minor (see below)
- **Extension:** `.md` for Markdown, `.yaml` for YAML

**Examples:**
- `PSD-0001_CustomerListPage_v1.0.md`
- `PSD-0042_OrderApprovalFlow_v2.1.yaml`
- `PSD-0315_AccountStatusManagement_v1.3.md`

### Version Numbering

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New document | 1.0 | Initial creation |
| Structural change (new section, section removed, archetype change) | Major (+1.0) | 1.0 → 2.0 |
| Content update (field added, rule modified, criteria changed) | Minor (+0.1) | 1.0 → 1.1 |
| Typo or formatting fix | Minor (+0.1) | 1.1 → 1.2 |

---

## Scope & Granularity

### What One PSD Covers

One PSD = **one testable function**. A function is testable if a QA engineer can write acceptance tests that verify it
works end-to-end in isolation.

**Decision guide:**

| Question | If Yes → | If No → |
|----------|----------|---------|
| Can a QA engineer write a standalone test suite for this? | It's one function → one PSD | Break it down further |
| Does it serve a single user goal in one interaction? | It's one function → one PSD | Split into multiple PSDs |
| Does it require multiple archetypes? | Split into separate PSDs | It's one function → one PSD |

### When to Create a New PSD vs. Update Existing

| Scenario | Action |
|----------|--------|
| New function identified in FRD | Create new PSD |
| Existing function adds a new field | Update existing PSD (minor version) |
| Existing function changes archetype (e.g., simple CRUD becomes a workflow) | Create new PSD, retire old one |
| Existing function splits into two (e.g., one page becomes list page + detail page) | Create two new PSDs, retire old one |
| Bug reveals missing specification | Update existing PSD (minor version) |

### Relationship to Parent/Child Documents

| Relationship | Direction | Example |
|-------------|-----------|---------|
| Parent: FRD | PSD implements a subset of the FRD | FRD-0012 → PSD-0041, PSD-0042, PSD-0043 |
| Child: LLD | LLD provides technical design for the PSD | PSD-0041 → LLD-0078 |
| Child: TC | Test cases are derived from PSD acceptance criteria | PSD-0041 → TC-0120 |
| Sibling: PSD | Functions in the same module reference each other | PSD-0041 ↔ PSD-0042 |

---

## Section-by-Section Explanation

### Section 1: Function Overview

**Purpose:** Establish what this function is and classify it immediately.

**What to include:**
- 2–3 sentence description of the function's purpose and user value
- Function type selection (exactly one archetype)
- Owning module/service name
- The actor who triggers the function

**What NOT to include:**
- Technical implementation details (that's the LLD)
- Multiple functions (one PSD = one function)

**Required:** Yes

---

### Section 2: User Roles & Permissions

**Purpose:** Define who can do what within this function.

**What to include:**
- Every role that interacts with this function
- Specific permissions per role (not inherited system-wide roles unless they apply here)

**What NOT to include:**
- System-wide role definitions (reference the system role matrix instead)
- Authentication mechanism details (that's NFR or SAD)

**Example:**

| Role | Permissions |
|------|-------------|
| Sales Rep | Create, Read, Update (own records only) |
| Sales Manager | Create, Read, Update, Delete (team records) |
| Admin | Full CRUD (all records) |

**Required:** Yes

---

### Section 3: Preconditions & Dependencies

**Purpose:** Define what must be true before this function can work.

**What to include:**
- Data preconditions (e.g., "Customer record must exist")
- System state preconditions (e.g., "Service X must be available")
- External dependencies with system names

**What NOT to include:**
- Obvious platform preconditions (e.g., "User must be logged in" — unless login has special requirements for this
  function)

**Required:** Yes

---

### Section 4: Specification — DATA PAGE (CRUD)

**Purpose:** Complete specification for dataset page functions.

**When to complete:** Only when Function Type = DATA PAGE.

**What to include:**
- **Entity Definition:** The data entity name, description, and primary key
- **Field Catalog:** Every field with data type, constraints, validation, and CRUD behavior
- **List View:** Table configuration including sort, search, filter, pagination, bulk actions
- **Detail View:** Single-record layout, section grouping, inline editing
- **CRUD Operations:** Detailed behavior for Create, Read, Update, and Delete including triggers, confirmations,
  success/failure actions, conflict strategy, and cascade effects

**What NOT to include:**
- Database schema details (column types, indexes — that's the LLD)
- API endpoint definitions (that's the API spec)
- CSS/styling specifics (reference wireframes in Attachments)

**Example — Field Catalog entry:**

| Field Name | Data Type | Required | Validation Rules | On Create | On Update |
|------------|-----------|----------|------------------|-----------|-----------|
| email | String | Yes | Email format, unique per tenant | Editable | Read-only |
| created_at | DateTime | Yes | — | Auto-generated | Read-only |

**Required when applicable:** Yes

---

### Section 5: Specification — PROCESS FLOW

**Purpose:** Complete specification for triggered process functions.

**When to complete:** Only when Function Type = PROCESS FLOW.

**What to include:**
- **Trigger:** What starts the process (user action, schedule, event, API call)
- **Inputs:** All data required to begin, with source and validation
- **Processing Steps:** Ordered steps including decision branches, actors, timeouts, retry policies
- **Outputs:** All results produced and their destinations
- **Error Handling:** Every failure scenario with system behavior and recovery
- **SLA:** Expected duration and timeout behavior

**What NOT to include:**
- Internal algorithm implementation (that's the LLD)
- Infrastructure topology (that's the HLD/DG)

**Required when applicable:** Yes

---

### Section 6: Specification — STATUS GROUP

**Purpose:** Complete specification for status lifecycle functions.

**When to complete:** Only when Function Type = STATUS GROUP.

**What to include:**
- **Entity Context:** Which entity and field this status group governs
- **Statuses:** Every mutually exclusive status with entry/active/exit processing rules, allowed actions, and
  restrictions
- **Transitions:** Every valid transition with trigger, authorization, preconditions, validation, side effects, and
  reversibility
- **Transition Matrix:** Quick-reference grid of valid/forbidden transitions

**What NOT to include:**
- Database state machine implementation (that's the LLD)
- UI component specifications (reference wireframes)

**Example — Transition entry:**

| From | To | Trigger | Roles | Preconditions | Side Effects |
|------|----|---------|-------|---------------|--------------|
| ACTIVE | SUSPENDED | Admin clicks "Suspend" | Admin | None | Send email to account owner, disable API keys |

**Required when applicable:** Yes

---

### Section 7: Business Rules

**Purpose:** Capture discrete, testable rules that govern function behavior.

**What to include:**
- Atomic rules in Condition → Action → Exception format
- Priority when rules may conflict
- Source of the rule (regulation, business decision, etc.)

**What NOT to include:**
- Validation rules (those go in Section 8)
- Non-functional rules (those go in Section 12)

**Example:**

| Rule ID | Condition | Action | Exception |
|---------|-----------|--------|-----------|
| BR-001 | Order total > $10,000 | Require manager approval | Whitelisted customer accounts |

**Required:** Yes

---

### Section 8: Validation Rules

**Purpose:** Define every validation check with exact error messages.

**What to include:**
- Field-level format, range, and required validations
- Cross-field validations (e.g., "end_date must be after start_date")
- Exact user-facing error messages and machine-readable error codes

**What NOT to include:**
- Business rules that aren't validations (those go in Section 7)
- Server-side technical validations invisible to users (those go in LLD)

**Required:** Yes

---

### Section 9: UI / UX Behavior

**Purpose:** Define interaction patterns without prescribing visual design.

**What to include:**
- Navigation entry point
- Loading, success, error, and empty state behaviors
- Responsive behavior notes

**What NOT to include:**
- Pixel-perfect layout (attach wireframes instead)
- Color codes, font sizes (reference design system)

**Required:** No (recommended for DATA PAGE and STATUS GROUP)

---

### Section 10: Integration Points

**Purpose:** Document all external touchpoints.

**What to include:**
- System name, direction, protocol, data exchanged
- Error handling behavior for each integration
- SLA expectations

**What NOT to include:**
- Full API contracts (reference the API spec document)
- Network topology (that's the HLD)

**Required:** No

---

### Section 11: Acceptance Criteria

**Purpose:** Provide directly testable criteria in Given-When-Then format.

**What to include:**
- At least one acceptance criterion per business rule
- At least one acceptance criterion per CRUD operation (for DATA PAGE)
- At least one acceptance criterion per transition (for STATUS GROUP)
- At least one acceptance criterion per processing step (for PROCESS FLOW)
- Priority classification and linked business rules

**What NOT to include:**
- Performance test cases (those go in TC with NFR reference)
- Negative test cases that aren't tied to specific business rules (those go in TC)

**Required:** Yes

---

### Section 12: Non-Functional Requirements

**Purpose:** Function-specific performance, security, and availability needs.

**What to include:**
- Requirements that differ from or extend system-wide defaults
- Function-specific SLAs

**What NOT to include:**
- System-wide NFRs (reference the NFR document)
- Requirements identical to platform defaults

**Required:** No (use when function has specific NFR needs)

---

### Section 13: Assumptions & Constraints

**Purpose:** Document what was assumed during specification and what limits design choices.

**What to include:**
- Assumptions that, if wrong, invalidate part of the spec
- Technical, business, regulatory, and resource constraints

**What NOT to include:**
- Universally true statements (e.g., "System requires internet access")

**Required:** Yes

---

### Section 14: Open Questions

**Purpose:** Track unresolved items requiring stakeholder input.

**What to include:**
- Question text, owner, assignee, status, and answer when resolved
- **Approval gate:** Document MUST NOT be Approved while any question is in Open status

**Required:** No (but strongly recommended during Draft/In Review phases)

---

### Section 15: Attachments

**Purpose:** Reference supporting artifacts.

**What to include:**
- Wireframes, flow diagrams, ERDs, sequence diagrams, data samples
- File type classification for easy filtering

**Required:** No

---

### Change Log

**Purpose:** Version history.

**What to include:**
- Every version with date, author, and summary of changes

**Required:** Yes

---

## Update Triggers

### Creation Triggers

| Event | Action |
|-------|--------|
| New function identified during FRD elaboration | Create new PSD |
| New function discovered during sprint planning or backlog refinement | Create new PSD |
| Existing function requires different archetype | Create new PSD, retire old one |
| Existing function splits into multiple functions | Create new PSDs, retire old one |

### Update Triggers

| Event | Version Bump | Action |
|-------|-------------|--------|
| Field added or removed from field catalog | Minor | Update PSD |
| Business rule added, modified, or removed | Minor | Update PSD |
| Validation rule changed | Minor | Update PSD |
| New acceptance criterion identified | Minor | Update PSD |
| Status or transition added/changed | Minor (or Major if structural) | Update PSD |
| Process step added or reordered | Minor (or Major if structural) | Update PSD |
| Archetype changed | Major | Typically retire and create new PSD |
| Defect reveals missing specification | Minor | Update PSD |
| Integration point added or changed | Minor | Update PSD |

### Review Triggers

| Event | Action |
|-------|--------|
| Quarterly document health check | Re-review all Approved PSDs for currency |
| Related FRD is updated | Review affected PSDs for impact |
| Post-incident review identifies spec gap | Review and update affected PSD |
| Prior to major release | Review all PSDs in release scope |

### Retirement Triggers

| Event | New Status |
|-------|-----------|
| Function is removed from the system | Retired |
| Function is replaced by a new function (new PSD created) | Superseded |
| Parent FRD is retired | Retired |
| System or module is decommissioned | Retired |

---

## Roles & Responsibilities

| Role | Responsibility |
|------|---------------|
| **Business Analyst** | Authors the PSD. Gathers requirements from stakeholders, writes business rules and acceptance criteria. Primary owner. |
| **Product Owner** | Reviews the PSD for business alignment. Confirms acceptance criteria completeness. Approves the document. |
| **Technical Lead / Architect** | Reviews the PSD for technical feasibility. Validates integration points, NFRs, and constraints. |
| **QA Lead** | Reviews acceptance criteria for testability. Confirms that criteria are sufficient to derive test cases. |
| **Developer** | Consulted during drafting for feasibility. Consumes the approved PSD to implement the function. |
| **Author (BA)** | Accountable for keeping the PSD current throughout the function's lifecycle. |

### RACI Summary

| Activity | BA | PO | Tech Lead | QA Lead | Developer |
|----------|----|----|-----------|---------|-----------|
| Author PSD | **R/A** | C | C | C | C |
| Review PSD | I | **R** | **R** | **R** | I |
| Approve PSD | I | **A** | I | I | I |
| Update PSD | **R/A** | I | C | C | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## Quality Checklist

Before submitting a PSD for review, the author must verify:

- [ ] Document ID follows `PSD-[NNNN]` format
- [ ] File name follows `PSD-[NNNN]_[ShortTitle]_v[X.Y].[ext]` convention
- [ ] Exactly one function type is selected (DATA PAGE, PROCESS FLOW, or STATUS GROUP)
- [ ] Only the applicable specification section (4, 5, or 6) is completed; others are marked N/A
- [ ] All required sections are completed (Sections 1, 2, 3, 7, 8, 11, 13, Change Log)
- [ ] Every field in the field catalog has all CRUD behaviors specified (DATA PAGE)
- [ ] Every status has entry/active/exit processing rules defined (STATUS GROUP)
- [ ] Every process step has actor, type, input, and output specified (PROCESS FLOW)
- [ ] Every business rule has Condition, Action, and Exception defined
- [ ] Every validation rule has an exact error message and error code
- [ ] Every acceptance criterion is in Given-When-Then format
- [ ] At least one acceptance criterion exists per business rule
- [ ] All open questions are tracked with owner and assignee
- [ ] No open questions remain in "Open" status (for Approved documents)
- [ ] Parent document (FRD) is linked in metadata
- [ ] Related documents (LLD, TC, sibling PSDs) are linked
- [ ] Change log is updated with current version entry
- [ ] Reviewed by: Product Owner, Technical Lead, QA Lead
