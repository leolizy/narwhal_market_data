# Product Specification Document — Product Canonical Query

| Field | Value |
|-------|-------|
| Document ID | PSD-0002 |
| Title | Product Canonical Query |
| Version | v0.1 |
| Status | Draft |
| Created | 2026-03-01 |
| Last Updated | 2026-03-01 |
| Author | Leo |
| Reviewer | TBD |
| Approver | TBD |
| Parent Document | FRD-NMD-0001 |
| Related Documents | PC-NMD-0001, FRD-NMD-0001, PSD-0001 |
| Classification | Internal |

---

## 1. Function Overview

Provides a read-only query interface for all internal modules to resolve instrument identity against
the canonical entity table — supporting lookup by canonical key and attribute-based search with
role-dependent status filtering.

| Field | Value |
|-------|-------|
| Function Type | PROCESS_FLOW |
| Module | NMD-CANONICAL |
| Triggering Actors | Data Owner via Operator UI (ACT-001/ACT-002), Data Ingestion Module (ACT-003), Query & Export Module (ACT-004) |

---

## 2. User Roles and Permissions

| Role | Type | Permitted Operations | Status Filter |
|------|------|---------------------|--------------|
| Data Owner | Human | Lookup by canonical key; Attribute search | All status types — Active, Inactive, Disabled |
| Data Ingestion Module | System | Lookup by canonical key; Attribute search | All status types — Active, Inactive, Disabled |
| Query & Export Module | System | Lookup by canonical key; Attribute search | Active by default; Inactive allowed if explicitly specified — Disabled never returned |

---

## 3. Preconditions and Dependencies

### Preconditions

| ID | Precondition |
|----|-------------|
| PRE-001 | Canonical entity table is initialised and accessible |
| PRE-002 | Caller is authenticated and their role is determinable at query time |
| PRE-003 | Canonical records exist — created via PSD-0001 (Canonical Maintenance) |

### Dependencies

| ID | Dependency | Notes |
|----|-----------|-------|
| DEP-001 | PSD-0001 (Canonical Maintenance) | Canonical records must exist before queries can return results |
| DEP-002 | FRD-NMD-0002 source configuration schema | Source identifier lookup (FR-NMD-001-011) is out of scope for this PSD and will be specified under FRD-NMD-0002 |

---

## 4. Process Flow Specification

### Flow A — Lookup by Canonical Key

**Trigger:** ET-006 — Internal module requests canonical lookup by canonical key

**Inputs:**

| Field | Type | Required | Match Type | Notes |
|-------|------|----------|-----------|-------|
| `canonical_key` | string | Yes | Exact | |
| `status_filter` | enum | No | N/A | Optional — role-dependent; omit to use default (Active only) |

**Processing Steps:**

1. Validate `canonical_key` is non-empty
2. Resolve caller role and permitted status filter
3. Query canonical table by exact `canonical_key` match
4. Apply status filter per caller role
5. Return full canonical record or `NOT_FOUND`

**Outputs:**

- **Success:** Full canonical record — all 5 hierarchy columns, `canonical_key`, `asset_class`,
  `entity_type`, `status`, `source`, `created_by`, `created_at`, `last_updated_by`, `last_updated_at`
- **Not found:** `NOT_FOUND` response — no auto-create

**SLA:** Hot path — called by every ingestion run; must meet platform latency target
(NFR-NMD-001-001, TBD)

---

### Flow B — Attribute Search

**Trigger:** ET-007 — Caller searches canonical by attribute

**Inputs:**

| Field | Type | Required | Match Type | Notes |
|-------|------|----------|-----------|-------|
| `exchange` | string | No | Exact | |
| `commodity` | string | No | Exact | |
| `product_type` | enum | No | Exact | |
| `product_code` | string | No | Exact | |
| `contract` | string | No | Prefix match | Fuzzy ticker search — prefix match only |
| `entity_type` | enum | No | Exact | |
| `status_filter` | enum | No | N/A | Optional — role-dependent; omit to use default (Active only) |

At least one of the above search fields must be provided.

**Processing Steps:**

1. Validate at least one search attribute is provided
2. Resolve caller role and permitted status filter
3. Build AND filter query across all provided attributes; apply prefix match on `contract` if supplied
4. Apply status filter per caller role
5. Sort results: Active first, then Inactive, then Disabled; then by `exchange`, `commodity`,
   `product_type`, `product_code`
6. Apply pagination — default page size 50, maximum 2000
7. Return paginated result set

**Outputs:**

- **Success:** Paginated list of matching canonical records — full record per item; empty list if
  no matches
- **Pagination:** Default page size 50; maximum page size 2000

**SLA:** Non-hot path — UI and export use; SLA TBD (OQ-001)

---

### Out of Scope

| Flow | Reason |
|------|--------|
| Lookup by Source Identifier | Source identifier resolution requires source-to-canonical mapping owned by FRD-NMD-0002 — to be specified in a PSD under FRD-NMD-0002 (FR-NMD-001-011) |

