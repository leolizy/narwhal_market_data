# API Contract — NMD Canonical Management & Query API

| Field | Value |
|-------|-------|
| Document ID | API-0001 |
| OpenAPI Version | 3.1.0 |
| Title | NMD Canonical Management & Query API |
| Version | v0.1 |
| Status | Draft |
| Created | 2026-03-01 |
| Last Updated | 2026-03-01 |
| Author | Leo |
| Related Documents | FRD-NMD-0001,PSD-0001,PSD-0002 |
| Classification | Internal |
| Source FRD | FRD-NMD-0001 |

---

## 1. Overview

REST API for the NMD Product Canonical module. Provides lifecycle management of canonical instrument records (create, update, status change) and read-only query access (lookup by canonical key and attribute search). This is the authoritative identity layer for all NMD ingestion, normalisation, and export modules.

Source FRD: FRD-NMD-0001 — Product Canonical Management & Query
Maintenance spec: PSD-0001
Query spec: PSD-0002

---

## 2. Endpoints

### Canonical Maintenance

Create, update, and manage status of canonical instrument records (PSD-0001)

### Canonical Query

Read-only lookup and attribute search of canonical records (PSD-0002)

#### `POST /canonical`

**Create a new canonical instrument record**

Creates a new canonical instrument record. The canonical key is computed by the system as a deterministic hash of the 5 hierarchy columns. Initial status is supplied by the caller (Data Owner) or taken from source configuration (Source Processing). Duplicate canonical keys are rejected.

Ref: PSD-0001 CRUD — Create

**Request Body:** `CanonicalRecordCreateRequest` (see Schemas section)

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Canonical record created successfully |
| 400 | Validation error — e.g. missing exchange, invalid entity type, duplicate canonical key |
| 401 | Unauthorised |
| 403 | Forbidden — caller role does not have create permission |
| 409 | Conflict — canonical record with this key already exists |
| 500 | Internal server error |

#### `GET /canonical/{canonical_key}`

**Lookup canonical record by canonical key**

Returns the full canonical record for the given canonical key, subject to the caller's role-based status filter. By default only Active records are returned. Data Owner and Data Ingestion Module may also retrieve Inactive and Disabled records. Query & Export Module may never retrieve Disabled records.

Ref: PSD-0002 Flow A

**Parameters:**

| Name | In | Required | Type | Description |
|------|----|----------|------|-------------|
| `canonical_key` | path | Yes | string | The deterministic hash key identifying the canonical record |
| `status_filter` | query | No | string — one of: Active, Inactive, Disable | Optional status filter. Permitted values depend on caller role. Query & Export Module may not request Disabled. |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Canonical record found |
| 400 | Bad request — e.g. empty canonical_key or disallowed status_filter for caller role |
| 401 | Unauthorised |
| 404 | Canonical record not found |
| 500 | Internal server error |

#### `PUT /canonical/{canonical_key}`

**Update non-locked fields of a canonical record**

Updates the non-locked fields of an existing canonical record. The 5 hierarchy columns (exchange, commodity, product_type, product_code, contract), asset_class, entity_type, and canonical_key are immutable after creation and are rejected if included. Only status is editable via this endpoint — see PATCH /canonical/{canonical_key}/status for status lifecycle changes.

Ref: PSD-0001 CRUD — Update

**Parameters:**

| Name | In | Required | Type | Description |
|------|----|----------|------|-------------|
| `canonical_key` | path | Yes | string | The canonical key of the record to update |

**Request Body:** `CanonicalRecordUpdateRequest` (see Schemas section)

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Record updated successfully |
| 400 | Validation error — e.g. attempt to modify locked fields |
| 401 | Unauthorised |
| 403 | Forbidden — caller role does not have update permission |
| 404 | Canonical record not found |
| 500 | Internal server error |

#### `PATCH /canonical/{canonical_key}/status`

**Change the status of a canonical record**

Changes the status of a canonical record and triggers a top-down cascade to all non-Disabled descendants. A child record cannot be set to a status more permissive than its parent. One canonical.status.changed event is emitted per affected record (including cascade-triggered descendants).

Ref: PSD-0001 CRUD — Status Change; AEC-0003

**Parameters:**

| Name | In | Required | Type | Description |
|------|----|----------|------|-------------|
| `canonical_key` | path | Yes | string | The canonical key of the record whose status to change |

**Request Body:** `StatusChangeRequest` (see Schemas section)

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Status changed successfully. Response includes the updated record; cascade to descendants is async. |
| 400 | Validation error — e.g. child status more permissive than parent |
| 401 | Unauthorised |
| 403 | Forbidden — caller role does not have status change permission |
| 404 | Canonical record not found |
| 500 | Internal server error |

#### `GET /canonical/search`

**Attribute search of canonical records**

Searches the canonical entity table by one or more attributes. At least one attribute must be provided — open-ended queries with no filter are not permitted. Contract ticker search uses prefix match only. Results are sorted Active → Inactive → Disabled, then by exchange, commodity, product_type, product_code. Paginated — default page size 50, maximum 2000.

Ref: PSD-0002 Flow B

**Parameters:**

