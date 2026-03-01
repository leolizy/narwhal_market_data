# HLD — High-Level Design Document: Policy & Governance

## 1. Document Overview

### 1.1 What Is an HLD?

A High-Level Design (HLD) document describes the architectural blueprint of a system or subsystem. It translates
requirements (from SRS, FRD, and NFR documents) into an actionable design that developers, architects, and tech leads
can use to understand, build, and evolve the system.

### 1.2 Function in the SDLC

The HLD sits between the **Requirements Phase** and the **Detailed Design / Implementation Phase**. It is the first
design artifact produced after requirements are baselined and serves as the primary input to Low-Level Design (LLD)
documents, implementation plans, and infrastructure provisioning.

```
PC / FRD / SRS / NFR
        │
        ▼
   ┌─────────┐
   │   HLD   │  ◄── You are here
   └─────────┘
        │
        ▼
  LLD / API Spec / Implementation

```

### 1.3 Document Hierarchy

| Upstream (Inputs)         | Downstream (Outputs)              |
|--------------------------|----------------------------------|
| SRS — Software Requirements Specification | LLD — Low-Level Design Document |
| FRD — Functional Requirements Document    | API — API Specification Document |
| NFR — Non-Functional Requirements Document| DG — Deployment Guide            |
| SAD — Software Architecture Document      | TP — Test Plan (architecture-level) |

---

## 2. Naming & ID Convention

### 2.1 ID Format

```
HLD-[NNNN]

```

- **Prefix:** `HLD` — identifies the document type unambiguously.
- **Numbering:** Four-digit sequential number, zero-padded (e.g., `HLD-0001`, `HLD-0042`).
- **Scope:** Numbering is **global per organization or per program**, not per project — this avoids ID collisions when
  documents are shared across teams.

### 2.2 File Naming Convention

```
HLD-[NNNN]_[ShortTitle]_v[X.Y].[ext]

```

**Examples:**
- `HLD-0001_OrderManagementSystem_v1.0.md`
- `HLD-0015_PaymentGateway_v2.1.yaml`

**Rules:**
- `ShortTitle` uses PascalCase with no spaces.
- Version follows Semantic versioning (Major.Minor).
- Extension matches format: `.md` for Markdown, `.yaml` for YAML, `.pdf` for published snapshots.

### 2.3 Version Numbering

| Change Type | Version Impact | Example |
|-------------|---------------|---------|
| New document created | 0.1 (Draft) | Initial draft |
| Structural change (new component, removed section) | Major increment (1.0 → 2.0) | Added new subsystem |
| Content update (clarification, diagram refresh) | Minor increment (1.0 → 1.1) | Updated data flow |
| Approved baseline | Round to next Major (→ 1.0, 2.0) | Post-review approval |

---

## 3. Scope & Granularity

### 3.1 Unit of Documentation

One HLD instance covers **one system or one subsystem**. The boundary should align with a deployable unit, a bounded
context (in DDD terms), or a logical system boundary recognized by the architecture team.

### 3.2 When to Create a New HLD vs. Update an Existing One

| Scenario | Action |
|----------|--------|
| Greenfield system being designed | Create new HLD |
| Existing system adding a new major component | Update existing HLD (major version increment) |
| Existing system undergoing minor design refinement | Update existing HLD (minor version increment) |
| New subsystem that will be independently deployed | Create new HLD with reference to parent system HLD |
| System redesign / re-architecture | Create new HLD; mark previous as Superseded |

### 3.3 Parent–Child Relationships

A system-level HLD may reference subsystem-level HLDs. Use the `related_documents` field in metadata to establish
traceability. The parent HLD should contain a component listing that points to child HLDs where detailed design is
delegated.

---

## 4. Section-by-Section Explanation

### Section 1: Introduction

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Establishes context — why the design exists, what problem it solves. |
| **What to Include** | Design motivation, system boundary, audience assumptions, references to upstream docs. |
| **What NOT to Include** | Detailed requirements (those belong in SRS/FRD), implementation specifics (those belong in LLD). |
| **Required** | Yes |

### Section 2: Design Goals & Constraints

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Defines the architectural drivers that shape every design decision. |
| **What to Include** | Quality attribute goals (from NFRs), hard constraints (regulatory, budgetary, legacy), and assumptions with impact analysis. |
| **What NOT to Include** | Business justification (that belongs in PC), functional requirements (SRS/FRD). |
| **Required** | Yes |

### Section 3: System Architecture Overview

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Gives the reader a "10,000-foot view" of the system. |
| **What to Include** | Architecture style justification, top-level diagram (C4 Context/Container or equivalent), narrative walkthrough. |
| **What NOT to Include** | Detailed class or sequence diagrams (LLD), infrastructure sizing calculations. |
| **Examples** | "The system adopts a microservices architecture with event-driven communication between bounded contexts." |
| **Required** | Yes |

### Section 4: Component Design

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Decomposes the system into its major building blocks. This is the core of the HLD. |
| **What to Include** | For each component: responsibility, interfaces (with direction and protocol), dependencies, and technology stack. |
| **What NOT to Include** | Internal class structure, method signatures, database column definitions (those belong in LLD). |
| **Required** | Yes |

### Section 5: Technology Stack

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Provides a consolidated, justified view of all technology selections. |
| **What to Include** | Category-level summary table, key decision rationale, links to ADRs. |
| **What NOT to Include** | Version-specific library dependencies (those belong in LLD or package manifests). |
| **Required** | Yes |

### Section 6: Data Architecture

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Describes data storage, flow, and governance across the system. |
| **What to Include** | Conceptual/logical data model, data flow diagram, storage strategy with retention policies. |
| **What NOT to Include** | Physical schema (column types, indexes) — that belongs in LLD. |
| **Required** | Yes |

