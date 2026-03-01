"""FRD → Data Contract (DC) generator.

Produces a DC scaffold for a single data entity, aligned with
43-dc_template.yaml.

Entry point
-----------
    generate_dc(frd, entity, sequence, today)
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
from ..naming import generate_dc_id
from ._contract_helpers import extract_common


def generate_dc(
    frd: dict,
    entity: dict,
    sequence: int = 1,
    today: Optional[str] = None,
) -> dict:
    """
    Scaffold one DC (Data Contract) document for a single data entity.

    Args:
        frd:      Source FRD dict.
        entity:   Entity dict from frd["data_requirements"]["entities"], or {}.
        sequence: Numeric sequence for DC-NNNN.
        today:    ISO date string; defaults to today.
    """
    if today is None:
        today = date.today().isoformat()
    common = extract_common(frd, today)
    return _generate_dc(common, entity, sequence)


# ---------------------------------------------------------------------------
# Private implementation
# ---------------------------------------------------------------------------

def _generate_dc(common: dict, entity: dict, sequence: int) -> dict:
    """Build a full DC scaffold dict aligned with 43-dc_template.yaml."""
    frd_id      = common["frd_id"]
    module_name = common["module_name"]
    today       = common["today"]
    dc_id       = generate_dc_id(sequence)

    entity_name = entity.get("entity_name", module_name) if entity else module_name
    entity_desc = entity.get("description", "")           if entity else ""
    sensitivity = entity.get("sensitivity", "")           if entity else ""
    crud_str    = entity.get("crud", "")                  if entity else ""

    # Infer data tier from sensitivity label
    tier_map = {"high": "Tier 1 (Critical)", "medium": "Tier 2 (Important)"}
    tier = tier_map.get(sensitivity.lower(), "Tier 2 (Important)") if sensitivity else f"{MARKER_DRAFT_REVIEW} Tier 1 (Critical) | Tier 2 (Important) | Tier 3 (Informational)"

    # Derive supported write modes from CRUD string
    crud_up = crud_str.upper()
    write_modes = {
        "insert":      "C" in crud_up,
        "update":      "U" in crud_up,
        "upsert":      False,
        "soft_delete": "D" in crud_up,
        "hard_delete": False,
    }

    return {
        "kind": "DataContract",
        "metadata": {
            "document_id":    dc_id,
            "title":          f"{entity_name} Data Contract",
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

        # Section 1
        "contract_overview": {
            "description": "High-level summary of this data contract — dataset, business context, and why it exists.",
            "content": (
                entity_desc
                or f"{MARKER_DRAFT_REVIEW} Describe what dataset '{entity_name}' governs and the business context it supports."
            ),
            "required": True,
        },

        # Section 2
        "data_product_identification": {
            "description": "Unique identification, ownership, domain, and classification metadata.",
            "required":     True,
            "product_name": entity_name,
            "product_id":   f"{MARKER_DRAFT_REVIEW} Unique ID in the data catalog",
            "domain":       module_name,
            "subdomain":    f"{MARKER_DRAFT_REVIEW} Optional subdomain",
            "owner_team":   f"{MARKER_AUTO_REVIEW} {common['author'] or 'To be assigned'}",
            "owner_contact": f"{MARKER_DRAFT_REVIEW} Email or Slack channel",
            "data_steward": f"{MARKER_DRAFT_REVIEW} Individual responsible for data quality",
            "tier":         tier,
            "tags":         [],
        },

        # Section 3
        "schema_definition": {
            "description": (
                "The authoritative schema — every field, type, constraint, and semantic meaning. "
                "Consumers rely on this not changing without notice."
            ),
            "required":           True,
            "schema_format":      f"{MARKER_DRAFT_REVIEW} Avro | Protobuf | JSON Schema | DDL | Parquet | Custom",
            "schema_version":     DRAFT_VERSION,
            "schema_registry_url": f"{MARKER_DRAFT_REVIEW} URL to schema registry entry",
            "fields": [
                {
                    "name":          "id",
                    "description":   f"Unique identifier of the {entity_name}",
                    "data_type":     "string",
                    "logical_type":  "uuid",
                    "nullable":      False,
                    "primary_key":   True,
                    "foreign_key":   "",
                    "default_value": "",
                    "constraints":   "format: uuid",
                    "pii":           False,
                    "sensitive":     False,
                    "example":       "550e8400-e29b-41d4-a716-446655440000",
                    "tags":          [],
                },
                {
                    "name":          f"{MARKER_DRAFT_REVIEW} field_name",
                    "description":   "",
                    "data_type":     f"{MARKER_DRAFT_REVIEW} string | integer | float | boolean | date | timestamp | array | struct",
                    "logical_type":  "",
                    "nullable":      True,
                    "primary_key":   False,
                    "foreign_key":   "",
                    "default_value": "",
                    "constraints":   "",
                    "pii":           False,
                    "sensitive":     False,
                    "example":       "",
                    "tags":          [],
                },
            ],
        },

        # Section 4
        "semantic_definitions": {
            "description": "Business-level definitions and validation rules to prevent ambiguity between producer and consumer teams.",
            "required":     True,
            "business_glossary": [
                {
                    "term":            entity_name,
                    "definition":      f"{MARKER_DRAFT_REVIEW} Define {entity_name} in business terms",
                    "source_of_truth": frd_id,
                }
            ],
            "business_rules": [
                {
                    "rule_id":          "PC-001",
                    "description":      f"{MARKER_DRAFT_REVIEW} Define business rule for {entity_name}",
                    "validation_logic": "",
                    "severity":         "Critical",
                    "action_on_failure": "Reject",
                }
            ],
        },

        # Section 5
        "write_path_contract": {
            "description": (
                "Guarantees and constraints governing how data is written into this dataset. "
                "Bridges DBC postconditions and the physical database layer (DBAD)."
            ),
            "required":          True,
            "db_architecture_ref": f"{MARKER_AUTO_COMPLETE} DBAD document ID",
            "transaction_guarantees": {
                "description":          "ACID guarantees for write operations.",
                "isolation_level":      f"{MARKER_DRAFT_REVIEW} READ COMMITTED | REPEATABLE READ | SERIALIZABLE",
                "transaction_boundary": f"{MARKER_DRAFT_REVIEW} Single Row | Single Table | Multi-Table",
                "atomicity_notes":      f"{MARKER_DRAFT_REVIEW} Describe atomicity boundaries",
                "rollback_guarantee":   f"{MARKER_DRAFT_REVIEW} What is guaranteed to be undone on failure",
                "required":             True,
            },
            "idempotency": {
                "description":           "Idempotency contract for write operations.",
                "supported":             True,
                "idempotency_key_fields": ["id"],
                "deduplication_window":  f"{MARKER_DRAFT_REVIEW} e.g. 24 hours | indefinite",
                "on_duplicate_behavior": f"{MARKER_DRAFT_REVIEW} Ignore | Upsert | Reject | Return existing",
                "required":              True,
            },
            "locking_strategy": {
                "description":       "Concurrency control strategy.",
                "strategy":          f"{MARKER_DRAFT_REVIEW} Optimistic | Pessimistic | None",
                "conflict_resolution": f"{MARKER_DRAFT_REVIEW} Last-Write-Wins | First-Write-Wins | Merge | Reject",
                "lock_timeout":      f"{MARKER_DRAFT_REVIEW} e.g. 5 seconds",
                "retry_policy":      "3 retries with exponential backoff",
                "required":          True,
            },
            "write_modes": {
                "description":           "Permitted write operations.",
                "supported_operations":  write_modes,
                "soft_delete_field":     f"{MARKER_DRAFT_REVIEW} Field name for soft delete flag (if applicable)",
                "required":              True,
            },
            "batch_write_behaviour": {
                "description":             "Constraints for batch/bulk write operations.",
                "max_batch_size":          None,
                "partial_failure_handling": f"{MARKER_DRAFT_REVIEW} All-or-nothing | Best-effort | Per-record result",
                "ordering_guarantee":      "None",
                "required":                False,
            },
            "transformation_contract": {
                "description":       "Mapping between upstream payload and stored schema.",
                "source_schema_ref": f"{MARKER_AUTO_COMPLETE} API or AEC document ID",
                "transformations":   [
                    {
                        "source_field":        f"{MARKER_DRAFT_REVIEW} source_field",
                        "target_field":        f"{MARKER_DRAFT_REVIEW} target_field",
                        "transformation_logic": "",
                        "nullable_handling":   "",
                    }
                ],
                "enrichment_sources": [],
                "required":          False,
            },
        },

        # Section 6
        "data_quality_standards": {
            "description": "Measurable quality expectations the data producer commits to.",
            "required":     True,
            "quality_dimensions": {
                "completeness": {
                    "description":       "Percentage of non-null values in required fields",
                    "threshold":         f"{MARKER_DRAFT_REVIEW} e.g. >= 99.5%",
                    "measurement_method": f"{MARKER_DRAFT_REVIEW} SQL query | Great Expectations | dbt test",
                },
                "accuracy": {
                    "description":       "Degree to which data correctly represents real-world entities",
                    "threshold":         f"{MARKER_DRAFT_REVIEW}",
                    "measurement_method": f"{MARKER_DRAFT_REVIEW}",
                },
                "freshness": {
                    "description":       "Maximum allowed age of the most recent record",
                    "threshold":         f"{MARKER_DRAFT_REVIEW} e.g. <= 15 minutes",
                    "measurement_method": f"{MARKER_DRAFT_REVIEW}",
                },
                "uniqueness": {
                    "description":       "No duplicate records on the defined primary key",
                    "threshold":         "0 duplicates",
                    "measurement_method": f"{MARKER_DRAFT_REVIEW}",
                },
                "consistency": {
                    "description":       "Values are consistent across related datasets",
                    "threshold":         f"{MARKER_DRAFT_REVIEW}",
                    "measurement_method": f"{MARKER_DRAFT_REVIEW}",
                },
                "validity": {
                    "description":       "Data conforms to defined formats and constraints",
                    "threshold":         f"{MARKER_DRAFT_REVIEW}",
                    "measurement_method": f"{MARKER_DRAFT_REVIEW}",
                },
            },
            "custom_checks": [],
        },

        # Section 7
        "service_level_agreements": {
            "description": "Operational commitments from the data producer.",
            "required":     True,
            "availability": {
                "target":               f"{MARKER_DRAFT_REVIEW} e.g. 99.9%",
                "measurement_window":   "monthly",
                "exclusions":           f"{MARKER_DRAFT_REVIEW} Planned maintenance windows",
            },
            "latency": {
                "ingestion_latency":   f"{MARKER_DRAFT_REVIEW} Max time from source event to landing",
                "processing_latency":  f"{MARKER_DRAFT_REVIEW} Max time from landing to ready-for-consumption",
                "end_to_end_latency":  f"{MARKER_DRAFT_REVIEW} Source event to consumer-accessible",
            },
            "delivery_schedule": {
                "frequency":             f"{MARKER_DRAFT_REVIEW} Real-time | Hourly | Daily | Weekly | On-demand",
                "expected_delivery_time": f"{MARKER_DRAFT_REVIEW} e.g. Daily by 06:00 UTC",
                "timezone":              "UTC",
            },
            "throughput": {
                "expected_volume":  f"{MARKER_DRAFT_REVIEW} e.g. ~500K records/day",
                "max_volume":       f"{MARKER_DRAFT_REVIEW} Peak capacity",
                "record_size_limit": f"{MARKER_DRAFT_REVIEW} Max size per record",
            },
            "incident_response": {
                "notification_channel": f"{MARKER_DRAFT_REVIEW} e.g. #data-incidents Slack channel",
                "response_time":        f"{MARKER_DRAFT_REVIEW} e.g. < 1 hour for Tier 1",
                "resolution_time":      f"{MARKER_DRAFT_REVIEW} e.g. < 4 hours for Tier 1",
                "escalation_path":      f"{MARKER_DRAFT_REVIEW} Escalation path",
            },
        },

        # Section 8
        "access_and_security": {
            "description": "Who can access this dataset, how access is granted, and security controls.",
            "required":     True,
            "access_mechanism":   f"{MARKER_DRAFT_REVIEW} e.g. SQL via Snowflake | Kafka topic | S3 bucket | API",
            "connection_details": f"{MARKER_DRAFT_REVIEW} Endpoint or topic name (non-sensitive)",
            "authentication_method": f"{MARKER_DRAFT_REVIEW} OAuth2 | IAM Role | Service Account | API Key",
            "authorization_model":   f"{MARKER_DRAFT_REVIEW} RBAC | ABAC | Column-level | Row-level",
            "approved_consumers": [
                {
                    "team":         f"{MARKER_DRAFT_REVIEW} Consumer team name",
                    "access_level": f"{MARKER_DRAFT_REVIEW} Read | Read-Write | Admin",
                    "granted_date": today,
                    "expiry_date":  "",
                }
            ],
            "data_masking": [],
            "retention_policy": {
                "retention_period":  f"{MARKER_DRAFT_REVIEW} e.g. 3 years | indefinite",
                "archival_strategy": f"{MARKER_DRAFT_REVIEW} e.g. Move to cold storage after 1 year",
                "deletion_procedure": f"{MARKER_DRAFT_REVIEW} Steps for GDPR/regulatory deletion",
            },
        },

        # Section 9
        "lineage_and_dependencies": {
            "description": "Where the data comes from (upstream) and where it flows to (downstream).",
            "required":     True,
            "source_systems": [
                {
                    "system_name":       module_name,
                    "description":       f"{module_name} service writes via API/event",
                    "extraction_method": f"{MARKER_DRAFT_REVIEW} CDC | Full Load | API Pull | Streaming",
                    "refresh_frequency": f"{MARKER_DRAFT_REVIEW}",
                }
            ],
            "upstream_datasets":    [],
            "downstream_consumers": [],
            "transformation_summary": f"{MARKER_DRAFT_REVIEW} High-level description of transformations applied",
        },

        # Section 10
        "versioning_and_compatibility": {
            "description": "Rules governing how this contract and its schema evolve over time.",
            "required":     True,
            "versioning_strategy": "Semantic Versioning (MAJOR.MINOR.PATCH)",
            "breaking_changes": {
                "definition":         "Removing fields, changing types, renaming fields, changing PKs, altering business rule semantics.",
                "notification_period": f"{MARKER_DRAFT_REVIEW} e.g. 30 days minimum",
                "migration_support":  f"{MARKER_DRAFT_REVIEW} e.g. Dual-publish for 2 sprints",
            },
            "non_breaking_changes": {
                "definition":         "Adding new nullable fields, improving descriptions, relaxing constraints.",
                "notification_period": "In next release notes",
            },
            "deprecation_policy": {
                "notice_period": f"{MARKER_DRAFT_REVIEW} e.g. 90 days",
                "sunset_process": f"{MARKER_DRAFT_REVIEW} Steps before retiring a field or dataset",
            },
        },

        # Section 11
        "support_and_communication": {
            "description": "How consumers can get help and stay informed about changes.",
            "required":     False,
            "support_channel":     f"{MARKER_DRAFT_REVIEW} e.g. #team-data-platform, JIRA queue",
            "documentation_url":   f"{MARKER_DRAFT_REVIEW} Link to data catalog or wiki page",
            "office_hours":        "",
            "announcement_channel": f"{MARKER_DRAFT_REVIEW} Where breaking changes are communicated",
            "feedback_mechanism":  f"{MARKER_DRAFT_REVIEW} How consumers submit enhancement requests",
        },

        "attachments": {
            "description": "ERD diagrams, sample data files, schema registry exports, data flow diagrams.",
            "required":    False,
            "files":       [],
        },
        "change_log": {
            "description": "Version history of this contract document.",
            "required":    True,
            "entries": [
                {
                    "version": DRAFT_VERSION,
                    "date":    today,
                    "author":  "sdlc_chain (auto-generated)",
                    "changes": f"Initial draft scaffolded from {frd_id}",
                }
            ],
        },
    }
