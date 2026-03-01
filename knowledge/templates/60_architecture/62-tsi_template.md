# Technology Stack Inventory (TSI)

| Field              | Value                                                        |
|--------------------|--------------------------------------------------------------|
| Document ID        | TSI-[NNNN]                                                   |
| Title              |                                                              |
| Version            |                                                              |
| Status             | Draft / In Review / Approved / Superseded / Retired          |
| Classification     | Public / Internal / Confidential / Restricted                |
| Created Date       |                                                              |
| Last Updated       |                                                              |
| Author             |                                                              |
| Reviewer           |                                                              |
| Approver           |                                                              |
| System Name        |                                                              |
| System ID          |                                                              |
| Related Documents  |                                                              |

---

## 1. Executive Summary

> **Guidance:** Provide a brief overview (2–4 paragraphs) of the system's technology landscape. State the system
purpose, its architectural style (monolith, microservices, serverless, etc.), and a high-level summary of the key
technology choices.

[Content here]

---

## 2. System Context

> **Guidance:** Define the boundaries of the system this inventory covers. Include a context diagram reference if
available. List upstream/downstream systems and integration points so readers understand what is in-scope vs.
out-of-scope.

**System Boundary:** [Brief description of what is in-scope]

**Architecture Style:** [e.g., Microservices, Monolith, Event-Driven, Serverless]

**Context Diagram Reference:** [Link or document ID]

### Upstream Systems

| System Name | Integration Type | Description |
|-------------|-----------------|-------------|
|             |                 |             |

### Downstream Systems

| System Name | Integration Type | Description |
|-------------|-----------------|-------------|
|             |                 |             |

---

## 3. Technology Stack Summary

> **Guidance:** A categorized summary table of every technology component in the system. Group by layer (Presentation,
Application, Data, Infrastructure, etc.). This provides a quick-reference overview before the detailed breakdown in
subsequent sections.

| Category                      | Technology        | Version  | Purpose (Brief)       |
|-------------------------------|-------------------|----------|-----------------------|
| **Presentation Layer**        |                   |          |                       |
| **Application Layer**         |                   |          |                       |
| **Data Layer**                |                   |          |                       |
| **Infrastructure & Platform** |                   |          |                       |
| **DevOps & CI/CD**            |                   |          |                       |
| **Monitoring & Observability**|                   |          |                       |
| **Security**                  |                   |          |                       |
| **Third-Party Services & APIs**|                  |          |                       |

---

## 4. Detailed Technology Registry

> **Guidance:** The core of the inventory. For each technology component, capture all relevant attributes below.
Duplicate the entry table for each technology in the system.

### 4.1 [Technology Name]

| Attribute                     | Value                                              |
|-------------------------------|----------------------------------------------------|
| Category                      |                                                    |
| Component Type                | Language / Framework / Library / Database / Platform / Service / Tool |
| Version In Use                |                                                    |
| Latest Stable Version         |                                                    |
| Version Gap Status            | Current / Minor Behind / Major Behind / EOL        |
| License Type                  |                                                    |
| License Compliance Status     | Compliant / Review Needed / Non-Compliant          |
| Vendor / Maintainer           |                                                    |
| Support Model                 | Community / Commercial Support / Vendor SLA / Internal |
| End-of-Life Date              |                                                    |
| Purpose                       |                                                    |
| Dependencies                  |                                                    |
| Integration Points            |                                                    |
| Environment: Development      | Yes / No                                           |
| Environment: Staging          | Yes / No                                           |
| Environment: Production       | Yes / No                                           |
| Owner Team                    |                                                    |
| Risk Rating                   | Low / Medium / High / Critical                     |
| Risk Notes                    |                                                    |
| Migration Plan Reference      |                                                    |
| Notes                         |                                                    |

---

## 5. Version & Compatibility Matrix *(Optional)*

> **Guidance:** A matrix showing compatibility relationships between key technologies. Useful for upgrade planning —
identifies which components must be upgraded together and which can be upgraded independently.

| Technology A | Technology B | Compatible Versions                  | Notes |
|-------------|-------------|--------------------------------------|-------|
|             |             |                                      |       |

---

## 6. Licensing Summary

> **Guidance:** Consolidated view of all license types in use. Flag any copyleft, proprietary, or restrictive licenses
that require legal review. Include cost information for commercial licenses.

| Technology | License Type | Cost               | Renewal Date | Legal Review Status          | Restrictions |
|------------|-------------|--------------------|--------------|-----------------------------|--------------|
|            |             |                    |              | Approved / Pending / Flagged |              |

---

## 7. End-of-Life & Deprecation Tracker

> **Guidance:** Track technologies approaching or past end-of-life. Include planned actions (upgrade, replace,
decommission) and timelines. This section drives proactive lifecycle management.

| Technology | Current Version | EOL Date | EOL Status                          | Planned Action                         | Target Version / Replacement | Deadline | Owner | Status                            |
|------------|----------------|----------|-------------------------------------|----------------------------------------|------------------------------|----------|-------|-----------------------------------|
|            |                |          | Active / Approaching EOL / EOL / Deprecated | Upgrade / Replace / Decommission / Accept Risk |                              |          |       | Not Started / In Progress / Completed |

---

## 8. Security Considerations

> **Guidance:** Document known vulnerabilities, security posture of each technology, and any security-specific
configurations. Reference CVE databases and vulnerability scanning results where applicable.

**Vulnerability Scanning Tool:** [e.g., Snyk, Dependabot, OWASP Dependency-Check]

**Last Scan Date:** [YYYY-MM-DD]

### Critical Vulnerabilities

| CVE ID | Technology | Severity | Status | Remediation Plan |
|--------|-----------|----------|--------|-----------------|
|        |           |          |        |                 |

### Security Notes

[Content here]

---

## 9. Architecture Decision References *(Optional)*

> **Guidance:** Link to Architecture Decision Records (ADRs) or design documents that explain WHY specific technologies
were chosen. This provides traceability from technology choices back to architectural rationale.

| ADR ID | Title | Decision Date | Technologies Affected | Summary | Link |
|--------|-------|---------------|-----------------------|---------|------|
|        |       |               |                       |         |      |

---

## 10. Dependency Map *(Optional)*

> **Guidance:** A visual or tabular representation of how technologies in this inventory depend on one another. Helps
identify blast radius for upgrades and single points of failure.

**Diagram Reference:** [Link to dependency diagram (e.g., Mermaid, draw.io)]

### Critical Dependencies

| Technology | Depended On By                  | Impact if Unavailable |
|------------|--------------------------------|-----------------------|
|            |                                |                       |

---

## 11. Operational Notes *(Optional)*

> **Guidance:** Capture any operational considerations: known performance constraints, scaling limits, configuration
quirks, or tribal knowledge about technologies in this stack.

[Content here]

---

## 12. Attachments *(Optional)*

> **Guidance:** Supporting files such as architecture diagrams, license certificates, scan reports, or vendor contracts.

| Filename | Description | Type                                        |
|----------|-------------|---------------------------------------------|
|          |             | Diagram / Report / Contract / Certificate / Other |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
|         |      |        |         |
