# FRD-NMD-0002: Multi-Source Ingestion, Normalization & Query

| Field              | Value                                                        |
|--------------------|--------------------------------------------------------------|
| Document ID        | FRD-NMD-0002                                                 |
| Module Code        | ING                                                          |
| Title              | Multi-Source Ingestion, Normalization & Query                |
| Version            | v0.2                                                         |
| Status             | Draft                                                        |
| Classification     | Internal                                                     |
| Created Date       | 2026-03-01                                                   |
| Last Updated       | 2026-03-01                                                   |
| Author             | Leo                                                          |
| Reviewer           | TBD                                                          |
| Approver           | TBD                                                          |
| Parent BRD         | PC-NMD-0001                                                  |
| Related Documents  | FRD-NMD-0001                                                 |
| Tags               | market-data, ingestion, normalization, query-api, scd-type-2, reprocessing |
| Supersedes         |                                                              |

---

## 1. Overview

**Summary:** The ING module handles ingestion of reference data and daily updates from multiple external source types, generates derived sources, normalizes data against the product canonical, and exposes query/export APIs for downstream consumption. It is the operational core of NMD — everything between source and consumer.

**Purpose:** This document specifies the functional requirements for the Multi-Source Ingestion, Normalization & Query module within the Narwhal Market Data platform. It translates PC-NMD-0001 requirements FR-002 through FR-008 and FR-010 into detailed, testable specifications.

**Audience:** Developers, QA engineers, data owners, and downstream system integrators.

---

## 2. Scope

### In Scope

1. Source onboarding — configuring and registering new data sources via common framework (FR-010)
2. Reference data ingestion — product static, contracts, with SCD Type 2 persistence (FR-002)
3. Daily update ingestion — settlement prices, margin rates, corporate actions per business date (FR-003)
4. Multi-source type support — exchange websites, public APIs, SFTP, structured documents, data feeds (FR-004)
5. Derived source processing — transform and reshape already-ingested data for customized export formats (FR-005)
6. Data normalization, mapping control, and validation linked to product canonical (FR-006)
7. Centralized ingestion framework — scheduling, run tracking, snapshot persistence (FR-007)
8. Reprocessing — authorized re-ingestion with delta versioning for corrections
9. Settlement history — versioned daily updates with business date tagging
10. Query and export APIs for downstream system consumption (FR-008)

### Out of Scope

1. Product canonical maintenance (covered by FRD-NMD-0001)
2. UI for data owners to manage sources, ingestion, and data (FR-009)
3. Real-time streaming and subscription-based data delivery (Phase 3)
4. Direct integration or data delivery to downstream systems (Phase 2)
5. Equities (Phase 2)
6. Fixed income and structured products (Phase 3)

---

## 3. Definitions

| Term | Definition |
|------|------------|
| Snapshot | A point-in-time extract of data from one or more sources, used as input to the normalization pipeline. |
| Derived Source | A source that transforms and reshapes already-ingested data from one or more upstream sources into customized export formats, rather than pulling from an external system. Constructed by parsing source data in a configured step sequence where later steps override earlier values. |
| Ingestion Framework | The centralized component that manages, schedules, tracks, and monitors the processing of all data sources. |
| Source Adapter | A pluggable component that handles connectivity and parsing for a specific source type (e.g., SFTP, REST API, website scraper). |
| SCD Type 2 | Slowly Changing Dimension Type 2 — a persistence pattern that tracks changes over time using effective_date / expiry_date ranges. A new record version is created when content changes; the previous version is expired, not overwritten. |
| Reprocessing | Authorized re-ingestion of a source for a given business date, triggered when corrections or restatements are received. Increments the version and persists only delta records. |
| Delta Record | A record persisted during reprocessing that contains only the changed values compared to the previous version for the same business date. |
| Business Date | The trading or valuation date to which a daily update record belongs, as opposed to the calendar date when the data was ingested. |
| Composite Key | The combination of source, entity, and record_type used to identify a unique record for SCD Type 2 change detection in reference data. |
| Active Layer (Reference Data) | Storage tier containing current, non-expired SCD Type 2 reference data records. This is the data served by the query API. |
| Active Layer (Daily Updates) | Storage tier containing daily update records from the last 7 days, latest version per business date. This is the data served by the query API. |
| Archive Layer (Reference Data) | Separate database containing expired SCD Type 2 reference data records. Retained for audit and historical queries. |
| Archive Layer (Daily Updates) | Separate database containing superseded daily update versions and daily update records older than 7 days before the current day snapshot. Retained for audit and historical queries. |

