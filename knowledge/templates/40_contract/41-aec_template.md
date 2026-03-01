# Async Event Contract

| Field            | Value                                                          |
|------------------|----------------------------------------------------------------|
| Document ID      | AEC-[NNNN]                                                     |
| Title            |                                                                |
| Version          |                                                                |
| Status           | Draft / In Review / Approved / Deprecated / Retired            |
| Classification   | Public / Internal / Confidential / Restricted                  |
| Created Date     |                                                                |
| Last Updated     |                                                                |
| Author           |                                                                |
| Reviewer         |                                                                |
| Approver         |                                                                |
| Related Docs     |                                                                |

---

## 1. Event Overview

> **Guidance:** Provide a concise summary of what this event represents in the business domain, why it exists, and what
downstream behavior it triggers.

| Field                 | Value |
|-----------------------|-------|
| Event Name            |       |
| Domain                |       |
| Event Type            |       |
| Business Description  |       |
| Trigger Condition     |       |

**Event Type Options:** Domain | Integration | System | Notification

---

## 2. Ownership & Contacts

> **Guidance:** Identify the producing team, consuming teams, and escalation contacts. This section establishes
accountability for the event lifecycle.

### Producer

| Field              | Value |
|--------------------|-------|
| Producer Team      |       |
| Producer Service   |       |
| Producer Contact   |       |

### Registered Consumers

| Consumer Team | Consumer Service | Contact | Use Case |
|---------------|------------------|---------|----------|
|               |                  |         |          |

### Escalation

| Field               | Value |
|---------------------|-------|
| Escalation Contact  |       |

---

## 3. Channel & Transport Configuration (Kafka)

> **Guidance:** Define the Kafka topic, partitioning strategy, and transport-level configuration. Aligned with AsyncAPI
channel and binding concepts.

### Channel

| Field                        | Value |
|------------------------------|-------|
| Channel Name (Topic)         |       |
| Channel Naming Convention    |       |
| Protocol                     | kafka |

### Kafka Bindings

| Field                  | Value |
|------------------------|-------|
| Cluster                |       |
| Partition Count        |       |
| Partition Key          |       |
| Partition Strategy     |       |
| Replication Factor     |       |
| Retention (ms)         |       |
| Cleanup Policy         |       |
| Min In-Sync Replicas   |       |
| Compression Type       |       |

**Partition Strategy Options:** Key-based | Round-robin | Custom
**Cleanup Policy Options:** delete | compact | delete,compact
**Compression Options:** none | gzip | snappy | lz4 | zstd

### Consumer Configuration

| Field                         | Value |
|-------------------------------|-------|
| Consumer Group Convention     |       |
| Dead Letter Topic             |       |

---

## 4. Message Specification

> **Guidance:** Define the message envelope, headers, and payload structure. Aligned with AsyncAPI message object and
CloudEvents-compatible headers.

### Message Envelope

| Field                 | Value |
|-----------------------|-------|
| Message ID Strategy   |       |
| Content Type          |       |
| Encoding              | UTF-8 |

**Message ID Options:** UUID | ULID | Snowflake | Custom
**Content Type Options:** application/json | application/avro | application/protobuf

### Schema Registry

| Field                | Value |
|----------------------|-------|
| Enabled              |       |
| Registry URL         |       |
| Subject Name         |       |
| Compatibility Mode   |       |

**Compatibility Options:** BACKWARD | FORWARD | FULL | NONE

### Standard Headers

| Header Name      | Type   | Description                                              | Required |
|------------------|--------|----------------------------------------------------------|----------|
| ce_id            | string | Unique event identifier (CloudEvents 'id')               | Yes      |
| ce_source        | string | URI identifying the event producer (CloudEvents 'source') | Yes      |
| ce_type          | string | Event type identifier, e.g., 'com.example.order.created' | Yes      |
| ce_time          | string | ISO 8601 timestamp of when the event occurred            | Yes      |
| ce_specversion   | string | CloudEvents specification version, e.g., '1.0'          | Yes      |
| correlation_id   | string | Trace/correlation ID for distributed tracing             | Yes      |
| schema_version   | string | Version of the payload schema                            | Yes      |

### Payload Schema

> **Guidance:** Define each field in the event payload. Use JSON Schema-compatible types and constraints.

| Field Name | Type | Description | Required | Constraints | Example |
|------------|------|-------------|----------|-------------|---------|
|            |      |             |          |             |         |

### Sample Message

```json
{
  "headers": {
    "ce_id": "evt-abc123",
    "ce_source": "/order-service",
    "ce_type": "com.example.order.created",
    "ce_time": "2026-01-15T10:30:00Z",
    "ce_specversion": "1.0",
    "correlation_id": "corr-xyz789",
    "schema_version": "1.0"
  },
  "payload": {
  }
}

```

---

## 5. Schema Evolution & Compatibility

> **Guidance:** Define the rules for how the event schema may change over time without breaking existing consumers.

| Field                    | Value |
|--------------------------|-------|
| Compatibility Strategy   |       |
| Versioning Strategy      |       |

**Compatibility Options:** BACKWARD | FORWARD | FULL
**Versioning Options:** Header-based | Topic-per-version | Schema registry

