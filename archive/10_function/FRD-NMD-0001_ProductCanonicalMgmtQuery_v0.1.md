# FRD-NMD-0001: Product Canonical Management & Query

| Field              | Value                                                        |
|--------------------|--------------------------------------------------------------|
| Document ID        | FRD-NMD-0001                                                 |
| Module Code        | NMD-CANONICAL                                                |
| Title              | Product Canonical Management & Query                         |
| Version            | v0.1                                                         |
| Status             | Draft                                                        |
| Classification     | Internal                                                     |
| Created Date       | 2026-03-01                                                   |
| Last Updated       | 2026-03-01                                                   |
| Author             | Leo                                                          |
| Reviewer           | TBD                                                          |
| Approver           | TBD                                                          |
| Parent BRD         | PC-NMD-0001                                                  |
| Related Documents  | PC-NMD-0001                                                  |
| Tags               | market-data, canonical, product-management                   |
| Supersedes         |                                                              |

---

## 1. Overview

**Summary:** This module owns the product canonical — the master reference record for every financial instrument in NMD. It is the authoritative identity layer that all ingestion, normalization, and export modules resolve their data against.

**Purpose:** To define the functional requirements for maintaining and querying the NMD product canonical entity table, including the 5-column hierarchical model, canonical key computation, status lifecycle, and cross-module query interface.

**Audience:** Developers, QA engineers, and business analysts building or testing the NMD platform

---

## 2. Scope

### In Scope

1. Product canonical entity table maintenance — create, update, deactivate records
2. 5-column hierarchical model: Exchange, Commodity, Product Type, Product Code, Contract
3. Deterministic canonical key hash computation
4. Status lifecycle management: Active, Inactive, Disable with top-down inheritance
5. User and Source Processing creation and status management
6. Full audit trail for all canonical record changes
7. Canonical query interface — lookup by key, source identifier, and attributes
8. Phase 1 asset classes: Futures & Options, FX

### Out of Scope

1. Data ingestion source management and processing (FRD-NMD-0002)
2. Query and export APIs for downstream systems (FRD-NMD-0003)
3. Operator UI implementation (FRD-NMD-0004)
4. Bulk import of canonical records
5. Phase 2+ asset classes: Equities, Fixed Income, Structured Products

---

## 3. Definitions

| Term | Definition |
|------|------------|
| Canonical Record | A single row in the canonical entity table representing one unique financial instrument, identified by its canonical key |
| Canonical Key | A deterministic hash computed from all 5 hierarchy columns (with null placeholders for skipped levels) that uniquely identifies a market data entity across all NMD modules |
| 4-Layer Hierarchy | The structural model: Exchange (L1) → Commodity (L2) → Product [Type + Code] (L3) → Contract (L4) |
| Asset Class | A category of financial instruments (e.g., Futures & Options, FX) that defines its own mapping of the 5 hierarchy columns and supported product types |
| Golden Source | A designated data source whose ingested data is treated as authoritative for canonical record creation and update, as defined in the source configuration |
| Status Cascade | The automatic propagation of a canonical record's status change to all descendant records in the hierarchy, exempting records already in Disabled state |
| Source Processing | The automated ingestion pipeline (FRD-NMD-0002) that creates or updates canonical records based on source configuration |

---

## 4. Business Context

**Parent PC Objectives Supported:** `OBJ-001`, `OBJ-002`, `OBJ-005`

The product canonical is the data foundation of NMD. Without a clean, maintained canonical, cross-source data linkage is impossible — every ingestion run, query, and export depends on resolving instrument identity against this table. This module eliminates the absence of a single authoritative product record that currently causes data inconsistency across internal systems.

---

## 5. Actors

| ID | Actor | Type | Role |
|----|-------|------|------|
| ACT-001 | Data Owner | Human (primary) | Creates, updates, and manages canonical records and status via the Operator UI |
| ACT-002 | Operator UI | Internal system (primary) | Exposes canonical management and query functions to data owners |
| ACT-003 | Data Ingestion Module | Internal system (primary) | Resolves ingested data against canonical records; auto-creates canonical records when processing data from a golden source |
| ACT-004 | Query & Export Module | Internal system (secondary) | Reads canonical records to enrich and serve downstream queries and exports |

---

## 6. Functional Overview

The Product Canonical module provides two core capabilities: (1) Canonical Management — full lifecycle management of instrument master records including creation, update, deactivation, status management, and audit trail; (2) Canonical Query — a read interface for all internal modules to resolve instrument identity by canonical key, source identifier, or attribute search.

---

## 7. Event Triggers

