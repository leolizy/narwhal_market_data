# Data Layer Contract — Policy & Governance Document

## 1. Document Overview

### What Is a Data Layer Contract?

A Data Layer Contract (DC) is a formal, versioned agreement between a **data producer** (the team that creates and
maintains a dataset) and its **data consumers** (teams that read and depend on that dataset). It codifies the schema,
quality guarantees, SLAs, access rules, and evolution policies for a specific dataset or table.

### Function in the SDLC

The Data Layer Contract sits at the intersection of **design** and **operations** in the SDLC. It is created during the
design phase when a new data product is introduced, and it lives as a living document throughout the operational
lifecycle. It serves as the single source of truth for all technical and operational expectations around a dataset.

### Position in the Document Hierarchy

```
SAD / HLD (System Architecture)
  └── API Specification (service-level interfaces)
  └── Data Layer Contract (data-level interfaces)   ← This document
        └── Schema Registry Entry (machine-readable schema)
        └── Data Quality Suite (automated test definitions)

```

The DC complements API specifications by governing **data interfaces** rather than service interfaces. It is referenced
by downstream design documents (LLD), test plans (TP), and runbooks (RB).

---

## Document Dependencies

### Upstream Documents (Dependencies)

- PSD-0001

### Downstream Documents (Depend on This)

- UT-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## 2. Naming & ID Convention

### ID Format

```
DC-[NNNN]

```

- **Prefix:** `DC` (Data Contract)
- **Numbering:** Sequential, organization-wide. Assigned by the data platform team or data catalog system.
- **Examples:** DC-0001, DC-0042, DC-0150

### File Naming Convention

```
DC-[NNNN]_[DataProductName]_v[X.Y].[ext]

```

**Examples:**
- `DC-0001_CustomerOrders_v1.0.yaml`
- `DC-0001_CustomerOrders_v1.0.md`
- `DC-0042_ClickstreamEvents_v2.1.yaml`

### Version Numbering

Semantic versioning: **MAJOR.MINOR**

- **MAJOR** increment: Breaking schema changes (field removal, type change, PK change, semantic redefinition)
- **MINOR** increment: Non-breaking changes (new nullable field, description update, constraint relaxation, SLA
  adjustment)

---

## 3. Scope & Granularity

### What Does One Document Cover?

One Data Layer Contract covers **one logical dataset or table**. A "logical dataset" is defined as a coherent,
independently consumable unit of data with a single owner team.

**Examples of one DC:**
- A single table in a data warehouse (e.g., `dim_customer`, `fact_orders`)
- A single Kafka topic (e.g., `order.created.v1`)
- A single API response payload that serves as a data product
- A single file-based dataset (e.g., a daily CSV drop)

### When to Create a New DC vs. Update an Existing One

| Scenario | Action |
|----------|--------|
| New dataset is introduced | Create a new DC |
| Existing dataset gets a new field (nullable) | Update existing DC (minor version) |
| Existing dataset changes a field type | Update existing DC (major version) |
| A dataset is split into two | Create new DCs for both; retire the original |
| A dataset is merged with another | Create a new DC; retire the originals |
| Ownership transfers to a new team | Update existing DC metadata |

### Relationship to Parent/Child Documents

- **Parent:** The HLD or SAD that defines the system architecture containing this data product
- **Children:** Schema registry entries, data quality test suites, monitoring dashboards
- **Siblings:** Other DCs in the same domain, API specifications for services that produce/consume this data

---

## 4. Section-by-Section Explanation

### Section 1: Contract Overview

- **Purpose:** Provides a human-readable summary so anyone can understand what this contract governs without reading
  every detail.
- **What to include:** The dataset name, its business purpose, who produces it, who consumes it, and why it matters.
- **What NOT to include:** Technical schema details, SLA numbers, or access credentials. Keep it at a summary level.
- **Required:** Yes

### Section 2: Data Product Identification