---

## 4. Business Context

**Parent PC Objectives Supported:** `{'id': 'OBJ-001', 'description': 'Eliminate vendor feed dependencies', 'supported_by': ['FR-002', 'FR-003', 'FR-004']}`, `{'id': 'OBJ-002', 'description': 'Single authoritative data source', 'supported_by': ['FR-005', 'FR-006']}`, `{'id': 'OBJ-003', 'description': 'Reduce onboarding time', 'supported_by': ['FR-007', 'FR-010']}`, `{'id': 'OBJ-004', 'description': 'Normalized, queryable API', 'supported_by': ['FR-008']}`

This module delivers on the core NMD value proposition — eliminating direct vendor/exchange dependencies by centralizing ingestion and normalization. It provides a single, authoritative pipeline from external data sources to normalized, queryable data for downstream consumption.

---

## 5. Actors

| ID | Actor | Type | Role |
|----|-------|------|------|
|  | Ingestion Framework | System | Primary |
|  | External Data Source | External | External |
|  | Product Canonical | System | Secondary |
|  | Downstream System | System | Secondary |
|  | Data Owner | Human | Secondary |

---

## 6. Functional Overview

It automates collection, validation, and normalization of reference data and daily updates to the canonical entity. It also supports derived sources that transform and reshape already-ingested data for customized export formats.

The module processes two distinct data categories that share the same source adapter framework, scheduling, and validation approach, but differ in persistence and retention behavior:

Reference Data — Static or semi-static product attributes such as contract specifications, multipliers, and payment methods. Reference data is persisted using SCD Type 2 with date ranges (effective_date / expiry_date). A new snapshot is created only when content changes for the same composite key (source, entity, record_type). Expired records are retained in another database for reference.

Daily Updates — Settlement prices, margin rates, and corporate actions received per business date. Daily update records are tagged to a specific business date with a version starting at 1. When corrections arrive via authorized reprocessing, the version increments and only delta records (changed values) are persisted in the new version. Older versions are retained in another database for reference. Records of dates a week before the current day snapshot will also be moved to that database.

The module covers: source onboarding, scheduling, run tracking, normalization, mapping control, snapshot persistence, validation, daily update ingestion and validation, settlement history, reprocessing, derived source processing, and query.

---

## 7. Event Triggers

| ID | Trigger | Type | Initiates |
|----|---------|------|-----------|
| ET-001 | Scheduled ingestion run (e.g. daily EOD) | Scheduled | FR-ING-007, FR-ING-008, FR-ING-010, FR-ING-011, FR-ING-012 — pull from configured sources |
| ET-002 | Manual ingestion trigger by data owner | User action | FR-ING-007, FR-ING-008, FR-ING-010, FR-ING-011, FR-ING-012 — on-demand pull for specific source |
| ET-003 | Source file/data available (e.g. SFTP file landed) | External signal | FR-ING-007, FR-ING-008, FR-ING-010, FR-ING-011, FR-ING-012 — event-driven ingestion |
| ET-004 | Ingestion complete | System event | FR-ING-014, FR-ING-015, FR-ING-016 — triggers normalization and snapshot derivation |
| ET-005 | Downstream system query request | System event | FR-ING-024 through FR-ING-028 — API serves normalized data |
| ET-006 | Authorized reprocessing request for a source and business date | User action | FR-ING-032 — re-ingest with version increment, delta persistence |
| ET-007 | Daily retention window shift (current day advances) | Scheduled | FR-ING-039 — move daily update records older than 7 days to archive DB |
| ET-008 | SCD Type 2 expiry detected during reference data ingestion | System event | FR-ING-037 — move expired reference records to archive DB |

