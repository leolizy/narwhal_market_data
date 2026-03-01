# AEC-0001: Async Event Contract (AEC) — Policy & Governance Document

**Version:** 1.0
**Last Updated:** 2026-02-23
**Owner:** Architecture / Platform Engineering

---

## Document Overview

### What Is an Async Event Contract?

An Async Event Contract (AEC) is a formal specification that defines the structure, behavior, ownership, and operational
expectations of a single asynchronous event published through a messaging platform (Kafka). It serves as the binding
agreement between the producing service and all consuming services.

### Function in the SDLC

The AEC sits at the intersection of design and implementation phases. It is created after the Product Specification
Document (PSD) identifies the need for an asynchronous event and before any producer or consumer code is written. It
acts as the source of truth for event-driven integration points and feeds into test plans, deployment guides, and API
documentation.

### Document Hierarchy

The AEC relates to other SDLC documents as follows:

- **Parent documents:** PSD-0001 (Product Specification Document)
- **Sibling documents:** API Specification (for synchronous counterparts), DBC (Database Contract)
- **Child documents:** Deployment Guides (DG) for Kafka topic provisioning
- **Cross-references:** NFR (for SLA baselines)

---

## Document Dependencies

### Upstream Documents (Dependencies)

- PSD-0001

### Downstream Documents (Depend on This)

- UT-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

### Document ID Format

**Format:** `AEC-[NNNN]`

- **Prefix:** `AEC` (Async Event Contract)
- **Numbering:** Sequential, globally unique across the organization. Assigned by the document management system or
  architecture team.
- **Examples:** AEC-0001, AEC-0042, AEC-0100

### File Naming Convention

**Format:** `AEC-[NNNN]_[ShortTitle]_v[X.Y].[ext]`

- `[ShortTitle]`: CamelCase or kebab-case summary of the event, e.g., `OrderCreated`, `PaymentProcessed`
- `[X.Y]`: Semantic version — Major.Minor
- `[ext]`: `.yaml` for machine-readable, `.md` for human-readable

**Examples:**

- `AEC-0001_OrderCreated_v1.0.yaml`
- `AEC-0001_OrderCreated_v1.0.md`

### Version Numbering

- **Major version (X.0):** Breaking changes — field removal, type changes, partition key changes, topic rename
- **Minor version (X.Y):** Non-breaking changes — new optional fields, description updates, SLA adjustments

---

## Scope & Granularity

### Document Scope

Each AEC covers exactly **one event type**. An event type is a unique combination of domain + action (e.g.,
`order.created`, `payment.refunded`, `inventory.reserved`).

### When to Create a New AEC

Create a new AEC when:

- A new event type is introduced into the system
- An existing event is forked into a distinct variant with different semantics (e.g., `order.created.v2` with
  fundamentally different payload structure)
