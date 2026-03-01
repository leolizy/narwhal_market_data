# NFR-0001: Non-Functional Requirements (NFR) — Document Policy

## Document Overview

### What Is This Document Type?

The Non-Functional Requirements (NFR) document captures the quality attributes, constraints, and measurable thresholds
that a system must satisfy beyond its functional behaviour. While functional requirements describe *what* a system does,
NFRs define *how well* it must perform, how reliable it must be, how secure, how maintainable, and how observable.

### Function in the SDLC

The NFR document serves as the authoritative contract between product, engineering, SRE, security, and compliance
stakeholders regarding system quality expectations. It is created during the requirements analysis phase (after the PC
and alongside or after the FRD), and it remains a living document throughout the system's lifecycle. NFRs directly
inform architecture decisions, testing strategies, infrastructure sizing, and operational runbooks.

### Position in the Document Hierarchy

The NFR document sits in the requirements tier of the SDLC document hierarchy:

```
Platform Canon (PC)
  └── Functional Requirements Document (FRD)
  └── Non-Functional Requirements Document (NFR)  ← this document
        └── Requirements Traceability Matrix (RTM)
        └── High-Level Design (HLD)
        └── Test Plan / Test Strategy

```

The PC provides business context. The FRD and NFR together provide the complete requirements picture. The NFR feeds into
the HLD (for architectural decisions driven by quality attributes), the Test Plan (for non-functional test scenarios),
and the RTM (for end-to-end traceability).

---

## Document Dependencies

### Upstream Documents (Dependencies)

- PC-0001

### Downstream Documents (Depend on This)

- CICD-0001, DBAD-0001, TSI-0001, NFRAR-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

### Document ID Format

```
NFR-[NNNN]

```

Where `NNNN` is a zero-padded sequential number, unique per system. Examples: `NFR-0001`, `NFR-0002`.

### Prefix

Use `NFR` as the prefix. This distinguishes non-functional requirements documents from other document types (PC, FRD,
HLD, etc.) and provides immediate recognition in document registries and traceability matrices.

### Numbering Scheme

Sequential per system. Each system maintains its own NFR document counter starting at `0001`. If a system has only one
NFR document (the typical case for per-system granularity), it will be `NFR-0001`.

### File Naming Convention

```
NFR-[NNNN]_[ShortTitle]_v[X.Y].[ext]

```

Examples:
- `NFR-0001_OrderManagementSystem_v1.0.md`
- `NFR-0001_OrderManagementSystem_v1.0.yaml`
- `NFR-0001_OrderManagementSystem_v2.1.md`

### Version Numbering

Semantic Major.Minor versioning:
- **Major increment (X.0):** Structural changes — new sections added/removed, significant re-scoping, or major threshold
  changes that affect architecture.
- **Minor increment (X.Y):** Content updates — refined acceptance criteria, updated thresholds, new individual NFRs
  added within existing categories, editorial corrections.

---

## Scope & Granularity

### Unit of Documentation

One NFR document instance covers **one system (or application)**. The "system" is defined as the deployable unit with a
distinct identity, team ownership, and SLA boundary.

### When to Create a New Document vs. Update an Existing One

**Create a new NFR document** when:
- A new system is being built from scratch.
- A system is being split into independently deployable services that will have distinct SLA boundaries.
- A system is undergoing a major re-architecture where the previous NFR baseline is no longer applicable.

**Update the existing NFR document** when:
- New non-functional requirements are identified for the same system.
- Acceptance criteria thresholds change (e.g., availability target moves from 99.9% to 99.95%).
- New compliance obligations apply to the system (e.g., system comes into ISO 27001 scope).
- Open items are resolved or new open items are identified.

### Relationship to Parent/Child Documents

- **Parent:** PC — provides the business drivers that justify NFRs.
- **Sibling:** FRD — provides functional requirements; some functional requirements may generate non-functional
  implications.
- **Children:** RTM (maps NFRs to verification evidence), HLD (references NFRs as architecture drivers), Test Plan
  (references NFRs for non-functional test scenarios).

---

## Section-by-Section Explanation

### Section 1: Document Control

**Purpose:** Establishes the governance metadata — who owns this document, what version it is, and what related
documents exist.

