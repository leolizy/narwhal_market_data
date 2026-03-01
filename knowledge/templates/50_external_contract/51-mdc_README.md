# MDC — Market Data Contract

## README & Governance Guide

**Template:** `51-mdc_template.yaml`
**Layer:** 3 (Contracts & Architecture)
**Parent:** PSD (Product Specification Document)
**Downstream:** UT (Unit Test Document)

---

## What Is a Market Data Contract?

A Market Data Contract (MDC) is a specialisation of the Data Contract (DC) designed specifically for **external market
data sourcing**. It governs the extraction and normalisation of raw market price, reference, and event data from
external authoritative sources (exchanges, clearing houses, vendors) into the canonical entity model.

### MDC vs DC

| Aspect | DC (Data Contract) | MDC (Market Data Contract) |
|--------|--------------------|-----------------------------|
| Scope | Any internal data product | External market data sources only |
| Source systems | Internal or mixed | External exchanges, vendors, clearing houses |
| Key sections | Schema + write path | Schema + input/source location + transformation contract + end result mockup |
| Entity model | Generic | Canonical entity key (6 columns + hash_key, per PSD-0002) |
| Fixtures | Optional | Required (sample extraction record) |

Use **DC** for internal data products. Use **MDC** when the data originates from an external market data source that
must be parsed, mapped to canonical entity keys, and resolved against the ENT module.

---

## When to Create an MDC

Create a new MDC when:

1. **Onboarding a new exchange or data vendor** — each external source (or logical source group) gets its own MDC
2. **Adding a new data category** from an existing source — e.g., adding margin rates from a source that previously only
   provided settlement prices
3. **Restructuring source adapters** — when extraction logic fundamentally changes for a source

Do **not** create an MDC for:
- Internal data products → use DC
- API contracts → use API
- Database schemas → use DBC
- Event-driven contracts → use AEC

---

## The Canonical Entity Key Model (PSD-0002)

Every market data record extracted through an MDC must resolve to **7 output fields** defined in PSD-0002:

```
clearing_house  +
exchange        +
commodity       +    ──→   hash_key (deterministic, PSD-0002 BR-004)
product_type    +          (PHY | FUT | CMB | OOP | OOF | OOC)
product_code    +
contract             (YYYYMM or YYYYMMDD pattern)

```

**Search modes** (PSD-0002):
- **EXACT** — O(1) hash key lookup, used by ING, MCE, DQM modules during processing
- **BLURRING** — partial column filter with wildcard support, used for ad-hoc queries and QRY module

**Rules:**
- All 6 key columns must be non-blank for hash computation
- The same 6-column input must always produce the same hash (determinism — PSD-0002 BR-004)
- `product_type` must be one of: PHY, FUT, CMB, OOP, OOF, OOC (PSD-0002 VR-004)
- Source adapters must normalise values before hashing
- Changing how a key field is derived = **breaking change** (MAJOR version increment + 30-day notice)
- Records that cannot be resolved are quarantined, not dropped silently

---

## Section-by-Section Guide

### 1. Contract Overview

High-level summary: what sources, what data, why it matters.

### 2. Data Product Identification

Product name, ID, domain, tier. Use `market-data-feed` as the domain. Tag with data categories: `reference-data`,
`settlement-data`, `event`, `inbound`.

### 3. Input & Source Location (MDC-specific)

**This is the key differentiator from DC.** For each source:
- Assign a stable `source_id` (e.g., `SOURCE-CME-SPAN`)
- Document delivery mechanism, formats, schedule, and authentication
- Include the public URL for data downloads or documentation
- List data categories: `product-list`, `product-detail`, `daily-price`, `contract-dates`, `margin-rates`,
  `exchange-fees`

### 4. Schema Definition

Split into two blocks:
- **`canonical_key_fields`** — the 7 fixed fields (6 key columns + `hash_key`) per PSD-0002. These are identical across
  all MDC documents.
- **`additional_fields`** — source-specific fields beyond the canonical key.

### 5. Semantic Definitions

Business glossary and business rules specific to the source. Includes an **`entity_resolution`** sub-section
documenting:
- How source records map to the 6 canonical key columns
- Reference to PSD-0002 (`canonical_key_ref`)
- Both search modes (EXACT / BLURRING)
- Hash determinism requirement (PSD-0002 BR-004)

### 6. Write Path Contract

Batch atomicity, idempotency (batch_id + source_id + business_date), and per-source adapter transformation logic.

### 7. Data Quality Standards

Quality dimensions: completeness, conformity, uniqueness, timeliness. Add custom checks for hash determinism and
unmapped record rates.

### 8. Service Level Agreements

Availability, data readiness SLO, throughput limits, incident response.

### 9. Access & Security

Internal pipeline access only. List approved downstream consumers (e.g., ING, MCE, QRY, DQM modules).

### 10. Lineage & Dependencies

Upstream: external sources. Downstream: internal consuming modules (ING, MCE, QRY, DQM per PSD-0002). Each consumer
specifies its `search_mode` (EXACT or BLURRING). Includes a **`canonical_entity_integration`** block referencing
PSD-0002.

### 11. Versioning & Compatibility

Breaking changes: removing key columns, changing hash algorithm, altering enum values, changing contract format.

### 12. End Result Mockup

**Required for MDC.** Show the expected JSON structure of a fully resolved extraction record with angle-bracket
placeholders.

### 13. Sample Fixture

**Required for MDC.** Provide a concrete synthetic test record. Mark as "do not use in production".

### 14–16. Support, Attachments, Change Log

Standard sections — same as DC.

---

## Data Categories Priority

When sourcing market data from exchanges, prioritise in this order:

| Priority | Data Category | Description |
|----------|---------------|-------------|
| 1 (Highest) | Product list | Complete list of all listed products/instruments |
| 2 | Product detail | Per-product specifications (lot size, tick, currency, etc.) |
| 3 | Daily price | End-of-day settlement prices and volume |
| 4 | Contract dates | Expiry dates, first/last trade dates, delivery months |
| 5 | Margin rates | Initial/maintenance margin requirements |
| 6 (Lowest) | Exchange fees | Trading, clearing, and membership fees |

---

## Source Onboarding Checklist

Before an MDC can move from `draft` to `approved`:

- [ ] Source ID assigned and documented
- [ ] Delivery mechanism confirmed and tested
- [ ] Input format(s) identified with sample files
- [ ] Per-field mapping to 6 canonical key columns documented
- [ ] Adapter mapping version 1.0 created
- [ ] Authentication method confirmed
- [ ] End result mockup matches actual adapter output
- [ ] Sample fixture validates against schema
- [ ] PDF parsing strategy resolved (if source uses PDF)
- [ ] Unmapped record rate threshold defined
- [ ] Delivery schedule confirmed with source provider

---

## Related Documents

| Document | Relevance |
|----------|-----------|
| DC template (`43-dc_template.yaml`) | Base data contract — MDC extends this for market data |
| FRD (Data Ingestion) | Functional requirements for the ingestion pipeline |
| PSD-0002 (Canonical Entity Search) | Defines the 6-column key model, hash determinism (BR-004), product_type enum (VR-004), and search modes (EXACT/BLURRING) |
| API | Consumer-facing query API for market data |

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2026-02-25 | Product team | Initial MDC template README — governance guide for Market Data Contracts |