- A domain introduces its first event (also create the domain's event catalog entry)

### When to Update an Existing AEC

Update the existing AEC (with a new version) when:

- Fields are added or removed from the payload
- SLA or delivery guarantees change
- New consumers register
- Kafka topic configuration changes (partitions, retention)
- Security or compliance requirements change
- Schema compatibility mode changes

### Relationship to AsyncAPI Specification

The AEC is a governance and documentation artifact. It complements (but does not replace) a machine-readable AsyncAPI
specification file. Teams are encouraged to maintain both: the AEC for human governance and the AsyncAPI YAML for
tooling and code generation. The AEC's structure aligns with AsyncAPI 3.x concepts to minimize translation effort.

---

## Section-by-Section Explanation

### Section 1: Event Overview

- **Purpose:** Establish the business meaning and identity of the event so any reader immediately understands what it
  represents.
- **What to include:** The machine-readable event name (dot-notation), the owning domain/bounded context, the
  business-language description, and the specific trigger condition that causes this event to be emitted.
- **What NOT to include:** Implementation details (code snippets, class names). Keep this at the domain/business level.
- **Required:** Yes

### Section 2: Ownership & Contacts

- **Purpose:** Establish clear accountability. In event-driven systems, unclear ownership is the primary cause of
  integration failures.
- **What to include:** The producing team and service, every known consuming team with their use case, and an escalation
  contact for incidents or breaking changes.
- **What NOT to include:** Individual developer names (use team aliases or roles). Individuals rotate; teams persist.
- **Required:** Yes

### Section 3: Channel & Transport Configuration (Kafka)

- **Purpose:** Define the physical transport layer so that infrastructure teams can provision resources and consumers
  can configure correctly.
- **What to include:** Topic name, partition count and key, replication factor, retention policy, compression, consumer
  group naming convention, and dead letter topic.
- **What NOT to include:** Application-level consumer logic. This section is about the Kafka infrastructure, not
  business logic.
- **Required:** Yes

### Section 4: Message Specification

- **Purpose:** Define the exact structure of the message that flows through the topic — the core of the contract.
- **What to include:** Message ID strategy, content type, encoding, schema registry configuration, all standard headers
  (CloudEvents-compatible), the full payload schema with types and constraints, and at least one sample message.
- **What NOT to include:** Multiple alternative payload formats in a single contract. If the event can be serialized in
  multiple formats, create separate contracts or clearly designate one as canonical.
- **Required:** Yes

### Section 5: Schema Evolution & Compatibility

- **Purpose:** Prevent breaking changes from silently disrupting consumers. This section codifies the rules of change.
- **What to include:** The chosen compatibility strategy (BACKWARD recommended), an explicit list of allowed vs.
  breaking changes, the deprecation policy with notice period, and the versioning strategy.
- **What NOT to include:** Change history (that goes in the Change Log). This section defines the rules; it doesn't
  track instances.
- **Required:** Yes

### Section 6: Delivery Guarantees & SLA

- **Purpose:** Set measurable expectations for event delivery performance so consumers can architect their systems
  accordingly.
- **What to include:** Delivery semantics (at-least-once is the Kafka default), ordering guarantees, throughput
  estimates, latency targets, retry policy, dead letter handling, and idempotency requirements.
- **What NOT to include:** Aspirational targets. Only commit to SLAs that the infrastructure can actually support.
  Consult the platform team.
- **Required:** Yes

### Section 7: Security & Access Control

- **Purpose:** Ensure events carrying sensitive data are properly protected and access is controlled.
- **What to include:** Authentication mechanism, producer and consumer ACLs, data classification, PII field inventory,
  encryption settings (in-transit, at-rest, field-level), and compliance requirements.
- **What NOT to include:** Specific passwords, certificates, or secrets. Reference a secrets management system instead.
- **Required:** Yes

### Section 8: Observability & Monitoring

- **Purpose:** Ensure the event is operationally visible so issues can be detected and resolved quickly.
- **What to include:** Key metrics to track, dashboard links, alerting rules with severity and notification channels,
  distributed tracing configuration, and logging requirements.
- **What NOT to include:** Alert thresholds that change frequently. Reference a monitoring-as-code repository instead if
  thresholds are dynamic.
- **Required:** No (Optional, but strongly recommended for production events)

### Section 9: Testing & Validation

- **Purpose:** Define how the contract is verified before and after deployment.
- **What to include:** Contract testing tool and approach (for both producer and consumer sides), schema validation
  configuration, integration test environment details, sample test events, and chaos testing scenarios.
- **What NOT to include:** Full test case specifications. Link to the Unit Test (UT) document instead.
- **Required:** No (Optional, but strongly recommended)

### Section 10: Dependencies & Related Events

- **Purpose:** Map the event within the broader event-driven architecture so teams understand the event flow.
- **What to include:** Upstream and downstream events, saga participation details (if applicable), related APIs, and a
  link to an event flow diagram.
- **What NOT to include:** Full architecture diagrams. Link to the PSD instead.
- **Required:** No (Optional, but recommended for events in complex workflows or sagas)

---

## Update Triggers

### Creation Triggers

- A new asynchronous event type is identified during design
- A domain team needs to publish data to other services asynchronously
- An existing synchronous integration is being migrated to event-driven
- A saga or choreography pattern requires a new event

### Update Triggers

- Payload schema changes (fields added, removed, or type-changed)
- New consumer team registers for the event
- Kafka topic configuration changes (partition count, retention, replication)
- SLA or delivery guarantee changes
- Security or compliance requirement changes
- Schema compatibility mode changes
- Producer or consumer service is renamed, replatformed, or decommissioned

### Review Triggers (re-review without changes)

- Quarterly review cycle (recommended)
- Post-incident review where this event was involved
- Architecture review board audit
- Consumer onboarding (existing contract reviewed for fitness)
- Compliance audit

### Retirement Triggers

- The event type is no longer produced (all consumers migrated away)
- The event has been superseded by a new version (mark old as Deprecated, then Retired after sunset period)
- The producing domain/service is decommissioned
- Business process that triggers the event is eliminated

---

## Roles & Responsibilities

| Role                   | Responsibility                                                                                      |
|------------------------|-----------------------------------------------------------------------------------------------------|
| **Author**             | The producer team's tech lead or senior engineer. Drafts and maintains the contract.                |
| **Reviewer**           | A peer from the consuming team(s) and/or a platform engineer. Validates schema, SLA, and Kafka config. |
| **Approver**           | Architecture lead or domain architect. Signs off on compatibility strategy and cross-domain impact.  |
| **Accountable Owner**  | The producing team. They are responsible for keeping the contract current with every release.        |
| **Platform Team**      | Validates Kafka configuration feasibility (partitions, retention, ACLs). Advisory role.             |
| **Security Team**      | Reviews Section 7 (Security) for events classified as Confidential, PII, or PHI. Advisory role.     |

---

## Quality Checklist

Use this checklist before submitting the AEC for review:

- [ ] Document ID follows `AEC-[NNNN]` format
- [ ] File name follows `AEC-[NNNN]_[ShortTitle]_v[X.Y].[ext]` convention
- [ ] All required sections (1–7) are completed
- [ ] Event name follows dot-notation convention (e.g., `domain.entity.action`)
- [ ] Kafka topic name follows the organization's naming convention
- [ ] Partition key is explicitly defined and justified
- [ ] At least one sample message is provided
- [ ] Payload schema includes types, constraints, and required flags for all fields
- [ ] Schema compatibility strategy is declared (BACKWARD recommended)
- [ ] Delivery guarantee and ordering guarantee are explicitly stated
- [ ] All known consumers are registered with use cases
- [ ] PII fields are identified if data classification is Confidential or higher
- [ ] Producer and consumer ACLs are specified
- [ ] Related documents (PSD, API, etc.) are linked
- [ ] Change log is updated with the current version's changes
- [ ] Reviewed by at least one consuming team representative
- [ ] Approved by architecture lead or domain architect

---

## Appendix: Event Naming Conventions

### Event Name Format

**Format:** `{domain}.{entity}.{action}`

- **domain:** The bounded context (lowercase, singular). E.g., `order`, `payment`, `inventory`
- **entity:** The aggregate or entity (lowercase, singular). E.g., `order`, `invoice`, `stock`
- **action:** Past-tense verb describing what happened (lowercase). E.g., `created`, `updated`, `cancelled`, `shipped`

**Examples:** `order.order.created`, `payment.invoice.paid`, `inventory.stock.reserved`

### Topic Name Format

**Format:** `{domain}.events.{entity}.{action}`

**Examples:** `order.events.order.created`, `payment.events.invoice.paid`

### Consumer Group Format

**Format:** `{consumer-service}.{domain}.{entity}.{action}.cg`

**Examples:** `notification-service.order.order.created.cg`, `analytics-service.payment.invoice.paid.cg`