### Section 7: Integration Architecture

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Covers all internal and external integration points. |
| **What to Include** | Service-to-service communication patterns, external API integrations with SLA and failure handling, integration diagram. |
| **What NOT to Include** | Detailed API request/response payloads (those belong in API Spec documents). |
| **Required** | Yes |

### Section 8: Security Architecture

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Defines the security posture — authN, authZ, data protection, threat mitigations. |
| **What to Include** | Authentication and authorization mechanisms, encryption strategy, threat model summary. |
| **What NOT to Include** | Detailed security test cases (those belong in Test Plan), penetration test results. |
| **Required** | Yes |

### Section 9: Deployment Architecture

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Describes how the system is deployed and the runtime infrastructure. |
| **What to Include** | Infrastructure overview, deployment diagram, deployment strategy (blue-green, canary, etc.), environment listing. |
| **What NOT to Include** | Step-by-step deployment procedures (those belong in Deployment Guide). |
| **Required** | Yes |

### Section 10: Observability & Operations

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Ensures the system is operationally ready — monitorable, debuggable, alertable. |
| **What to Include** | Monitoring strategy, logging approach, alerting definitions, SLA/SLO/SLI definitions. |
| **What NOT to Include** | Specific dashboard JSON configurations, runbook procedures (those belong in Runbook documents). |
| **Required** | Yes |

### Section 11: Design Decisions & Rationale

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Records the "why" behind significant architecture choices using the ADR pattern. |
| **What to Include** | Context, options considered (with pros/cons), chosen option with rationale, consequences. |
| **What NOT to Include** | Trivial decisions (e.g., code formatting style). Only decisions with architectural significance. |
| **Required** | Yes |

### Section 12: Risks & Mitigations

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Identifies architectural and technical risks so they are visible and actively managed. |
| **What to Include** | Risk description, likelihood, impact, mitigation strategy, and owner. |
| **What NOT to Include** | Business/project risks (those belong in PMP), security vulnerabilities (those belong in threat model). |
| **Required** | Yes |

### Section 13: Future Considerations

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Captures deferred decisions and anticipated evolution to inform future design iterations. |
| **What to Include** | Known future enhancements, scaling considerations, deferred decisions with rationale. |
| **Required** | No — Optional, but strongly recommended for systems expected to evolve. |

### Section 14: Glossary

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Ensures consistent terminology across the audience. |
| **What to Include** | Technical terms, acronyms, and domain-specific language used in the document. |
| **Required** | No — Optional, but recommended when the audience may have varying domain familiarity. |

---

## 5. Update Triggers

### 5.1 Creation Triggers

A new HLD must be created when:
- A new system or independently deployable subsystem is being designed.
- An existing system is undergoing a complete re-architecture.
- A spin-off of an existing system into a separate bounded context is planned.

### 5.2 Update Triggers

An existing HLD must be updated when:
- An architecture decision is changed (e.g., switching from monolith to microservices).
- A new major component or service is added to the system.
- A new external integration point is introduced.
- The technology stack changes materially (e.g., database migration, cloud provider change).
- A design risk materializes and the mitigation changes the architecture.
- Non-functional requirements are revised (e.g., new SLA targets, scaling requirements).

### 5.3 Review Triggers

An HLD must be re-reviewed (even without content changes) when:
- A new compliance or regulatory requirement is imposed.
- A related upstream document (SRS, NFR) is significantly revised.
- A post-incident review identifies architectural gaps.
- 12 months have elapsed since the last review (annual review cycle).

### 5.4 Retirement Triggers

An HLD should be marked as **Superseded** or **Retired** when:
- A new HLD replaces it due to system re-architecture.
- The system it describes is decommissioned.
- It has been superseded by a combined SAD (Software Architecture Document) that absorbs its content.

---

## 6. Roles & Responsibilities

| Role | Responsibility |
|------|---------------|
| **Solution Architect / Lead Architect** | Primary author. Responsible for design integrity and completeness. |
| **Tech Lead** | Co-author or contributor, especially for component design and technology stack sections. |
| **Peer Architect** | Reviewer. Validates design decisions, identifies gaps, and challenges assumptions. |
| **Engineering Manager** | Approver. Confirms organizational alignment and resource feasibility. |
| **Security Architect** | Reviewer for Section 8 (Security Architecture). |
| **DevOps / Platform Lead** | Reviewer for Section 9 (Deployment) and Section 10 (Observability). |
| **Author (ongoing)** | Accountable for keeping the HLD current through the system's lifecycle. |

---

## 7. Quality Checklist

Before submitting the HLD for review, the author should verify:

- [ ] All **required** sections are completed with substantive content (not just placeholders).
- [ ] Document ID follows the `HLD-[NNNN]` naming convention.
- [ ] File is named per convention: `HLD-[NNNN]_[ShortTitle]_v[X.Y].[ext]`.
- [ ] All related documents are linked in the metadata and Section 1.4 References.
- [ ] Architecture diagrams are included or referenced (not described only in text).
- [ ] Every component in Section 4 has defined interfaces and dependencies.
- [ ] Technology choices in Section 5 include rationale (not just names).
- [ ] Security section addresses authentication, authorization, and data protection.
- [ ] At least one design decision is documented in Section 11.
- [ ] All identified risks have a mitigation strategy and an assigned owner.
- [ ] Change log is updated with the current version entry.
- [ ] Document has been spell-checked and diagrams are legible.
- [ ] Reviewed by: Peer Architect, Security Architect (Sec 8), DevOps Lead (Sec 9–10).

---

*This policy document governs the creation, maintenance, and governance of HLD documents within the organization. For
questions or proposed changes to this policy, contact the Architecture Office.*
