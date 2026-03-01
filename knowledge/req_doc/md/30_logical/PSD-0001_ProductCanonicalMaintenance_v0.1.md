# Product Specification Document — Product Canonical Maintenance

| Field | Value |
|-------|-------|
| Document ID | PSD-0001 |
| Title | Product Canonical Maintenance |
| Version | v0.1 |
| Status | Draft |
| Created | 2026-03-01 |
| Last Updated | 2026-03-01 |
| Author | Leo |
| Reviewer | TBD |
| Approver | TBD |
| Parent Document | FRD-NMD-0001 |
| Related Documents | PC-NMD-0001, FRD-NMD-0001 |
| Classification | Internal |

---

## 1. Function Overview

Provides full lifecycle management of the NMD product canonical entity table — creating, updating,
deactivating, and managing the status of instrument master records, with a full audit trail on every
write.

| Field | Value |
|-------|-------|
| Function Type | DATA_PAGE |
| Module | NMD-CANONICAL |
| Triggering Actors | Data Owner (ACT-001), Data Ingestion Module / Source Processing (ACT-003) |

---

## 2. User Roles and Permissions

| Role | Type | Permitted Operations |
|------|------|---------------------|
| Data Owner | Human | Create canonical record; Update canonical record (non-locked fields only); Deactivate canonical record (via Disable status); Change status to any value subject to parent status constraint (BR-006) |
| Data Ingestion Module (Source Processing) | System | Create canonical record (golden source only); Set status as defined by source configuration only |

---

## 3. Preconditions and Dependencies

### Preconditions

| ID | Precondition |
|----|-------------|
| PRE-001 | Canonical entity table is initialised and accessible |
| PRE-002 | Phase 1 asset class definitions (Futures & Options, FX) are configured in the system |
| PRE-003 | Hash algorithm is agreed and implemented platform-wide (see OI-001 in FRD-NMD-0001) |
| PRE-004 | For Data Owner path: user is authenticated with Data Owner role |
| PRE-005 | For Source Processing path: source configuration exists with golden source flag and initial status defined (FRD-NMD-0002) |

### Dependencies

| ID | Dependency | Blocks |
|----|-----------|--------|
| DEP-001 | FRD-NMD-0002 source configuration schema | Auto-create path cannot be designed until source configuration is finalised |
| DEP-002 | Asset class mapping definitions for Phase 1 (Futures & Options, FX) | Field validation rules for entity type and Product Type cannot be finalised |
| DEP-003 | Hash algorithm agreed across all NMD modules | Canonical key computation must be consistent platform-wide |

---

## 4. Data Page Specification

### Entity Definition

**Entity:** Canonical Record

A single row in the canonical entity table representing one unique financial instrument, identified
by its canonical key. No hard delete — retirement via Disable status only.

**Primary Key:** `canonical_key`

### Field Catalog

| Field | Type | Source | Create | Update | Required | Notes |
|-------|------|--------|--------|--------|----------|-------|
| `canonical_key` | string | System-computed | Auto — hash of 5 hierarchy columns | Locked — fixed at creation | Yes | Deterministic hash; same 5-column input always produces the same key |
| `exchange` | string | User / Source Processing | Required | Locked | Yes | Mandatory on every record. For FX records: fixed value 'FX' |
| `commodity` | string | User / Source Processing | Optional — required for entity types above L1 | Locked | No | For FX Currency Pair: must be XXXYYY format (6 uppercase characters) |
| `product_type` | enum | User / Source Processing | Optional — required for L3+ entity types | Locked | No | Futures & Options: PHY \| FUT \| CMB \| OOP \| OOF \| OOC. FX: must be null |
| `product_code` | string | User / Source Processing | Optional — required for L3+ entity types | Locked | No | FX: must be null |
| `contract` | string | User / Source Processing | Optional — required for contract-level entity types | Locked | No | Format validated per entity type. Option Contract: YYYYMM_CP_STRIKE \| YYYYMMDD_CP_STRIKE \| YYYYMMWN_CP_STRIKE where CP = C or P. FX: must be null |
| `asset_class` | enum | User / Source Processing | Required | Locked | Yes | Futures & Options \| FX |
| `entity_type` | enum | User / Source Processing | Required | Locked | Yes | Must match a predefined entity type for the selected asset class |
| `status` | enum | User / Source Processing | Required | Editable | Yes | Active \| Inactive \| Disable. Subject to parent status constraint (BR-006). Source Processing: from source configuration only |
| `source` | string | System | Auto | Read-only | Yes | Identifies creation actor: 'User' or source processing identifier |
| `created_by` | string | System | Auto | Read-only | Yes | |
| `created_at` | timestamp | System | Auto | Read-only | Yes | |
| `last_updated_by` | string | System | Auto | Auto | Yes | |
| `last_updated_at` | timestamp | System | Auto | Auto | Yes | |

