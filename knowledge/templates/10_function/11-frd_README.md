# FRD-0001: FRD Policy — Functional Requirements Document

## Document Overview

### What is an FRD?

A Functional Requirements Document (FRD) captures the detailed functional behavior of a specific module or feature group
within a system. It translates high-level business requirements from the parent BRD into precise, testable, and
implementable functional specifications that developers, QA engineers, and business analysts use as a shared contract.

> **Template version 2.0 changes (2026-02):**
> - Merged §1 Introduction + §2 Purpose → §1 Overview (added `audience` field)
> - Added §11 Module Interface — exposes APIs, events published, data owned
> - Simplified §13 Data Requirements — removed `core_fields` (field-level belongs in DC/DBC); added `ownership` field
> - Merged §16 Assumptions + §17 Constraints → §17 Assumptions & Constraints
> - Fixed `document_id` pattern in metadata (`FRD-[PROJECT]-[NNNN]`)
> - Added `module_code` field to metadata

### Function in the SDLC

The FRD sits directly below the BRD in the requirements hierarchy and is the primary input to design (HLD/LLD) and
testing (Test Plan, Test Cases) activities:

```
BRD (Business Requirements — per initiative)
 └── FRD (Functional Requirements — per module/feature group)   ◀ YOU ARE HERE
      └── HLD (High-Level Design — per system/component)
           └── LLD (Low-Level Design — per module)
                └── TC (Test Cases — per feature/module)

```

The FRD answers the question: *"What must this module do, under what conditions, and how should it behave when things go
wrong?"* It does **not** prescribe technology choices, database schemas, or class structures — those belong in the HLD
and LLD.

### Alignment to Standards

This FRD template and policy are aligned to:

- **IEEE 830-1998 / ISO/IEC/IEEE 29148:2018** — for requirements structure, classification, traceability, and the
  definitions/scope framework.
- **BABOK 3.0** (Business Analysis Body of Knowledge) — for elicitation patterns, stakeholder analysis, and requirement
  prioritization (MoSCoW).

---

## Document Dependencies

### Upstream Documents (Dependencies)

- BRD-0001

### Downstream Documents (Depend on This)

- PSD-0001, AEC-0001, API-0001, DBC-0001, DC-0001, UT-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

### Document ID Format

```
FRD-[PROJECT_CODE]-[NNNN]

```

| Component       | Rule                                                                 | Example         |
|-----------------|----------------------------------------------------------------------|-----------------|
| Prefix          | Always `FRD`                                                         | `FRD`           |
| PROJECT_CODE    | 2–5 uppercase alphanumeric characters identifying the project/system | `NPH`           |
| NNNN            | 4-digit zero-padded sequential number, scoped per project            | `0001`          |

**Example:** `FRD-NPH-0001` — First FRD for the Narwhal Product Hub project.

### File Naming Convention

```
FRD-[PROJECT_CODE]-[NNNN]_[ShortTitle]_v[Major.Minor].[ext]

```

**Example:** `FRD-NPH-0001_DataIngestion_v1.3.md`

Rules:
- `ShortTitle` uses PascalCase, no spaces, max 40 characters.
- Extension matches the format: `.md` for Markdown, `.yaml` for YAML.
- Version in filename must match the version inside the document.

### Version Numbering

| Change Type                                          | Version Impact | Example       |
|------------------------------------------------------|----------------|---------------|
| Structural change (section added/removed/reordered)  | Major bump     | 1.3 → 2.0    |
| Scope change (in-scope / out-of-scope modified)      | Major bump     | 1.3 → 2.0    |
| Requirement added or removed                         | Major bump     | 1.3 → 2.0    |
| Business rule added or materially changed            | Major bump     | 1.3 → 2.0    |
| Content refinement (wording, clarification, typo)    | Minor bump     | 1.3 → 1.4    |
| Metadata-only change (reviewer, date, status)        | Minor bump     | 1.3 → 1.4    |

### Internal ID Conventions

The following ID formats are used within the FRD body:

| Entity                       | Format                  | Example              | Scope                  |
|------------------------------|-------------------------|----------------------|------------------------|
| Functional Area              | `FA-N`                  | `FA-1`               | Grouping header only   |
| Functional Requirement       | `FR-NNN`                | `FR-001`             | Unique within document |
| Sub-Requirement              | `FR-NNN.N`              | `FR-001.1`           | Scoped to parent FR    |
| Acceptance Criteria          | `AC-FR-NNN-NN`          | `AC-FR-001-01`       | Scoped to parent FR    |
| Business Rule                | `BRL-NNN`               | `BRL-001`            | Unique within document |
| Exception Scenario           | `EX-NNN`                | `EX-001`             | Unique within document |
| Event Trigger                | `ET-NNN`                | `ET-001`             | Unique within document |
| Module Interface             | `IF-NNN`                | `IF-001`             | Unique within document |
| Published Event              | `EVT-NNN`               | `EVT-001`            | Unique within document |
| NFR (Functional Impact)      | `NFR-FM-NNN`            | `NFR-FM-001`         | Unique within document |
| Dependency                   | `DEP-NNN`               | `DEP-001`            | Unique within document |
| Assumption                   | `ASM-NNN`               | `ASM-001`            | Unique within document |
| Constraint                   | `CON-NNN`               | `CON-001`            | Unique within document |
| Module Acceptance Criteria   | `MAC-NNN`               | `MAC-001`            | Unique within document |
| Open Issue                   | `OI-NNN`                | `OI-001`             | Unique within document |

ID rules:
- IDs are **immutable** once assigned — never reuse a retired ID.
- Numbering is sequential within the document instance.
- Functional requirements: `FR-001`–`FR-499` (functional), `FR-500`+ (reserved for future extension) — these ranges are
  recommended but not enforced.

---

## Scope & Granularity

### What Does One FRD Cover?

One FRD covers **one module or one feature group** within a project. A module is defined as a logically cohesive set of
functionality that can be designed, built, and tested as a unit.

| Scenario                                                          | Action                                         |
|-------------------------------------------------------------------|-------------------------------------------------|
| New module identified during BRD elaboration                      | Create a new FRD                               |
| New feature group within an existing module with distinct behavior | Create a new FRD                               |
| Minor feature addition within existing module scope               | Update the existing FRD (major version bump)   |
| Requirement refinement or clarification (no new scope)            | Update the existing FRD (minor version bump)   |
| Module split into sub-modules                                     | Create new FRDs per sub-module; deprecate original |
| Cross-cutting concern (e.g., audit logging)                       | Dedicated FRD or section within each affected FRD |

### Relationship to Parent & Child Documents

| Document            | Relationship                                                               |
|---------------------|----------------------------------------------------------------------------|
| BRD (Parent)        | One BRD produces one or more FRDs; each FRD traces to BRD requirements     |
| HLD (Child)         | HLD references FRD requirements to justify design decisions                |
| LLD (Child)         | LLD details the implementation of FRD requirements at module level         |
| Test Plan           | Test Plan scopes testing based on FRD functional areas and priorities      |
| Test Cases (Child)  | Each test case traces to one or more FRD requirements                      |
| Change Request      | CRs that affect module scope must reference and update the relevant FRD    |

---

## Section-by-Section Explanation

### Metadata Header

**Purpose:** Unique identification, ownership, and lifecycle tracking. Links the FRD to its parent BRD and downstream
artifacts.

**What to include:** Document ID (using the `FRD-[PROJECT]-[NNNN]` pattern), `module_code`, title, version, status,
classification, dates, ownership roles, parent BRD reference, related document IDs.

**What NOT to include:** Document body content. Do not use the metadata section for narrative.

**Required:** Yes — every field must be populated before the document leaves Draft status.

### Section 1 — Overview

**Purpose:** Orient the reader in a single section. Covers what the module is, why this document exists, and who should
read it. Combines what were previously separate Introduction and Purpose sections.

**What to include:** A `summary` paragraph (3–5 sentences) identifying the module, its role, and why this FRD exists; a
`purpose` statement describing what decisions this document supports; an `audience` field naming the primary readers
(architects, developers, QA lead, product owner).