**What to include:** Version number, status, scope statement, and links (absolute paths or URLs) to the parent PC,
sibling FRD, and the RTM CSV.

**What NOT to include:** Detailed requirement content — that belongs in the NFR Catalog. Do not duplicate metadata that
already exists in the metadata table at the top.

**Required:** Yes.

---

### Section 2: Traceability Model

**Purpose:** Defines the two reference dimensions that every NFR must trace to — Business Drivers (why this NFR exists)
and Verification Evidence Types (how compliance is proven).

**What to include:**
- Business Drivers (BD): High-level business motivations such as SLA commitments, regulatory obligations, competitive
  benchmarks, user experience targets, or cost constraints. Each BD gets a unique ID (BD-01, BD-02, ...).
- Verification Evidence Types (VE): Categories of proof artifacts. Each VE gets a unique ID (VE-01, VE-02, ...) and maps
  to a concrete artifact type (e.g., load test report, SLO dashboard, DR drill record, security scan report).

**What NOT to include:** The actual evidence artifacts — those are linked from the NFR Catalog and the Attachments
section. This section defines the *types* of evidence, not instances.

**Examples:**
- BD-01: "99.9% uptime SLA commitment to enterprise clients"
- VE-04: "Security Scan & Vulnerability SLA Report — quarterly output from automated scanning pipeline"

**Required:** Yes.

---

### Section 3: NFR Catalog

**Purpose:** The authoritative register of all non-functional requirements for this system. This is the core of the
document.

**What to include:** For each NFR:
- **ID:** Sequential (NFR-001, NFR-002, ...).
- **Category:** Aligned to ISO 25010 quality characteristics — Performance, Reliability, Usability, Maintainability,
  Security, Observability. Optionally include Portability and Compatibility if relevant.
- **Requirement Statement:** A clear, testable, unambiguous statement of the requirement.
- **Rationale:** Why this requirement matters to the business (links back to Business Drivers).
- **Measurable Acceptance Criteria:** A quantified threshold with a defined test method. Must be objectively verifiable.
- **Priority:** Critical, High, Medium, or Low.
- **Traceability:** Links to specific BD and VE IDs from Section 2.
- **Compliance Tags:** ISO 27001 Annex A controls and/or SOC2 Trust Service Criteria that this NFR supports (if
  applicable).

**What NOT to include:** Functional requirements, design decisions, or implementation details. NFRs describe quality
attributes, not how to achieve them.

**Examples:**
- Good: "The system shall respond to 95% of API requests within 200ms under a load of 1,000 concurrent users, measured
  via load testing with k6."
- Bad: "The system should be fast." (not measurable)
- Bad: "Use Redis for caching to improve performance." (implementation detail, not a requirement)

**Required:** Yes.

---

### Section 4: NFR Baseline Checklist

**Purpose:** A quick-reference pre-flight checklist ensuring the author has addressed all quality categories before
submitting the document for review.

**What to include:** A checkbox list grouped by ISO 25010 category, with sub-areas that should be explicitly defined in
the NFR Catalog.

**What NOT to include:** The actual requirements — this is a completeness check, not a duplicate of the catalog. Authors
check each box to confirm they have addressed the sub-area in Section 3.

**Required:** Yes.

---

### Section 5: Compliance Mapping (ISO 27001 / SOC2)

**Purpose:** Provides a cross-reference from NFRs to specific ISO 27001 Annex A controls and SOC2 Trust Service
Criteria. This section supports audit readiness by demonstrating that quality requirements are mapped to compliance
obligations.

**What to include:** For each relevant NFR, list the ISO 27001 controls (e.g., A.8.24 — Use of cryptography) and SOC2
criteria (e.g., CC6.1 — Logical and physical access controls) it satisfies, along with a reference to the verification
evidence.

**What NOT to include:** Full control descriptions — reference the control ID and let auditors cross-reference against
the standard. Do not duplicate the NFR Catalog content.

**Required:** No — required only when the system is in scope for ISO 27001 certification or SOC2 audit.

---

### Section 6: Open Items

**Purpose:** Tracks unresolved questions, pending decisions, or gaps. Open items are the primary blocker between
Conditionally Approved and Approved status.

**What to include:** Each open item needs a unique ID (OI-001, OI-002, ...), a description, the impacted NFR IDs, an
owner, a target resolution date, a status, and a description of what closure evidence is required.

