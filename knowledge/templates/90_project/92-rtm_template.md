# Requirements Traceability Matrix (RTM)

| Field            | Value                                                      |
|------------------|------------------------------------------------------------|
| Document ID      | RTM-[NNNN]                                                 |
| Title            |                                                            |
| System Name      |                                                            |
| Version          |                                                            |
| Status           | Draft / In Review / Approved / Superseded / Retired        |
| Classification   | Public / Internal / Confidential / Restricted              |
| Created Date     |                                                            |
| Last Updated     |                                                            |
| Author           |                                                            |
| Reviewer         |                                                            |
| Approver         |                                                            |
| Related Documents|                                                            |

---

## 1. Purpose & Scope

> **Guidance:** Define the objective of this traceability matrix, the system it covers, and the boundaries of
traceability (which artifact types are traced and which are excluded).

[Content here]

### 1.1 System Boundary

> **Guidance:** Identify the system or subsystem boundary. All requirements within this boundary are in scope for
tracing.

[Content here]

### 1.2 Trace Coverage Goal

> **Guidance:** State the target coverage percentage and any exceptions. Example: "100% of approved functional
requirements must have at least one linked test case and one linked design element."

[Content here]

---

## 2. Artifact Registry

> **Guidance:** Enumerate all source and target artifact types included in this matrix. Each artifact type should
reference its document prefix and repository location.

| Artifact Type            | Prefix | Source Location | Owner Role       |
|--------------------------|--------|-----------------|------------------|
| Platform Canon           | PC    |                 |                  |
| Functional Requirement   | FRD    |                 |                  |
| Non-Functional Requirement | NFR  |                 |                  |
| High-Level Design        | HLD    |                 |                  |
| Low-Level Design         | LLD    |                 |                  |
| Test Case                | TC     |                 |                  |
| Defect                   | DEF    |                 |                  |
| Release                  | RN     |                 |                  |

---

## 3. Traceability Matrix

> **Guidance:** The core matrix. Each row represents a single business or functional requirement and traces it forward
to design, test, defect, and release artifacts, and backward to its originating business requirement.

| Req ID | Req Description | Priority | Status | Source PC ID | HLD Ref | LLD Ref | Test Case IDs | Test Status | Defect IDs | Release ID | Verification Method | Comments |
|--------|-----------------|----------|--------|---------------|---------|---------|---------------|-------------|------------|------------|---------------------|----------|
|        |                 |          |        |               |         |         |               |             |            |            |                     |          |

**Column Definitions:**

- **Req ID**: Unique requirement identifier (e.g., FRD-0023)
- **Req Description**: Brief description of the requirement
- **Priority**: Critical / High / Medium / Low
- **Status**: Proposed / Approved / Implemented / Verified / Deferred / Deleted
- **Source PC ID**: Backward trace — originating PC requirement ID
- **HLD Ref**: Forward trace — linked HLD section or component ID
- **LLD Ref**: Forward trace — linked LLD module or class ID
- **Test Case IDs**: Forward trace — list of linked test case IDs
- **Test Status**: Aggregate test result: Not Run / Pass / Fail / Blocked
- **Defect IDs**: Linked defect IDs discovered during testing
- **Release ID**: Release version in which this requirement is delivered
- **Verification Method**: How verified: Test / Inspection / Demonstration / Analysis
- **Comments**: Additional notes, risks, or dependencies

---

## 4. Coverage Summary

> **Guidance:** Provide quantitative traceability coverage metrics. This section is used for go/no-go decisions and
audit evidence.

| Metric                            | Value |
|-----------------------------------|-------|
| Total Requirements                |       |
| Requirements with Design Link     |       |
| Requirements with Test Link       |       |
| Requirements Fully Traced         |       |
| Requirements with No Trace        |       |
| Forward Coverage (%)              |       |
| Backward Coverage (%)             |       |
| Overall Coverage (%)              |       |

---

## 5. Gap Analysis

> **Guidance:** Identify requirements with incomplete trace links. List each gap, its risk level, and the planned
remediation action.

| Req ID | Missing Link Type | Risk Level | Remediation Action | Owner | Target Date |
|--------|-------------------|------------|--------------------|-------|-------------|
|        |                   |            |                    |       |             |

---

## 6. Bidirectional Trace Verification

> **Guidance:** Confirm that traceability works in both directions. Forward trace ensures every requirement leads to a
verifiable outcome. Backward trace ensures every test case and design element links to an approved requirement (no
gold-plating).

### 6.1 Forward Trace Check

> **Guidance:** Verify that every approved requirement has at least one test case and one design reference.

- **Status**: Complete / In Progress / Not Started
- **Exceptions**:

[List any exceptions here]

### 6.2 Backward Trace Check

> **Guidance:** Verify that every test case traces back to an approved requirement. Every design element traces back to
an approved requirement. Flag orphaned artifacts.

- **Status**: Complete / In Progress / Not Started
- **Orphaned Test Cases**:

[List any orphaned test cases here]

- **Orphaned Design Elements**:

[List any orphaned design elements here]

---

## 7. Sign-Off

> **Guidance:** Formal sign-off confirming traceability coverage meets the agreed threshold and all critical gaps are
remediated.

| Role              | Name | Date | Signature |
|-------------------|------|------|-----------|
| Business Analyst  |      |      |           |
| QA Lead           |      |      |           |
| Project Manager   |      |      |           |

---

## 8. Attachments

> **Guidance:** Supporting files such as exported matrix spreadsheets, coverage reports, or tool-generated traceability
reports. *(Optional)*

[List attachments here]

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
|         |      |        |         |