**What NOT to include:** Detailed business justification (that's in the BRD), requirements (those start in Section 8),
or technology decisions (HLD/LLD).

**Required:** Yes.

### Section 3 — Scope

**Purpose:** Draw a clear boundary around what this FRD covers. Scope disputes between modules are a common source of
confusion — this section prevents them.

**What to include:** Explicit in-scope items (features, capabilities, integrations) and explicit out-of-scope items
(related features owned by other modules, future phases).

**What NOT to include:** Requirements (those go in Section 9). Scope defines the boundary; requirements define what
happens within it.

**Required:** Yes — both in-scope and out-of-scope must be populated.

### Section 4 — Definitions & Acronyms

**Purpose:** Ensure all readers share the same understanding of module-specific and domain-specific terms.

**What to include:** Terms, acronyms, and abbreviations used in this FRD. Include terms from the parent BRD only if
their meaning is refined or extended at the module level.

**What NOT to include:** Common industry terms that don't need definition (e.g., "API", "HTTP" — unless used with
module-specific meaning).

**Required:** Optional — but strongly recommended for domain-heavy modules.

### Section 5 — Business Context

**Purpose:** Bridge business intent to functional behavior. This section ensures developers understand *why* the module
exists, not just *what* it does.

**What to include:** Business drivers specific to this module, expected outcomes, and explicit references to the parent
BRD business objectives (`BO-NNN`) that this module supports.