---

## 8. Functional Requirements

### Source Connectivity

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-001 | System shall support ingestion from exchange websites via HTTP/HTTPS | Must |  | At least one exchange website source adapter successfully ingests data |
| FR-ING-002 | System shall support ingestion from public APIs (REST/JSON) | Must |  | At least one REST API source adapter successfully ingests data |
| FR-ING-003 | System shall support ingestion from SFTP file drops | Must |  | SFTP adapter connects, detects new files, and ingests successfully |
| FR-ING-004 | System shall support ingestion from structured documents (CSV, XML, PDF) | Must |  | Document adapter parses CSV, XML, and PDF formats and extracts data correctly |
| FR-ING-005 | System shall support ingestion from data feeds | Must |  | Feed adapter connects and ingests data from at least one feed source |
| FR-ING-006 | Each source type shall be handled by a pluggable source adapter with a common interface | Must |  | New source adapter can be added without modifying core ingestion framework code |

### Source Onboarding

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-029 | System shall support onboarding of new data sources via a common framework without changes to core ingestion logic | Should |  | New source onboarded and producing data without code changes to core framework |
| FR-ING-030 | System shall provide a source configuration interface to define connection details, schedule, mapping rules, and validation rules per source | Must |  | Source configuration created with all required fields; source activates on schedule |
| FR-ING-031 | System shall validate source configuration before activating a new source for scheduled ingestion | Must |  | Invalid configuration rejected with clear error; source not activated until valid |

### Reference Data Ingestion

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-007 | System shall ingest product static data (contract specs, tick sizes, lot sizes) from configured sources | Must |  | Product static data ingested and stored as versioned source snapshot |
| FR-ING-008 | System shall ingest contract listings (expiry dates, series, strike prices) from configured sources | Must |  | Contract listings ingested and stored as versioned source snapshot |
| FR-ING-009 | System shall persist ingested reference data using SCD Type 2 with effective_date / expiry_date ranges. A new snapshot is created only when content changes for the same composite key (source, entity, record_type) | Must |  | Unchanged records do not generate new versions; changed records create new SCD Type 2 entry with correct date ranges |

### Daily Update Ingestion

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-010 | System shall ingest daily settlement prices from configured sources | Must |  | Settlement prices ingested with correct business date and version tagging |
| FR-ING-011 | System shall ingest margin rates from configured sources | Must |  | Margin rates ingested and stored as dated source snapshot |
| FR-ING-012 | System shall ingest corporate events from configured sources | Must |  | Corporate events ingested and stored as dated source snapshot |
| FR-ING-013 | System shall tag daily update records to a specific business date with a version starting at 1. When corrections arrive via authorized reprocessing, the version increments and only delta records (changed values) are persisted in the new version | Must |  | Version increments on reprocessing; only changed values persisted in new version; previous versions retained in archive |
| FR-ING-032 | System shall support authorized reprocessing of a source for a given business date, incrementing the version and persisting only delta records | Must |  | Reprocessing creates new version with only delta records; requires authorization |
| FR-ING-033 | System shall maintain settlement history — all versions of daily updates per business date queryable for audit | Must |  | All versions of a daily update for a given business date retrievable via API or archive query |

### Derived Source Processing

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-014 | System shall support derived sources that transform and reshape already-ingested data from upstream sources into customized export formats, constructed by parsing source data in a configured step sequence where later steps override earlier values | Must |  | Derived source produces correct output from upstream ingested data in configured step order |

### Normalization & Validation

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-015 | System shall normalize ingested data to a standard internal format | Must |  | Output data conforms to internal schema regardless of source format |
| FR-ING-016 | System shall link each normalized record to its corresponding product canonical record | Must |  | Every normalized record carries a canonical record ID or is flagged as unmatched |
| FR-ING-017 | System shall flag records that cannot be matched to a canonical record for manual review | Must |  | Unmatched records visible with unmatched status; data owner can review and resolve |
| FR-ING-034 | System shall provide mapping control to define field-level transformation and normalization rules per source | Must |  | Mapping rules applied during normalization; field transformations produce expected output |
| FR-ING-035 | System shall validate ingested data against configured validation rules before persistence | Must |  | Records failing validation are flagged and not persisted to active layer |