| ID | Trigger | Type | Initiates |
|----|---------|------|-----------|
| ET-001 | Data owner creates a new instrument record via UI | User action | FA-01: Canonical Maintenance |
| ET-002 | Data owner updates an existing canonical record | User action | FA-01: Canonical Maintenance |
| ET-003 | Data owner deactivates or retires an instrument | User action | FA-01: Canonical Maintenance |
| ET-004 | Data owner changes the status of a canonical record | User action | FA-01: Canonical Maintenance (status change + cascade) |
| ET-005 | Internal module requests canonical lookup by source identifier | System event | FA-02: Canonical Query |
| ET-006 | Internal module requests canonical lookup by canonical key | System event | FA-02: Canonical Query |
| ET-007 | Data owner searches canonical by attribute (exchange, commodity, product type, product code) | User action | FA-02: Canonical Query |
| ET-008 | Data Ingestion Module processes data from a golden source and encounters an instrument | System event | FA-01: Canonical Maintenance (auto-create or update) |

---

## 8. Functional Requirements

### FA-01: Product Canonical Maintenance

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-NMD-001-001 | System shall maintain a canonical entity table with 5 columns representing 4 hierarchical layers: Exchange (L1), Commodity (L2), Product Type + Product Code (L3 — Product), and Contract (L4) | Must | FR-001 | Canonical table exists with all 5 columns; all Phase 1 asset classes can be represented |
| FR-NMD-001-002 | System shall compute a deterministic canonical key as a hash of all 5 columns in fixed order, using null placeholders for skipped levels; the same 5-column input must always produce the same key | Must | FR-001 | Hash is reproducible across all callers; same 5-column values always produce identical key |
| FR-NMD-001-003 | The 4-layer structure shall be defined as: Exchange (primary trading venue), Commodity (underlying of the product), Product (type + code — the product published/traded on the exchange), Contract (additional contract identifier for derivatives) | Must | FR-001 | All 4 layers are present and correctly defined in the data model |
| FR-NMD-001-004 | Each asset class shall define its own mapping of the 5 columns and its supported product types; no asset class may reuse another's column mapping or product type definitions | Must | FR-001 | Phase 1 asset classes (Futures & Options, FX) each have distinct, non-overlapping column mappings and product type definitions |
| FR-NMD-001-005 | System shall support three canonical status values: Active (all reference data and daily updates imported), Inactive (reference data only), Disable (no data loaded) | Must | FR-001 | All three status values are supported; ingestion pipeline gates data loading by canonical status correctly |
| FR-NMD-001-006 | Canonical status shall be inherited top-down — a status change at a parent level shall trigger automatic status sync to all descendant records, except descendants already in Disabled state which remain unchanged | Must | FR-001 | Parent status change cascades correctly to all non-Disabled descendants; Disabled descendants are unaffected |
| FR-NMD-001-007 | Canonical status shall be manageable by: User (may set any record to any status, subject to parent constraints), or Source Processing (status defined by source configuration) | Must | FR-001 | Both User and Source Processing can set canonical status within defined rules |
| FR-NMD-001-008 | Canonical records shall be created by: User (manual creation via UI — bulk import not required in Phase 1), or Source Processing (auto-created as defined by source processing configuration) | Must | FR-001 | Both creation paths produce valid canonical records with correct initial status |
| FR-NMD-001-009 | System shall maintain a full audit trail of all canonical record changes — capturing who or what made the change, when, which field changed, old value, and new value | Must | FR-001 | Every canonical write produces an immutable audit log entry; no write path bypasses the audit trail |

### FA-02: Product Canonical Query

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-NMD-001-010 | System shall support lookup of a canonical record by canonical key (hash) | Must | FR-001 | Exact match by canonical key returns correct record or NOT_FOUND |
| FR-NMD-001-011 | System shall support lookup by source-specific identifier, returning the matching canonical record | Must | FR-001 | Source identifier resolves to correct canonical record across all Phase 1 asset classes |
| FR-NMD-001-012 | System shall support search by one or more attributes: Exchange, Commodity, Product Type, Product Code | Must | FR-001 | Attribute search returns all matching records; supports single and multi-attribute filter combinations |
| FR-NMD-001-013 | System shall return the full canonical record including all 5 hierarchy columns, canonical key, status, and audit metadata | Must | FR-001 | All required fields present in every query response |
| FR-NMD-001-014 | System shall return only Active canonical records by default; support optional filter to include Inactive and Disabled records | Should | FR-001 | Default query excludes Inactive and Disabled; optional filter correctly includes them |

---

## 9. Business Rules

