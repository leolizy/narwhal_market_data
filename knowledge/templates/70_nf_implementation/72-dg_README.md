# DG-0001: Deployment Guide — Policy & Governance Document

## Document Overview

### What Is a Deployment Guide?

A Deployment Guide (DG) is a per-system or per-service operational document that provides the complete, step-by-step
procedure for deploying a specific application or service across all environments. It covers everything from
pre-deployment verification through post-deployment signoff, including rollback procedures, troubleshooting, and
communication protocols.

### Function in the SDLC

The Deployment Guide sits at the boundary between **development** and **operations** in the SDLC. It is created during
the implementation phase when a system is first prepared for production deployment, and it lives as a continuously
updated document throughout the system's operational lifecycle. While the CI/CD Handbook (CICD) defines the
organizational framework and standards, the DG translates those standards into concrete, executable procedures for a
specific system.

### Position in the Document Hierarchy

```
CI/CD Framework & Handbook (CICD)        — Organization-wide standards
└── Deployment Guide (DG)                ← THIS DOCUMENT (per system/service)

```

**Upward references:**
- **CICD Handbook** — The DG must comply with the parent CICD handbook's standards for deployment strategies, quality
  gates, security controls, and approval workflows.
- **PSD-0001** — The DG references the Product Specification Document for architectural context.
- **AEC** — The DG references the Async Event Contract for event-driven integration details.

**Lateral references:**
- **API Specification** — Deployment may involve API contract changes.
- **DBC** — Database changes that accompany the deployment.
- **DC** — Data contracts affected by the deployment.

---

## Naming & ID Convention

### ID Format

```
DG-[NNNN]

```

- **Prefix:** `DG` (Deployment Guide)
- **Numbering:** Sequential, organization-wide. One DG per deployable system or service. Assigned when the system first
  reaches production readiness.
- **Examples:** DG-0001, DG-0015, DG-0042

### File Naming Convention

```
DG-[NNNN]_[SystemName]_v[X.Y].[ext]

```

**Examples:**
- `DG-0001_OrderService_v1.0.yaml`
- `DG-0001_OrderService_v1.0.md`
- `DG-0015_PaymentGateway_v2.3.md`

### Version Numbering

Semantic versioning: **MAJOR.MINOR**

- **MAJOR** increment: Fundamental changes to the deployment process (e.g., new deployment strategy, migration from VMs
  to Kubernetes, new environment tier added, complete pipeline redesign).
- **MINOR** increment: Updates within the existing process (e.g., new troubleshooting entry, updated rollback command,
  configuration key change, new dependency added).

---

## Scope & Granularity

### What Does One Document Cover?

One Deployment Guide covers **one deployable system or service**. A "deployable system" is a unit that goes through a
single deployment pipeline and is released as a cohesive whole.

**Examples of one DG:**
- A single microservice (e.g., Order Service)
- A monolithic application (e.g., the core ERP system)
- A serverless application composed of related Lambda functions
- A data pipeline (e.g., the ETL pipeline for customer analytics)
- A frontend application (e.g., the React SPA for the customer portal)