### Ingestion Framework

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-018 | System shall provide a centralized registry of all configured data sources | Must |  | Source registry lists all configured sources with connection details and schedules |
| FR-ING-019 | System shall support scheduled ingestion runs (configurable per source) | Must |  | Scheduled runs execute at configured times without manual intervention |
| FR-ING-020 | System shall support manual on-demand ingestion for a specific source | Must |  | Data owner can trigger ingestion for a specific source and monitor its progress |
| FR-ING-021 | System shall detect source file availability and trigger ingestion automatically | Must |  | File landing on SFTP or equivalent triggers ingestion within configured detection interval |
| FR-ING-022 | System shall track ingestion run status (pending, running, completed, failed) per source | Must |  | Run status queryable in real time; historical runs retained |
| FR-ING-023 | System shall log all ingestion activity with source, timestamp, record counts, and outcome | Must |  | Audit log contains source ID, run timestamp, records processed, records failed, and final outcome |

### Query & Export API

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-024 | System shall expose a query API to retrieve normalized reference data by instrument, product type, or exchange | Must |  | API returns correct reference data filtered by requested parameters |
| FR-ING-025 | System shall expose a query API to retrieve daily settlement prices by instrument and date/date range | Must |  | API returns correct settlement prices for requested instrument and date range |
| FR-ING-026 | System shall expose a query API to retrieve margin rates by instrument and date | Must |  | API returns correct margin rates for requested instrument and date |
| FR-ING-027 | System shall support bulk export of normalized data as file download (CSV/JSON) | Should |  | Bulk export generates downloadable file in requested format with correct data |
| FR-ING-028 | System shall support filtering, pagination, and sorting on all query endpoints | Must |  | All query endpoints accept filter, page, page_size, and sort parameters and return correct results |
| FR-ING-036 | System shall support query of archived data (expired reference records, older daily update versions and dates) from the archive database | Should |  | Archive query returns correct historical data from the archive database |

### Data Retention

| ID | Requirement | Priority | Traces To | Acceptance Criteria |
|----|-------------|----------|-----------|---------------------|
| FR-ING-037 | System shall move expired SCD Type 2 reference data records to the archive database | Must |  | Expired reference records no longer in active DB; present in archive DB |
| FR-ING-038 | System shall move superseded daily update versions to the archive database | Must |  | Only latest version per business date remains in active DB; older versions in archive DB |
| FR-ING-039 | System shall move daily update records older than 7 days before the current day snapshot to the archive database | Must |  | Active DB contains only last 7 days of daily updates; older records in archive DB |

---

## 9. Business Rules

| ID | Rule | Affects |
|----|------|---------|
| BRL-001 | A source snapshot must be fully ingested before normalization begins — no partial processing | FR-ING-014, FR-ING-015 |
| BRL-002 | Derived sources transform already-ingested data by parsing in a configured step sequence — each step overlays the previous, so later steps override earlier values for the same field. Derived sources use the same adapter framework as external sources. | FR-ING-014 |
| BRL-003 | Daily update records are tagged to a business date with version starting at 1. Corrections via authorized reprocessing increment the version; only delta records (changed values) are persisted in the new version. Older versions are retained in the archive database. | FR-ING-013, FR-ING-032, FR-ING-038 |
| BRL-004 | Normalization must not create or modify product canonical records — only link to existing ones | FR-ING-016 |
| BRL-005 | Ingestion runs for the same source must not execute concurrently — queue or reject if already running | FR-ING-019, FR-ING-020, FR-ING-021 |
| BRL-006 | All API query results return data from the latest completed normalization run only — in-progress data is never exposed | FR-ING-024, FR-ING-025, FR-ING-026 |
| BRL-007 | Reference data changes are detected by comparing incoming data against the current active record for the same composite key (source, entity, record_type). A new SCD Type 2 record is created only when content differs — unchanged records do not generate new versions. | FR-ING-009 |
| BRL-008 | Reprocessing requires explicit authorization — the system shall not allow ad-hoc re-ingestion without a controlled trigger. | FR-ING-032 |
| BRL-009 | Daily update records older than 7 days before the current day snapshot are moved to the archive database. This retention window applies per business date, not per ingestion date. | FR-ING-039 |

