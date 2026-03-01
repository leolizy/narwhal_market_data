# Async Event Contract — Canonical Status Changed

| Field | Value |
|-------|-------|
| Document ID | AEC-0003 |
| Title | Canonical Status Changed |
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
| Event Name | `canonical.status.changed` |
| Domain | canonical |
| Event Type | notification |
| Trigger | The status of a canonical record changes — either directly by a Data Owner or Source Processing, or as a result of a top-down status cascade from a parent record. One event is emitted per affected record including cascade-triggered descendants. |

**Business Description**

Signals to downstream systems that the operational status of a canonical instrument has changed. Consumers gate their processing behaviour on canonical status — Active enables full data loading, Inactive enables reference data only, Disable suppresses all loading. The new_status field is included in the payload to allow consumers to act without a round-trip to the Query API.

---

## 2. Ownership

**Producer Team:** NMD Team
**Producer Service:** NMD-CANONICAL (FRD-NMD-0001)
**Escalation Contact:** Team Lead

### Registered Consumers

| Team | Service | Purpose |
|------|---------|---------|
| NMD Team | Data Ingestion Module (FRD-NMD-0002) | Gate data loading behaviour by canonical status — Active allows full ingestion, Inactive reference data only, Disable suppresses all loading |
| NMD Team | Query & Export Module (FRD-NMD-0003) | Refresh export eligibility — Active and Inactive records included per caller permissions, Disabled records excluded |

---

## 3. Channel Configuration

| Field | Value |
|-------|-------|
| Topic | `nmd.canonical.status.changed` |
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
| `type` | canonical.status.changed |
| `source` | nmd/canonical |
| `id` | UUID — unique per event |
| `time` | ISO 8601 timestamp |
| `datacontenttype` | application/json |

### Payload

**Schema Format:** TBD

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `canonical_key` | string | Yes | The canonical key hash of the record whose status changed |
| `new_status` | string | Yes | The new status value — one of: Active, Inactive, Disable. Included in payload to allow consumers to act without a round-trip to the Query API. |
| `triggered_by` | string | Yes | Identifies the change trigger — one of: User, SourceProcessing, Cascade. Cascade indicates the status change was propagated from a parent record. |

---

## 5. Data Transformation

### Producer Mapping

| Source Field | Event Field | Transform |
|-------------|-------------|-----------|
| canonical_key (Canonical Record) | `payload.canonical_key` | Direct copy |
| status (Canonical Record — post-update value) | `payload.new_status` | Direct copy of new status value |
| change_trigger (audit log entry) | `payload.triggered_by` | Map to User | SourceProcessing | Cascade based on change actor |

### Consumer Mappings

**Data Ingestion Module (FRD-NMD-0002)**

| Event Field | Consumer Action |
|-------------|----------------|
| `payload.canonical_key` | Identify which instrument's ingestion pipeline to adjust |
| `payload.new_status` | Active → enable full ingestion; Inactive → reference data only; Disable → suppress all loading |

**Query & Export Module (FRD-NMD-0003)**

| Event Field | Consumer Action |
|-------------|----------------|
| `payload.canonical_key` | Identify which instrument's export eligibility to refresh |
| `payload.new_status` | Active/Inactive → include per caller permissions; Disable → exclude from all exports |

---

## 6. Schema Evolution

| Field | Value |
|-------|-------|
| Compatibility Strategy | Backward compatible — new optional fields may be added without a version bump; no existing fields (canonical_key, new_status, triggered_by) may be removed or have their type changed without a major version increment |
| Breaking Changes | Topic rename, field removal, field type change, new required field, partition key change — all require major version bump and 30-day consumer migration notice |
| Deprecation Policy | Deprecated fields must be flagged in the schema with a deprecation notice and remain present for a minimum of 30 days before removal |
| Versioning | Breaking changes result in a new event type (e.g., canonical.status.changed.v2) published in parallel until all consumers have migrated |

---

## 7. Delivery SLA

| Field | Value |
|-------|-------|
| Guarantee | At-least-once — consumers must be idempotent on (canonical_key, new_status) combination |
| Ordering | Ordered per canonical_key within a partition — status changes for the same record are processed in order |
| Latency | TBD — within platform event pipeline SLA; cascade events may produce a burst of messages for large hierarchies |
| Availability | TBD — platform standard |
| Retry Policy | Standard Kafka producer retry — platform standard |
| Dead Letter Topic | `nmd.canonical.status.changed.dlt` — failed consumer messages routed here after max retries |
| Idempotency | Consumers must deduplicate on (canonical_key, event id); cascade scenarios may produce high event volumes — consumers should be designed for burst throughput |

---

## 8. Security

| Field | Value |
|-------|-------|
| Authentication | Kafka ACL — mTLS or SASL (TBD — platform standard) |
| Produce Permission | NMD-CANONICAL service only |
| Consume Permission | Data Ingestion Module (FRD-NMD-0002), Query & Export Module (FRD-NMD-0003) |
| Encryption | TLS in transit — platform standard |
| PII Handling | No PII in payload — canonical_key is a deterministic hash; new_status and triggered_by are operational metadata only |
| Compliance | Internal classification — no regulatory data handling requirements for this event |

---

## 9. Observability

**Metrics:**

- Event production rate (events/sec) — monitor for cascade bursts
- Consumer lag per partition
- DLT message count
- Cascade event volume per parent change (to detect runaway cascades)

**Alerting:**

- Alert on DLT message count > 0
- Alert on consumer lag exceeding threshold (TBD)
- Alert on cascade event burst exceeding expected volume threshold (TBD)

**Tracing:** Propagate trace ID in CloudEvents extension header; link cascade child events to parent event trace for full cascade visibility

**Logging:** Producer logs canonical_key, new_status, triggered_by, and event ID on each publish; consumer logs canonical_key and new_status on receipt

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------| 
| v0.1 | 2026-03-01 | Leo | Initial draft — status change notification carrying canonical_key, new_status, and triggered_by; one event per affected record including cascade-triggered descendants |
