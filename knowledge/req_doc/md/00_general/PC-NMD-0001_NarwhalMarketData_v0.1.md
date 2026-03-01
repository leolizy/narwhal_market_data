# PC-NMD-0001: Narwhal Market Data

## Metadata

| Field | Value |
|-------|-------|
| Document ID | PC-NMD-0001 |
| Title | Narwhal Market Data |
| Version | v0.1 |
| Status | Draft |
| Classification | Internal |
| Created Date | 2026-03-01 |
| Last Updated | 2026-03-01 |
| Author | Leo |
| Reviewer | TBD |
| Approver | TBD |
| Business Sponsor | TBD |
| Tags | market-data, sell-side, fintech |

## Executive Summary

Narwhal Market Data (NMD) is a centralized data gateway for sell-side financial market operations.
It automates reference data collection from multiple sources, ingests daily settlement prices, and
provides standardized query APIs to downstream systems — reducing duplication, improving data
consistency, and strengthening operational resilience through a shared enterprise-grade platform.
Phase 1 delivers a SILO service with the core functional flow: product canonical maintenance,
multi-source snapshot import, data normalization, and query/export APIs.

## Problem Statement

Multiple internal systems independently pull from external market data vendors and exchanges
directly. There is no centralized ingestion layer, causing reference data, settlement prices,
and margin inputs to be duplicated across systems. Onboarding a new data feed requires extensive
human effort and project arrangements to deploy changes across all systems. There is no single
authoritative product canonical, leading to data inconsistency and operational fragility.

## Objectives

| ID | Objective | Success Measure |
|----|-----------|-----------------|
| OBJ-001 | Eliminate dependency on market data vendors by processing exchange files and data directly for internal systems | Zero vendor feed dependencies for covered data types in Phase 1 |
| OBJ-002 | Provide a single authoritative source for reference data, settlement prices, and margin inputs | All consuming systems source from NMD, not external vendors |
| OBJ-003 | Reduce time to onboard a new consuming system and support a new data feed | Target onboarding time TBD — baseline to be measured in Phase 1 |
| OBJ-004 | Deliver a normalized, queryable data API for downstream system consumption | API available with documented endpoints for all Phase 1 data types |
| OBJ-005 | Establish Phase 1 SILO service as the foundation for future enhancements | Phase 1 delivered; architecture supports plugging in SSO, integrations, and multi-system features in future phases |

## Scope

### In Scope

- Product canonical maintenance
- Multi-source snapshot import and generation — reference data (product static, contracts) and
  daily updates (settlement prices, margin rates, corporate events)
- External official source ingestion: exchange websites, rulebooks, public APIs, documents, SFTP
  files, feeds, and any integratable system
- Derived snapshot generation from multiple external sources
- Data normalization and clean-up pipeline linking to product canonical
- Centralized market data ingestion framework to manage and track all source processing
- Query and export APIs for downstream system consumption
- Simple UI for data owners to manage sources, ingestion, and data
- Phase 1 data types: Futures and Options (exchange TBC), FX

### Out of Scope

- Any processing outside market data management
- Direct integration or data delivery to downstream systems (Phase 2)
- Equities (Phase 2)
- Fixed income and structured products (Phase 3)
- SSO integration (Phase 3)
- Real-time streaming and subscription-based data delivery (Phase 3)

### Domain Definitions

| Term | Definition |
|------|-----------|
| Phase 1 | SILO service delivering core functional flow: product canonical, multi-source ingestion, normalization, query/export APIs, and operator UI |
| Phase 2 | Extends Phase 1 with equities data types and direct downstream system integration/data delivery |
| Phase 3 | Extends Phase 2 with fixed income, structured products, SSO, and real-time streaming subscription delivery |

## Stakeholders

| Role | Party | Interest |
|------|-------|----------|
| Author / Delivery Lead | Leo | Building and delivering the platform |
| Data Owner / Operator | Internal team (TBD) | Operates the UI, manages ingestion sources, and validates output data |
| Downstream System | Internal systems (TBD) | Queries normalized data via API or file export |
| Business Sponsor | TBD | Funds and approves the initiative |
| External Data Source | Exchanges and vendors (TBD) | Provides raw market data |

## Current State

- Multiple internal systems independently pull from external market data vendors and exchanges directly
- No centralized ingestion layer
- Reference data, settlement prices, and margin inputs are duplicated across systems
- Onboarding a new data feed requires extensive human effort and project arrangements to deploy
  changes across all systems
- No single authoritative product canonical

## Future State

**Vision:** NMD acts as the single gateway for all market data, providing a centralized,
authoritative, and normalized data platform for sell-side financial operations.

**Target Outcomes:**

- Data owners manage sources and ingestion via a simple UI
- Downstream systems query clean, normalized data via standardized APIs or file delivery (TBD)
- New feeds and consuming systems can be onboarded through a common framework
- Phase 1 covers Futures and Options and FX; roadmap established for Phases 2 and 3

## Requirements

### Functional Requirements

| ID | Requirement | Priority | Objectives |
|----|-------------|----------|-----------|
| FR-001 | System shall maintain a product canonical (master record for each instrument) | Must | OBJ-001, OBJ-002 |
| FR-002 | System shall ingest reference data (product static, contracts) from external sources | Must | OBJ-001 |
| FR-003 | System shall ingest daily updates (settlement prices, margin rates, corporate events) from external sources | Must | OBJ-001 |
| FR-004 | System shall support multiple source types: exchange websites, public APIs, SFTP, documents, feeds, and any integratable system | Must | OBJ-001 |
| FR-005 | System shall generate derived snapshots from multiple external sources | Must | OBJ-002 |
| FR-006 | System shall normalize and clean ingested data, linking it to the product canonical | Must | OBJ-002 |
| FR-007 | System shall provide a centralized ingestion framework to manage and track all source processing | Must | OBJ-003 |
| FR-008 | System shall expose query and export APIs for downstream system consumption | Must | OBJ-004 |
| FR-009 | System shall provide a simple UI for data owners to manage sources, ingestion, and data | Must | OBJ-004 |
| FR-010 | System shall support onboarding of new data feeds via a common framework without changes to core ingestion logic | Should | OBJ-003 |