**What NOT to include:** The full business case (that's in the BRD). Keep this focused on the module's contribution to
business goals.

**Example:**
> This module supports `BO-001` (Centralize data ingestion) by implementing automated file retrieval, validation, and
loading for all approved external data sources.

**Required:** Yes.

### Section 6 — Actors & Stakeholders

**Purpose:** Identify who and what interacts with this module. This drives use case modeling and helps QA design test
personas.

**What to include:** Human actors (users, operators), system actors (upstream/downstream systems, schedulers), and
external actors (third-party APIs, partners). Specify the type, role, and responsibility for each.

**What NOT to include:** The full organizational stakeholder map (that's in the BRD). Focus only on actors relevant to
this module's behavior.

**Required:** Yes.

### Section 7 — Functional Overview

**Purpose:** Provide a mental model of the module before diving into detailed requirements. This helps reviewers
understand the big picture.

**What to include:** A narrative summary of the module's major capabilities and process flows. Reference or embed
high-level diagrams (context diagram, flow diagram, state diagram) where they add clarity.

**What NOT to include:** Detailed requirements or implementation specifics. This is a map, not the territory.

**Required:** Yes.

### Section 8 — Event Triggers

**Purpose:** Identify all events that initiate processing within this module. This is critical for understanding the
module's activation model and for designing test scenarios.

**What to include:** Each trigger with a unique ID (`ET-NNN`), the event description, its source (User, System,
Scheduler, External), and the requirements it activates.

**What NOT to include:** The detailed functional response (that's in Section 9). This section identifies *what starts
things*; Section 9 defines *what happens next*.

**Required:** Yes.

### Section 9 — Functional Requirements

**Purpose:** The core of the FRD. Defines in precise, testable language what this module must do. Every requirement must
be traceable, prioritized, and verifiable.

**What to include:**
- Requirements grouped by functional area (`FA-N`)
- Each requirement uniquely identified (`FR-NNN` or `FR-NNN.N` for sub-requirements)
- MoSCoW priority for each requirement (Must / Should / Could / Won't)
- Traceability to parent BRD requirements (`BR-NNN`)
- Acceptance criteria (`AC-FR-NNN-NN`) for key requirements

**What NOT to include:** Implementation details (e.g., "use PostgreSQL stored procedure", "call REST API at endpoint
X"). Requirements should describe *what* the system does, not *how*. Technology-specific design decisions belong in the
HLD/LLD.

**Granularity guidance:** Each requirement should be independently testable. If a requirement cannot be verified by a
single test case or a small set of related test cases, it should be decomposed into sub-requirements.

**Example:**
> `FR-001`: The system shall validate all incoming data files against the predefined schema before processing.
> - `FR-001.1`: The system shall reject files that do not match the expected column structure.
> - `FR-001.2`: The system shall log all validation failures with file name, timestamp, and failure reason.

**Required:** Yes — this is the most critical section of the FRD.

### Section 10 — Business Rules

**Purpose:** Capture the business logic that constrains or governs functional behavior. Business rules are often
implicit in stakeholder conversations — this section makes them explicit and traceable.

**What to include:** Each rule with a unique ID (`BRL-NNN`), a clear statement, and a list of requirements it affects.

**What NOT to include:** Technical implementation rules (e.g., "use UTC timestamps"). Those are constraints (Section 17)
or design decisions (HLD/LLD).

**Example:**
> `BRL-001`: A data file received after the end-of-day cutoff (17:00 UTC) shall be processed in the next business day's
batch. Applies to: `FR-003`, `FR-007`.

**Required:** Yes.

### Section 11 — Exception Scenarios

**Purpose:** Ensure the system's behavior is defined not just for the happy path but also for known failure and
edge-case conditions. This section directly informs QA negative testing.

**What to include:** Each exception with a unique ID (`EX-NNN`), the trigger condition, the expected system behavior,
and the user-visible outcome (error message, fallback, retry, escalation).

**What NOT to include:** Generic error handling patterns (e.g., "show 500 error page"). Each exception should describe a
specific, module-relevant scenario.

**Required:** Yes — minimum 3 exception scenarios per module.

### Section 11 — Module Interface

**Purpose:** Define what this module *exposes* to the rest of the system — its public surface. This is the producer
perspective; Section 12 covers the consumer perspective. Together, the two sections give a complete picture of the
module's integration surface.

**What to include:**
- `apis_provided`: REST/GraphQL/gRPC/Async APIs this module serves, with consumer list and API spec reference (API doc
  ID)
- `events_published`: Domain events this module emits, with consumer list and schema reference (AEC doc ID)
- `data_owned`: Entities this module is the source of truth for, noting which modules read that data

**What NOT to include:** APIs or events this module *consumes* (those go in Section 12). Do not include internal
service-to-service calls that don't cross module boundaries.

**Required:** Optional — skip only if the module truly has no external interface (rare; most modules expose at least
data ownership).

### Section 12 — Cross-Module Interactions

**Purpose:** Map the integration surface this module *consumes* — other modules and external systems it calls, reads
from, subscribes to, or depends on. Essential for impact analysis when changes are proposed.

**What to include:** Each interaction with the target module/system, the type (Read, Write, Call, Subscribe, Publish),
the direction (Inbound, Outbound, Bidirectional), a description, and a reference to the relevant API spec, AEC, or
interface document.

**What NOT to include:** Internal interactions within this module. The interface surface this module *provides* lives in
Section 11.

**Required:** Yes.

### Section 13 — Data Requirements

**Purpose:** Define the data entities this module interacts with at a high level. This guides data contract design and
helps data stewards understand entity ownership. Field-level design is explicitly out of scope here — it belongs in
DC/DBC.

**What to include:**
- Key entities with CRUD operations, ownership classification, and sensitivity
- Data retention policy where applicable

**What NOT to include:** Field-level schema, data types, constraints, indexes, or migration plans — those belong in
DC/DBC/LLD. The `core_fields` sub-section from prior template versions has been removed to enforce this boundary.

**Required:** Yes.

### Section 14 — Non-Functional Requirements (Functional Impact)

**Purpose:** Capture only the NFRs that require specific functional accommodations within this module. System-wide NFRs
live in the parent BRD or a dedicated NFR document.

**What to include:** Each NFR with a unique ID (`NFR-FM-NNN`), category, statement, measurable target, and a description
of how it impacts functional design.

**What NOT to include:** System-wide NFRs that don't require module-specific functional changes. If an NFR is handled
purely at the infrastructure level (e.g., network latency), it doesn't belong here.

**Example:**
> `NFR-FM-001` (Performance): File validation must complete within 30 seconds per 100MB file. *Functional impact:
requires streaming validation rather than full-file load.*

**Required:** Yes.

### Section 15 — Dependencies

**Purpose:** Identify anything outside the module team's direct control that could block or delay delivery or affect
runtime behavior.

**What to include:** Each dependency with a unique ID (`DEP-NNN`), the type (System, Team, Data, Third-Party,
Infrastructure), the owner, and the impact if the dependency is unavailable.

**What NOT to include:** Internal task-level dependencies (e.g., "Story A must be completed before Story B") — those
belong in the project plan or sprint backlog.

**Required:** Yes.

### Section 17 — Assumptions & Constraints

**Purpose:** Capture both implicit beliefs (assumptions) and hard design boundaries (constraints) in one place.
Separating them in prior versions created two near-identical tables — merging them reduces document weight without
losing any information.

**Assumptions sub-section:** Make implicit beliefs explicit. Each assumption (`ASM-NNN`) needs a validation method and
an impact-if-false statement. If something has been confirmed, it's a fact, not an assumption — remove it from here.

**Constraints sub-section:** Document hard boundaries (`CON-NNN`) that limit solution design choices — technical
mandates, regulatory requirements, budget/timeline restrictions. A constraint is non-negotiable; a preference is a
design choice that belongs in HLD.

**Example assumption:**
> `ASM-001`: External data providers will deliver files in CSV format with UTF-8 encoding. *Validation: Confirm with
provider during onboarding. Impact if false: File parser must support additional formats, affecting FR-001 and FR-002.*

**Required:** Yes.

### Section 18 — Traceability Matrix

**Purpose:** Provide a cross-reference map from parent BRD requirements to FRD requirements and downstream artifacts.
This enables impact analysis when scope changes occur.

**What to include:** BRD requirement ID → FRD requirement ID(s) → downstream document IDs (HLD section, LLD module, test
case IDs).

**What NOT to include:** Narrative explanations. This is a reference table.

**Required:** Yes — required before the FRD moves to Approved status. May be partially populated during Draft.

### Section 19 — Acceptance Criteria (Module-Level)

**Purpose:** Define the high-level conditions under which this module is considered complete and ready for handover to
QA or UAT. These are broader than individual requirement acceptance criteria.

**What to include:** Each criterion with a unique ID (`MAC-NNN`), a statement, and a verification method (Test, Demo,
Inspection, Analysis).

**What NOT to include:** Individual requirement acceptance criteria (those are in Section 9). Module-level criteria
address cross-cutting concerns like integration readiness, performance benchmarks, and deployment readiness.

**Required:** Yes.

### Section 20 — Open Issues

**Purpose:** Track unresolved questions, pending decisions, or ambiguities. This section provides transparency about
what is known and unknown at the current version.

**What to include:** Each issue with a unique ID (`OI-NNN`), description, owner, raised date, target resolution date,
status (Open, In Progress, Resolved, Deferred), and resolution when available.

**What NOT to include:** Resolved issues that have been incorporated into the requirements — remove them from this
section (or mark as Resolved with reference to the affected requirement).

**Required:** Optional — but if open issues exist, they must be documented here. The FRD should not move to Approved
status with unresolved `Open` issues.

### Section 21 — Approval

**Purpose:** Formal sign-off from accountable stakeholders. This is the gate that transitions the FRD from InReview to
Approved.

**What to include:** Role, name, decision (Approved / Approved with Conditions / Rejected), signature, and date.

**What NOT to include:** Informal agreements. All approvals must be explicitly recorded.

**Required:** Yes — the FRD cannot move to Approved status without this section completed.

### Change Log

**Purpose:** Maintain an auditable history of all document versions. Every version must have an entry.

**What to include:** Version number, date, author, and a concise summary of what changed.

**Required:** Yes — every version must have an entry.

### Attachments

**Purpose:** Reference supplementary materials (diagrams, spreadsheets, data samples, external specifications).

**What to include:** Filename, description, and location (relative path or URL).

**Required:** Optional.

---

## Update Triggers

### Creation Triggers

A new FRD must be created when:

| Trigger                                                          | Action              |
|------------------------------------------------------------------|---------------------|
| New module identified during BRD elaboration or design           | Create new FRD      |
| New feature group with distinct behavior within a system         | Create new FRD      |
| Existing module split into sub-modules                           | Create new FRDs; deprecate original |
| New project phase requiring substantially different module scope | Create new FRD (reference prior) |

### Update Triggers

The existing FRD must be updated (new version) when:

| Trigger                                                          | Version Impact |
|------------------------------------------------------------------|----------------|
| Approved Change Request modifies module functional scope         | Major          |
| Functional requirement added, removed, or materially changed     | Major          |
| Business rule added, removed, or materially changed              | Major          |
| In-scope / out-of-scope boundary changed                         | Major          |
| New exception scenario identified                                | Major          |
| Cross-module interaction added or changed                        | Major          |
| Data entity added or removed                                     | Major          |
| Requirement clarification or wording refinement (no scope impact)| Minor          |
| Acceptance criteria refined                                      | Minor          |
| Open issue resolved (with requirement update)                    | Minor          |
| Metadata change (reviewer, approver, date)                       | Minor          |

### Review Triggers

The FRD must be re-reviewed (even without changes) when:

| Trigger                                                          |
|------------------------------------------------------------------|
| Parent BRD is updated (any version)                              |
| HLD or LLD for this module is updated                            |
| Defect found in testing that traces back to this FRD             |
| Project reaches a major phase gate (e.g., code freeze, UAT entry)|
| 6 months have elapsed since last review                          |
| Organizational or team restructure affecting module ownership    |

### Retirement Triggers

The FRD should be marked as Deprecated when:

| Trigger                                                          | New Status   |
|------------------------------------------------------------------|--------------|
| A new FRD supersedes this one (module redesign or split)         | Deprecated   |
| Module is decommissioned                                         | Deprecated   |
| Parent BRD is deprecated                                         | Deprecated   |
| Project is cancelled                                             | Deprecated   |

When deprecating, set the `supersedes` field in the new FRD to reference the deprecated document's ID.

---

## Roles & Responsibilities

| Role                          | Responsibility                                                                |
|-------------------------------|-------------------------------------------------------------------------------|
| Business Analyst / Author     | Drafts and maintains the FRD; elicits detailed requirements from stakeholders |
| Technical Lead / Architect    | Reviews for technical feasibility, completeness, and alignment with HLD       |
| QA Lead                       | Reviews for testability; confirms acceptance criteria are verifiable           |
| Product Owner                 | Approves functional scope and priority; ensures alignment with BRD            |
| Developers                    | Review for implementability; identify missing edge cases or ambiguities       |
| All stakeholders              | Provide input during elicitation; validate the document during review cycles  |

---

## Quality Checklist

Use this checklist before submitting the FRD for review:

- [ ] Document ID follows the naming convention (`FRD-[PROJECT]-[NNNN]`)
- [ ] `module_code` field is populated in metadata
- [ ] Parent BRD ID is populated and correct
- [ ] All required sections are populated (see Required flag per section above)
- [ ] §1 Overview includes summary, purpose, and audience
- [ ] Every functional requirement has a unique ID (`FR-NNN`) and MoSCoW priority
- [ ] Every functional requirement traces to at least one parent BRD requirement
- [ ] Key requirements have acceptance criteria (`AC-FR-NNN-NN`) defined
- [ ] All business rules have unique IDs (`BRL-NNN`) and are linked to affected requirements
- [ ] Exception scenarios cover at least 3 distinct failure conditions
- [ ] §11 Module Interface is populated if the module exposes APIs, events, or owned data
- [ ] §12 Cross-Module Interactions specifies direction and interface reference for each entry
- [ ] §13 Data entities include CRUD operations, ownership, and sensitivity classification
- [ ] §13 does NOT contain field-level schema (belongs in DC/DBC)
- [ ] NFRs with functional impact include a measurable target metric
- [ ] §17 Assumptions include validation method and impact-if-false
- [ ] §17 Constraints are genuinely non-negotiable (preferences → HLD)
- [ ] Traceability matrix links BRD → FRD → downstream artifacts
- [ ] No unresolved Open Issues with status `Open` (for Approved status)
- [ ] Change Log has an entry for the current version
- [ ] Related Documents field is populated with known upstream/downstream IDs
- [ ] File name matches the naming convention
- [ ] Version in filename matches version inside the document

---

## YAML vs Markdown Template Relationship

Two template formats are provided:

| Aspect              | YAML Template                                | Markdown Template                        |
|---------------------|----------------------------------------------|------------------------------------------|
| Primary audience    | AI agents, automation pipelines, CI/CD       | Human authors and reviewers              |
| Authoring method    | Programmatic or AI-assisted                  | Manual editing in any text editor        |
| Validation          | JSON Schema validatable                      | Manual review against checklist          |
| Section structure   | Identical to Markdown (mirrored)             | Identical to YAML (mirrored)             |
| Guidance            | `description` field per section              | Blockquote guidance notes per section    |

Both formats are considered equally valid. An organization should choose one as the primary authoring format and
generate the other programmatically if dual-format is desired.