### Allowed Changes

- Add optional fields with default values
- Add new header fields
- *(add more as applicable)*

### Breaking Changes (require versioning)

- Remove or rename existing fields
- Change field types
- Change partition key semantics
- *(add more as applicable)*

### Deprecation Policy

| Field                    | Value |
|--------------------------|-------|
| Notice Period            |       |
| Communication Channel    |       |
| Sunset Process           |       |

---

## 6. Delivery Guarantees & SLA

> **Guidance:** Define the quality-of-service expectations for this event, including latency, ordering, and reliability
guarantees.

### Core Guarantees

| Field                       | Value |
|-----------------------------|-------|
| Delivery Guarantee          |       |
| Ordering Guarantee          |       |
| Expected Throughput         |       |
| Max Publish Latency         |       |
| Max End-to-End Latency      |       |
| Availability Target         |       |

**Delivery Options:** At-least-once | At-most-once | Exactly-once
**Ordering Options:** Per-partition (by key) | Global | None

### Retry Policy

| Field                  | Value |
|------------------------|-------|
| Max Retries            |       |
| Backoff Strategy       |       |
| Backoff Initial (ms)   |       |
| Backoff Max (ms)       |       |

**Backoff Options:** Fixed | Exponential | Linear

### Dead Letter Handling

| Field                    | Value |
|--------------------------|-------|
| Enabled                  |       |
| DLT Topic                |       |
| Alert on DLT             |       |
| Reprocessing Strategy    |       |

**Reprocessing Options:** Manual | Automated | Scheduled

### Idempotency

| Field                    | Value |
|--------------------------|-------|
| Required                 |       |
| Idempotency Key          |       |
| Deduplication Window     |       |

---

## 7. Security & Access Control

> **Guidance:** Define authentication, authorization, and data sensitivity controls for producing and consuming this
event.

### Authentication & Authorization

| Field                       | Value |
|-----------------------------|-------|
| Authentication Mechanism    |       |
| Producer ACL                |       |
| Consumer ACL                |       |

**Auth Options:** mTLS | SASL/SCRAM | SASL/OAUTHBEARER | None

### Data Classification

| Field                        | Value |
|------------------------------|-------|
| Data Classification          |       |
| PII Fields                   |       |

**Classification Options:** Public | Internal | Confidential | PII | PHI

### Encryption

| Field                        | Value |
|------------------------------|-------|
| In Transit                   |       |
| At Rest                      |       |
| Field-Level Encryption       |       |
| Encrypted Fields             |       |

### Compliance

| Field                        | Value |
|------------------------------|-------|
| Data Retention Compliance    |       |

---

## 8. Observability & Monitoring *(Optional)*

> **Guidance:** Define the monitoring, alerting, and tracing expectations for this event to ensure operational
visibility.

### Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
|             |      |             |

**Type Options:** Counter | Gauge | Histogram

### Dashboards

- *(Link to Grafana/Datadog dashboards)*

### Alerting Rules

| Alert Name | Condition | Severity | Notification Channel |
|------------|-----------|----------|----------------------|
|            |           |          |                      |

**Severity Options:** Critical | Warning | Info

### Distributed Tracing

| Field            | Value |
|------------------|-------|
| Enabled          |       |
| Trace Header     |       |
| Tracing System   |       |

### Logging Requirements

> *(Describe logging expectations, e.g., "Log event_id and correlation_id at INFO level on publish and consume")*

---

## 9. Testing & Validation *(Optional)*

> **Guidance:** Define the testing strategy for validating event production, consumption, schema compliance, and failure
scenarios.

### Contract Testing

| Field            | Value |
|------------------|-------|
| Tool             |       |
| Producer Tests   |       |
| Consumer Tests   |       |

**Tool Options:** Pact | Spring Cloud Contract | Custom

### Schema Validation

| Field                | Value |
|----------------------|-------|
| Validation Point     |       |
| Reject on Invalid    |       |

### Test Environment

| Field                         | Value |
|-------------------------------|-------|
| Integration Test Environment  |       |

### Sample Test Events

```json
[]

```

### Chaos Testing

| Field    | Value |
|----------|-------|
| Enabled  |       |

**Scenarios:** broker failure | consumer crash | schema mismatch | network partition

---

## 10. Dependencies & Related Events *(Optional)*

> **Guidance:** Map the event's relationships to other events, services, and documents to understand the broader event
flow.

### Event Chain

| Direction   | Event Name | Document ID |
|-------------|------------|-------------|
| Upstream    |            |             |
| Downstream  |            |             |

### Saga Participation

| Field               | Value |
|---------------------|-------|
| Saga Name           |       |
| Saga Step           |       |
| Compensating Event  |       |

### Related APIs

- *(List REST/gRPC APIs related to this event)*

### Event Flow Diagram

- *(Link to visual event flow diagram)*

---

## Attachments

> **Guidance:** Attach supporting files such as AsyncAPI spec files, Avro/Protobuf schemas, architecture diagrams, or
sample payloads.

| Filename | Description | Location |
|----------|-------------|----------|
|          |             |          |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
|         |      |        |         |
