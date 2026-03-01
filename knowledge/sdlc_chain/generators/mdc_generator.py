"""FRD → Market Data Contract (MDC) generator.

Produces an MDC scaffold for an external data source, aligned with
51-mdc_template.yaml v3.0.

Entry point
-----------
    generate_mdc(frd, source, sequence, today)
"""
from datetime import date
from typing import Optional

from ..config import (
    DRAFT_VERSION,
    MARKER_AUTO_COMPLETE,
    MARKER_AUTO_REVIEW,
    MARKER_DRAFT_REVIEW,
    STATUS_DRAFT,
)
from ..naming import generate_mdc_id
from ._contract_helpers import extract_common


def generate_mdc(
    frd: dict,
    source: dict,
    sequence: int = 1,
    today: Optional[str] = None,
) -> dict:
    """
    Scaffold one MDC (Market Data Contract) document for an external data source.

    Args:
        frd:      Source FRD dict.
        source:   Source dict from frd["data_requirements"]["external_sources"], or {}.
        sequence: Numeric sequence for MDC-NNNN.
        today:    ISO date string; defaults to today.
    """
    if today is None:
        today = date.today().isoformat()
    common = extract_common(frd, today)
    return _generate_mdc(common, source, sequence)


# ---------------------------------------------------------------------------
# Private implementation
# ---------------------------------------------------------------------------