---

## 10. Exception Scenarios

| ID | Trigger Condition | Expected Behaviour |
|----|-------------------|--------------------|
| EXC-001 | External source unavailable (connection failure, timeout) |  |
| EXC-002 | Source file format changed (unexpected schema/columns) |  |
| EXC-003 | Record cannot be matched to a canonical record during normalization |  |
| EXC-004 | Duplicate ingestion run triggered (same source, same schedule window) |  |
| EXC-005 | Source returns empty dataset (zero records) |  |
| EXC-006 | Reprocessing requested without authorization |  |
| EXC-007 | Reprocessing produces zero delta records (no changes detected) |  |
| EXC-008 | Archive DB unavailable when retention move triggered |  |
| EXC-009 | SCD Type 2 change detection fails (composite key mismatch or corrupt data) |  |

---

## 11. Module Interface

### APIs Provided

| API Name | Operations | Consumers |
|----------|------------|-----------|
| Query Reference Data | Retrieve normalized reference data by instrument, product type, or exchange | Downstream systems |
| Query Settlement Prices | Retrieve settlement prices by instrument and date/date range | Downstream systems |
| Query Margin Rates | Retrieve margin rates by instrument and date | Downstream systems |
| Bulk Export | Download normalized data as CSV/JSON | Downstream systems |
| Ingestion Status | Query ingestion run status per source | Data owner, UI (FR-009) |
| Archive Query | Retrieve expired reference records, older daily update versions and dates from archive database | Downstream systems, Data owner |

### Events Published

| Event | Trigger | Consumers |
|-------|---------|-----------|
|  | Ingestion run finishes (success or failure) |  |
|  | Normalization run finishes |  |
|  | Records failed canonical matching |  |

### Data Owned

| Entity | Ownership | Notes |
|--------|-----------|-------|
| Reference Data Record | ING | SCD Type 2 records; active in main DB, expired in archive DB |
| Daily Update Record | ING | Business-date-tagged with versioning; last 7 days active, older in archive DB |
| Derived Source Output | ING | Output of derived source processing |
| Normalized Record | ING | Linked to canonical, serves query API |
| Ingestion Run Log | ING | Operational audit trail |

---

## 12. Cross-Module Interactions

| Dependency | Type | Purpose |
|------------|------|---------|
|  |  | Linking normalized data to master records (FR-ING-016) |
|  |  | Input to ingestion pipeline |

---

## 13. Data Requirements

| Entity | Operations | Sensitivity | Notes |
|--------|------------|-------------|-------|
| Reference Data Record | CRU | Internal | SCD Type 2 records with effective_date / expiry_date. Active records in main DB, expired records moved to archive DB |
| Daily Update Record | CR | Internal | Business-date-tagged records with version counter. Latest 7 days in active DB, older records and superseded versions moved to archive DB |
| Derived Source Output | CR | Internal | Output of derived source processing, reshaping ingested data for export formats |
| Normalized Record | CRU | Internal | Linked to canonical, serves query API |
| Ingestion Run Log | CR | Internal | Operational audit trail for all ingestion activity |
| Source Configuration | CRUD | Internal | Source registry, connection details, schedules, mapping rules, validation rules, step sequences |
| Unmatched Record | CR | Internal | Flagged for data owner review during normalization |

**Data Retention:** Two-tier storage with separate retention behavior per data category:

Reference Data:
  Active DB — current, non-expired SCD Type 2 records (latest effective version per composite key).
  Archive DB — expired SCD Type 2 records, retained for audit and historical queries.

Daily Updates:
  Active DB — records from the last 7 days (latest version per business date).
  Archive DB — superseded versions and records older than 7 days before current day snapshot.

Both archive databases are queryable via FR-ING-036.

---

## 14. Non-Functional Requirements