- **Purpose:** Machine-readable metadata that integrates with data catalogs, search tools, and governance platforms.
- **What to include:** Unique product name/ID, owning domain, responsible team and steward, criticality tier, and
  searchable tags.
- **What NOT to include:** Schema details or quality metrics — those have dedicated sections.
- **Examples:** `product_name: "customer_orders"`, `domain: "Sales"`, `tier: "Tier 1 (Critical)"`
- **Required:** Yes

### Section 3: Schema Definition

- **Purpose:** The authoritative, field-level specification of the dataset. This is what consumers code against.
- **What to include:** Every field with its name, data type, logical type, nullability, constraints, PII flag, and an
  example value. Specify the schema format and link to the schema registry.
- **What NOT to include:** Transformation logic (that belongs in Lineage). Do not include sample data files inline —
  attach them instead.
- **Required:** Yes

### Section 4: Semantic Definitions & Business Rules

- **Purpose:** Eliminates ambiguity. When two teams disagree on what "active customer" means, this section is the
  arbiter.
- **What to include:** A glossary of domain-specific terms used in the schema, plus explicit business rules with
  validation logic and failure actions.
- **What NOT to include:** Generic industry definitions that are universally understood. Focus on terms unique to your
  organization or domain.
- **Required:** Yes

### Section 5: Data Quality Standards

- **Purpose:** Quantified quality commitments that can be monitored and alerted on. Turns quality from a vague
  aspiration into a measurable contract.
- **What to include:** Thresholds for the six standard dimensions (completeness, accuracy, freshness, uniqueness,
  consistency, validity) plus any custom checks.
- **What NOT to include:** The actual test code — reference the test suite location instead. Do not set thresholds you
  cannot measure.
- **Required:** Yes

### Section 6: Service Level Agreements (SLAs)

- **Purpose:** Operational guarantees that consumers can plan around. If this section says "daily by 06:00 UTC,"
  downstream dashboards can be scheduled at 07:00 UTC with confidence.
- **What to include:** Availability targets, latency bounds, delivery schedule, throughput expectations, and incident
  response commitments.
- **What NOT to include:** Aspirational targets — only commit to what you can actually deliver and measure. Do not
  confuse SLAs with SLOs (objectives) or SLIs (indicators); this section defines the contractual SLAs.
- **Required:** Yes

### Section 7: Access & Security

- **Purpose:** Controls who can see and use this data. Especially critical for datasets containing PII or financial
  data.
- **What to include:** Access mechanism, authentication/authorization model, approved consumer list, masking rules for
  sensitive fields, and retention/deletion policies.
- **What NOT to include:** Actual credentials, connection strings with passwords, or API keys. Reference a secrets
  manager instead.
- **Required:** Yes

### Section 8: Lineage & Dependencies

- **Purpose:** Enables impact analysis. Before changing this dataset, you can trace who will be affected. Before
  trusting this dataset, you can trace where it came from.
- **What to include:** Source systems, upstream dataset references, downstream consumer list, and a summary of
  transformations applied.
- **What NOT to include:** Full ETL/ELT code — link to the pipeline repository instead. Keep the transformation summary
  at a conceptual level.
- **Required:** Yes

### Section 9: Versioning & Compatibility

- **Purpose:** Protects consumers from surprise breaking changes. Establishes a social contract for how evolution
  happens.
- **What to include:** Versioning strategy, clear definitions of breaking vs. non-breaking changes, notification
  periods, migration support commitments, and deprecation policies.
- **What NOT to include:** The actual migration scripts — those belong in the pipeline repo or migration guide.
- **Required:** Yes

### Section 10: Support & Communication

- **Purpose:** Reduces friction for consumers who need help or want to stay informed.
- **What to include:** Support channels, documentation links, office hours, announcement channels, and feedback
  mechanisms.
