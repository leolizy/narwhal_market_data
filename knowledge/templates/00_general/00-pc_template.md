# Platform Canon (PC)

| Field              | Value                                                        |
|--------------------|--------------------------------------------------------------|
| Document ID        | PC-[PROJECT_CODE]-[NNNN]                                    |
| Title              |                                                              |
| Version            |                                                              |
| Status             | Draft / InReview / Approved / Deprecated                     |
| Classification     | Public / Internal / Confidential / Restricted                |
| Created Date       |                                                              |
| Last Updated       |                                                              |
| Author             |                                                              |
| Reviewer           |                                                              |
| Approver           |                                                              |
| Business Sponsor   |                                                              |
| Related Documents  |                                                              |
| Supersedes         |                                                              |

---

## 1. Executive Summary

> **Guidance:** Provide a concise overview of the initiative, its business driver, and the expected outcome. Should be
understandable by a senior stakeholder in under 2 minutes. This section sets the context for all subsequent content.
*(Reference: BABOK Section 4.5 — Define Business Need)*

[Content here]

---

## 2. Business Objectives

> **Guidance:** List measurable business goals this initiative aims to achieve. Each objective should be SMART
(Specific, Measurable, Achievable, Relevant, Time-bound). Use the ID format `BO-NNN`. *(Reference: BABOK Section 6.1 —
Define Future State)*

| ID     | Objective Statement                          | Success Measure          |
|--------|----------------------------------------------|--------------------------|
| BO-001 |                                              |                          |
| BO-002 |                                              |                          |

---

## 3. Problem Statement

> **Guidance:** Articulate the current pain points, inefficiencies, or gaps that justify this initiative. This section
should make the "why" immediately clear and tie directly to the Business Objectives above. *(Reference: BABOK Section
4.4 — Define Business Need)*

[Content here]

---

## 4. Scope

> **Guidance:** Define a clear boundary of what is included and excluded. Include domain-specific data entity
definitions or term clarifications where the business domain requires precision. *(Reference: IEEE 830 Section 1.2 —
Scope)*

### In Scope

1. [Item]

### Out of Scope

1. [Item]

### Domain Definitions

> **Guidance:** Define domain-specific data entities, hierarchies, or business terms that are essential for interpreting
the requirements in this document. Only include definitions that directly affect how requirements should be read.

[Content here — e.g., data entity levels, business term definitions]

---

## 5. Stakeholder Analysis

> **Guidance:** Identify all parties with an interest in or influence over the initiative. Include their role, what they
care about, and what they are responsible for. *(Reference: BABOK Section 2.2 — Stakeholder Analysis)*

| Stakeholder          | Role                | Interest                    | Responsibility                      |
|----------------------|---------------------|-----------------------------|-------------------------------------|
|                      |                     |                             |                                     |

---

## 6. Current State Analysis

> **Guidance:** Describe the existing situation — processes, systems, and pain points. This establishes the baseline
against which improvements will be measured. *(Reference: BABOK Section 6.1 — Define Current State)*

1. [Current state observation]

---

## 7. Future State Vision

> **Guidance:** Describe the desired end state after the initiative is delivered. Include measurable target-state
outcomes. *(Reference: BABOK Section 6.2 — Define Future State)*

### Vision

[Vision narrative]

### Target-State Outcomes

1. [Outcome]

---

## 8. Functional Requirements

> **Guidance:** Each requirement must be uniquely identified (`PC-NNN`), prioritized using MoSCoW, and traceable to a
Business Objective (`BO-NNN`). Group related requirements under a functional area heading (`FR-N`). Sub-requirements use
dotted notation (`FR-N.N`). Acceptance criteria use the format `AC-PC-NNN-NN`. *(Reference: IEEE 830 Section 3 —
Specific Requirements; BABOK Section 7)*

### FR-1 [Functional Area Name]

- **FR-1.1** [Requirement statement]
- **FR-1.2** [Requirement statement]

| Requirement ID | Priority | Traces To | Acceptance Criteria ID | Acceptance Statement |
|----------------|----------|-----------|------------------------|--------------------- |
| PC-001         | Must     | BO-001    | AC-PC-001-01           |                      |

### FR-2 [Functional Area Name]

- **FR-2.1** [Requirement statement]

---

## 9. Non-Functional Requirements

> **Guidance:** Quality attributes and system-wide constraints. Each should include a measurable target metric.
Categories include: Availability, Performance, Scalability, Reliability, Security, Auditability, Maintainability,
Observability, Interoperability, Compliance, Data Retention. *(Reference: IEEE 830 Section 3.3 — Performance
Requirements)*

| #  | Category        | Requirement Statement                                    | Target Metric         |
|----|-----------------|----------------------------------------------------------|-----------------------|
| 1  | Availability    |                                                          |                       |
| 2  | Performance     |                                                          |                       |

---

## 10. Assumptions & Constraints

> **Guidance:** Assumptions are conditions believed to be true but not yet confirmed — they must be validated during
delivery. Constraints are fixed limitations (technical, regulatory, budgetary) that bound the solution. *(Reference:
BABOK Section 6.3)*

### Assumptions

1. [Assumption]

### Constraints

1. [Constraint]

---

## 11. Risks & Mitigation Strategies

> **Guidance:** Identify business and delivery risks. Assess impact and likelihood. Provide concrete mitigation
strategies. *(Reference: BABOK Section 6.4 — Define Risk)*

| Risk                          | Impact | Likelihood | Mitigation                                    |
|-------------------------------|--------|------------|-----------------------------------------------|
|                               |        |            |                                               |

---

## 12. Success Metrics / KPIs

> **Guidance:** Quantifiable indicators that will be used to measure initiative success post-delivery. Each metric
should map back to a Business Objective.

| Metric                     | Target                  | Measurement Method            |
|----------------------------|-------------------------|-------------------------------|
|                            |                         |                               |

---

## 13. Dependencies

> **Guidance:** External or internal dependencies that could affect delivery timeline or scope. Include system
dependencies, team dependencies, and third-party dependencies.

1. [Dependency]

---

## 14. Glossary

> **Guidance:** Definitions of domain-specific terms, acronyms, and abbreviations used in this document. *(Reference:
IEEE 830 Section 1.4 — Definitions)*

| Term       | Definition                                       |
|------------|--------------------------------------------------|
|            |                                                  |

---

## 15. Traceability Matrix

> **Guidance:** Maps each requirement to its originating business objective and downstream artifacts (FRD, test cases,
etc.) for impact analysis and coverage tracking. This section may be maintained separately in a traceability tool and
linked here.

| Requirement ID | Traces To Objective | Downstream Artifacts         |
|----------------|---------------------|------------------------------|
| PC-001         | BO-001              | FRD-NPH-0001, TC-NPH-001    |

---

## 16. Approval

> **Guidance:** Document is not considered Approved until all required approvals are captured.

| Role                                      | Name | Decision                                      | Signature | Date |
|-------------------------------------------|------|-----------------------------------------------|-----------|------|
| Product Manager (System Owner)            |      | Approved / Approved with Conditions / Rejected |           |      |
| Head of Consuming Team Representative     |      |                                                |           |      |
| Risk/Margin Methodology Owner             |      |                                                |           |      |
| Technology Delivery Lead                  |      |                                                |           |      |
| Information Security/Compliance Rep       |      |                                                |           |      |

---

## Change Log

| Version | Date | Author | Change Summary |
|---------|------|--------|----------------|
|         |      |        |                |

---

## Attachments

| Filename | Description | Location |
|----------|-------------|----------|
|          |             |          |
