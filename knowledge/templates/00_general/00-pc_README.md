# PC-0001: Platform Canon Policy

## Overview

### What is a PC?

A Platform Canon (PC) is the authoritative, canonical reference for the system. It captures the high-level business
needs, objectives, and requirements for a proposed initiative, serving as the primary contract between stakeholders and
delivery teams by defining **what** the platform must achieve (not **how** to build it).

### Function in the SDLC

The PC is the first formal requirements artifact produced after an initiative is approved for discovery. It sits at the
top of the requirements hierarchy as the single source of truth and drives all downstream documentation:

```
PC (Platform Canon)
 └── FRD (Functional Requirements — per module/feature)
      └── SRS (Software Requirements Specification — per system)
           └── HLD / LLD (Design Documents)
                └── TC (Test Cases)

```

The PC answers the question: *"What does the business need and why?"* It does **not** prescribe solution design,
technology choices, or implementation details — those belong in downstream artifacts (FRD, HLD, LLD).

### Alignment to Standards

This PC template and policy are aligned to:

- **BABOK 3.0** (Business Analysis Body of Knowledge) — for business analysis structure, stakeholder analysis,
  current/future state, and elicitation patterns.
- **IEEE 830-1998** (Software Requirements Specification) — for requirements identification, classification,
  traceability, and the glossary/definitions structure.

---

## Document Dependencies

### Upstream Dependencies

- **None** — PC-0001 is the source of truth for business requirements.

### Downstream Documents (Must be Updated When PC Changes)

- **FRD-0001** — Functional Requirements derived from business objectives
- **NFR-0001** — Non-Functional Requirements derived from business objectives
- **PSD-0001** — Product specifications must align with business requirements
- **AEC-0001, API-0001, DBC-0001, DC-0001** — Contract documents must align
- **CICD-0001, DBAD-0001, TSI-0001** — Architecture decisions must support business goals
- **UT-0001, NFRAR-0001** — Test specifications validate against requirements
- **MVP-0001, RTM-0001** — Project documents must maintain traceability

**Impact of Changes:** Any change to PC business objectives, scope, or requirements cascades to ALL downstream
documents.

---

## Naming & ID Convention

### Document ID Format

```
PC-[PROJECT_CODE]-[NNNN]

```

| Component       | Rule                                                                 | Example         |
|-----------------|----------------------------------------------------------------------|-----------------|
| Prefix          | Always `PC`                                                         | `PC`           |
| PROJECT_CODE    | 2–5 uppercase alphanumeric characters identifying the project/system | `NPH`           |
| NNNN            | 4-digit zero-padded sequential number, scoped per project            | `0001`          |

**Example:** `PC-NPH-0001` — First PC for the Narwhal Product Hub project.

### File Naming Convention

```
PC-[PROJECT_CODE]-[NNNN]_[ShortTitle]_v[Major.Minor].[ext]

```

**Example:** `PC-NPH-0001_NarwhalProductHub_v1.7.md`

Rules:
- `ShortTitle` uses PascalCase, no spaces, max 40 characters.
- Extension matches the format: `.md` for markdown, `.yaml` for YAML.
- Version in filename must match the version inside the document.

### Version Numbering

| Change Type                                          | Version Impact | Example       |
|------------------------------------------------------|----------------|---------------|
| Structural change (section added/removed/reordered)  | Major bump     | 1.7 → 2.0    |
| Scope change (in-scope / out-of-scope modified)      | Major bump     | 1.7 → 2.0    |
| Requirement added or removed                         | Major bump     | 1.7 → 2.0    |
| Content refinement (wording, clarification, typo)    | Minor bump     | 1.7 → 1.8    |
| Metadata-only change (reviewer, date, status)        | Minor bump     | 1.7 → 1.8    |

### Internal ID Conventions

The following ID formats are used within the PC body:

| Entity                | Format                  | Example              | Scope                  |
|-----------------------|-------------------------|----------------------|------------------------|
| Business Objective    | `BO-NNN`                | `BO-001`             | Unique within document |
| Business Requirement  | `PC-NNN`                | `PC-001`             | Unique within document |
| Acceptance Criteria   | `AC-PC-NNN-NN`          | `AC-PC-001-01`       | Scoped to parent PC    |
| Functional Area       | `FR-N`                  | `FR-1`               | Grouping header only   |
| Sub-Requirement       | `FR-N.N`                | `FR-1.1`             | Scoped to parent FR    |

