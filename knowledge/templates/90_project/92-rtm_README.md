# RTM-0001: Requirements Traceability Matrix (RTM) — Policy Document

## Document Overview

The Requirements Traceability Matrix (RTM) is a living SDLC artifact that establishes and maintains bidirectional links
between business requirements, functional requirements, design artifacts, test cases, defects, and release deliverables.
Its primary function is to provide verifiable evidence that every approved requirement has been designed, implemented,
tested, and delivered — and conversely, that no artifact exists without an originating requirement.

Within the SDLC document hierarchy, the RTM sits as a cross-cutting governance artifact. It does not belong to a single
phase; rather, it spans the entire lifecycle from requirements elicitation through release. It consumes outputs from PC,
FRD/SRS, NFR, HLD, LLD, TP, TC, and RN documents and serves as the single source of truth for coverage and completeness.

**Position in Document Hierarchy:**

```
PC (Platform Canon)
 └── FRD / SRS / NFR (Detailed Requirements)
      └── HLD → LLD (Design)
           └── TC (Test Cases)
                └── DEF (Defects)
                     └── RN (Release Notes)

RTM ← traces across ALL of the above →

```

---

## Document Dependencies

### Upstream Documents (Dependencies)

- All other documents (PC-0001, FRD-0001, NFR-0001, PSD-0001, AEC-0001, API-0001, DBC-0001, DC-0001, CICD-0001,
  DBAD-0001, TSI-0001, UT-0001, NFRAR-0001)

### Downstream Documents (Depend on This)

- None - RTM-0001 maintains traceability

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

**ID Format:** `RTM-[NNNN]`

- **Prefix:** `RTM` — stands for Requirements Traceability Matrix
- **Numbering:** Sequential within the organization, scoped per system. Example: `RTM-0001` is the first RTM for the
  first system; `RTM-0002` may cover a different system or a major re-baseline of the same system.
- **File Naming:** `RTM-[NNNN]_[SystemName]_v[X.Y].[ext]`
  - Example: `RTM-0001_PaymentGateway_v1.0.yaml`
  - Example: `RTM-0001_PaymentGateway_v1.2.md`
- **Version Numbering:** Semantic (Major.Minor)
  - **Major** (X): Structural changes such as adding new artifact types to the trace, changing the matrix schema, or
    re-baselining after a major release.
  - **Minor** (Y): Content updates such as adding new requirement rows, updating test status, linking new defects.

---

## Scope & Granularity

**Unit of Coverage:** One RTM instance covers one system. A "system" is defined as a deployable unit with its own
requirement set and release cycle.

**When to Create a New RTM:**

- A new system or major subsystem is introduced
- A system undergoes a full re-baseline (e.g., major architectural overhaul)
- Regulatory or compliance requirements mandate a separate traceability scope

**When to Update the Existing RTM (not create a new one):**

- New requirements are approved for the system
- Design, test, or release artifacts are created or modified
- Defects are discovered and linked
- Test execution results change
- A new release is cut

**Relationship to Parent/Child Documents:** The RTM does not replace any source document. It references them by ID. If a
PC, FRD, HLD, or TC document is updated, the RTM must be reviewed and updated to reflect the change. The RTM is the
dependent artifact — it inherits changes from all source documents.

---

## Section-by-Section Explanation

### Purpose & Scope (Required)

