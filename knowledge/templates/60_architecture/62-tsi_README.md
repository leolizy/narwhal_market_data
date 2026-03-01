# Technology Stack Inventory (TSI) — Policy & Governance Document

## 1. Document Overview

### 1.1 What Is a Technology Stack Inventory?

A Technology Stack Inventory (TSI) is a living SDLC artifact that provides a comprehensive, structured record of every
technology component used by a specific system or application. It captures languages, frameworks, libraries, databases,
platforms, services, and tools — along with their versions, licensing, support status, risk posture, and lifecycle
state.

### 1.2 Function in the SDLC

The TSI serves as the authoritative source of truth for technology decisions within a system. It supports multiple SDLC
activities: architecture reviews, upgrade planning, security audits, dependency management, licensing compliance, and
onboarding. It sits downstream of Architecture Decision Records (ADRs) and upstream of operational runbooks and security
assessments.

### 1.3 Position in the Document Hierarchy

```
Enterprise Architecture Standards
  └── Architecture Decision Records (ADRs)
        └── Technology Stack Inventory (TSI)  ← this document
              ├── Security Assessment Reports
              ├── Dependency Audit Reports
              └── Operational Runbooks

```

---

## Document Dependencies

### Upstream Documents (Dependencies)

- NFR-0001

### Downstream Documents (Depend on This)

- NFRAR-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## 2. Naming & ID Convention

### 2.1 Document ID Format

**Format:** `TSI-[NNNN]`

- **Prefix:** `TSI` — Technology Stack Inventory
- **Numbering:** Four-digit sequential, zero-padded, assigned per system/application (e.g., TSI-0001, TSI-0002)
- **Uniqueness:** Each system/application receives exactly one TSI document ID. The ID does not change across versions.

### 2.2 File Naming Convention

**Format:** `TSI-[NNNN]_[ShortTitle]_v[X.Y].[ext]`

Examples:

- `TSI-0001_OrderManagementSystem_v1.0.yaml`
- `TSI-0001_OrderManagementSystem_v1.0.md`
- `TSI-0015_PaymentGateway_v2.1.md`

### 2.3 Version Numbering

Semantic versioning using **Major.Minor**:

- **Major increment (X.0):** Structural changes to the inventory (new sections added, sections removed), or a technology
  tier replacement (e.g., migrating from PostgreSQL to DynamoDB)
- **Minor increment (X.Y):** Content updates within existing sections (version bumps, new library added, license
  renewed, EOL dates updated)

---

## 3. Scope & Granularity

### 3.1 Unit of Documentation

One TSI document covers **one system or application**. A "system" is defined as a deployable unit or a logically
cohesive set of services that share a common domain boundary.

### 3.2 When to Create a New Document

- A new system or application is introduced
- A major system is split into independent sub-systems (each gets its own TSI)
- An acquired product is integrated and needs its own technology baseline

### 3.3 When to Update an Existing Document (vs. Create New)

Update the existing TSI when:

- A new technology is added to or removed from the stack
- A version upgrade is performed
- A license is renewed or changes
- An EOL date is announced or reached
- A security scan reveals new findings

Do NOT create a new TSI — create a new version of the existing one.

### 3.4 Relationship to Parent/Child Documents

- **Parent:** ADRs justify the technology choices documented in the TSI
- **Siblings:** Other TSIs for other systems in the same portfolio
- **Children:** Security assessment reports, dependency audit reports, and operational runbooks may reference or derive
  from the TSI

---

## 4. Section-by-Section Explanation

### Section 1: Executive Summary

- **Purpose:** Give readers a fast orientation to the system's technology landscape without reading the entire document.
- **What to include:** System purpose, architectural style, dominant technology choices, and any notable constraints or
  decisions.
- **What NOT to include:** Detailed version numbers, licensing terms, or security findings — those belong in later
  sections.
- **Required:** Yes

### Section 2: System Context

- **Purpose:** Establish clear boundaries so readers know exactly what this inventory covers.
- **What to include:** System boundary description, architecture style, context diagram reference, upstream and
  downstream systems.
- **What NOT to include:** Internal component-level architecture (that belongs in a System Design Document / SDD).
- **Required:** Yes

### Section 3: Technology Stack Summary

- **Purpose:** Provide a quick-reference table grouped by technology layer.
- **What to include:** Every technology in the system, categorized into layers (Presentation, Application, Data,
  Infrastructure, DevOps, Monitoring, Security, Third-Party).
- **What NOT to include:** Detailed attributes — this is a summary. Details go in Section 4.
- **Required:** Yes

### Section 4: Detailed Technology Registry

- **Purpose:** The core of the document. A comprehensive record of each technology with all relevant attributes.
- **What to include:** Technology name, category, component type, version in use, latest stable version, version gap
  status, license type, compliance status, vendor/maintainer, support model, EOL date, purpose, dependencies,
  integration points, environment usage, owner team, risk rating, risk notes, migration plan references.
- **What NOT to include:** Source code, configuration files, or deployment scripts. Reference those by link.
- **Examples:** See the YAML template for the full attribute schema.
- **Required:** Yes

### Section 5: Version & Compatibility Matrix

- **Purpose:** Document inter-technology compatibility constraints to support upgrade planning.
- **What to include:** Pairs of technologies with version compatibility rules (e.g., "React 18.x requires Node >= 16").
- **What NOT to include:** Every possible combination — focus on critical or non-obvious constraints.
- **Required:** No (Optional — recommended for complex systems with tight coupling)