| Name | In | Required | Type | Description |
|------|----|----------|------|-------------|
| `exchange` | query | No | string | Exact match on exchange |
| `commodity` | query | No | string | Exact match on commodity |
| `product_type` | query | No | string — one of: PHY, FUT, CMB, OOP, OOF, OOC | Exact match on product type (Futures & Options only) |
| `product_code` | query | No | string | Exact match on product code |
| `contract` | query | No | string | Prefix match on contract ticker — contains and suffix match not supported in Phase 1 |
| `entity_type` | query | No | string | Exact match on entity type |
| `status_filter` | query | No | string — one of: Active, Inactive, Disable | Optional status filter — role-dependent; Query & Export Module may not request Disabled |
| `page` | query | No | integer | Page number (1-based) |
| `page_size` | query | No | integer | Page size — default 50, maximum 2000. Requests exceeding 2000 are capped at 2000. |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Search results |
| 400 | Bad request — e.g. no search attributes provided, or disallowed status_filter for caller role |
| 401 | Unauthorised |
| 500 | Internal server error |

---

## 3. Schemas

### `CanonicalRecord`

A canonical instrument record — the authoritative identity for one unique financial instrument in NMD

| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `canonical_key` | string | Yes | Yes | Deterministic hash of the 5 hierarchy columns — immutable after creation |
| `exchange` | string | Yes | Yes | Exchange identifier. For FX records: fixed value 'FX' |
| `commodity` | string | No | Yes | Commodity identifier. For FX Currency Pair: XXXYYY format (6 uppercase characters). Null for L1 entity types. |
| `product_type` | string (PHY,FUT,CMB,OOP,OOF,OOC) | No | Yes | Product type — Futures & Options only. Null for FX and entity types below L3. |
| `product_code` | string | No | Yes | Product code — null for entity types below L3 and all FX records |
| `contract` | string | No | Yes | Contract ticker. For Option Contract: YYYYMM_CP_STRIKE | YYYYMMDD_CP_STRIKE | YYYYMMWN_CP_STRIKE. Null for non-contract entity types and all FX records. |
| `asset_class` | string (Futures & Options,FX) | Yes | Yes | Asset class — immutable after creation |
| `entity_type` | string | Yes | Yes | Entity type — must be valid for the selected asset class. Immutable after creation. |
| `status` | string (Active,Inactive,Disable) | Yes | No | Operational status — editable via PATCH /canonical/{canonical_key}/status |
| `source` | string | Yes | Yes | Creation actor — 'User' or source processing identifier |
| `created_by` | string | Yes | Yes |  |
| `created_at` | string | Yes | Yes |  |
| `last_updated_by` | string | Yes | Yes |  |
| `last_updated_at` | string | Yes | Yes |  |

### `CanonicalRecordCreateRequest`

Request body for creating a new canonical record

| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `exchange` | string | Yes | No | Exchange identifier. Use 'FX' for FX records. |
| `commodity` | string | No | No | Commodity identifier. Required for entity types above L1. FX: XXXYYY format. |
| `product_type` | string (PHY,FUT,CMB,OOP,OOF,OOC) | No | No | Product type — Futures & Options L3+ only. Must be null for FX. |
| `product_code` | string | No | No | Product code — L3+ only. Must be null for FX. |
| `contract` | string | No | No | Contract ticker — contract-level entity types only. Must be null for FX. |
| `asset_class` | string (Futures & Options,FX) | Yes | No |  |
| `entity_type` | string | Yes | No | Entity type — must be valid for the selected asset class |
| `status` | string (Active,Inactive,Disable) | Yes | No | Initial status. Source Processing: taken from source configuration — never defaulted. |

### `CanonicalRecordUpdateRequest`

Request body for updating non-locked fields of a canonical record. The 5 hierarchy columns, asset_class, entity_type, and canonical_key may not be included — locked after creation.

| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `status` | string (Active,Inactive,Disable) | No | No | Use PATCH /canonical/{canonical_key}/status for status changes with cascade semantics. Included here for completeness — direct status update without cascade is not the canonical path. |

### `StatusChangeRequest`

Request body for changing the status of a canonical record

| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `new_status` | string (Active,Inactive,Disable) | Yes | No | The target status. Child record status cannot be more permissive than parent status. |

### `CanonicalSearchResponse`

Paginated attribute search results

| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `data` | array | No | No | Matching canonical records — sorted Active → Inactive → Disabled, then by exchange, commodity, product_type, product_code |
| `pagination` | PaginationMeta | No | No |  |

### `PaginationMeta`



| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `page` | integer | No | No |  |
| `page_size` | integer | No | No |  |
| `total_items` | integer | No | No |  |
| `total_pages` | integer | No | No |  |

### `ErrorResponse`



| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| `error_code` | string | Yes | No | Machine-readable error code |
| `message` | string | Yes | No | Human-readable error message |
| `details` | array | No | No | Optional list of validation errors |

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| v0.1 | 2026-03-01 | Leo | Initial draft — covers POST /canonical (create), PUT /canonical/{key} (update), PATCH /canonical/{key}/status (status change with cascade), GET /canonical/{key} (lookup), GET /canonical/search (attribute search with prefix match on contract, pagination 50/2000, fixed sort order) |