| ID | Requirement | Source NFR |
|----|-------------|------------|
| NFR-ING-001 | Daily settlement file processing must complete within SLA window (ref NFR-001: T+1 by 08:00) | Performance |
| NFR-ING-002 | Query API responses must meet latency target (ref NFR-004: <500ms p95) | Performance |
| NFR-ING-003 | All ingested data must be traceable to its source with full audit log (ref NFR-003) | Data Integrity |
| NFR-ING-004 | Ingestion failures must trigger operational alerts (ref NFR-008) | Observability |
| NFR-ING-005 | Source adapter addition must not require changes to core ingestion framework (ref NFR-006) | Maintainability |

---

## 15. Traceability Matrix

| PC Requirement | FRD Requirements | Downstream |
|----------------|------------------|------------|
| FR-002 | FR-ING-007, FR-ING-008, FR-ING-009 | PSD, DC, UT |
| FR-003 | FR-ING-010, FR-ING-011, FR-ING-012, FR-ING-013, FR-ING-032, FR-ING-033, FR-ING-038, FR-ING-039 | PSD, DC, UT |
| FR-004 | FR-ING-001, FR-ING-002, FR-ING-003, FR-ING-004, FR-ING-005, FR-ING-006 | PSD, AEC, UT |
| FR-005 | FR-ING-014 | PSD, DC, UT |
| FR-006 | FR-ING-015, FR-ING-016, FR-ING-017, FR-ING-034, FR-ING-035, FR-ING-037 | PSD, DC, UT |
| FR-007 | FR-ING-018, FR-ING-019, FR-ING-020, FR-ING-021, FR-ING-022, FR-ING-023 | PSD, UT |
| FR-008 | FR-ING-024, FR-ING-025, FR-ING-026, FR-ING-027, FR-ING-028, FR-ING-036 | API, UT |
| FR-010 | FR-ING-029, FR-ING-030, FR-ING-031 | PSD, UT |

---

## 16. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-001 | At least one source adapter successfully ingests reference data and daily updates from an external source |
| AC-002 | Derived source processing produces correct output from upstream ingested data in configured step order |
| AC-003 | All normalized records are linked to a canonical record or flagged as unmatched |
| AC-004 | Query API returns normalized data with <500ms p95 latency |
| AC-005 | Ingestion framework tracks run status and logs all activity with full source traceability |
| AC-006 | Settlement price versioning works correctly — multiple intraday updates tracked via delta versioning, latest tagged |
| AC-007 | All nine exception scenarios (EXC-001 through EXC-009) behave as specified |
| AC-008 | SCD Type 2 persistence works correctly — new versions created only on content change, expired records moved to archive |
| AC-009 | Reprocessing creates new version with delta records only when authorized |
| AC-010 | Data retention operates correctly — daily updates older than 7 days moved to archive DB |
| AC-011 | New source can be onboarded via configuration without changes to core ingestion logic |

---

## 17. Assumptions & Constraints

### Assumptions

| ID | Assumption |
|----|------------|
| ASM-001 | Exchange files for Futures and Options and FX are accessible via public or permissioned sources (SFTP, website, API) |
| ASM-004 | Exchange selection for Futures and Options will be confirmed before detailed design begins |

### Constraints

| ID | Constraint |
|----|------------|
| CON-002 | Data types limited to Futures and Options and FX in Phase 1 |
| CON-003 | Exchange selection for Futures and Options TBC |

---

## 18. Dependencies

| ID | Dependency |
|----|------------|
| DEP-001 | Exchange or official source access credentials or agreements for Futures and Options (TBC) |
| DEP-002 | Confirmation of target exchanges for Phase 1 Futures and Options data |
| DEP-ING-001 | Product Canonical module (FRD-NMD-0001) operational for normalization linking |

---

## 19. Open Issues

No open issues.

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
| v0.2 | 2026-03-01 | Leo | Major update: revised functional overview with two-category data model (reference data with SCD Type 2, daily updates with delta versioning). Added source onboarding (FR-010), reprocessing, derived source processing, mapping control, validation, data retention rules, and archive query. Total requirements increased from 28 to 39. Added 4 new exception scenarios, 3 new business rules, 3 new event triggers. |
