# <System Name> — Non-Functional Requirements (NFR)

| Field            | Value                                                                               |
|------------------|-------------------------------------------------------------------------------------|
| Document ID      | NFR-[NNNN]                                                                          |
| Title            |                                                                                     |
| System Name      |                                                                                     |
| Version          |                                                                                     |
| Status           | Draft / InReview / CondApproved / Approved / Superseded / Retired                  |
| Classification   | Public / Internal / Confidential / Restricted                                       |
| Created Date     |                                                                                     |
| Last Updated     |                                                                                     |
| Author           |                                                                                     |
| Reviewer         |                                                                                     |
| Approver         |                                                                                     |
| Parent PC       |                                                                                     |
| Supersedes       |                                                                                     |
| Tags             |                                                                                     |

## Related Documents

| Document ID | Title | Path/URL |
|-------------|-------|----------|
|             |       |          |
|             |       |          |
|             |       |          |

---

## 1. Document Control

> **Guidance:** Capture the version, status, scope, and links to related upstream/downstream documents (PC, FRD, RTM).
This section establishes the governance envelope for this NFR document instance.

- **Version:** <vX.Y>
- **Status:** <Draft | InReview | CondApproved | Approved | Superseded | Retired>
- **Scope:** <System or process scope statement — what this NFR document covers>
- **Related Documents:**
  - PC: <absolute path or URL>
  - FRD Traceability Matrix: <absolute path or URL>
  - RTM CSV: <absolute path or URL>

---

## 2. Traceability Model

> **Guidance:** Define the business drivers (BD) that justify each NFR and the verification evidence types (VE) used to
prove compliance. Every NFR in the catalog must trace back to at least one BD and one VE.

### 2.1 Business Drivers (BD)

> **Guidance:** High-level business motivations that generate non-functional needs. Examples include regulatory
obligations, SLA commitments, user experience targets, competitive benchmarks, and cost constraints.

- **BD-01:** <driver statement>
- **BD-02:** <driver statement>
- **BD-03:** <driver statement>

### 2.2 Verification Evidence Types (VE)

> **Guidance:** Categories of evidence that prove an NFR has been met. Each VE maps to a concrete artifact type (report,
dashboard, drill record, scan output).

| VE ID  | Evidence Type                                   | Description |
|--------|-------------------------------------------------|-------------|
| VE-01  | e.g., Load/Performance Test Report              |             |
| VE-02  | e.g., Availability/SLO Dashboard                |             |
| VE-03  | e.g., DR/Restore Drill Record                   |             |
| VE-04  | e.g., Security Scan & Vulnerability SLA Report  |             |
| VE-05  | e.g., Usability/Accessibility Audit Evidence    |             |
| VE-06  | e.g., CI/CD and Release Logs                    |             |
| VE-07  | e.g., Observability Dashboards & PIR Records    |             |

---

## 3. NFR Catalog

> **Guidance:** The authoritative register of all non-functional requirements for this system. Each NFR must be uniquely
identified (NFR-0001, NFR-0002, ...), categorised per ISO 25010 quality characteristics, linked to business drivers and
verification evidence, and include quantified, measurable acceptance criteria. Categories: Performance, Reliability,
Usability, Maintainability, Security, Observability, Portability (optional), Compatibility (optional).

| ID      | Category        | Requirement Statement         | Rationale          | Measurable Acceptance Criteria       | Priority | Traceability (BD; VE) | Compliance Tags         |
|---------|-----------------|-------------------------------|--------------------|--------------------------------------|----------|-----------------------|-------------------------|
| NFR-001 | Performance     | <clear, testable requirement> | <why it matters>   | <quantified threshold + test method> |          | BD-xx; VE-zz          | ISO27001-A.xx, SOC2-CCx |
| NFR-002 | Reliability     | <clear, testable requirement> | <why it matters>   | <quantified threshold + test method> |          | BD-xx; VE-zz          |                         |
| NFR-003 | Usability       | <clear, testable requirement> | <why it matters>   | <quantified threshold + test method> |          | BD-xx; VE-zz          |                         |
| NFR-004 | Maintainability | <clear, testable requirement> | <why it matters>   | <quantified threshold + test method> |          | BD-xx; VE-zz          |                         |
| NFR-005 | Security        | <clear, testable requirement> | <why it matters>   | <quantified threshold + test method> |          | BD-xx; VE-zz          |                         |
| NFR-006 | Observability   | <clear, testable requirement> | <why it matters>   | <quantified threshold + test method> |          | BD-xx; VE-zz          |                         |

---

## 4. NFR Baseline Checklist

> **Guidance:** A quick-reference checklist ensuring that each ISO 25010 quality category has been adequately addressed.
Authors must confirm all applicable sub-areas are covered before submitting for review.

### Performance

- [ ] Response time targets defined
- [ ] Throughput targets defined
- [ ] Scalability requirements defined (horizontal/vertical)
- [ ] Concurrency limits defined
- [ ] Resource utilisation thresholds defined

### Reliability

- [ ] Availability target defined (e.g., 99.9%)
- [ ] RTO (Recovery Time Objective) defined
- [ ] RPO (Recovery Point Objective) defined
- [ ] Failure handling and graceful degradation defined
- [ ] Backup and restore strategy defined
- [ ] Disaster recovery plan referenced

### Usability

- [ ] Accessibility standard defined (e.g., WCAG 2.1 AA)
- [ ] Onboarding/learning expectations defined
- [ ] UI responsiveness targets defined
- [ ] Internationalisation/localisation requirements defined