- **What NOT to include:** Detailed troubleshooting guides — link to runbooks instead.
- **Required:** No (Optional, but strongly recommended for Tier 1 and Tier 2 datasets)

### Section 11: Attachments

- **Purpose:** Collects supplementary materials that support the contract but don't belong inline.
- **What to include:** ERD diagrams, sample data files, schema exports, data flow diagrams, or links to related
  dashboards.
- **What NOT to include:** The contract content itself — attachments are supplements, not replacements.
- **Required:** No (Optional)

### Change Log

- **Purpose:** Audit trail of the contract document's own evolution.
- **What to include:** Version, date, author, and a concise description of what changed.
- **Required:** Yes

---

## 5. Update Triggers

### Creation Triggers

A new Data Layer Contract **must** be created when:

- A new dataset, table, or data product is introduced to production
- An existing dataset is split into multiple datasets
- A dataset is migrated to a new platform and its interface changes materially
- A previously undocumented dataset is onboarded into the governance framework

### Update Triggers (Minor Version)

The DC **must** be updated when:

- A new nullable field is added to the schema
- Data quality thresholds are adjusted
- SLA targets are modified
- A new consumer team is onboarded
- Delivery schedule changes
- Masking rules are added or modified
- Support channels or ownership contacts change

### Update Triggers (Major Version)

The DC **must** be versioned as a major change when:

- A field is removed or renamed
- A field's data type changes
- The primary key definition changes
- Business rule semantics are altered
- The delivery mechanism fundamentally changes (e.g., batch → streaming)
- Access mechanism changes (e.g., SQL table → API endpoint)

### Review Triggers

The DC **must** be reviewed (even without changes) when:

- Quarterly governance review cycle
- Post-incident review reveals a data-related root cause
- A dependent system undergoes a major architectural change
- Ownership or team structure changes
- Compliance audit preparation

### Retirement Triggers

The DC should be marked as **Superseded** or **Retired** when:

- The dataset is decommissioned
- The dataset is replaced by a new dataset (link to successor DC)
- All consumers have migrated away
- The source system is retired

---

## 6. Roles & Responsibilities

| Role | Responsibility |
|------|---------------|
| **Data Product Owner** | Authors and maintains the DC. Accountable for accuracy and currency. Typically a senior data engineer or analytics engineer on the owning team. |
| **Data Steward** | Reviews data quality standards, semantic definitions, and business rules. Ensures alignment with enterprise data governance policies. |
| **Platform / Infra Reviewer** | Reviews SLAs, access controls, lineage, and infrastructure-related sections. Typically from the data platform or SRE team. |
| **Consuming Team Lead** | Reviews the contract from the consumer perspective. Validates that SLAs, schema, and quality commitments meet their needs. |
| **Approver** | Final sign-off authority. Typically a data engineering manager, data architect, or governance committee lead. |

---

## 7. Quality Checklist

Before submitting a Data Layer Contract for review, the author should verify:

- [ ] All required sections (1–9, Change Log) are completed
- [ ] Document ID follows the `DC-[NNNN]` naming convention
- [ ] File is named following `DC-[NNNN]_[DataProductName]_v[X.Y].[ext]`
- [ ] Schema definition includes every field with type, nullability, and constraints
- [ ] PII and sensitive flags are set correctly for all fields
- [ ] Business glossary covers all domain-specific terms used in the schema
- [ ] Data quality thresholds are quantified and measurable
- [ ] SLAs are realistic and based on actual infrastructure capabilities
- [ ] At least one approved consumer is listed (or "none yet" is explicitly stated)
- [ ] Lineage section traces data from source to this dataset
- [ ] Breaking vs. non-breaking change definitions are clear
- [ ] Related documents (HLD, API specs, upstream DCs) are linked
- [ ] Change log is updated with the current version entry
- [ ] Reviewed by Data Steward
- [ ] Reviewed by Platform / Infra Reviewer
- [ ] Reviewed by at least one Consuming Team Lead
