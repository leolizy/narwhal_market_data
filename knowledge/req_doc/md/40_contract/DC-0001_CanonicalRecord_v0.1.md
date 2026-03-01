# Data Contract — Canonical Record Data Contract

| Field | Value |
|-------|-------|
| Document ID | DC-0001 |
| Title | Canonical Record Data Contract |
| Version | v0.1 |
| Status | Draft |
| Created | 2026-03-01 |
| Last Updated | 2026-03-01 |
| Author | Leo |
| Reviewer | TBD |
| Approver | TBD |
| Related Documents | FRD-NMD-0001, PSD-0001, PSD-0002, AEC-0001, AEC-0002, AEC-0003 |
| Classification | Internal |

---

## 1. Contract Overview

This data contract governs the canonical instrument record — the authoritative identity for every unique financial instrument in NMD. The canonical entity table is the single source of truth for instrument identity. All ingestion, normalisation, and export modules resolve their data against this table. The contract defines the schema, ownership, quality standards, SLA, and access rules for the canonical record dataset.

---

## 2. Data Product Identification

| Field | Value |
|-------|-------|
| Product Name | Canonical Record |
| Product Id | NMD-CANONICAL |
| Domain | NMD |
| Subdomain | Canonical |
| Owner Team | NMD Team |
| Owner Contact | Team Lead |
| Data Steward | Data Owner (ACT-001) |
| Tier | Tier 1 (Critical) |
| Tags | canonical, instrument-identity, market-data, master-data |

---

## 3. Schema Definition

**Schema Format:** JSON Schema / DDL
**Schema Version:** v0.1
**Schema Registry:** TBD — platform schema registry

### Fields

| Field | Type | Nullable | PK | Constraints | Description |
|-------|------|----------|----|-------------|-------------|
| `canonical_key` | string | No | Yes | Unique; non-empty; computed by system — not supplied by caller | Deterministic hash of the 5 hierarchy columns (null placeholders for absent levels). Primary key — unique across all records. Immutable after creation. |
| `exchange` | string | No | No | Non-empty; for FX asset class: must equal 'FX' | Exchange identifier. Mandatory on every record. For FX records: fixed value 'FX'. Locked after creation. |
| `commodity` | string | Yes | No | For FX Currency Pair: exactly 6 uppercase characters (XXXYYY format) | Commodity identifier. Required for entity types above L1. For FX Currency Pair: must be XXXYYY format (6 uppercase characters, no separator). Locked after creation. |
| `product_type` | string | Yes | No | Futures & Options: one of PHY, FUT, CMB, OOP, OOF, OOC. FX: must be null. | Product type — Futures & Options only. Required for L3+ entity types. Must be null for FX. Locked after creation. |
| `product_code` | string | Yes | No | FX: must be null | Product code — required for L3+ entity types. Must be null for FX. Locked after creation. |
| `contract` | string | Yes | No | Option Contract: YYYYMM_CP_STRIKE | YYYYMMDD_CP_STRIKE | YYYYMMWN_CP_STRIKE. FX: must be null. | Contract ticker — required for contract-level entity types. Must be null for FX. Locked after creation. Option Contract format: YYYYMM_CP_STRIKE | YYYYMMDD_CP_STRIKE | YYYYMMWN_CP_STRIKE where CP = C or P. |
| `asset_class` | string | No | No | One of: Futures & Options, FX | Asset class. One of: Futures & Options, FX. Locked after creation. |
| `entity_type` | string | No | No | Must be valid for the selected asset_class | Entity type — must match a predefined type for the selected asset class. Locked after creation. Futures & Options: Exchange | Commodity | Product | Future Contract | Option Reference Contract | Option Contract. FX: FX Currency Pair. |
| `status` | string | No | No | One of: Active, Inactive, Disable. Cannot be more permissive than parent record status. | Operational status. Subject to parent status constraint — child cannot be more permissive than parent. Editable. |
| `source` | string | No | No | System-assigned; non-empty | Creation actor identifier. 'User' for Data Owner; source processing identifier for automated creation. Read-only. |
| `created_by` | string | No | No | System-assigned; non-empty | Identity of the actor who created the record. System-assigned. Read-only. |
| `created_at` | timestamp | No | No | System-assigned | Timestamp of record creation. System-assigned. Read-only. |
| `last_updated_by` | string | No | No | System-assigned; non-empty | Identity of the actor who last updated the record. System-assigned on every write. |
| `last_updated_at` | timestamp | No | No | System-assigned | Timestamp of the most recent update. System-assigned on every write. |