### Maintainability

- [ ] Coding standards and linting rules defined
- [ ] CI/CD pipeline requirements defined
- [ ] Deployment frequency targets defined
- [ ] Modularity and coupling constraints defined
- [ ] Documentation requirements defined
- [ ] Technical debt management approach defined

### Security

- [ ] Authentication and authorisation model defined
- [ ] Encryption in transit and at rest requirements defined
- [ ] Privacy and compliance obligations defined (GDPR, SOC2, ISO 27001)
- [ ] Vulnerability management SLA defined
- [ ] Secrets management approach defined
- [ ] Audit logging requirements defined
- [ ] Penetration testing cadence defined

### Observability

- [ ] Logging standards and retention defined
- [ ] Metrics and dashboards defined
- [ ] Alerting thresholds and escalation paths defined
- [ ] Distributed tracing requirements defined
- [ ] Incident response process referenced
- [ ] Post-incident review (PIR) cadence defined

---

## 5. Compliance Mapping (ISO 27001 / SOC2)

> **Guidance:** Maps each NFR to relevant ISO 27001 Annex A controls and/or SOC2 Trust Service Criteria. Required when
the system is in scope for ISO 27001 certification or SOC2 audit. Optional otherwise.

| NFR ID  | ISO 27001 Controls | SOC2 Criteria | Evidence Reference |
|---------|--------------------|---------------|--------------------|
|         |                    |               |                    |
|         |                    |               |                    |

---

## 6. Open Items

> **Guidance:** Track unresolved questions, pending decisions, or gaps that must be closed before the NFR document can
achieve full Approved status. Each open item must have an owner, a target date, and defined closure evidence.

| Open Item ID | Description   | Impacted NFR IDs | Owner       | Raised Date | Target Resolution Date | Status                      | Closure Evidence      | Resolution |
|--------------|---------------|------------------|-------------|-------------|------------------------|-----------------------------|-----------------------|------------|
| OI-001       | <description> | NFR-xxx          | <role/name> | YYYY-MM-DD  | YYYY-MM-DD             | Open / In Progress / Closed | <required artifact>   |            |

---

## 7. Stakeholder Sign-Off

> **Guidance:** Records formal approval from each required stakeholder group. The document cannot reach Approved status
until all open items are Closed and all stakeholders have signed off.

### 7.1 Required Stakeholders

- Product Owner
- Engineering Lead
- SRE/DevOps Lead
- Security Lead
- Compliance Lead
- Operations/Support Lead

### 7.2 Conditional Approval Rules

| Status                 | Criteria                                                                             |
|------------------------|--------------------------------------------------------------------------------------|
| Blocked                | Open items unresolved with no clear owner or target date.                            |
| Conditionally Approved | Reviewed and accepted, but open items pending with assigned owners and target dates. |
| Approved               | All open items closed and verified with linked closure evidence.                     |

### 7.3 Sign-Off Tracker

| Stakeholder Group  | Reviewer | Decision                                                         | Signature | Decision Date | Conditions / Notes |
|--------------------|----------|------------------------------------------------------------------|-----------|---------------|--------------------|
| Product            | <name>   | Pending / Approved / Conditionally Approved / Rejected           |           | YYYY-MM-DD    |                    |
| Engineering        | <name>   | Pending / Approved / Conditionally Approved / Rejected           |           | YYYY-MM-DD    |                    |
| SRE/DevOps         | <name>   | Pending / Approved / Conditionally Approved / Rejected           |           | YYYY-MM-DD    |                    |
| Security           | <name>   | Pending / Approved / Conditionally Approved / Rejected           |           | YYYY-MM-DD    |                    |
| Compliance         | <name>   | Pending / Approved / Conditionally Approved / Rejected           |           | YYYY-MM-DD    |                    |
| Operations/Support | <name>   | Pending / Approved / Conditionally Approved / Rejected           |           | YYYY-MM-DD    |                    |

---

## 8. Appendix — RTM Mapping Guidance

> **Guidance:** Defines the minimum required columns for the Requirements Traceability Matrix (RTM) CSV that accompanies
this NFR document. The RTM provides bidirectional traceability from business requirements through NFRs to verification
evidence.

For each NFR in the RTM CSV, include these columns at minimum:

| Column               | Description                                          |
|----------------------|------------------------------------------------------|
| NFR_ID               | Unique NFR identifier                                |
| Category             | ISO 25010 quality category                           |
| PC_Section          | Originating PC section reference                    |
| PC_Requirement_IDs  | Linked PC requirement IDs                           |
| FRD_File             | Related FRD file reference                           |
| Requirement_Summary  | Brief requirement description                        |
| Business_Drivers     | Linked BD IDs                                        |
| Owner_Role           | Responsible role                                     |
| Verification_Method  | How the NFR is verified                              |
| Primary_Artifact     | Main evidence artifact                               |
| Review_Cadence       | How often this NFR is re-reviewed                    |
| KPI_or_SLO           | Target metric or SLO                                 |
| Status               | Current status                                       |
| ISO27001_Control     | Mapped ISO 27001 Annex A control (if applicable)     |
| SOC2_Criteria        | Mapped SOC2 Trust Service Criteria (if applicable)   |

---

## Attachments

> **Guidance:** List supporting files referenced by this document (test reports, dashboards, scan outputs, DR drill
records, etc.).

| Filename | Description | Location |
|----------|-------------|----------|
|          |             |          |

---

## Change Log

| Version | Date | Author | Change Summary |
|---------|------|--------|----------------|
|         |      |        |                |