### Section 6: Licensing Summary

- **Purpose:** Consolidate licensing information for compliance reviews and cost tracking.
- **What to include:** License type, cost, renewal dates, legal review status, and restrictions for every technology.
- **What NOT to include:** Full license text. Link to license files or contracts in the Attachments section.
- **Required:** Yes

### Section 7: End-of-Life & Deprecation Tracker

- **Purpose:** Proactively manage technology lifecycle by tracking EOL status and planned actions.
- **What to include:** Technologies approaching or past EOL, planned actions (upgrade/replace/decommission), target
  versions, deadlines, owners, and progress status.
- **What NOT to include:** Technologies that are actively supported with no EOL concerns.
- **Required:** Yes

### Section 8: Security Considerations

- **Purpose:** Document the security posture of the technology stack, including vulnerability findings.
- **What to include:** Vulnerability scanning tool used, last scan date, critical unresolved vulnerabilities (CVEs), and
  security-specific notes.
- **What NOT to include:** Full vulnerability scan reports. Attach those as files. Do not include secrets, keys, or
  credentials.
- **Required:** Yes

### Section 9: Architecture Decision References

- **Purpose:** Provide traceability from technology choices back to the architectural rationale.
- **What to include:** ADR IDs, titles, decision dates, affected technologies, and brief summaries with links.
- **What NOT to include:** Full ADR content. Link to the ADR documents instead.
- **Required:** No (Optional — strongly recommended if your organization maintains ADRs)

### Section 10: Dependency Map

- **Purpose:** Visualize inter-technology dependencies to understand blast radius of changes and single points of
  failure.
- **What to include:** Diagram reference (Mermaid, draw.io, etc.), critical dependency list with impact assessment.
- **What NOT to include:** Application-level code dependency graphs. This is about technology-to-technology
  dependencies.
- **Required:** No (Optional — recommended for systems with 10+ technologies)

### Section 11: Operational Notes

- **Purpose:** Capture tribal knowledge and operational considerations that do not fit elsewhere.
- **What to include:** Performance constraints, scaling limits, known quirks, configuration pitfalls, workarounds.
- **What NOT to include:** Standard operational procedures — those belong in runbooks.
- **Required:** No (Optional)

### Section 12: Attachments

- **Purpose:** Link or embed supporting files referenced throughout the document.
- **What to include:** Architecture diagrams, license certificates, scan reports, vendor contracts.
- **What NOT to include:** Source code or executable files.
- **Required:** No (Optional)

---

## 5. Update Triggers

### 5.1 Creation Triggers

- A new system or application is initiated
- An existing system undergoes a complete technology re-platforming
- A system is acquired or onboarded from an external source

### 5.2 Update Triggers

- A new technology (language, framework, library, service) is added to the stack
- A technology is removed or replaced
- A version upgrade is deployed to any environment
- A license is renewed, changed, or expires
- A new EOL date is announced by a vendor
- A security vulnerability scan produces new critical or high findings
- A new ADR is created that affects the system's technology choices
- A vendor changes its support model (e.g., community to paid, or discontinuation)

### 5.3 Review Triggers

- Quarterly review cycle (recommended minimum cadence)
- Before any major release or architecture review
- During annual compliance or security audits
- When planning a major upgrade or migration initiative
- When onboarding a new team lead or architect to the system

### 5.4 Retirement Triggers

- The system is fully decommissioned
- The system is replaced by a successor system (mark as Superseded, link to new TSI)
- The system is merged into another system (update the absorbing system's TSI, retire this one)

---

## 6. Roles & Responsibilities

| Role               | Responsibility                                                                                      |
|--------------------|-----------------------------------------------------------------------------------------------------|
| **Author**         | Engineering Lead or Tech Lead of the system. Responsible for creating and maintaining the inventory. |
| **Reviewer**       | Solution Architect or Principal Engineer. Validates accuracy and completeness.                       |
| **Approver**       | Engineering Manager or Architecture Review Board (ARB). Formally approves the document.             |
| **Accountable**    | System Owner / Product Engineering Lead. Accountable for keeping the inventory current.              |
| **Contributors**   | DevOps engineers, security engineers, and platform engineers provide input on their respective areas.|

---

## 7. Quality Checklist

Before submitting the TSI for review, confirm the following:

- [ ] All **required** sections are completed (Sections 1, 2, 3, 4, 6, 7, 8)
- [ ] Document ID follows the `TSI-[NNNN]` naming convention
- [ ] File is named according to `TSI-[NNNN]_[ShortTitle]_v[X.Y].[ext]`
- [ ] Version number is incremented appropriately (Major vs. Minor)
- [ ] Every technology in the stack has a registry entry in Section 4
- [ ] Summary table (Section 3) matches detailed entries (Section 4)
- [ ] All license types are documented in Section 6
- [ ] EOL/Deprecation tracker (Section 7) is current
- [ ] Security scan date and findings (Section 8) are up-to-date
- [ ] Related documents are linked (ADRs, SDDs, etc.)
- [ ] Change log is updated with the current version entry
- [ ] Reviewed by the designated Reviewer role
- [ ] No secrets, credentials, or API keys are included anywhere in the document