def _generate_mdc(common: dict, source: dict, sequence: int) -> dict:
    """Build a full MDC scaffold dict aligned with 51-mdc_template.yaml v3.0.

    Template structure (v3.0):
      Section 1:  contract_overview
      Section 2:  data_product_identification
      Section 3:  input_and_source_location
      Section 4:  EXTRACTION PIPELINE (L1-L5 contiguous)
                  L1: source_data_catalog
                  L2: dataset_extraction_plan (incl. per-dataset write path)
                  L3: canonical_key_resolution (incl. entity_resolution)
                  L4: field_extraction_spec
                  L5: end_result (DC-0004 snapshot mockups)
      Section 5:  semantic_definitions (glossary + business rules only)
      Section 6:  data_quality_standards
      Section 7:  service_level_agreements
      Section 8:  access_and_security
      Section 9:  lineage_and_dependencies
      Section 10: versioning_and_compatibility
      Section 11: sample_fixture
      Section 12: support_and_communication
      Section 13: attachments
      Section 14: change_log
    """
    frd_id      = common["frd_id"]
    module_name = common["module_name"]
    today       = common["today"]
    mdc_id      = generate_mdc_id(sequence)

    source_name = source.get("source_name", module_name) if source else module_name
    source_desc = source.get("description", "")           if source else ""
    exchange    = source.get("exchange", "")               if source else ""
    delivery    = source.get("delivery_mechanism", "")     if source else ""
    formats_raw = source.get("input_formats", [])          if source else []
    categories  = source.get("data_categories", [])        if source else []

    return {
        "kind": "MarketDataContract",
        "metadata": {
            "document_id":    mdc_id,
            "title":          f"{source_name} Market Data Contract",
            "version":        DRAFT_VERSION,
            "status":         STATUS_DRAFT,
            "classification": common["classification"],
            "created_date":   today,
            "last_updated":   today,
            "author":         common["author"],
            "reviewer":       common["reviewer"],
            "approver":       common["approver"],
            "related_documents": [frd_id],
        },

        # ── Section 1 ──
        "contract_overview": {
            "description": (
                "High-level summary of this market data contract — which external "
                "data sources it governs, the business context for ingesting this "
                "data, and the canonical entity model it feeds into."
            ),
            "content": (
                source_desc
                or f"{MARKER_DRAFT_REVIEW} Describe what external market data source "
                   f"'{source_name}' provides and the business context it supports."
            ),
            "required": True,
        },

        # ── Section 2 ──
        "data_product_identification": {
            "description": (
                "Uniquely identifies the market data product covered by this contract. "
                "Includes ownership, domain classification, tier, and searchable tags."
            ),
            "required":      True,
            "product_name":  source_name,
            "product_id":    f"{MARKER_DRAFT_REVIEW} Unique identifier in the data catalog",
            "domain":        f"{MARKER_AUTO_REVIEW} market-data-feed",
            "subdomain":     f"{MARKER_DRAFT_REVIEW} Optional subdomain (e.g., reference-data / settlement-data)",
            "owner_team":    f"{MARKER_AUTO_REVIEW} {common['author'] or 'To be assigned'}",
            "owner_contact": f"{MARKER_DRAFT_REVIEW} Email or Slack channel",
            "data_steward":  f"{MARKER_DRAFT_REVIEW} Individual responsible for data quality",
            "tier":          f"{MARKER_DRAFT_REVIEW} Tier 1 (Critical) | Tier 2 (Important) | Tier 3 (Informational)",
            "tags":          categories or [],
        },

        # ── Section 3 ──
        "input_and_source_location": {
            "description": (
                "Documents where market data originates — the external authoritative "
                "sources (exchanges, clearing houses, vendors), how data is delivered, "
                "in what format, and authentication requirements."
            ),
            "required": True,
            "source_systems": [
                {
                    "source_id":          f"{MARKER_DRAFT_REVIEW} e.g. SOURCE-{source_name.upper().replace(' ', '-')}",
                    "description":        source_desc or f"{MARKER_DRAFT_REVIEW} What this source provides",
                    "delivery_mechanism": delivery or f"{MARKER_DRAFT_REVIEW} SFTP | website-download | datafeed-subscription | API | manual-download",
                    "input_formats":      formats_raw or [f"{MARKER_DRAFT_REVIEW} CSV, JSON, XML, FIX, Parquet, PDF"],
                    "delivery_schedule":  f"{MARKER_DRAFT_REVIEW} e.g. EOD 17:30 ET | T+1 by 08:00 UTC",
                    "authentication":     f"{MARKER_DRAFT_REVIEW} SSH key | API key | mTLS | OAuth",
                    "public_url":         f"{MARKER_DRAFT_REVIEW} Public-facing URL for data download or documentation",
                    "exchange":           exchange or f"{MARKER_DRAFT_REVIEW} Exchange or clearing house name",
                    "data_categories":    categories or [f"{MARKER_DRAFT_REVIEW} product-list, product-detail, daily-price, contract-dates, margin-rates, exchange-fees"],
                }
            ],
            "transformation_summary": f"{MARKER_DRAFT_REVIEW} High-level description of how raw data is parsed and normalised",
        },

        # ── Section 4: Extraction Pipeline ──

        # L1 — Source Data Catalog
        "source_data_catalog": {
            "description": (
                "High-level inventory of all data families / record groups that "
                "the external source provides. This is the 'menu' — not every "
                "item needs to be extracted."
            ),
            "required": True,
            "source_format":            f"{MARKER_DRAFT_REVIEW} Fixed-width | CSV | JSON | XML | API | PDF",
            "source_format_version":    f"{MARKER_DRAFT_REVIEW} Version / standard (e.g., SPAN PA2 positional)",
            "source_documentation_url": f"{MARKER_DRAFT_REVIEW} Link to the official format specification",
            "data_families": [
                {
                    "family_id":          f"{MARKER_DRAFT_REVIEW} e.g. FAM-HEADER",
                    "name":               f"{MARKER_DRAFT_REVIEW} Human-readable name",
                    "description":        f"{MARKER_DRAFT_REVIEW} What this family contains",
                    "source_record_types": [],
                    "update_frequency":   f"{MARKER_DRAFT_REVIEW} static | daily | intraday | event-driven",
                    "volume_estimate":    f"{MARKER_DRAFT_REVIEW} Approximate record count per delivery",
                    "business_relevance": f"{MARKER_DRAFT_REVIEW} Why this data matters",
                }
            ],
        },

        # L2 — Dataset Extraction Plan (includes per-dataset write path)
        "dataset_extraction_plan": {
            "description": (
                "Defines which datasets are actually extracted from the source "
                "data families listed in L1. Each dataset becomes a distinct "
                "record_type in the DC-0004 snapshot table. Write path behaviour "
                "(batch atomicity, idempotency, write mode) is specified per dataset."
            ),
            "required": True,
            "datasets": [
                {
                    "dataset_id":         f"{MARKER_DRAFT_REVIEW} e.g. DS-SETTLE",
                    "name":               f"{MARKER_DRAFT_REVIEW} Human-readable name",
                    "record_type":        f"{MARKER_DRAFT_REVIEW} e.g. settlement_price",
                    "source_families":    [],
                    "update_frequency":   f"{MARKER_DRAFT_REVIEW} Inherited or overridden from source family",
                    "extraction_trigger": f"{MARKER_DRAFT_REVIEW} schedule | event | manual",
                    "description":        f"{MARKER_DRAFT_REVIEW} What this dataset represents",
                    "row_granularity":    f"{MARKER_DRAFT_REVIEW} e.g. one contract x one business date",
                    "expected_volume":    f"{MARKER_DRAFT_REVIEW} Approximate rows per extraction run",
                    "retention_class":    f"{MARKER_DRAFT_REVIEW} live | archive",
                    # Write path behaviour (per dataset)
                    "write_mode":         f"{MARKER_DRAFT_REVIEW} append | reprocess",
                    "batch_atomicity":    f"{MARKER_DRAFT_REVIEW} all-or-nothing | partial",
                    "idempotency_key":    f"{MARKER_DRAFT_REVIEW} e.g. entity_hash_key + record_type + business_date",
                    "duplicate_run_guard": f"{MARKER_DRAFT_REVIEW} How duplicate runs are handled",
                }
            ],
        },

        # L3 — Canonical Key Resolution (includes entity resolution)
        "canonical_key_resolution": {
            "description": (
                "Defines how each extracted dataset resolves to the DC-0004 "
                "snapshot composite key and how the 6 canonical entity key columns "
                "(per PSD-0002) are derived. Also documents entity resolution "
                "mechanics, search mode expectations, and partial-key hashing."
            ),
            "required": True,
            "target_contract_ref":  "DC-0004",
            "canonical_entity_ref": "PSD-0002",
            "snapshot_key_derivation": {
                "source_code":     f"{MARKER_DRAFT_REVIEW} How source_code is determined",
                "record_type":     f"{MARKER_DRAFT_REVIEW} How record_type is determined (from L2 datasets[].record_type)",
                "entity_hash_key": "Deterministic hash of the 6 canonical key columns below",
            },
            "canonical_key_columns": [
                {
                    "column":      "clearing_house",
                    "data_type":   "String",
                    "constraints": "Non-blank",
                    "description": "Clearing house code (e.g., CME, ICE, EUREX)",
                    "source_derivation": f"{MARKER_DRAFT_REVIEW} How to obtain from source",
                },
                {
                    "column":      "exchange",
                    "data_type":   "String",
                    "constraints": "Non-blank",
                    "description": "Exchange code (e.g., XCME, IFEU)",
                    "source_derivation": f"{MARKER_DRAFT_REVIEW} How to obtain from source",
                },
                {
                    "column":      "commodity",
                    "data_type":   "String",
                    "constraints": "Non-blank",
                    "description": "Commodity or product group identifier",
                    "source_derivation": f"{MARKER_DRAFT_REVIEW} How to obtain from source",
                },
                {
                    "column":      "product_type",
                    "data_type":   "Enum",
                    "constraints": "enum: [PHY, FUT, CMB, OOP, OOF, OOC]",
                    "description": "Product type classification",
                    "source_derivation": f"{MARKER_DRAFT_REVIEW} How to obtain from source",
                },
                {
                    "column":      "product_code",
                    "data_type":   "String",
                    "constraints": "Non-blank",
                    "description": "Source-specific product code",
                    "source_derivation": f"{MARKER_DRAFT_REVIEW} How to obtain from source",
                },
                {
                    "column":      "contract",
                    "data_type":   "String",
                    "constraints": "YYYYMM or YYYYMMDD; supports wildcard in blurring search",
                    "description": "Contract period identifier",
                    "source_derivation": f"{MARKER_DRAFT_REVIEW} How to obtain from source",
                },
            ],
            "hash_key": {
                "computation": "Deterministic hash of the 6 canonical key columns (PSD-0002 PC-004)",
                "determinism_rule": (
                    "Same 6-column input must always produce the same hash_key. "
                    "Source adapters must normalise values (trim, uppercase, etc.) before hashing."
                ),
            },
            "per_dataset_key_resolution": [
                {
                    "dataset_id":       f"{MARKER_DRAFT_REVIEW} Must match an L2 dataset_id",
                    "granularity_tier": f"{MARKER_DRAFT_REVIEW} exchange-level | product-level | contract-level",
                    "populated_columns": [],
                    "null_columns":     [],
                    "hash_key_note":    f"{MARKER_DRAFT_REVIEW} How partial keys affect hash computation",
                }
            ],
            "entity_resolution": {
                "canonical_key_ref": "PSD-0002",
                "search_modes": {
                    "exact":    "O(1) hash key lookup — used by ING, MCE, DQM modules during processing",
                    "blurring": "Partial column filter with wildcard support — used for ad-hoc queries and QRY module",
                },
                "hash_determinism": (
                    "Same 6-column input must always produce the same hash_key (PSD-0002 PC-004). "
                    "Source adapters must normalise values before hashing. "
                    "For datasets at coarser granularity, unpopulated columns are set to a "
                    "deterministic sentinel value before hashing to ensure consistency."
                ),
            },
        },

        # L4 — Field Extraction Spec
        "field_extraction_spec": {
            "description": (
                "Per-dataset, per-field specification of how to obtain each "
                "attribute value from the source data. Each dataset defined in L2 "
                "should have a corresponding entry here."
            ),
            "required": True,
            "dataset_field_maps": [
                {
                    "dataset_id":         f"{MARKER_DRAFT_REVIEW} Must match an L2 dataset_id",
                    "dataset_name":       f"{MARKER_DRAFT_REVIEW} Human-readable",
                    "record_type":        f"{MARKER_DRAFT_REVIEW} Must match L2 record_type",
                    "source_record_types": [],
                    "fields": [
                        {
                            "target_field":       f"{MARKER_DRAFT_REVIEW} Field name in snapshot.content JSON",
                            "target_type":        f"{MARKER_DRAFT_REVIEW} String | Integer | Float | Boolean | Date | Enum | JSON",
                            "required":           False,
                            "source_location":    f"{MARKER_DRAFT_REVIEW} Where to find raw value",
                            "extraction_logic":   f"{MARKER_DRAFT_REVIEW} How to read the raw value",
                            "transformation_rule": f"{MARKER_DRAFT_REVIEW} How to convert raw to target",
                            "default_value":      "",
                            "validation_rule":    "",
                            "description":        f"{MARKER_DRAFT_REVIEW} Business meaning",
                            "pii":                False,
                        }
                    ],
                }
            ],
        },

        # L5 — End Result (DC-0004 snapshot mockups)
        "end_result": {
            "description": (
                "Layer 5 of the extraction pipeline. Shows the complete DC-0004 "
                "snapshot row that the extraction pipeline produces — including "
                "the composite key columns, temporal columns, and the content "
                "JSON payload populated by L4 field mappings. One mockup per "
                "dataset defined in L2."
            ),
            "required": True,
            "target_contract_ref":    "DC-0004",
            "snapshot_schema_version": f"{MARKER_DRAFT_REVIEW} DC-0004 schema version",
            "dataset_mockups": [
                {
                    "dataset_id":  f"{MARKER_DRAFT_REVIEW} Must match an L2 dataset_id",
                    "record_type": f"{MARKER_DRAFT_REVIEW} Must match L2 record_type",
                    "description": f"{MARKER_DRAFT_REVIEW} What this mockup illustrates",
                    "snapshot_row": {
                        "snapshot_id":     "<auto-generated>",
                        "source_code":     f"{MARKER_DRAFT_REVIEW} e.g. MDC-0001-HKEX",
                        "entity_hash_key": "<hash of 6 canonical key columns>",
                        "record_type":     f"{MARKER_DRAFT_REVIEW} e.g. settlement_price",
                        "effective_date":  "<business_date>",
                        "expiry_date":     None,
                        "content":         {},
                        "batch_id":        "<ingestion_run.batch_id>",
                        "status":          "active",
                    },
                }
            ],
        },

        # ── Section 5 ──
        "semantic_definitions": {
            "description": (
                "Business-level definitions and rules governing how market data "
                "should be interpreted, validated, and mapped. Entity resolution "
                "mechanics are defined in Section 4 Layer L3; this section captures "
                "the business glossary and business rules only."
            ),
            "required": True,
            "business_glossary": [
                {
                    "term":       source_name,
                    "definition": f"{MARKER_DRAFT_REVIEW} Define {source_name} in business terms",
                },
                {
                    "term":       "Canonical Entity Key",
                    "definition": "The composite key (clearing_house, exchange, commodity, product_type, product_code, contract) that uniquely identifies a market data entity",
                },
            ],
            "business_rules": [
                {
                    "id":   "PC-MDC-001",
                    "rule": f"{MARKER_DRAFT_REVIEW} Define primary business rule for {source_name} data extraction",
                    "ref":  frd_id,
                },
            ],
        },

        # ── Section 6 ──
        "data_quality_standards": {
            "description": (
                "Measurable quality expectations for extracted market data. "
                "Covers completeness, conformity, uniqueness, and timeliness "
                "of canonical entity resolution output."
            ),
            "required": True,
            "quality_dimensions": [
                {
                    "dimension":  "Completeness",
                    "definition": "All expected records from the source are extracted and resolved",
                    "target":     f"{MARKER_DRAFT_REVIEW} e.g. 100% of resolved records",
                },
                {
                    "dimension":  "Conformity",
                    "definition": "All canonical key fields conform to defined formats and constraints",
                    "target":     f"{MARKER_DRAFT_REVIEW} e.g. 100% pass schema validation",
                },
                {
                    "dimension":  "Uniqueness",
                    "definition": "No duplicate hash_key values within a single extraction batch",
                    "target":     "0 duplicates per batch",
                },
                {
                    "dimension":  "Timeliness",
                    "definition": "Data is available within the agreed SLA window after source availability",
                    "target":     f"{MARKER_DRAFT_REVIEW} e.g. within 30 minutes of source availability",
                },
            ],
            "custom_checks": [
                {
                    "check_id":    "QC-MDC-001",
                    "description": f"{MARKER_DRAFT_REVIEW} Custom quality check for {source_name}",
                    "applies_to":  f"{MARKER_DRAFT_REVIEW} Which field or process",
                },
            ],
        },

        # ── Section 7 ──
        "service_level_agreements": {
            "description": (
                "Operational commitments regarding availability, data readiness, "
                "throughput, and incident response for market data extraction."
            ),
            "required":          True,
            "availability":      f"{MARKER_DRAFT_REVIEW} e.g. 99.99%",
            "latency":           f"{MARKER_DRAFT_REVIEW} Max time from source availability to data readiness",
            "delivery_schedule": f"{MARKER_DRAFT_REVIEW} Frequency and expected delivery time",
            "throughput":        f"{MARKER_DRAFT_REVIEW} Expected and peak volume",
            "incident_response": f"{MARKER_DRAFT_REVIEW} Notification and response time commitments",
        },

        # ── Section 8 ──
        "access_and_security": {
            "description": (
                "Defines who can access the extracted market data, how access is "
                "granted, and what security controls are in place."
            ),
            "required":              True,
            "access_mechanism":      f"{MARKER_DRAFT_REVIEW} e.g. Internal pipeline only",
            "connection_details":    f"{MARKER_DRAFT_REVIEW} Endpoint, topic, table path (non-sensitive)",
            "authentication_method": f"{MARKER_DRAFT_REVIEW} OAuth2 | IAM Role | Service Account | API Key",
            "authorization_model":   f"{MARKER_DRAFT_REVIEW} RBAC | ABAC | Role-based",
            "approved_consumers":    [f"{MARKER_DRAFT_REVIEW} List of consuming modules or teams"],
            "data_masking":          f"{MARKER_DRAFT_REVIEW} Masking rules if applicable",
            "retention_policy":      f"{MARKER_DRAFT_REVIEW} Retention period and archival strategy",
        },

        # ── Section 9 ──
        "lineage_and_dependencies": {
            "description": (
                "Documents where market data comes from (upstream external sources) "
                "and where it flows to (downstream internal consumers)."
            ),
            "required": True,
            "source_systems": [
                {
                    "system":   source_name,
                    "type":     "External",
                    "delivery": delivery or f"{MARKER_DRAFT_REVIEW} Delivery mechanism",
                }
            ],
            "upstream_datasets":    [],
            "downstream_consumers": [
                {
                    "consumer":    f"{MARKER_DRAFT_REVIEW} Consuming module or team (e.g., ING, MCE, QRY, DQM)",
                    "usage":       f"{MARKER_DRAFT_REVIEW} What they use the data for",
                    "search_mode": f"{MARKER_DRAFT_REVIEW} EXACT | BLURRING",
                }
            ],
            "canonical_entity_integration": {
                "entity_search_ref": "PSD-0002",
                "resolution_flow": (
                    "Extracted records are mapped to the 6 canonical key columns, hash_key is computed, "
                    "and records are written to the canonical entity table. Downstream modules consume "
                    "via EXACT (hash key O(1) lookup) or BLURRING (partial column filter) search modes."
                ),
            },
            "transformation_summary": f"{MARKER_DRAFT_REVIEW} High-level data flow description",
        },

        # ── Section 10 ──
        "versioning_and_compatibility": {
            "description": (
                "Rules governing how this contract and its schema evolve over time. "
                "Defines what constitutes a breaking vs. non-breaking change for "
                "the canonical entity model."
            ),
            "required":            True,
            "versioning_strategy": "Semantic Versioning (MAJOR.MINOR)",
            "breaking_changes": [
                "Remove or rename canonical key fields",
                "Change hash_key computation logic (PSD-0002 PC-004)",
                "Alter field data types or product_type enum values",
            ],
            "non_breaking_changes": [
                "Add new optional output fields",
                "Add new source adapter mappings",
                "Improve descriptions or documentation",
            ],
            "deprecation_policy": f"{MARKER_DRAFT_REVIEW} Notice period and sunset process",
        },

        # ── Section 11 ──
        "sample_fixture": {
            "description": (
                "A concrete synthetic test fixture with representative placeholder "
                "values. Intended for unit test reference, QA test case writing, "
                "and new team member onboarding."
            ),
            "required": False,
            "fixture":  {},
        },

        # ── Section 12 ──
        "support_and_communication": {
            "description": (
                "How consumers can get help, report issues, and stay informed "
                "about changes to this market data product."
            ),
            "required":              False,
            "support_channel":       f"{MARKER_DRAFT_REVIEW} e.g. #team-market-data, JIRA queue",
            "documentation_url":     f"{MARKER_DRAFT_REVIEW} Link to data catalog or wiki page",
            "announcement_channel":  f"{MARKER_DRAFT_REVIEW} Where changes are communicated",
            "feedback_mechanism":    f"{MARKER_DRAFT_REVIEW} How consumers submit enhancement requests",
        },

        # ── Section 13 ──
        "attachments": {
            "description": (
                "Supporting files such as sample data files, source adapter "
                "specifications, mapping tables, or data flow diagrams."
            ),
            "required": False,
            "files":    [],
        },

        # ── Section 14 ──
        "change_log": {
            "description": "Version history of this contract document.",
            "required":    True,
            "entries": [
                {
                    "version": DRAFT_VERSION,
                    "date":    today,
                    "author":  "sdlc_chain (auto-generated)",
                    "summary": f"Initial draft scaffolded from {frd_id}",
                }
            ],
        },
    }