ID rules:
- IDs are **immutable** once assigned — never reuse a retired ID.
- Numbering is sequential within the document instance.
- Functional requirements (`PC-001`–`PC-099`), non-functional (`PC-100`–`PC-199`), constraints (`PC-200`+) — these
  ranges are recommended but not enforced.

---

## Scope & Granularity

### What Does One PC Cover?

One PC covers **one initiative, project, or program**. An initiative may span multiple systems, modules, or phases — but
the PC captures the unified business need.

| Scenario                                                    | Action                                      |
|-------------------------------------------------------------|---------------------------------------------|
| New project / initiative                                    | Create a new PC                            |
| New phase of an existing project with changed scope         | Create a new PC (reference the prior one)  |
| Minor scope refinement within the same initiative           | Update the existing PC (minor version)     |
| New module within an approved initiative                    | Do NOT create a new PC — create an FRD     |
| Separate business initiative with independent funding/goals | Create a new PC                            |

### Relationship to Other Documents

| Downstream Document | Relationship                                                          |
|---------------------|-----------------------------------------------------------------------|
| FRD                 | One PC produces one or more FRDs (per module or feature group)       |
| HLD                 | HLD references the PC for business context and scope                 |
| Test Plan           | Test Plan traces test scope back to PC objectives and requirements   |
| Change Request      | CRs that affect business scope must reference and update the PC      |

---

## Section-by-Section Explanation

### Metadata Header

**Purpose:** Unique identification, ownership, and lifecycle tracking.

**What to include:** Document ID, title, version, status, classification, dates, ownership roles, related document
references.

**What NOT to include:** Document body content. Do not use the metadata section for narrative.

**Required:** Yes — every field must be populated before the document leaves Draft status.

### Section 1 — Executive Summary

**Purpose:** Give a senior stakeholder a complete picture of the initiative in under 2 minutes. This is the most-read
section of the PC.

**What to include:** The business driver, what will be built at a high level, the expected outcome, and which phase this
PC covers.

**What NOT to include:** Technical architecture, implementation details, or exhaustive requirement lists. Keep it to 1–3
paragraphs.

**Required:** Yes.

### Section 2 — Business Objectives

**Purpose:** Define the measurable goals that justify the initiative. Everything in the PC should trace back to at least
one objective.

**What to include:** SMART objectives with unique IDs (`BO-NNN`). Include a success measure for each.

**What NOT to include:** Solution-level goals (e.g., "migrate to Kubernetes") — those belong in the HLD. Objectives
should be business outcomes.

**Example:**
> `BO-001`: Centralize ingestion and management of reference and settlement data from approved external sources —
measured by 100% of target data sources onboarded within 6 months.

**Required:** Yes — minimum 2 objectives.

### Section 3 — Problem Statement

**Purpose:** Articulate the pain. This section justifies the initiative's existence and should make the "why"
immediately clear.

**What to include:** Current pain points, inefficiencies, cost of inaction. Use concrete evidence where possible (e.g.,
"5 teams each maintain separate integrations").

**What NOT to include:** The solution. This section describes the problem, not the answer.

**Required:** Yes.

### Section 4 — Scope

**Purpose:** Draw a clear boundary. Scope disputes are the #1 cause of delivery overruns — this section prevents them.

**What to include:** Explicit in-scope items, explicit out-of-scope items, and domain definitions where the business
domain requires precision (e.g., data entity hierarchies, product type definitions).

**What NOT to include:** Requirements (those go in Section 8). Scope defines the boundary; requirements define what
happens within it.

**The Domain Definitions sub-section** is for business-domain concepts that affect how requirements should be
interpreted. For example, if "Contract level" has a specific meaning with defined `contractTicker` formats, define it
here so that all readers share the same understanding.

**Required:** Yes — both in-scope and out-of-scope must be populated.

### Section 5 — Stakeholder Analysis

**Purpose:** Ensure all relevant parties are identified, their interests understood, and their responsibilities
assigned.

**What to include:** Every stakeholder group with their role, interest area, and specific responsibility.