---

## 4. Semantic Definitions

### Business Glossary

| Term | Definition |
|------|-----------|
| Canonical Record | A single authoritative row in the canonical entity table representing one unique financial instrument, identified by its canonical key. No two instruments share the same canonical key. |
| Canonical Key | A deterministic hash computed from the 5 hierarchy columns (exchange, commodity, product_type, product_code, contract) with null placeholders for absent levels. The same 5-column input always produces the same key. |
| Hierarchy Columns | The 5 columns that define instrument identity: exchange, commodity, product_type, product_code, contract. These are locked after creation — corrections require disabling the record and creating a new one. |
| Status | Active: full data loading enabled. Inactive: reference data only, no market data loading. Disable: all loading suppressed; record excluded from exports. |
| Status Cascade | A top-down propagation of a status change from a parent record to all non-Disabled descendants. Disabled descendants are exempt and remain unchanged. |
| Entity Type | The level of the hierarchy this record represents. Futures & Options: Exchange, Commodity, Product, Future Contract, Option Reference Contract, Option Contract. FX: FX Currency Pair. |

### Business Rules

- Exchange is mandatory on every record
- Canonical key is immutable after creation
- The 5 hierarchy columns, asset_class, and entity_type are locked after creation
- Status cascade is top-down to all non-Disabled descendants
- Child status cannot be more permissive than parent status
- No hard deletes — retirement via Disable status only
- All writes produce an immutable audit log entry

---

## 5. Write Path Contract

**DB Architecture Reference:** TBD — DBAD document not yet created
**Transaction Guarantees:** Each write operation (create, update, status change) is atomic — the record update and audit log entry are committed together or not at all
**Idempotency:** Create: idempotent on canonical_key — duplicate keys are rejected (409 Conflict). Status change: idempotent on (canonical_key, new_status) — reapplying the same status is a no-op.
**Locking Strategy:** TBD — platform standard row-level locking for concurrent write protection
**Batch Write Behaviour:** Not supported in Phase 1 — records created individually by Data Owner or Source Processing
**Transformation Contract:** Canonical key is computed by the system as a deterministic hash of the 5 hierarchy columns at creation time. The hash algorithm must be agreed and implemented consistently across all NMD modules (PRE-003 in PSD-0001).

**Write Modes:**

| Mode | Supported |
|------|-----------|
| insert | Yes |
| update | Yes |
| upsert | No |
| soft_delete | Yes |
| hard_delete | No |

---

## 6. Data Quality Standards

### Completeness

- exchange must be non-null and non-empty on every record
- asset_class must be non-null on every record
- entity_type must be non-null on every record
- status must be non-null on every record
- All 5 audit fields (source, created_by, created_at, last_updated_by, last_updated_at) populated by system on every write

### Uniqueness

- canonical_key is unique across all records — duplicate keys rejected on creation

### Validity

- asset_class: one of Futures & Options, FX
- entity_type: valid for the selected asset_class
- product_type: Futures & Options — one of PHY, FUT, CMB, OOP, OOF, OOC; FX — must be null
- contract (Option Contract): YYYYMM_CP_STRIKE | YYYYMMDD_CP_STRIKE | YYYYMMWN_CP_STRIKE
- commodity (FX Currency Pair): exactly 6 uppercase characters (XXXYYY format)
- status: one of Active, Inactive, Disable

