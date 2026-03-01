# NFTS-0001: NFTS — Non-Functional Test Specification: Policy and Governance README

> **Version:** 1.0 | **Standard:** ISO/IEC/IEEE 29119-3, ISO 25010, IEEE 829-2008 | **Last Updated:** 2026-02-25

---

## Table of Contents

1. [Document Overview](#1-document-overview)
2. [Naming and ID Convention](#2-naming-and-id-convention)
3. [Scope and Granularity](#3-scope-and-granularity)
4. [Section-by-Section Explanation](#4-section-by-section-explanation)
5. [Update Triggers](#5-update-triggers)
6. [Roles and Responsibilities](#6-roles-and-responsibilities)
7. [Quality Checklist](#7-quality-checklist)

---

## Document Overview

### What is the Non-Functional Test Specification?

The Non-Functional Test Specification (NFTS) is the primary governing document for testing quality attributes of a
system that are not captured by functional test cases. It defines **what** non-functional characteristics will be
tested, **how** they will be tested, the **acceptance criteria** for each, and the **environment and data** required to
execute them.

Non-functional requirements — such as performance, security, reliability, scalability, and usability — are often the
most business-critical attributes of a production system. A functional system that fails under load, is breached by a
SQL injection, or cannot recover from a node failure is not fit for release. The NFTS ensures these risks are explicitly
tested and signed off before deployment.

### Function in the SDLC

The NFTS sits within the **Test Phase** of the SDLC, but its inputs are gathered throughout the design and requirements
phases. It is produced after the following documents are approved:

- Non-Functional Requirements (NFR) — supplies the acceptance thresholds
- Architecture documents (CICD, DBAD, TSI) — define the system architecture and integration points
- High-Level Design (HLD) — informs environment replication and integration points

The NFTS feeds into the **NFR Acceptance Report (NFRAR)** at the end of the test cycle. The NFRAR consolidates NFTS
execution results and directly informs the **go/no-go decision** for production deployment.

### Position in the Document Hierarchy

```
     NFR (Non-Functional Requirements)
        │
        ▼
     Architecture Docs (CICD, DBAD, TSI)
        │
        ▼
     NFTS (Non-Functional Test Specification)  ◀── [THIS DOCUMENT]
        │
        ▼
     NFRAR (NFR Acceptance Report)

```

---

## Naming and ID Convention

### Document ID Format

```
NFTS-[NNNN]

```

| Element   | Rule                                                                                   |
|-----------|----------------------------------------------------------------------------------------|
| **NFTS**  | Fixed prefix for all Non-Functional Test Specification documents                       |
| **NNNN**  | 4-digit sequential number, zero-padded (e.g., 0001, 0042)                             |
| Example   | `NFTS-0001`, `NFTS-0012`                                                              |

### Numbering Scope

Numbering is **sequential per project**. A new NFTS instance is created per release cycle for the same system; each
receives a new document ID. Do not reuse IDs.

### File Naming Convention

```
NFTS-[NNNN]_[SystemName]_[ReleaseVersion]_v[X.Y].[ext]

```

**Examples:**

```
NFTS-0001_PaymentService_v2.3_v1.0.md
NFTS-0001_PaymentService_v2.3_v1.0.yaml
NFTS-0001_PaymentService_v2.3_v1.2.md    ← minor revision

```

### Version Numbering

| Version Type  | When to Increment                                                            | Example       |
|---------------|------------------------------------------------------------------------------|---------------|
| Major (X.0)   | Structural change — new test type added, major scope change, NFR baseline change | 1.0 → 2.0 |
| Minor (X.Y)   | Content update — new scenario added, threshold adjusted, tool change         | 1.0 → 1.1     |

> Do not increment the version for minor typo corrections. Use the Change Log to record all amendments.

---

## Scope and Granularity

### One Document Per Release Cycle

A single NFTS instance covers one **release cycle** for a specific **system or service**. If a release spans multiple
services with independent NFRs (e.g., a microservices platform), a separate NFTS should be created per service unless
the NFT environment and tooling are entirely shared.

### When to Create a New NFTS vs. Update an Existing One

| Situation                                      | Action                                                              |
|------------------------------------------------|---------------------------------------------------------------------|
| New release cycle begins                       | Create a new NFTS (new document ID, new version starting at 1.0)   |
| NFR thresholds revised mid-cycle               | Update existing NFTS (minor version increment)                     |
| New test type added mid-cycle (approved)       | Update existing NFTS (major version increment if structural)       |
| Environment changes significantly              | Update existing NFTS (Section 5) with minor version increment      |
| Scope reduces (test type deferred)             | Update existing NFTS, document rationale in Section 3.2            |

### Parent / Child Relationship

- The NFTS is a **child of the NFR** — the NFR supplies the acceptance thresholds and quality attribute definitions; the
  NFTS provides the detailed non-functional testing specification against those requirements.
- Architecture documents (CICD, DBAD, TSI) inform the NFTS by defining the system architecture, deployment topology, and
  integration points under test.
- Each performance scenario in the NFTS traces back to an **NFR entry** — orphaned test scenarios (without NFR
  traceability) must be justified or removed.
- Results from NFTS execution feed into the **NFR Acceptance Report (NFRAR)**, which is the evidence artefact for
  sign-off. The NFTS-to-NFRAR relationship is direct: every test scenario documented in the NFTS must have a
  corresponding result entry in the NFRAR.

---

## Section-by-Section Explanation

### Section 1 — Introduction

**Purpose:** Establishes context for the document and the test effort.

**What to include:** System name and release version, high-level description of what non-functional characteristics are
being tested, and an explicit in-scope / out-of-scope list. The definitions table should include all NFT-specific
metrics (TPS, P95, RTO, RPO, MTTR, MTBF) to prevent ambiguity during results review.

**What NOT to include:** Functional test coverage, business requirements, design descriptions. The NFTS covers quality
attributes only.

**Required:** Yes.

---

### Section 2 — References

**Purpose:** Provides traceability to all governing documents, standards, and NFRs. Every acceptance criterion in the
NFTS must trace to a document listed here.

**What to include:** Document IDs and versions of all NFRs, architecture documents (CICD, DBAD, TSI), HLD, FRD, and
applicable standards (ISO 29119, ISO 25010, OWASP Top 10, relevant compliance frameworks).

**What NOT to include:** Informal references such as email threads, verbal agreements, or undocumented assumptions. If
an NFR was communicated verbally, it must be formalised in the NFR document before being referenced here.

**Required:** Yes.

---

### Section 3 — Test Strategy

**Purpose:** Defines the overarching approach and execution model for NFT.

**What to include:** A brief narrative on the test approach (e.g., automated, tool-driven, dedicated environment), a
table of all non-functional test types with their execution status (Active / Deferred / Not Applicable), and the
recommended execution sequence including inter-test dependencies.

**What NOT to include:** Detailed test scenario data (that belongs in Sections 7–12). The strategy section is
high-level.

**Key decision to document:** Why certain test types are deferred or not applicable. Deferred tests without rationale
create audit risks and scope disputes.

**Required:** Yes.

---

### Section 4 — Entry and Exit Criteria

**Purpose:** Defines the quality gates for starting and completing NFT. These are the contractual conditions between the
NFT team and project stakeholders.

**What to include:** Specific, measurable, and verifiable criteria. "System is ready" is not a valid criterion.
"Functional regression pass rate ≥ 95%" is. Each criterion must have an owner.

**What NOT to include:** Criteria that cannot be objectively verified (subjective criteria), or criteria that duplicate
functional testing gates.

**Suspension and Resumption criteria** are optional but strongly recommended for complex programmes where NFT runs over
multiple weeks.

**Required:** Yes (Entry and Exit are mandatory; Suspension/Resumption are optional).

---

### Section 5 — Test Environment

**Purpose:** Defines the infrastructure required to produce valid NFT results. Environment fidelity is the single
biggest factor in result reliability.

**What to include:** Full hardware specs for all nodes, software and middleware versions, network topology, all test
tools with versions and license status, and a critical table documenting differences from production.

**What NOT to include:** Functional test environment details or developer workstation specifications.

**Critical rule:** If the NFT environment differs significantly from production (e.g., 10% of production capacity), this
must be documented and results must be interpreted with scaling assumptions stated explicitly.

**Required:** Yes.

---

### Section 6 — Test Data Requirements

**Purpose:** Specifies the data volumes and preparation required for NFT to produce statistically meaningful results.

**What to include:** Minimum record counts per key entity (users, orders, transactions, etc.), the data
generation/anonymisation approach, PII/compliance handling, and the data reset strategy between test runs.

**What NOT to include:** Functional test data (specific test case inputs). NFT data requirements focus on volume and
distribution, not specific values.

**Common mistake:** Running performance tests against a database with 1,000 records when production has 50 million. This
produces completely invalid baseline and load test results.

**Required:** Yes.

---

### Section 7 — Performance Testing Specification

**Purpose:** The core section for all performance-related testing — baseline, load, stress, soak, and spike.

**What to include:** A documented baseline, workload models (concurrent users, transaction mix, ramp profiles), and a
scenario table with every acceptance criterion traceable to an NFR reference. Monitoring metrics to be captured must
also be specified here.

**What NOT to include:** Security or reliability scenarios — these have dedicated sections. Avoid mixing test types in a
single scenario.

**Key rule:** Every acceptance threshold (response time, throughput, error rate) must have an NFR reference.
Undocumented thresholds are engineering assumptions and carry risk if disputed at exit.

**Workload model guidance:** Always define think time (the pause between user actions). Tests without think time
simulate an unrealistic all-out attack rather than real user behaviour and will generate misleadingly poor results.

**Required:** Yes.

---

### Section 8 — Security Testing Specification

**Purpose:** Defines the security test scope, methodology, tools, and acceptance thresholds.

**What to include:** Framework references (OWASP Top 10, ASVS level), scenario table covering authentication,
authorisation, injection, sensitive data exposure, session management, security misconfiguration, and logging.
Vulnerability acceptance thresholds at exit (Critical must always be zero).

**What NOT to include:** Network penetration testing of production infrastructure (out of scope for application NFTS).
Separate engagement required for infrastructure pen testing.

**Methodology note:** SAST (Static Application Security Testing) should be integrated in CI/CD and run before NFT
commences. DAST (Dynamic Application Security Testing) is run during the NFT cycle. Manual penetration testing is
time-boxed and conducted by a named tester or third party.

**Required:** Yes.

---

### Section 9 — Reliability and Availability Testing Specification

**Purpose:** Validates that SLA commitments for uptime, failover, and recovery are achievable.

**What to include:** Availability targets from SLA (RTO, RPO, MTTR, MTBF), and failure injection scenarios that simulate
real outage conditions (node failure, database outage, network partition, disk full).

**What NOT to include:** Performance scenarios (Section 7) or security scenarios (Section 8). Keep test types separated.

**Disaster Recovery testing** is a sub-type that typically requires a separate execution window and stakeholder approval
due to its disruptive nature.

**Required:** Yes.

---

### Section 10 — Scalability Testing Specification

**Purpose:** Determines whether the system can scale to meet growth projections and validates auto-scaling behaviour.

**What to include:** Step-load scenarios with increasing concurrency levels, scaling type
(horizontal/vertical/auto-scale), and acceptance criteria defining whether scaling is linear, bounded, or degrading
gracefully.

**When this section is optional:** For systems with fixed infrastructure where scaling is not a design goal, this
section may be marked Not Applicable with rationale.

**Required:** Optional (required if scalability is an NFR).

---

### Section 11 — Usability Testing Specification

**Purpose:** Validates that the system meets usability and accessibility standards for its target users.

**What to include:** Accessibility compliance target (e.g., WCAG 2.1 Level AA), task-based usability scenarios with
participant profiles, and measurable success criteria (task completion rate, time-on-task, error rate).

**What NOT to include:** Subjective opinions. All usability acceptance criteria must be quantifiable and pre-agreed.

**Required:** Optional (required for customer-facing systems and regulated industries).

---

### Section 12 — Compatibility Testing Specification

**Purpose:** Validates behaviour across browsers, devices, operating systems, and integration environments.

**What to include:** Prioritised list of browsers and versions, device types and OS versions (based on market share data
from analytics), and external API/integration compatibility scenarios.

**Version selection guidance:** Use "latest" and "latest-1" for modern browsers. For enterprise systems, include
specific corporate-mandated browser versions (e.g., IE11 or legacy Chrome).

**Required:** Optional (required for web applications and systems with external integrations).

---

### Section 13 — Defect Management for NFT

**Purpose:** Defines how NFT-specific defects are classified, reported, and managed.

**What to include:** NFT-specific severity definitions (generic functional defect severities are inappropriate for NFT
failures), defect tracking tool, label/tagging convention, and retest policy.

**Key differentiator:** An NFT P1 defect is not the same as a functional P1. An NFT P1 means the system breaches its SLA
under target load — this is a release blocker. Misaligned severity definitions lead to incorrect prioritisation and
delayed resolution.

**Required:** Yes.

---

### Section 14 — Roles and Responsibilities

**Purpose:** Ensures accountability for every NFT activity.

**What to include:** Specific roles (not just job titles), their exact responsibilities in the NFT context, and named
assignees. Key roles include Performance Test Engineer, Security Test Engineer, NFT Lead, Test Manager,
DevOps/Infrastructure, System Architect, and Project Manager.

**What NOT to include:** Generic project roles unrelated to NFT execution. Limit to roles with direct NFT
accountability.

**Required:** Yes.

---

### Section 15 — Risks and Mitigations

**Purpose:** Documents known risks to NFT execution quality and timeline, with active mitigations.

**What to include:** Common NFT risks — environment instability, insufficient data volumes, production environment
differences, tool licensing constraints, narrow execution windows, and skills availability. Each risk must have
likelihood, impact, mitigation, and an owner.

**What NOT to include:** Project-level schedule risks (those belong in the PMP). The NFTS risk register focuses on risks
that could invalidate NFT results or prevent execution.

**Required:** Yes.

---

### Section 16 — Reporting Requirements

**Purpose:** Defines the reporting cadence and audience for NFT outcomes.

**What to include:** At minimum: a daily progress report during execution, scenario-level results reports (per test
type), and a Final NFT Completion Report at exit gate. Each report must have a defined audience, frequency, and format.

**Required:** Yes.

---

## Update Triggers

### Creation Triggers

A new NFTS must be created when:

- A new release cycle begins that carries NFRs to be validated
- A new system or service is onboarded into the test estate
- The scope of NFT expands to cover a new quality attribute not previously tested

### Update Triggers

The NFTS must be updated when:

- NFR thresholds are revised (updated acceptance criteria in Sections 7–12)
- The test environment specifications change (Section 5 update)
- A new non-functional test type is added or deferred during the cycle (Section 3 update)
- Test tools are changed or upgraded (Section 5.5 update)
- A new risk is identified that is not covered in Section 15
- The execution sequence changes due to dependency discovery

### Review Triggers

The NFTS must be reviewed (without necessarily updating content) when:

- A major production incident reveals a gap in NFT coverage
- A post-mortem identifies a non-functional failure that the NFTS did not cover
- The system architecture changes significantly between release cycles
- A new compliance or regulatory requirement is imposed

### Retirement Triggers

The NFTS should be marked as **Superseded** when:

- The corresponding release has been deployed to production and signed off
- A newer version NFTS has been created for the next release cycle

The NFTS should be marked as **Retired** when:

- The system under test has been decommissioned
- The test approach has been fully replaced by a successor document

---

## Roles and Responsibilities

| Role                     | Create | Review | Approve | Update | Archive |
|--------------------------|--------|--------|---------|--------|---------|
| Performance Test Engineer| ✓      |        |         | ✓      |         |
| Security Test Engineer   | ✓      |        |         | ✓      |         |
| NFT Lead / QA Lead       | ✓      | ✓      |         | ✓      | ✓       |
| Test Manager             |        | ✓      | ✓       |        | ✓       |
| System Architect         |        | ✓      |         |        |         |
| Project Manager          |        | ✓      |         |        |         |
| DevOps / Infrastructure  |        | ✓ (§5) |         | ✓ (§5) |         |

> **Accountable owner:** The **QA Lead / NFT Lead** is the single accountable owner for NFTS quality and currency
throughout the test cycle.

---

## Quality Checklist

Use this checklist before submitting the NFTS for review. All mandatory items must be checked before review commences.

### Mandatory Checks

- [ ] Document ID follows the `NFTS-[NNNN]` convention
- [ ] All metadata fields completed (status, version, classification, author, reviewer, approver)
- [ ] All related document references populated (NFR, CICD, DBAD, TSI, FRD, HLD)
- [ ] Section 1: In-scope and out-of-scope quality attributes explicitly listed
- [ ] Section 2: All referenced standards and documents listed with version numbers
- [ ] Section 3: All test types marked with status (Active / Deferred / N/A) and rationale for non-active types
- [ ] Section 4: Entry and exit criteria are specific, measurable, and have named owners
- [ ] Section 5: Environment hardware specs documented; differences from production table completed
- [ ] Section 6: Test data volumes specified; data reset strategy defined
- [ ] Section 7: Every performance acceptance threshold has an NFR reference (no orphaned thresholds)
- [ ] Section 7: Workload models include ramp-up, sustain, ramp-down, and think time
- [ ] Section 8: Vulnerability acceptance thresholds defined; Critical = 0 confirmed with stakeholders
- [ ] Section 9: RTO and RPO targets sourced from NFR/SLA document
- [ ] Section 13: NFT-specific severity definitions completed
- [ ] Section 14: All roles assigned to named individuals
- [ ] Section 15: Risks reviewed and owners assigned
- [ ] Section 16: Final NFT Completion Report audience and format agreed
- [ ] Change Log updated with version 1.0 entry

### Recommended Checks

- [ ] Threat model referenced or OWASP Top 10 default rationale documented (Section 8.2)
- [ ] Scalability section completed if scalability is an active NFR
- [ ] Accessibility standard specified if system is customer-facing (Section 11)
- [ ] All test tools confirmed as licensed for the NFT execution window (Section 5.5)
- [ ] Known environment-to-production differences acknowledged and risk-accepted (Section 5.6)

---

*This policy document is maintained by the QA Practice. For questions, contact the QA Lead or Test Manager.*