| ID | Rule | Affects |
|----|------|---------|
| BRL-001 | Exchange is mandatory on every canonical record — no record may exist without an Exchange | FR-NMD-001-001 |
| BRL-002 | Canonical key is a deterministic hash of all 5 columns in fixed order; null placeholders used for skipped levels; same 5-column values always produce the same key | FR-NMD-001-002 |
| BRL-003 | Each asset class defines its own mapping of the 5 columns AND its supported product types; no asset class may reuse another's column mapping or product type definitions | FR-NMD-001-004 |
| BRL-004 | Status cascade is top-down: Exchange → Commodity → Product → Contract; a parent status change propagates to all descendants except children already in Disabled state — Disabled children are exempt from cascade and remain Disabled | FR-NMD-001-006 |
| BRL-005 | A child record's status may not be more permissive than its parent: child cannot be Active if parent is Inactive or Disabled; child cannot be Inactive if parent is Disabled | FR-NMD-001-006, FR-NMD-001-007 |
| BRL-006 | User may set any record to any status directly (subject to BRL-005); Source Processing may only set status as defined in its source configuration | FR-NMD-001-007 |
| BRL-007 | When Source Processing creates a canonical record, initial status is defined by the source configuration — not defaulted to Active | FR-NMD-001-008 |
| BRL-008 | Duplicate canonical records are not permitted — identical 5-column hash cannot be inserted twice | FR-NMD-001-001, FR-NMD-001-002 |
| BRL-009 | Audit trail entries are immutable — no audit record may be updated or deleted after creation | FR-NMD-001-009 |

---

## 10. Exception Scenarios

| ID | Trigger Condition | Expected Behaviour |
|----|-------------------|--------------------|
| EX-001 | Source Processing attempts to create a canonical record with a hash that already exists | Reject creation; return conflict error with existing record reference; do not update existing record |
| EX-002a | User attempts to set a child record to Active when parent is Inactive or Disabled | Reject; return validation error stating parent status constraint |
| EX-002b | User attempts to set a child record to Inactive when parent is Disabled | Reject; return validation error stating parent status constraint |
| EX-003 | Parent status change cascade encounters DB error mid-update | Roll back entire cascade; leave all records at previous status; alert operator. Note: children already in Disabled state not changing is expected behaviour — not a failure |
| EX-004 | Source Processing attempts to create a canonical record missing Exchange | Reject; return validation error; log failed attempt with source details |
| EX-005 | Canonical lookup by source-specific identifier returns no match | Return empty result with NOT_FOUND status code; do not auto-create |
| EX-006 | Hash collision — two distinct 5-column combinations produce the same hash | Log critical alert; block both records until resolved; never silently overwrite |

---

## 11. Module Interface

### APIs Provided

| API Name | Operations | Consumers |
|----------|------------|-----------|
| Canonical Management API | Create canonical record, Update canonical record, Deactivate canonical record, Change canonical status | Operator UI (FRD-NMD-0004), Data Ingestion Module (FRD-NMD-0002) |
| Canonical Query API | Lookup by canonical key, Lookup by source identifier, Search by attributes | Data Ingestion Module (FRD-NMD-0002), Query & Export Module (FRD-NMD-0003), Operator UI (FRD-NMD-0004) |

### Events Published

| Event | Trigger | Consumers |
|-------|---------|-----------|
| canonical.record.created | New canonical record created by User or Source Processing | FRD-NMD-0002 |
| canonical.record.updated | Canonical record fields updated | FRD-NMD-0002, FRD-NMD-0003 |
| canonical.status.changed | Status changed on any record including cascade-triggered changes | FRD-NMD-0002, FRD-NMD-0003 |

### Data Owned

| Entity | Ownership | Notes |
|--------|-----------|-------|
| Canonical Entity Table | FRD-NMD-0001 | Single authoritative table — all other modules are read-only consumers |
| Canonical Audit Log | FRD-NMD-0001 | Immutable; owned and written only by this module |

---

## 12. Cross-Module Interactions

| Dependency | Type | Purpose |
|------------|------|---------|
| Source Processing (FRD-NMD-0002) | Internal system | Provides source configuration — golden source flag, initial status on creation, types of ingestion feed |
| Operator UI (FRD-NMD-0004) | Internal system | Delivers user actions for canonical CRUD and status changes |

---

## 13. Data Requirements

| Entity | Operations | Sensitivity | Notes |
|--------|------------|-------------|-------|
| Canonical Record | Create, Read, Update | Internal | No hard delete — retirement via Disable status only |
| Canonical Audit Log | Create, Read | Internal | Immutable — no update or delete permitted |

**Data Retention:** Indefinite — canonical records and audit log are permanent; no purge policy

---

## 14. Non-Functional Requirements