- **Purpose:** Establishes why this RTM exists, which system it covers, and the agreed-upon coverage targets.
- **What to include:** System name, trace coverage goal (e.g., "100% of approved functional requirements must be linked
  to at least one test case"), exclusions (e.g., "Deferred requirements are excluded from coverage metrics").
- **What NOT to include:** Detailed requirement descriptions (those belong in the FRD/SRS). Do not duplicate content
  from source documents.
- **Example:** "This RTM covers the Payment Gateway system (PGW). The trace coverage goal is 100% forward coverage from
  FRD to TC and 100% backward coverage from TC to FRD. NFR requirements related to performance must be linked to at
  least one load test case."

### Artifact Registry (Required)

- **Purpose:** Provides a lookup table of all artifact types participating in the trace. Enables consumers to locate
  source documents quickly.
- **What to include:** Artifact type name, document prefix, repository location (URL, SharePoint path, Confluence
  space), and the role responsible for maintaining that artifact type.
- **What NOT to include:** Individual document instances. This is a registry of *types*, not a list of every PC ever
  written.
- **Example:** "Functional Requirements | FRD | Confluence > PGW > Requirements | Business Analyst"

### Traceability Matrix (Required)

- **Purpose:** The core data table. Each row represents one requirement and its trace links in both directions.
- **What to include:** Requirement ID, brief description, priority, current status, backward link to PC, forward links
  to HLD, LLD, TC, DEF, and RN, verification method, and comments.
- **What NOT to include:** Full requirement text (keep descriptions brief, under 20 words). Do not include test steps —
  only link to the TC document by ID.
- **Required columns:** req_id, req_description, req_priority, req_status, source_pc_id, hld_ref, lld_ref,
  test_case_ids, test_status, defect_ids, release_id, verification_method
- **Optional column:** comments

### Coverage Summary (Required)

- **Purpose:** Quantitative dashboard for traceability health. Used in go/no-go decisions, sprint reviews, and audit
  responses.
- **What to include:** Total count of requirements, counts of linked vs. unlinked requirements, percentage metrics for
  forward coverage, backward coverage, and overall coverage.
- **What NOT to include:** Qualitative assessments or risk narratives (those go in Gap Analysis).

### Gap Analysis (Required)

- **Purpose:** Identifies and tracks requirements with missing trace links. Each gap has a risk level and remediation
  plan.
- **What to include:** Requirement ID, the type of missing link (e.g., "No test case"), risk level, remediation action,
  owner, and target date.
- **What NOT to include:** Gaps that have been fully remediated — move those to the Change Log. Only active gaps should
  appear here.

### Bidirectional Trace Verification (Required)

- **Purpose:** Explicit confirmation that both forward and backward traces are verified. Catches "gold-plating"
  (artifacts without a requirement) and "orphaned requirements" (requirements without any downstream artifact).
- **What to include:** Status of forward trace check, status of backward trace check, lists of orphaned test cases and
  orphaned design elements.
- **What NOT to include:** Do not list every passing trace link. Only list exceptions and orphans.

### Sign-Off (Required)

- **Purpose:** Formal governance gate. The matrix is not considered approved until all required roles have signed off.
- **What to include:** Role, name, date, and signature for each approver.
- **What NOT to include:** Do not include reviewers who only provided feedback but did not formally approve.

### Attachments (Optional)

- **Purpose:** Container for supplementary files such as exported spreadsheets, coverage heat maps, or tool-generated
  reports.
- **What to include:** File name, description, and date added.
- **What NOT to include:** Do not attach full source documents. Link to them by ID in the Artifact Registry instead.

---

## Update Triggers

### Creation Triggers

- A new system is initiated and its first requirements are approved
- A major re-baseline event occurs (e.g., architectural overhaul, platform migration)
- Regulatory audit requires a fresh traceability baseline

### Update Triggers

- A new requirement is approved (add row to matrix)
- An existing requirement is modified (update row, review downstream links)
- A requirement is deferred or deleted (update status, recalculate coverage)
- A new design artifact (HLD/LLD) is created or modified (update forward links)
- A test case is created, modified, or retired (update test_case_ids and test_status)
- Test execution results change (update test_status)
- A defect is raised against a requirement (update defect_ids)
- A release is cut and requirements are delivered (update release_id)

### Review Triggers

- Before each sprint review or iteration demo (verify coverage is current)
- Before each release go/no-go decision (coverage summary must meet threshold)
- After a major scope change or change request is approved
- During internal or external audit preparation
- Quarterly review even if no changes occurred (confirm matrix is still accurate)

### Retirement Triggers

- The system is decommissioned
- A new RTM is created as a re-baseline, superseding the current one
- The system is merged into another system with its own RTM

---

## Roles & Responsibilities

| Role               | Responsibility                                                                                         |
|--------------------|--------------------------------------------------------------------------------------------------------|
| **Business Analyst** | Authors and maintains backward trace links (PC → FRD). Validates that all business requirements are represented. |
| **QA Lead**          | Authors and maintains forward trace links (FRD → TC). Updates test status and defect links. Produces coverage metrics. |
| **Project Manager**  | Owns the RTM as a governance artifact. Ensures updates happen on schedule. Uses coverage summary for go/no-go decisions. |
| **Architect**        | Validates design trace links (FRD → HLD → LLD). Flags orphaned design elements.                        |
| **Release Manager**  | Updates release_id column when requirements are included in a release.                                  |

**Accountable for Currency:** The **QA Lead** is the primary owner responsible for keeping the RTM current. The
**Project Manager** is accountable for ensuring the QA Lead performs this duty.

---

## Quality Checklist

Use this checklist before submitting the RTM for review:

- [ ] All required sections are completed (Purpose, Artifact Registry, Matrix, Coverage Summary, Gap Analysis,
  Bidirectional Verification, Sign-Off)
- [ ] Document ID follows the naming convention (RTM-[NNNN])
- [ ] File name follows the convention (RTM-[NNNN]_[SystemName]_v[X.Y].[ext])
- [ ] All approved requirements have a row in the traceability matrix
- [ ] Every requirement row has at least one forward trace link (to HLD or TC)
- [ ] Every requirement row has a backward trace link (to PC)
- [ ] Coverage summary metrics are calculated and current
- [ ] All critical and high-risk gaps have a remediation plan with an owner and target date
- [ ] Bidirectional verification is performed — orphaned artifacts are flagged
- [ ] Related documents are listed in the metadata
- [ ] Change log is updated with the current version entry
- [ ] Sign-off section has the correct approver roles listed
- [ ] No full requirement text is duplicated — only IDs and brief descriptions
- [ ] Attachments (if any) are referenced, not embedded inline

---

## Best Practice Recommendations

**Tooling:** While this RTM can be maintained as a YAML or Markdown file, teams with more than 50 requirements should
consider tool-assisted traceability (e.g., Jira + Xray, Azure DevOps, IBM DOORS, Helix ALM). The templates provided here
can serve as the data schema for tool configuration.

**Automation:** The YAML template is designed for machine consumption. Teams can build CI/CD pipeline checks that parse
the YAML RTM and fail builds if coverage drops below the agreed threshold.

**Living Document:** The RTM is not a one-time deliverable. It must be updated continuously throughout the SDLC. Stale
RTMs provide false assurance and are worse than having no RTM at all.

**Trace Granularity:** Trace at the individual requirement level, not at the document level. "FRD-0023 → TC-0045" is
useful. "FRD document → Test Plan document" is not.