---

## 5. Business Rules

| ID | Rule |
|----|------|
| BR-001 | Active records are returned by default; Inactive records returned only when caller explicitly requests them |
| BR-002 | Disabled records are never returned to Query & Export Module regardless of filter parameter |
| BR-003 | A NOT_FOUND result is returned when no matching record exists — the query never auto-creates a canonical record |
| BR-004 | Every query response includes the full canonical record: all 5 hierarchy columns, canonical_key, status, and audit metadata |
| BR-005 | Attribute search requires at least one attribute — open-ended queries with no filter are not permitted |
| BR-006 | Caller identity determines the permitted status filter — callers cannot override their role's status access boundary |
| BR-007 | Attribute search sort order is fixed: status ascending (Active → Inactive → Disabled), then exchange, commodity, product_type, product_code |
| BR-008 | Attribute search results are paginated — default page size 50, maximum 2000; requests exceeding 2000 are capped at 2000 |
| BR-009 | Contract ticker search uses prefix match only — contains or suffix match not supported in Phase 1 |

---

## 6. Validation Rules

| ID | Field | Rule | Error Message |
|----|-------|------|--------------|
| VAL-001 | `canonical_key` | Must be non-empty for Flow A | "Canonical key is required" |
| VAL-002 | Attribute search inputs | At least one of exchange, commodity, product_type, product_code, contract, entity_type must be provided | "At least one search attribute is required" |
| VAL-003 | `status_filter` | Query & Export Module may not request Disabled records | "Status filter not permitted for caller role" |

---

## 7. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-001 | Given a caller submits a valid canonical_key, When Flow A executes, Then the matching record is returned in full or NOT_FOUND if no match exists |
| AC-002 | Given the same canonical_key is submitted by two different callers, When queried, Then both receive identical records subject to their respective status filters |
| AC-003 | Given a canonical_key lookup with no status filter specified, When the query runs, Then only Active records are returned by default |
| AC-004 | Given a Data Ingestion Module submits a lookup for a Disabled record, When the query runs, Then the Disabled record is returned |
| AC-005 | Given a Query & Export Module requests Disabled records explicitly, When the query runs, Then the request is rejected with "Status filter not permitted for caller role" |
| AC-006 | Given a caller submits an attribute search with at least one attribute, When Flow B executes, Then all matching records are returned subject to the caller's status filter |
| AC-007 | Given a caller submits a contract prefix search, When Flow B executes, Then all records with contract values beginning with the supplied prefix are returned |
| AC-008 | Given an attribute search is submitted with no attributes, When validation runs, Then the request is rejected with "At least one search attribute is required" |
| AC-009 | Given a Query & Export Module submits an attribute search with no status flag, When the query runs, Then only Active records are returned |
| AC-010 | Given a Query & Export Module submits an attribute search with Inactive flag specified, When the query runs, Then Active and Inactive records are returned — Disabled records excluded |
| AC-011 | Given an attribute search returns results, When the response is built, Then records are sorted Active first, then Inactive, then Disabled, then by exchange, commodity, product_type, product_code |
| AC-012 | Given an attribute search returns more than 50 records with no page size specified, When the response is built, Then only the first 50 records are returned |
| AC-013 | Given a caller requests a page size greater than 2000, When the query runs, Then the result set is capped at 2000 records |

---

## 8. Assumptions and Constraints

### Assumptions

| ID | Assumption |
|----|-----------|
| ASM-001 | Caller identity is determinable at query time — the canonical module can resolve which role a caller maps to |
| ASM-002 | Source identifier lookup (FR-NMD-001-011) is out of scope for this PSD — to be specified in a PSD under FRD-NMD-0002 |

### Constraints

| ID | Constraint |
|----|-----------|
| CON-001 | Read-only — no writes occur in this function |
| CON-002 | Query & Export Module is restricted to Active and Inactive results only — Disabled records never returned regardless of filter |
| CON-003 | Attribute search requires at least one input — unrestricted open queries are not permitted |
| CON-004 | Contract ticker search is prefix match only — contains or suffix match not supported in Phase 1 |
| CON-005 | Attribute search results are paginated — default page size 50, maximum 2000 |
| CON-006 | Attribute search sort order is fixed: status ascending (Active → Inactive → Disabled), then exchange, commodity, product_type, product_code |

---

## 9. Open Questions

| ID | Question |
|----|---------|
| OQ-001 | What is the response time SLA for attribute search distinct from the hot-path lookup SLA (NFR-NMD-001-001)? |

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| v0.1 | 2026-03-01 | Leo | Initial draft — PROCESS_FLOW spec for FA-02 Canonical Query from FRD-NMD-0001. Covers lookup by canonical key (FLOW-A) and attribute search (FLOW-B) with role-dependent status filtering, prefix match on contract ticker, fixed sort order, and pagination (default 50, max 2000). Source identifier lookup (FR-NMD-001-011) explicitly out of scope — deferred to FRD-NMD-0002. |
