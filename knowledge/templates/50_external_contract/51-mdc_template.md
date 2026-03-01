# Market Data Contract Template

> **Framework:** Open Data Contract Standard (ODCS) / Data Mesh
> **Scope:** Per external market data source or source group
> **Parent:** DC (Data Layer Contract) — specialised for external market data extraction and canonical entity resolution

---

## Metadata

| Field | Value |
|-------|-------|
| Document ID | MDC-[NNNN] |
| Title | |
| Version | |
| Status | Draft / In Review / Approved / Superseded / Retired |
| Classification | Public / Internal / Confidential / Restricted |
| Created | |
| Last Updated | |
| Author | |
| Reviewer | |
| Approver | |
| Related Documents | |

---

## 1. Contract Overview

> **Guidance:** High-level summary of this market data contract — which external data sources it governs, the business
context for ingesting this data, and the canonical entity model it feeds into.

[content]

---

## 2. Data Product Identification

> **Guidance:** Uniquely identifies the market data product covered by this contract. Includes ownership, domain
classification, tier, and searchable tags.

| Field | Value |
|-------|-------|
| Product Name | |
| Product ID | |
| Domain | |
| Subdomain | |
| Owner Team | |
| Owner Contact | |
| Data Steward | |
| Tier | Tier 1 (Critical) / Tier 2 (Important) / Tier 3 (Informational) |
| Tags | |

---

## 3. Input & Source Location

> **Guidance:** Documents where market data originates — the external authoritative sources (exchanges, clearing houses,
vendors), how data is delivered, in what format, and authentication requirements. Each source should have its own entry.

### Source Systems

| Field | Value |
|-------|-------|
| Source ID | e.g. SOURCE-CME-SPAN |
| Description | What this source provides |
| Delivery Mechanism | SFTP / website-download / datafeed-subscription / API / manual-download |
| Input Formats | CSV, JSON, XML, FIX, Parquet, PDF, etc. |
| Delivery Schedule | When data is available |
| Authentication | SSH key / API key / mTLS / OAuth |
| Public URL | Public-facing URL for data download or documentation |
| Exchange | Exchange or clearing house name |
| Data Categories | product-list, product-detail, daily-price, contract-dates, margin-rates, exchange-fees |

**Transformation Summary:** [How raw data is parsed and normalised]

---

## 4. Schema Definition

> **Guidance:** The authoritative schema for the canonical output. Defines the canonical entity key fields that every
inbound record must resolve to.

**Schema Format:** JSON / Avro / Protobuf / Parquet / Custom
**Schema Version:** [version]
**Datasets in Scope:** [list]

### Fields

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| | | | | |

---

## 5. Semantic Definitions

> **Guidance:** Business-level definitions and rules governing how market data should be interpreted, validated, and
mapped.

### Business Glossary

| Term | Definition |
|------|-----------|
| | |

### Business Rules

| ID | Rule | Ref |
|----|------|-----|
| | | |

---

## 6. Write Path Contract

> **Guidance:** Defines the guarantees and constraints governing how extracted market data is written. Covers batch
atomicity, idempotency, duplicate-run guards, and per-source adapter transformation logic.

| Field | Value |
|-------|-------|
| DB Architecture Ref | |
| Transaction Guarantees | |
| Idempotency | |
| Locking Strategy | |
| Write Modes | |
| Batch Write Behaviour | |

### Transformation Contract

| Field | Value |
|-------|-------|
| Source Schema Ref | |
| PDF Parsing Strategy | |
| Mapping Version Control | |

---

## 7. Data Quality Standards

> **Guidance:** Measurable quality expectations for extracted market data.

### Quality Dimensions

| Dimension | Definition | Target |
|-----------|-----------|--------|
| | | |

### Custom Checks

| Check ID | Description | Applies To |
|----------|-------------|------------|
| | | |

---

## 8. Service Level Agreements

> **Guidance:** Operational commitments regarding availability, data readiness, throughput, and incident response.

| SLA | Commitment |
|-----|-----------|
| Availability | |
| Latency | |
| Delivery Schedule | |
| Throughput | |
| Incident Response | |

---

## 9. Access & Security

> **Guidance:** Defines who can access the extracted market data, how access is granted, and what security controls are
in place.

| Field | Value |
|-------|-------|
| Access Mechanism | |
| Connection Details | |
| Authentication Method | |
| Authorization Model | |
| Approved Consumers | |
| Data Masking | |
| Retention Policy | |

---

## 10. Lineage & Dependencies

> **Guidance:** Documents where market data comes from (upstream) and where it flows to (downstream). Critical for
impact analysis.

**Upstream Sources:**

| System | Type | Delivery |
|--------|------|----------|
| | | |

**Downstream Consumers:**

| Consumer | Usage |
|----------|-------|
| | |

**Data Flow:** [transformation summary]

---

## 11. Versioning & Compatibility

> **Guidance:** Rules governing how this contract evolves. Defines breaking vs. non-breaking changes.

**Strategy:** Semantic Versioning (MAJOR.MINOR)

**Breaking changes:** [list]

**Non-breaking changes:** [list]

**Deprecation policy:** [notice period and sunset process]

---

## 12. End Result Mockup

> **Guidance:** The expected output structure of a fully resolved extraction record. Use angle-bracket placeholders for
variable values.

```json
{
}

```

---

## 13. Sample Fixture

> **Guidance:** A concrete synthetic test fixture with representative placeholder values. Do not use in production.

```json
{
}

```

---

## 14. Support & Communication

| Field | Value |
|-------|-------|
| Support Channel | |
| Documentation URL | |
| Announcement Channel | |
| Feedback Mechanism | |

---

## 15. Attachments

| Filename | Description | Location |
|----------|-------------|----------|
| | | |

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| | | | |