| ID | Requirement | Source NFR |
|----|-------------|------------|
| NFR-NMD-001-001 | Canonical query response time shall meet the platform latency target (TBD, e.g., <100ms p95) — this is a hot path called by every ingestion run | PC NFR-004 |
| NFR-NMD-001-002 | Status cascade on a large parent (e.g., disabling an Exchange with thousands of descendants) shall complete within a defined SLA window without blocking canonical queries | PC NFR-001 |
| NFR-NMD-001-003 | Canonical record writes and status changes shall be transactional — partial updates are not permitted | PC NFR-003 |
| NFR-NMD-001-004 | Canonical data is the cross-module golden source — read access available to all internal modules; write access restricted to authorised users and Source Processing only | PC NFR-005 |
| NFR-NMD-001-005 | All canonical data at rest shall be encrypted | PC NFR-007 |
| NFR-NMD-001-006 | All canonical writes shall be captured in the audit log — no write path may bypass the audit trail | PC NFR-003 |

---

## 15. Traceability Matrix

| PC Requirement | FRD Requirements | Downstream |
|----------------|------------------|------------|
| FR-001 | FR-NMD-001-001, FR-NMD-001-002, FR-NMD-001-003, FR-NMD-001-004, FR-NMD-001-005, FR-NMD-001-006, FR-NMD-001-007, FR-NMD-001-008, FR-NMD-001-009, FR-NMD-001-010, FR-NMD-001-011, FR-NMD-001-012, FR-NMD-001-013, FR-NMD-001-014 | PSD, DC, UT |
| PC NFR-002 | NFR-NMD-001-002 | NFTS |
| PC NFR-003 | NFR-NMD-001-003, NFR-NMD-001-006 | NFTS |
| PC NFR-004 | NFR-NMD-001-001 | NFTS |
| PC NFR-005 | NFR-NMD-001-004 | HLD, NFTS |
| PC NFR-007 | NFR-NMD-001-005 | DBAD, NFTS |

---

## 16. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-001 | Canonical entity table supports all 5 columns across all Phase 1 asset classes (Futures & Options, FX) with correct column mappings |
| AC-002 | Canonical key hash is deterministic — same 5-column input always produces the same key across all callers |
| AC-003 | Status cascade correctly propagates to all descendants on parent status change; Disabled children remain unchanged |
| AC-004 | User status constraint violations (EX-002a, EX-002b) are rejected with correct error responses |
| AC-005 | All canonical writes produce an immutable audit log entry with full field-level change detail |
| AC-006 | Canonical query API returns correct results for lookup by key, lookup by source identifier, and attribute search |
| AC-007 | Canonical query returns Active records only by default; Inactive and Disabled records returned only when explicitly requested |
| AC-008 | Source Processing auto-creation applies initial status from source configuration — never defaults to Active |
| AC-009 | Duplicate canonical records (same hash) are rejected by both User and Source Processing creation paths |
| AC-010 | All canonical data at rest is encrypted; write access restricted to authorised users and Source Processing |

---

## 17. Assumptions & Constraints

### Assumptions

| ID | Assumption |
|----|------------|
| ASM-001 | Asset class column mappings for Futures & Options and FX will be defined before detailed design begins |
| ASM-002 | Hash algorithm selection (e.g., SHA-256, MD5, MurmurHash) will be agreed upon before implementation — all modules must use the same algorithm |
| ASM-003 | Source Processing (FRD-NMD-0002) will define and own the golden source flag and initial status configuration — this module consumes that configuration |
| ASM-004 | No bulk import is required for Phase 1 — data owners create canonical records manually or via Source Processing |

### Constraints

| ID | Constraint |
|----|------------|
| CON-001 | Phase 1 asset classes: Futures & Options and FX only |
| CON-002 | No hard deletes — canonical records are permanent; retirement via Disable status only |
| CON-003 | Write access to canonical table restricted to this module only — all other modules are read-only consumers |

---

## 18. Dependencies

| ID | Dependency |
|----|------------|
| DEP-001 | FRD-NMD-0002 (Source Processing) — must define source configuration schema (golden source flag, initial status, ingestion feed types) before canonical module design is finalised |
| DEP-002 | Asset class mapping definitions for Phase 1 (Futures & Options, FX) — required before canonical table schema can be finalised |
| DEP-003 | Hash algorithm agreed across all NMD modules — canonical key computation must be consistent platform-wide |

---

## 19. Open Issues

| ID | Issue |
|----|-------|
| OI-001 | Hash algorithm not yet selected — impacts canonical key computation across all modules |
| OI-002 | Asset class column mappings for Phase 1 not yet defined — impacts table schema and validation rules |
| OI-003 | Specific exchange(s) for Futures & Options Phase 1 not yet confirmed — impacts asset class mapping |

---

## 20. Approvals

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Leo | TBD | TBD |
| Reviewer | TBD | TBD | TBD |
| Approver | TBD | TBD | TBD |

---

## Change Log

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v0.1 | 2026-03-01 | Leo | Initial draft |