### Consistency

- canonical_key always equals the deterministic hash of the 5 hierarchy columns
- child record status cannot be more permissive than parent record status

### Timeliness

- last_updated_at reflects the timestamp of the most recent write — no stale audit timestamps

### Custom Checks

- Verify canonical_key recomputation matches stored value on any read (data integrity check)
- Monitor for records with status Active where parent is Inactive or Disabled (consistency violation)

---

## 7. Service Level Agreements

**Availability:** TBD — platform standard
**Delivery Schedule:** Real-time — every write is immediately queryable; no batch windows
**Throughput:** TBD — platform standard; status cascade on large parent hierarchies may produce burst write volume
**Incident Response:** Escalation contact: Team Lead

**Latency:**

| Path | SLA |
|------|-----|
| Lookup By Canonical Key | Hot path — must meet platform latency target NFR-NMD-001-001 (TBD) |
| Attribute Search | Non-hot path — SLA TBD (OQ-001 in PSD-0002) |
| Write Operations | TBD — platform standard |

---

## 8. Access and Security

**Access Mechanism:** Canonical Query API (PSD-0002) for reads; Canonical Management API (PSD-0001) for writes. Direct database access not permitted.
**Authentication:** TBD — platform standard (JWT Bearer / mTLS)
**Authorization Model:** Role-based — Data Owner, Data Ingestion Module, Query & Export Module
**Data Masking:** Not applicable — no PII or sensitive data in canonical records
**Retention Policy:** Indefinite — no hard deletes; Disabled records retained permanently

**Approved Consumers:**

| Consumer | Access |
|----------|--------|
| Data Owner (ACT-001) | Read all status types; Write (create, update, status change) |
| Data Ingestion Module (ACT-003 / FRD-NMD-0002) | Read all status types; Write (create from golden source, set status per source config) |
| Query & Export Module (ACT-004 / FRD-NMD-0003) | Read Active and Inactive only — Disabled records never returned |

---

## 9. Lineage and Dependencies

**Source Systems:**
- Data Owner manual input via Operator UI
- Source Processing from golden sources (FRD-NMD-0002 — to be specified)

**Upstream Datasets:**
- Source configuration (FRD-NMD-0002) — provides golden source flag and initial status for Source Processing path

**Downstream Consumers:**
- Data Ingestion Module (FRD-NMD-0002) — source-to-canonical mappings and ingestion pipelines; triggered by AEC-0001 and AEC-0003
- Query & Export Module (FRD-NMD-0003) — enrichment cache and export eligibility; triggered by AEC-0002 and AEC-0003

**Transformation Summary:** No transformation — canonical record data is the authoritative source; consumers call the Canonical Query API to retrieve records. Canonical key is computed by the system at creation as a deterministic hash.

---

## 10. Versioning and Compatibility

**Versioning Strategy:** Schema changes follow the canonical record version. Breaking changes require a new document version and 30-day consumer migration notice.
**Deprecation Policy:** Deprecated fields must be flagged with a deprecation notice and remain present for a minimum of 30 days before removal

**Breaking Changes:**
- Removing or renaming any existing field
- Changing the data type of any existing field
- Adding a new non-nullable field without a default value
- Changing the canonical key hash algorithm

**Non-Breaking Changes:**
- Adding a new nullable field
- Adding a new enum value to status (if backward compatible)
- Updating field descriptions or examples

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| v0.1 | 2026-03-01 | Leo | Initial draft — full field catalog for canonical record entity. Covers 14 fields (5 hierarchy columns locked at creation, status, asset_class, entity_type, source audit fields). Includes semantic definitions, write path contract, data quality standards, SLA, access & security, lineage, and versioning policy. Aligned with PSD-0001, PSD-0002, AEC-0001/0002/0003. |