**Not separate DGs:**
- Individual Lambda functions within a single serverless application (covered by the application's DG)
- Database-only migrations without application changes (covered within the DG's database migration section)

### When to Create a New DG vs. Update an Existing One

| Scenario | Action |
|----------|--------|
| New system reaches production readiness | Create a new DG |
| Deployment process changes (e.g., new strategy) | Update existing DG (major or minor version) |
| New component added to an existing system | Update existing DG (minor version) |
| System is split into two independent services | Create new DGs for both; retire the original |
| System migrates to new infrastructure platform | Update existing DG (major version) |
| New environment tier added | Update existing DG (minor version) |
| Troubleshooting entry added from incident postmortem | Update existing DG (minor version) |
| System is decommissioned | Retire the DG |

### Relationship to Parent/Child Documents

- **Parent:** The CICD Handbook that defines organizational CI/CD standards.
- **Children:** None.
- **Siblings:** Other DGs for other systems; shared infrastructure DGs.

---

## Section-by-Section Explanation

### Section 1: Introduction

- **Purpose:** Provide context for anyone opening this guide — what system is being deployed, who should use this guide,
  and what they need to know before starting.
- **What to include:** System name and business context, criticality tier, scope boundaries, target audience with
  prerequisite knowledge, and references to related documents.
- **What NOT to include:** Detailed architecture (reference the PSD). General CI/CD concepts (reference the CICD
  Handbook).
- **Required:** Yes

### Section 2: Deployment Architecture

- **Purpose:** Establish the technical context for the deployment — what infrastructure is used, what components exist,
  and what external dependencies are required.
- **What to include:** Deployment topology (model, platform, orchestration), a complete component inventory with
  artifact types and deployment targets, and a dependency map showing what must be available at deploy time.
- **What NOT to include:** Application architecture details (reference the PSD). Detailed infrastructure provisioning
  steps (reference IaC documentation).
- **Required:** Yes

### Section 3: Environment Configuration

- **Purpose:** Document how environments are set up and how configuration flows from development through production.
- **What to include:** Environment matrix with promotion paths, configuration management strategy and hierarchy, secrets
  inventory (logical names only, never values), and IaC references.
- **What NOT to include:** Actual secret values, credentials, or connection strings. Environment provisioning procedures
  (those belong in infrastructure documentation).
- **Required:** Yes

### Section 4: Pre-Deployment Checklist

- **Purpose:** Ensure every deployment starts from a verified, ready state. This is the quality gate between "we want to
  deploy" and "we are deploying."
- **What to include:** Verifiable checklist items covering artifact validation, environment readiness, dependency
  health, and approvals/communication. Each item should have a concrete verification method.
- **What NOT to include:** The deployment steps themselves (those belong in Section 5). General project readiness
  criteria (this is deployment-specific).
- **Required:** Yes

### Section 5: Deployment Procedure

- **Purpose:** The core of the document — the step-by-step procedure for deploying the system.
- **What to include:** The deployment strategy and rationale, the primary automated deployment path with pipeline
  details, a manual fallback procedure, and database migration steps if applicable. Each step should specify the
  executor (automated/manual), expected duration, success criteria, and failure action.
- **What NOT to include:** CI pipeline details (those belong in the CICD Handbook). Code-level changes (those belong in
  version control history). One-time migration scripts (those belong in operational documentation).
- **Required:** Yes (manual deployment and database migration subsections are optional)

### Section 6: Post-Deployment Verification

- **Purpose:** Confirm the deployment is healthy before declaring it complete. This prevents silent failures from
  reaching end users.
- **What to include:** Smoke test suite and execution method, health check endpoints for each component, monitoring
  verification (metrics, logs, error rates), traffic validation for canary/blue-green deployments, and signoff criteria
  with observation period.
- **What NOT to include:** Full test plans (those belong in UT documents). Monitoring system setup (those belong in
  CICD-0001 or operational documentation).
- **Required:** Yes (traffic validation subsection is optional)

### Section 7: Rollback Procedure

- **Purpose:** Provide a tested, executable plan for reverting to the previous known-good state when a deployment fails.
- **What to include:** Automated and manual rollback triggers with thresholds, step-by-step rollback procedure with
  exact commands, database rollback strategy with data loss implications, post-rollback verification, and communication
  plan.
- **What NOT to include:** Root cause analysis procedures (those belong in incident management docs). Forward-fix
  procedures for non-rollbackable changes (document these in operational documentation).
- **Required:** Yes (database rollback subsection is optional if no database changes)

### Section 8: Troubleshooting Guide

- **Purpose:** Capture tribal knowledge and incident learnings so operators can resolve common problems quickly without
  escalation.
- **What to include:** Known issues with symptoms, causes, and resolutions. Diagnostic commands organized by category.
  Log locations with access methods and useful queries.
- **What NOT to include:** General system administration procedures (those belong in operational documentation).
  Application-level debugging guides (those belong in developer documentation).
- **Required:** Yes

### Section 9: Communication Plan

- **Purpose:** Ensure the right people are informed at the right time during routine deployments and incidents.
- **What to include:** Routine deployment notification templates and channels (pre, during, post), escalation path for
  incidents during deployment with contact methods and SLAs.
- **What NOT to include:** General incident management procedures (those belong in incident management docs).
  Non-deployment-related communication protocols.
- **Required:** Yes

### Section 10: Maintenance Windows & Scheduling

- **Purpose:** Define when deployments are allowed, when they are prohibited, and how emergency exceptions are handled.
- **What to include:** Standard deployment windows per environment, blackout periods with exception processes, emergency
  deployment approval requirements.
- **What NOT to include:** General change management processes (those belong in the CICD Handbook or change management
  docs).
- **Required:** No (Optional — but recommended for Tier 1 and Tier 2 systems)

### Section 11: Disaster Recovery

- **Purpose:** Cover catastrophic failure scenarios that go beyond a simple rollback.
- **What to include:** RTO/RPO targets, recovery procedures for specific catastrophic scenarios, backup references with
  restore procedure links.
- **What NOT to include:** Business continuity planning (that is an organizational-level document). Backup configuration
  and scheduling (those belong in infrastructure documentation).
- **Required:** No (Optional — but recommended for Tier 1 systems)

### Change Log

- **Purpose:** Audit trail of the deployment guide's own evolution.
- **What to include:** Version, date, author, and a concise description of what changed.
- **Required:** Yes

---

## Update Triggers

### Creation Triggers

A new Deployment Guide **must** be created when:

- A new system or service reaches production readiness for the first time
- An existing system is split into independently deployable services
- A system is migrated to a fundamentally different infrastructure platform (e.g., VM to Kubernetes) and existing
  procedures no longer apply
- A previously undocumented system is onboarded into the deployment governance framework

### Update Triggers (Minor Version)

The DG **must** be updated when:

- A new deployable component is added to the system
- Configuration keys or secrets are added, renamed, or removed
- A new external dependency is introduced
- The deployment pipeline is modified (new steps, changed parameters)
- A troubleshooting entry is added from an incident postmortem
- Rollback commands or procedures change
- Health check endpoints or monitoring queries change
- Communication channels or escalation contacts change
- A new environment is added to the promotion path
- Deployment windows or blackout periods change

### Update Triggers (Major Version)

The DG **must** be versioned as a major change when:

- The deployment strategy changes (e.g., rolling update to blue-green)
- The system migrates to a new infrastructure platform
- The deployment pipeline is fundamentally redesigned
- A new environment tier is added that changes the promotion path
- The database migration approach changes fundamentally
- The rollback strategy changes (e.g., from rollback-capable to forward-fix only)

### Review Triggers

The DG **must** be reviewed (even without changes) when:

- **Quarterly** — Mandatory quarterly review to catch stale information
- **Post-incident** — Any production incident during or caused by a deployment
- **Post-migration** — After any infrastructure or platform migration
- **Team change** — When the team responsible for the system changes
- **CICD Handbook update** — When the parent CICD Handbook is updated with new standards that may affect this system

### Retirement Triggers

The DG should be marked as **Superseded** or **Retired** when:

- The system is decommissioned and no longer deployed
- The system is replaced by a successor (link to the successor's DG)
- The system is absorbed into another system (link to the absorbing system's DG)

---

## Roles & Responsibilities

| Role | Responsibility |
|------|---------------|
| **Service Owner / Tech Lead** | Authors and maintains the DG. Accountable for accuracy and currency. Ensures the guide reflects the current deployment process. |
| **DevOps / Platform Engineer** | Reviews infrastructure, pipeline, and configuration sections. Validates that procedures align with platform capabilities and CICD Handbook standards. |
| **SRE / On-Call Engineer** | Reviews rollback, troubleshooting, and monitoring sections. Validates that procedures are executable under incident pressure. |
| **Release Manager** | Reviews approval workflows, communication plans, and scheduling sections. Ensures alignment with release management processes. |
| **Approver** | Final sign-off authority. Typically the Engineering Manager or Service Owner's manager. Confirms the guide is complete and has been reviewed by all required parties. |

---

## Quality Checklist

Before submitting a Deployment Guide for review, the author should verify:

- [ ] All required sections (1–9, Change Log) are completed
- [ ] Document ID follows the `DG-[NNNN]` naming convention
- [ ] File is named following `DG-[NNNN]_[SystemName]_v[X.Y].[ext]`
- [ ] System name and criticality tier are specified
- [ ] Component inventory lists every deployable component with artifact type and target
- [ ] Dependency map includes all external dependencies with health check methods
- [ ] Environment matrix covers all environments with promotion path
- [ ] Secrets inventory lists all secrets by logical name (no actual values)
- [ ] Pre-deployment checklist items are verifiable (each has a verification method)
- [ ] Deployment steps specify executor, expected duration, success criteria, and failure action
- [ ] Rollback procedure includes both automated triggers and manual steps
- [ ] Rollback procedure has been tested (or test date is scheduled)
- [ ] Troubleshooting guide includes at least the known issues from past incidents
- [ ] Communication plan covers both routine and incident scenarios
- [ ] Related documents (CICD handbook, PSD, AEC) are linked
- [ ] Change log is updated with the current version entry
- [ ] Reviewed by DevOps / Platform Engineer
- [ ] Reviewed by SRE / On-Call Engineer
- [ ] Reviewed by Release Manager (for Tier 1 and Tier 2 systems)