**What NOT to include:** Resolved items that have been closed in previous versions — move those to the Change Log. Keep
this section focused on currently active items.

**Required:** Yes (even if empty — indicate "No open items" explicitly).

---

### Section 7: Stakeholder Sign-Off

**Purpose:** Records formal approval decisions from each required stakeholder group. The document lifecycle cannot
advance to Approved without unanimous sign-off and all open items closed.

**What to include:**
- The list of required stakeholder groups.
- The conditional approval rules (Blocked, Conditionally Approved, Approved).
- The sign-off tracker with reviewer name, decision, date, and any conditions or notes.

**What NOT to include:** Detailed review feedback — that belongs in review comments or a separate review log. This
section records the *decision*, not the *discussion*.

**Required:** Yes.

---

### Section 8: Appendix — RTM Mapping Guidance

**Purpose:** Defines the structure of the companion RTM CSV file so that anyone generating or consuming the RTM knows
what columns to expect.

**What to include:** The minimum required columns for the RTM CSV, including NFR_ID, Category, PC linkages, verification
method, KPI/SLO targets, and compliance mappings (ISO27001_Control, SOC2_Criteria).

**What NOT to include:** Actual RTM data — the data lives in the CSV file itself, not in this appendix.

**Required:** Yes.

---

### Section 9: Attachments

**Purpose:** Centralises references to supporting files — test reports, dashboard screenshots, scan outputs, DR drill
records, and any other evidence artifacts.

**What to include:** Filename, brief description, and path/URL for each attachment.

**What NOT to include:** Inline content from the attachments — provide references only.

**Required:** No (optional, but strongly recommended for Approved documents).

---

### Change Log

**Purpose:** Version history. Every version increment must have a corresponding entry.

**What to include:** Version number, date, author, and a brief summary of changes.

**Required:** Yes.

---

## Update Triggers

### Creation Triggers

A new NFR document must be created when:
- A new system or application is initiated and enters the requirements phase.
- An existing system is being re-platformed or re-architected with fundamentally different quality requirements.
- A system is split into independently operated services with distinct SLA boundaries.

### Update Triggers

The existing NFR document must be updated when:
- New non-functional requirements are identified (e.g., new compliance obligation, new SLA tier).
- Acceptance criteria thresholds change (e.g., availability target increases).
- An open item is resolved or a new open item is identified.
- A post-incident review (PIR) reveals that an NFR was inadequate or missing.
- Architecture changes affect the feasibility of existing NFRs.
- A stakeholder requests a re-evaluation of priorities.
- The system comes into scope for a new compliance framework (e.g., ISO 27001, SOC2).

### Review Triggers

The NFR document must be re-reviewed (even without changes) when:
- A major release is planned — review NFRs for continued relevance and adequacy.
- Annual compliance review cycle — confirm NFRs still align with audit requirements.
- Organisational SLA policy changes — confirm system-level NFRs reflect the new policy.
- A significant incident occurs — review whether NFRs need strengthening.

### Retirement Triggers

The NFR document should be marked as **Superseded** or **Retired** when:
- The system is decommissioned.
- The system undergoes a complete re-architecture and a new NFR document is created to replace this one.
- The system is merged into another system whose NFR document absorbs the requirements.

---

## Roles & Responsibilities

| Role                     | Responsibility                                                                                   |
|--------------------------|--------------------------------------------------------------------------------------------------|
| **Author**               | Drafts and maintains the NFR document. Typically a Solutions Architect, Tech Lead, or Senior Engineer. |
| **Engineering Lead**     | Reviews for technical feasibility and completeness. Co-authors where necessary.                   |
| **Product Owner**        | Reviews for alignment with business priorities and SLA commitments.                              |
| **SRE/DevOps Lead**      | Reviews reliability, observability, and operational feasibility. Validates RTO/RPO targets.       |
| **Security Lead**        | Reviews security NFRs and compliance mappings. Validates alignment with ISO 27001/SOC2 controls.  |
| **Compliance Lead**      | Reviews compliance mapping section. Confirms audit readiness.                                    |
| **Operations/Support Lead** | Reviews usability and supportability requirements.                                            |
| **Approver**             | Grants final approval after all stakeholders have signed off and all open items are closed. Typically a Head of Engineering or CTO. |
| **Document Owner**       | Accountable for keeping the document current throughout the system's lifecycle. Typically the Solutions Architect or Tech Lead who owns the system. |