### List View

**Columns:** `canonical_key`, `exchange`, `commodity`, `product_type`, `product_code`, `contract`,
`asset_class`, `entity_type`, `status`, `last_updated_at`

**Default Sort:** `last_updated_at DESC`

**Filters:** `status`, `asset_class`, `exchange`

### Detail View

All fields including `created_by`, `created_at`, `source`, and link to full immutable audit trail.

### CRUD Operations

| Operation | Actors | Description | Post-conditions |
|-----------|--------|-------------|----------------|
| Create | Data Owner, Source Processing | Create a new canonical record. Canonical key computed from 5 hierarchy columns. Initial status set by actor: user-selected for Data Owner, source configuration for Source Processing. | Record persisted; canonical key computed and stored; audit log entry created; `canonical.record.created` event published |
| Update | Data Owner, Source Processing | Update non-locked fields on an existing canonical record. The 5 hierarchy columns, asset_class, entity_type, and canonical_key are immutable after creation. | Record updated; audit log entry created for each changed field; `canonical.record.updated` event published |
| Status Change | Data Owner, Source Processing | Change the status of a canonical record. Triggers top-down cascade to all non-Disabled descendants. | Record status updated; cascade applied to non-Disabled descendants; audit log entry created for each affected record; `canonical.status.changed` event published |
| Delete | — | Not permitted. Retirement via Disable status only. | — |

---

## 5. Business Rules

| ID | Rule |
|----|------|
| BR-001 | Exchange is mandatory on every record — creation rejected without it |
| BR-002 | Canonical key is computed as a deterministic hash of all 5 columns (null placeholders for skipped levels) at creation and is immutable thereafter |
| BR-003 | The 5 hierarchy columns (exchange, commodity, product_type, product_code, contract), asset_class, and entity_type are locked after creation — corrections require deactivating the record and creating a new one |
| BR-004 | Entity type must match a predefined type for the selected asset class; column population must conform to that entity type's rules |
| BR-005 | Status cascade is top-down — a status change propagates to all non-Disabled descendants; Disabled descendants are exempt and remain unchanged |
| BR-006 | A child record's status cannot be more permissive than its parent: child cannot be Active if parent is Inactive or Disabled; child cannot be Inactive if parent is Disabled |
| BR-007 | Data Owner may set status to any value subject to BR-006; Source Processing may only set status as defined by source configuration |
| BR-008 | Source Processing initial status is taken from source configuration — never defaulted to Active |
| BR-009 | Duplicate records (same canonical key hash) are rejected on creation |
| BR-010 | All writes produce an immutable audit log entry — no write path bypasses the audit trail |

---

## 6. Validation Rules

| ID | Field | Rule | Error Message |
|----|-------|------|--------------|
| VAL-001 | `exchange` | Must be non-empty | "Exchange is required" |
| VAL-002 | `asset_class` | Must be one of: Futures & Options, FX | "Invalid asset class" |
| VAL-003 | `entity_type` | Must match a predefined entity type for the selected asset_class | "Entity type not valid for asset class" |
| VAL-004 | `product_type` | For Futures & Options: must be one of PHY, FUT, CMB, OOP, OOF, OOC. For FX: must be null | "Invalid product type for asset class" |
| VAL-005 | `contract` | For Option Contract entity type: must match YYYYMM_CP_STRIKE \| YYYYMMDD_CP_STRIKE \| YYYYMMWN_CP_STRIKE where CP = C or P. For FX: must be null | "Invalid contract format for entity type" |
| VAL-006 | `commodity` | For FX Currency Pair entity type: must be exactly 6 uppercase characters (XXXYYY format) | "Currency pair must be 6 uppercase characters" |
| VAL-007 | `canonical_key` | Must be unique across all records | "Duplicate canonical record" |
| VAL-008 | `status` | Child status cannot be more permissive than parent status | "Status not permitted — parent is [parent_status]" |