**What NOT to include:** Individual names (use roles). Names go in the Approval section.

**Required:** Yes.

### Section 6 — Current State Analysis

**Purpose:** Document the baseline. Without a clear current state, you cannot measure improvement.

**What to include:** How things work today — processes, systems, pain points, workarounds.

**What NOT to include:** The future state (that's Section 7). Keep this factual and evidence-based.

**Required:** Yes.

### Section 7 — Future State Vision

**Purpose:** Describe the desired end state. This is the "north star" that guides all design and delivery decisions.

**What to include:** A vision narrative (1–2 paragraphs) and a list of measurable target-state outcomes.

**What NOT to include:** Implementation timelines or phasing details — those belong in the project plan.

**Required:** Yes.

### Section 8 — Functional Requirements

**Purpose:** The core of the PC. Defines what the system must do to meet the business objectives.

**What to include:**
- Requirements grouped by functional area (`FR-N`)
- Each requirement uniquely identified (`PC-NNN` or `FR-N.N`)
- MoSCoW priority for each requirement
- Traceability to Business Objectives (`BO-NNN`)
- Acceptance criteria (`AC-PC-NNN-NN`) for key requirements

**What NOT to include:** Implementation details (e.g., "use PostgreSQL", "deploy on AWS"). Requirements should be
technology-neutral at the PC level. Detailed functional specifications belong in the FRD.

**Granularity guidance:** PC functional requirements should be at the "capability" level (e.g., "System shall support
automated ingestion"). Detailed behavior (e.g., specific field mappings, API payload schemas) belongs in the FRD.

**Required:** Yes.

### Section 9 — Non-Functional Requirements

**Purpose:** Define quality attributes and system-wide constraints that apply across all functional areas.

**What to include:** Each NFR with a category, statement, and measurable target metric. Standard categories:
Availability, Performance, Scalability, Reliability, Security, Auditability, Maintainability, Observability,
Interoperability, Compliance, Data Retention.

**What NOT to include:** Functional behavior. If a requirement describes *what* the system does, it's functional. If it
describes *how well* the system does it, it's non-functional.

**Required:** Yes.

### Section 10 — Assumptions & Constraints

**Purpose:** Make implicit beliefs explicit (assumptions) and document fixed boundaries (constraints).

**What to include:**
- Assumptions: Conditions believed true but unvalidated. Each should be testable.
- Constraints: Hard boundaries — budget, timeline, regulatory, technology mandates.

**What NOT to include:** Risks (those go in Section 11). If an assumption failing would cause harm, capture the
corresponding risk in Section 11.

**Required:** Yes.

### Section 11 — Risks & Mitigation

**Purpose:** Proactively identify threats to initiative success and plan mitigations.

**What to include:** Risk description, impact (High/Medium/Low), likelihood (High/Medium/Low), and a concrete mitigation
strategy.

**What NOT to include:** Generic risks without specific mitigation. Every risk must have an actionable mitigation.

**Required:** Yes — minimum 3 risks.

### Section 12 — Success Metrics / KPIs

**Purpose:** Define how success will be measured post-delivery. These should directly map to Business Objectives.

**What to include:** Metric name, target value, and how it will be measured.

**What NOT to include:** Delivery metrics (e.g., sprint velocity, defect counts). This section is about business outcome
measurement.

**Required:** Yes.

### Section 13 — Dependencies

**Purpose:** Identify anything outside the team's direct control that could block or delay delivery.

**What to include:** External systems, third-party services, team dependencies, infrastructure dependencies.

**What NOT to include:** Internal task dependencies — those belong in the project plan.

**Required:** Yes.

### Section 14 — Glossary

**Purpose:** Ensure all readers share the same understanding of domain-specific terms.

**What to include:** Acronyms, abbreviations, and domain terms used in the document.

**What NOT to include:** Common industry terms that don't need definition.

**Required:** Optional — but strongly recommended for domain-heavy initiatives.

### Section 15 — Traceability Matrix

**Purpose:** Provide a cross-reference map from requirements to objectives and downstream artifacts. Enables impact
analysis when scope changes.

**What to include:** Requirement ID → Business Objective → Downstream document IDs (FRD, TC, etc.).

**What NOT to include:** This is a reference table, not a narrative section.

**Required:** Optional for initial Draft. Required before Approved status.

### Section 16 — Approval

**Purpose:** Formal sign-off from accountable stakeholders.

**What to include:** Role, name, decision (Approved / Approved with Conditions / Rejected), signature, date.

**What NOT to include:** Informal agreements. All approvals must be explicitly recorded.

**Required:** Yes — document cannot move to Approved status without this.

### Change Log

**Purpose:** Maintain an auditable history of all document versions.

**What to include:** Version number, date, author, and a summary of what changed.

**Required:** Yes — every version must have an entry.

### Attachments

**Purpose:** Reference supplementary materials (diagrams, spreadsheets, external specifications).

**What to include:** Filename, description, and location (relative path or URL).

**Required:** Optional.

---

## Update Triggers

### Creation Triggers

A new PC must be created when:

| Trigger                                                  | Action              |
|----------------------------------------------------------|---------------------|
| New project or initiative approved for discovery         | Create new PC      |
| Existing initiative enters a new phase with changed scope | Create new PC      |
| Separate initiative with independent funding/objectives  | Create new PC      |

### Update Triggers

The existing PC must be updated (new version) when:

| Trigger                                                  | Version Impact |
|----------------------------------------------------------|----------------|
| Approved Change Request modifies business scope          | Major          |
| Requirement added, removed, or materially changed        | Major          |
| Business Objective added, removed, or redefined          | Major          |
| In-scope / out-of-scope boundary changed                 | Major          |
| Stakeholder role or responsibility changed               | Minor          |
| Risk reassessment after incident or environment change   | Minor          |
| Clarification or wording refinement (no scope impact)    | Minor          |
| Reviewer/approver personnel change                       | Minor          |

### Review Triggers

The PC must be re-reviewed (even without changes) when:

| Trigger                                                  |
|----------------------------------------------------------|
| Project reaches a major phase gate (e.g., UAT entry)     |
| 6 months have elapsed since last review                  |
| Material incident affecting a system covered by this PC |
| Regulatory or compliance requirement change              |
| Organizational restructure affecting stakeholders        |

### Retirement Triggers

The PC should be marked as Deprecated when:

| Trigger                                                  | New Status   |
|----------------------------------------------------------|--------------|
| A new PC supersedes this one (new phase/major revision) | Deprecated   |
| Initiative is cancelled                                  | Deprecated   |
| System decommissioned                                    | Deprecated   |

When deprecating, set the `supersedes` field in the new PC to reference the deprecated document's ID.

---

## Roles & Responsibilities

| Role                       | Responsibility                                                               |
|----------------------------|------------------------------------------------------------------------------|
| Business Analyst / Author  | Drafts and maintains the PC; elicits requirements from stakeholders         |
| Product Manager / Owner    | Approves scope and priority; accountable for business alignment              |
| Reviewer(s)                | Reviews for completeness, accuracy, and feasibility                          |
| Approver(s)                | Formally signs off; authorizes delivery to proceed                           |
| Business Sponsor           | Provides strategic direction and funding authority                           |
| All stakeholders           | Provide input during elicitation; validate the document during review cycles |

---

## Quality Checklist

Use this checklist before submitting the PC for review:

- [ ] Document ID follows the naming convention (`PC-[PROJECT_CODE]-[NNNN]`)
- [ ] All required sections are populated (see Required flag in template)
- [ ] Every Business Objective has a success measure
- [ ] Every functional requirement has a unique ID and MoSCoW priority
- [ ] Every functional requirement traces to at least one Business Objective
- [ ] Key requirements have acceptance criteria defined
- [ ] Non-functional requirements have measurable target metrics
- [ ] In-scope and out-of-scope are both explicitly defined
- [ ] Risks have concrete mitigation strategies (not just "to be determined")
- [ ] Change Log has an entry for the current version
- [ ] Related Documents field is populated with known downstream/upstream IDs
- [ ] Glossary includes all domain-specific terms used in the document
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

The existing JSON Schema (`businessrequirements.schema.json`) validates the `metadata` and core `spec.objectives` /
`spec.requirements` sections of the YAML template. Extending the schema to cover all sections is recommended as a
follow-up.