---

## Quality Checklist

Authors must complete this checklist before submitting the NFR document for review:

- [ ] Document ID follows the naming convention (`NFR-[NNNN]`)
- [ ] File is named according to convention (`NFR-[NNNN]_[ShortTitle]_v[X.Y].[ext]`)
- [ ] All required sections are completed (Document Control, Traceability Model, NFR Catalog, Baseline Checklist, Open
  Items, Stakeholder Sign-Off, RTM Mapping Guidance, Change Log)
- [ ] Every NFR has a unique sequential ID (NFR-001, NFR-002, ...)
- [ ] Every NFR is categorised using ISO 25010 quality characteristics
- [ ] Every NFR has measurable, quantified acceptance criteria with a defined test method
- [ ] Every NFR traces to at least one Business Driver (BD) and one Verification Evidence Type (VE)
- [ ] Security-related NFRs include ISO 27001/SOC2 compliance tags where applicable
- [ ] The NFR Baseline Checklist is fully checked — all applicable sub-areas are addressed
- [ ] Compliance Mapping section is populated (if the system is in ISO 27001/SOC2 scope)
- [ ] All open items have an owner, target date, and defined closure evidence
- [ ] Related documents (PC, FRD, RTM) are linked with valid paths or URLs
- [ ] Change Log is updated with the current version entry
- [ ] Document has been spell-checked and reviewed for clarity
- [ ] Document has been reviewed by at least the Engineering Lead and one domain-specific stakeholder before formal
  sign-off

---

## Compliance Framework Reference

### ISO 25010 Quality Characteristics (Category Reference)

The NFR Catalog categories are aligned to the ISO/IEC 25010:2011 product quality model:

| Category        | ISO 25010 Characteristic | Description                                                        |
|-----------------|--------------------------|---------------------------------------------------------------------|
| Performance     | Performance Efficiency    | Time behaviour, resource utilisation, capacity                      |
| Reliability     | Reliability               | Maturity, availability, fault tolerance, recoverability             |
| Usability       | Usability                 | Learnability, operability, accessibility, UI aesthetics             |
| Maintainability | Maintainability           | Modularity, reusability, analysability, modifiability, testability  |
| Security        | Security                  | Confidentiality, integrity, non-repudiation, accountability, authenticity |
| Observability   | (Cross-cutting)           | Not a standalone ISO 25010 characteristic but essential for operational quality. Covers logging, metrics, tracing, and alerting. |
| Portability     | Portability               | Adaptability, installability, replaceability (optional)             |
| Compatibility   | Compatibility             | Co-existence, interoperability (optional)                           |

### ISO 27001 Annex A Controls (Common NFR Mappings)

| Control ID | Control Name                    | Typical NFR Category |
|------------|---------------------------------|----------------------|
| A.5.1      | Policies for information security | Security           |
| A.8.5      | Secure authentication            | Security            |
| A.8.9      | Configuration management         | Maintainability     |
| A.8.15     | Logging                          | Observability       |
| A.8.24     | Use of cryptography              | Security            |
| A.8.25     | Secure development lifecycle     | Maintainability     |
| A.8.28     | Secure coding                    | Security            |
| A.8.29     | Security testing                 | Security            |
| A.8.34     | Protection of info during audit  | Security            |

### SOC2 Trust Service Criteria (Common NFR Mappings)

| Criteria | Name                    | Typical NFR Category         |
|----------|-------------------------|------------------------------|
| CC6.1    | Logical/physical access  | Security                     |
| CC6.6    | Security against threats | Security                     |
| CC7.2    | System monitoring        | Observability                |
| CC7.3    | Evaluating events        | Observability                |
| CC7.4    | Incident response        | Reliability / Observability  |
| CC8.1    | Change management        | Maintainability              |
| A1.1     | Capacity and availability| Reliability / Performance    |
| A1.2     | Recovery mechanisms      | Reliability                  |

---

*Policy Version: 1.0 | Last Updated: 2026-02-23 | Framework: ISO 25010 + ISO 27001 / SOC2*