---

## 7. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-001 | Given a Data Owner submits a valid new canonical record with all required fields, When the create operation executes, Then the record is persisted with a computed canonical key and an audit log entry is created |
| AC-002 | Given the same 5 hierarchy column values are submitted twice, When canonical key is computed, Then both produce the identical hash |
| AC-003 | Given a create is attempted without an Exchange value, When validation runs, Then the request is rejected with "Exchange is required" |
| AC-004 | Given a create is attempted with a duplicate canonical key, When the system checks uniqueness, Then the request is rejected with "Duplicate canonical record" |
| AC-005 | Given a Data Owner changes the status of a parent record, When the change is saved, Then all non-Disabled descendants are updated to the new status and audit entries are created for each |
| AC-006 | Given a Data Owner attempts to set a child record to Active when the parent is Inactive or Disabled, When validation runs, Then the request is rejected with the parent status constraint error |
| AC-007 | Given Source Processing creates a canonical record from a golden source, When the record is persisted, Then initial status is taken from source configuration — never defaulted to Active |
| AC-008 | Given an entity type of Option Contract is submitted, When contract format is validated, Then only YYYYMM_CP_STRIKE, YYYYMMDD_CP_STRIKE, or YYYYMMWN_CP_STRIKE formats are accepted |
| AC-009 | Given a Futures & Options record is submitted with a Product Type not in PHY/FUT/CMB/OOP/OOF/OOC, When validation runs, Then the request is rejected with permitted values listed |
| AC-010 | Given an FX Currency Pair record is submitted with a Commodity not matching XXXYYY format, When validation runs, Then the request is rejected with "Currency pair must be 6 uppercase characters" |
| AC-011 | Given any canonical write occurs (create, update, status change), When the operation completes, Then an immutable audit log entry exists capturing actor, timestamp, field changed, old value, and new value |
| AC-012 | Given a Data Owner attempts to update any of the 5 hierarchy columns on an existing record, When the update is submitted, Then the request is rejected — locked fields cannot be modified |

---

## 8. Assumptions and Constraints

### Assumptions

| ID | Assumption |
|----|-----------|
| ASM-001 | Asset class column mappings for Phase 1 (Futures & Options, FX) are defined before detailed design begins |
| ASM-002 | Hash algorithm is agreed platform-wide before implementation |
| ASM-003 | Source Processing (FRD-NMD-0002) owns and provides the golden source flag and initial status configuration |
| ASM-004 | No bulk import required in Phase 1 — records created individually by Data Owner or Source Processing |

### Constraints

| ID | Constraint |
|----|-----------|
| CON-001 | Phase 1 asset classes: Futures & Options and FX only |
| CON-002 | No hard deletes — retirement via Disable status only |
| CON-003 | The 5 hierarchy columns and canonical key are immutable after creation — corrections require deactivate + new record |
| CON-004 | Write access restricted to Data Owner and Source Processing only |

---

## 9. Open Questions

| ID | Question |
|----|---------|
| OQ-001 | Is there a formal correction workflow for locked-field errors (e.g., wrong exchange on creation), or is deactivate + new record the only path? |
| OQ-002 | What is the SLA for status cascade on large parent records (e.g., disabling an Exchange with thousands of descendants)? Flagged in NFR-NMD-001-002 but not yet quantified. |

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| v0.1 | 2026-03-01 | Leo | Initial draft — DATA_PAGE spec for FA-01 Canonical Maintenance from FRD-NMD-0001. Covers field catalog, CRUD operations, business rules, validation rules, and acceptance criteria for both Futures & Options and FX asset classes. |