### Non-Functional Requirements

| ID | Requirement | Priority | Category |
|----|-------------|----------|----------|
| NFR-001 | System shall process and normalize daily settlement files within a defined SLA window (e.g., T+1 by 08:00) | Must | Performance |
| NFR-002 | System shall be available during market data processing hours with a defined uptime target (e.g., 99.5%) | Must | Availability |
| NFR-003 | All ingested data shall be traceable to its source with a full audit log | Must | Data Integrity |
| NFR-004 | API responses for query endpoints shall meet a defined latency target (e.g., <500ms p95) | Should | Performance |
| NFR-005 | System shall enforce access control — data owners vs read-only downstream consumers | Must | Security |
| NFR-006 | System shall support addition of new data sources without changes to core framework | Should | Maintainability |
| NFR-007 | All data in transit and at rest shall be encrypted | Must | Security |
| NFR-008 | System shall provide operational monitoring and alerting for ingestion failures | Must | Observability |
| NFR-009 | Phase 1 shall be deployable as a standalone SILO service with no SSO or cross-system dependencies | Must | Portability |

### Constraints

| ID | Constraint |
|----|-----------|
| CON-001 | Phase 1 is a SILO service — no SSO, no downstream system integrations |
| CON-002 | Data types limited to Futures and Options and FX in Phase 1 |
| CON-003 | Exchange selection for Futures and Options TBC |
| CON-004 | Downstream system specifics TBD |

## Assumptions and Constraints

### Assumptions

| ID | Assumption |
|----|-----------|
| ASM-001 | Exchange files for Futures and Options and FX are accessible via public or permissioned sources (SFTP, website, API) |
| ASM-002 | Data owners will be available to operate the UI and validate ingested data |
| ASM-003 | Downstream systems will integrate via query API or file export — no push delivery required in Phase 1 |
| ASM-004 | Exchange selection for Futures and Options will be confirmed before detailed design begins |
| ASM-005 | Phase 1 is a standalone SILO — no dependency on enterprise SSO or authentication systems |

## Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|-----------|
| RSK-001 | Exchange file formats change without notice, breaking ingestion pipelines | Medium | High | Build source adapters with schema versioning; monitor for format changes |
| RSK-002 | Exchange selection for Phase 1 delayed, blocking data source design | Medium | High | Confirm exchanges early; use FX as initial development target to unblock progress |
| RSK-003 | Downstream system requirements unclear, leading to API redesign | Medium | Medium | Define API contract early; validate with at least one consuming system before Phase 1 delivery |
| RSK-004 | Single operator dependency — if data owner is unavailable, ingestion stalls | Low | High | Document operational runbook; build alerting so ingestion failures are visible to broader team |

## Success Metrics

| ID | Metric | Target | Objective |
|----|--------|--------|-----------|
| SM-001 | Number of external vendor/exchange direct dependencies eliminated from downstream systems | At least 1 downstream system migrated to NMD in Phase 1 | OBJ-001 |
| SM-002 | Single authoritative product canonical in place covering Phase 1 data types | 100% of Phase 1 instruments represented in the canonical | OBJ-002 |
| SM-003 | Time to onboard a new data feed (from source identified to data available in API) | TBD — baseline to be measured in Phase 1 | OBJ-003 |
| SM-004 | Query API live and consumed by at least one downstream system | At least 1 downstream system consuming NMD API by Phase 1 delivery | OBJ-004 |
| SM-005 | Phase 1 SILO service deployed and operational | Deployed to target environment and passing acceptance criteria | OBJ-005 |

## Dependencies

| ID | Dependency |
|----|-----------|
| DEP-001 | Exchange or official source access credentials or agreements for Futures and Options (TBC) |
| DEP-002 | Confirmation of target exchanges for Phase 1 Futures and Options data |
| DEP-003 | At least one downstream system identified as Phase 1 consumer for API validation |

## Glossary

| Term | Definition |
|------|-----------|
| Product Canonical | The master reference record for a financial instrument, serving as the authoritative identity across all data sources |
| Reference Data | Static or slowly-changing data describing a financial instrument (e.g., contract specs, expiry dates, tick sizes) |
| Daily Update | Time-sensitive data published on a scheduled basis (e.g., settlement prices, margin rates, corporate events) |
| Settlement Price | The official end-of-day price for a financial instrument, published by the exchange, used for margin and P&L calculations |
| Margin Rate | The collateral requirement set by an exchange or clearing house for holding a position |
| Snapshot | A point-in-time extract of data from one or more sources, used as input to the normalization pipeline |
| SILO Service | A standalone, self-contained service deployment with no cross-system integrations or SSO dependencies |
| Data Owner | An internal operator responsible for managing data sources, monitoring ingestion, and validating output via the NMD UI |
| Ingestion Framework | The centralized component that manages, schedules, tracks, and monitors the processing of all data sources |
| Canonical Key | A standardized identifier used to link data from multiple sources to the same product canonical record |

## Approvals

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Leo | TBD | TBD |
| Reviewer | TBD | TBD | TBD |
| Approver | TBD | TBD | TBD |

## Change Log

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v0.1 | 2026-03-01 | Leo | Initial draft |
