# Async Event Contract — Canonical Record Updated

| Field | Value |
|-------|-------|
| Document ID | AEC-0002 |
| Title | Canonical Record Updated |
| Version | v0.1 |
| Status | Draft |
| Created | 2026-03-01 |
| Last Updated | 2026-03-01 |
| Author | Leo |
| Reviewer | TBD |
| Approver | TBD |
| Related Documents | FRD-NMD-0001, PSD-0001 |
| Classification | Internal |

---

## 1. Event Overview

| Field | Value |
|-------|-------|
| Event Name | `canonical.record.updated` |
| Domain | canonical |
| Event Type | notification |
| Trigger | A canonical record is modified via the update operation (PSD-0001). In Phase 1, editable fields are limited since the 5 hierarchy columns are locked; this event is defined for forward compatibility as additional metadata fields are added in future phases. |

**Business Description**

Signals to downstream systems that a canonical instrument record has been modified. Consumers should call the Canonical Query API (PSD-0002 FLOW-A) using the canonical_key to retrieve the latest record state. Distinct from canonical.status.changed — that event is raised specifically for status lifecycle changes.

---

## 2. Ownership

**Producer Team:** NMD Team
**Producer Service:** NMD-CANONICAL (FRD-NMD-0001)
**Escalation Contact:** Team Lead

### Registered Consumers

| Team | Service | Purpose |
|------|---------|---------|
| NMD Team | Data Ingestion Module (FRD-NMD-0002) | Detect canonical record changes to refresh source-to-canonical mappings |
| NMD Team | Query & Export Module (FRD-NMD-0003) | Detect canonical record changes to refresh enrichment caches |

---

## 3. Channel Configuration

| Field | Value |
|-------|-------|
| Topic | `nmd.canonical.record.updated` |
| Partition Key | `canonical_key` |
| Partitions | TBD — platform standard |
| Replication Factor | TBD — platform standard |
| Retention | TBD — platform standard |
| Compression | snappy |

---

## 4. Message Specification

### CloudEvents Headers

| Header | Value |
|--------|-------|
| `specversion` | 1.0 |
| `type` | canonical.record.updated |
| `source` | nmd/canonical |
| `id` | UUID — unique per event |
| `time` | ISO 8601 timestamp |
| `datacontenttype` | application/json |

### Payload

**Schema Format:** TBD

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `canonical_key` | string | Yes | The canonical key hash of the updated record. Consumers use this to call the Canonical Query API for the latest record state. |

---

## 5. Data Transformation

### Producer Mapping

| Source Field | Event Field | Transform |
|-------------|-------------|-----------|
| canonical_key (Canonical Record) | `payload.canonical_key` | Direct copy |

### Consumer Mappings

**Data Ingestion Module (FRD-NMD-0002)**

| Event Field | Consumer Action |
|-------------|----------------|
| `payload.canonical_key` | Call Canonical Query API (PSD-0002 FLOW-A) to fetch updated record and refresh source-to-canonical mappings |

**Query & Export Module (FRD-NMD-0003)**

| Event Field | Consumer Action |
|-------------|----------------|
| `payload.canonical_key` | Call Canonical Query API (PSD-0002 FLOW-A) to fetch updated record and invalidate enrichment cache entry |

---

## 6. Schema Evolution

| Field | Value |
|-------|-------|
| Compatibility Strategy | Backward compatible — new optional fields may be added without a version bump; no existing fields may be removed or have their type changed without a major version increment |
| Breaking Changes | Topic rename, field removal, field type change, partition key change — all require major version bump and 30-day consumer migration notice |
| Deprecation Policy | Deprecated fields must be flagged in the schema with a deprecation notice and remain present for a minimum of 30 days before removal |
| Versioning | Breaking changes result in a new event type (e.g., canonical.record.updated.v2) published in parallel until all consumers have migrated |

---

## 7. Delivery SLA

| Field | Value |
|-------|-------|
| Guarantee | At-least-once — consumers must be idempotent on canonical_key |
| Ordering | Ordered per canonical_key within a partition — no global ordering guarantee |
| Latency | TBD — within platform event pipeline SLA |
| Availability | TBD — platform standard |
| Retry Policy | Standard Kafka producer retry — platform standard |
| Dead Letter Topic | `nmd.canonical.record.updated.dlt` — failed consumer messages routed here after max retries |
| Idempotency | Consumers must deduplicate on canonical_key; duplicate events may be produced in failure/retry scenarios |

---

## 8. Security

| Field | Value |
|-------|-------|
| Authentication | Kafka ACL — mTLS or SASL (TBD — platform standard) |
| Produce Permission | NMD-CANONICAL service only |
| Consume Permission | Data Ingestion Module (FRD-NMD-0002), Query & Export Module (FRD-NMD-0003) |
| Encryption | TLS in transit — platform standard |
| PII Handling | No PII in payload — canonical_key is a deterministic hash; no personal or sensitive data transmitted |
| Compliance | Internal classification — no regulatory data handling requirements for this event |

---

## 9. Observability

**Metrics:**

- Event production rate (events/sec)
- Consumer lag per partition
- DLT message count

**Alerting:**

- Alert on DLT message count > 0
- Alert on consumer lag exceeding threshold (TBD)

**Tracing:** Propagate trace ID in CloudEvents extension header for end-to-end tracing

**Logging:** Producer logs canonical_key and event ID on each publish; consumer logs canonical_key on receipt

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------| 
| v0.1 | 2026-03-01 | Leo | Initial draft — lightweight notification event carrying canonical_key only; defined for forward compatibility as canonical record gains additional editable fields in future phases |
