"""FRD → Async Event Contract (AEC) generator.

Produces an AEC scaffold for a single published event, aligned with
41-aec_template.yaml.

Entry point
-----------
    generate_aec(frd, event_name, sequence, today)
"""
from datetime import date
from typing import List, Optional

from ..config import (
    DRAFT_VERSION,
    MARKER_AUTO_COMPLETE,
    MARKER_AUTO_REVIEW,
    MARKER_DRAFT_REVIEW,
    STATUS_DRAFT,
)
from ..naming import generate_aec_id
from ._contract_helpers import extract_common


def generate_aec(
    frd: dict,
    event_name: str,
    sequence: int = 1,
    today: Optional[str] = None,
) -> dict:
    """
    Scaffold one AEC (Async Event Contract) document.

    Args:
        frd:        Source FRD dict.
        event_name: Machine-readable event name, e.g. "order.created".
        sequence:   Numeric sequence for the document ID (AEC-NNNN).
        today:      ISO date string; defaults to today.
    """
    if today is None:
        today = date.today().isoformat()
    common = extract_common(frd, today)
    return _generate_aec(common, event_name, sequence)


# ---------------------------------------------------------------------------
# Private implementation
# ---------------------------------------------------------------------------

def _generate_aec(common: dict, event_name: str, sequence: int) -> dict:
    """Build a full AEC scaffold dict aligned with 41-aec_template.yaml."""
    frd_id      = common["frd_id"]
    module_name = common["module_name"]
    today       = common["today"]
    aec_id      = generate_aec_id(sequence)

    safe_event  = event_name.lower().replace(" ", ".").replace("-", ".")
    action      = safe_event.split(".")[-1]
    topic       = f"{common['module_slug']}.events.{action}"
    ce_type     = f"com.example.{safe_event}"
    source_uri  = f"/{module_name.lower().replace(' ', '-')}"

    return {
        "kind": "AsyncEventContract",
        "metadata": {
            "document_id":      aec_id,
            "title":            f"{event_name} Event Contract",
            "version":          DRAFT_VERSION,
            "status":           STATUS_DRAFT,
            "classification":   common["classification"],
            "created_date":     today,
            "last_updated":     today,
            "author":           common["author"],
            "reviewer":         common["reviewer"],
            "approver":         common["approver"],
            "related_documents": [frd_id],
        },

        # Section 1
        "event_overview": {
            "description": (
                "Provide a concise summary of what this event represents in the "
                "business domain, why it exists, and what downstream behavior it triggers."
            ),
            "content": {
                "event_name":           event_name,
                "domain":               module_name,
                "event_type":           f"{MARKER_AUTO_COMPLETE} Domain | Integration | System | Notification",
                "business_description": f"{MARKER_DRAFT_REVIEW} Plain-language meaning of {event_name}",
                "trigger_condition":    f"{MARKER_DRAFT_REVIEW} What action or state change produces this event",
            },
            "required": True,
        },

        # Section 2
        "ownership": {
            "description": "Identify the producing team, consuming teams, and escalation contacts.",
            "content": {
                "producer_team":    f"{MARKER_AUTO_REVIEW} {common['author'] or 'To be assigned'}",
                "producer_service": module_name,
                "producer_contact": f"{MARKER_DRAFT_REVIEW} Slack channel or email alias",
                "registered_consumers": [
                    {
                        "consumer_team":    f"{MARKER_DRAFT_REVIEW} Consumer team name",
                        "consumer_service": "",
                        "consumer_contact": "",
                        "use_case":         f"{MARKER_DRAFT_REVIEW} How this consumer uses {event_name}",
                    }
                ],
                "escalation_contact": f"{MARKER_DRAFT_REVIEW} On-call alias",
            },
            "required": True,
        },

        # Section 3
        "channel_config": {
            "description": "Kafka topic, partitioning strategy, and transport-level configuration.",
            "content": {
                "channel_name":              topic,
                "channel_naming_convention": "{domain}.events.{event_action}",
                "protocol":                  "kafka",
                "kafka_bindings": {
                    "cluster":             f"{MARKER_DRAFT_REVIEW} Kafka cluster identifier",
                    "partition_count":     None,
                    "partition_key":       f"{MARKER_DRAFT_REVIEW} Primary entity ID field, e.g. order_id",
                    "partition_strategy":  "Key-based",
                    "replication_factor":  3,
                    "retention_ms":        None,
                    "cleanup_policy":      "delete",
                    "min_insync_replicas": 2,
                    "compression_type":    f"{MARKER_DRAFT_REVIEW} none | gzip | snappy | lz4 | zstd",
                },
                "consumer_group_convention": f"{{consumer_service}}.{safe_event}.cg",
                "dead_letter_topic":         f"{topic}.dlt",
            },
            "required": True,
        },

        # Section 4
        "message_spec": {
            "description": "Message envelope, headers, and payload structure (CloudEvents-aligned).",
            "content": {
                "message_id_strategy": "UUID",
                "content_type":        "application/json",
                "encoding":            "UTF-8",
                "schema_registry": {
                    "enabled":            False,
                    "registry_url":       f"{MARKER_DRAFT_REVIEW} Schema registry URL",
                    "subject_name":       f"{topic}-value",
                    "compatibility_mode": "BACKWARD",
                },
                "headers": {
                    "description": "Standard CloudEvents-compatible message headers.",
                    "fields": [
                        {"name": "ce_id",          "type": "string", "description": "Unique event identifier (CloudEvents 'id')",                            "required": True},
                        {"name": "ce_source",      "type": "string", "description": f"URI identifying the producer: {source_uri}",                         "required": True},
                        {"name": "ce_type",        "type": "string", "description": f"CloudEvents type identifier, e.g. '{ce_type}'",                      "required": True},
                        {"name": "ce_time",        "type": "string", "description": "ISO 8601 timestamp of when the event occurred",                       "required": True},
                        {"name": "ce_specversion", "type": "string", "description": "CloudEvents specification version, e.g. '1.0'",                       "required": True},
                        {"name": "correlation_id", "type": "string", "description": "Trace/correlation ID for distributed tracing",                        "required": True},
                        {"name": "schema_version", "type": "string", "description": "Version of the payload schema",                                       "required": True},
                    ],
                },
                "payload_schema": {
                    "description": f"{MARKER_DRAFT_REVIEW} Define the {event_name} payload fields using the field structure below.",
                    "fields": _infer_payload_fields(event_name),
                },
                "sample_message": (
                    f'{{"headers": {{"ce_id": "evt-abc123", "ce_source": "{source_uri}", '
                    f'"ce_type": "{ce_type}", "ce_time": "{today}T00:00:00Z", '
                    f'"ce_specversion": "1.0", "correlation_id": "corr-xyz789", '
                    f'"schema_version": "{DRAFT_VERSION}"}}, "payload": {{}}}}'
                ),
            },
            "required": True,
        },

        # Section 5
        "data_transformation": {
            "description": (
                "How data is transformed entering (producer) and leaving (consumer) "
                "this event contract — makes mapping explicit and traceable."
            ),
            "required": True,
            "producer_mapping": {
                "source_ref":      f"{MARKER_AUTO_COMPLETE} Source API or DC contract ID",
                "source_type":     f"{MARKER_DRAFT_REVIEW} API Request | Domain Object | DB Read | Internal State",
                "field_mappings": [
                    {
                        "source_field":          f"{MARKER_DRAFT_REVIEW} source_field",
                        "payload_field":          f"{MARKER_DRAFT_REVIEW} payload_field",
                        "transformation_logic":   "",
                        "nullable_handling":      "",
                    }
                ],
                "enrichment":             [],
                "projection_exclusions":  [],
                "required":               True,
            },
            "consumer_mappings": {
                "consumers": [
                    {
                        "consumer_service":    f"{MARKER_DRAFT_REVIEW} Consumer service name",
                        "target_type":         f"{MARKER_DRAFT_REVIEW} DB Write | API Call | Read Model | Cache Update | Forward Event",
                        "target_contract_ref": f"{MARKER_AUTO_COMPLETE} DC, API, or AEC document ID",
                        "field_mappings":      [],
                        "filtering_logic":     "",
                        "ordering_sensitivity": "",
                    }
                ],
                "required": True,
            },
        },

        # Section 6
        "schema_evolution": {
            "description": "Rules for how the event schema may change without breaking existing consumers.",
            "content": {
                "compatibility_strategy": "BACKWARD",
                "allowed_changes": [
                    "Add optional fields with default values",
                    "Add new header fields",
                ],
                "breaking_changes": [
                    "Remove or rename existing fields",
                    "Change field types",
                    "Change partition key semantics",
                ],
                "deprecation_policy": {
                    "notice_period":        f"{MARKER_DRAFT_REVIEW} e.g. 30 days minimum",
                    "communication_channel": f"{MARKER_DRAFT_REVIEW} e.g. #event-contracts Slack channel",
                    "sunset_process":        f"{MARKER_DRAFT_REVIEW} Steps to retire an old schema version",
                },
                "versioning_strategy": "Header-based",
            },
            "required": True,
        },

        # Section 7
        "delivery_sla": {
            "description": "Quality-of-service expectations: latency, ordering, and reliability.",
            "content": {
                "delivery_guarantee":       f"{MARKER_DRAFT_REVIEW} At-least-once | At-most-once | Exactly-once",
                "ordering_guarantee":       "Per-partition (by key)",
                "expected_throughput":      f"{MARKER_DRAFT_REVIEW} e.g. ~500 events/sec peak",
                "max_publish_latency":      f"{MARKER_DRAFT_REVIEW} e.g. < 200ms p99",
                "max_end_to_end_latency":   f"{MARKER_DRAFT_REVIEW} e.g. < 2s from trigger to consumer",
                "availability_target":      f"{MARKER_DRAFT_REVIEW} e.g. 99.95%",
                "retry_policy": {
                    "max_retries":          3,
                    "backoff_strategy":     "Exponential",
                    "backoff_initial_ms":   500,
                    "backoff_max_ms":       30000,
                },
                "dead_letter_handling": {
                    "enabled":               True,
                    "dlt_topic":             f"{topic}.dlt",
                    "alert_on_dlt":          True,
                    "reprocessing_strategy": "Manual",
                },
                "idempotency": {
                    "required":              True,
                    "idempotency_key":       f"{MARKER_DRAFT_REVIEW} Field(s) used for deduplication",
                    "deduplication_window":  f"{MARKER_DRAFT_REVIEW} e.g. 1 hour",
                },
            },
            "required": True,
        },

        # Section 8
        "security": {
            "description": "Authentication, authorization, and data sensitivity controls.",
            "content": {
                "authentication_mechanism": f"{MARKER_DRAFT_REVIEW} mTLS | SASL/SCRAM | SASL/OAUTHBEARER | None",
                "authorization": {
                    "producer_acl": f"WRITE on topic {topic}",
                    "consumer_acl": f"READ on topic {topic}",
                },
                "data_classification": common["classification"],
                "pii_fields":          [],
                "encryption": {
                    "in_transit":       "TLS 1.3",
                    "at_rest":          f"{MARKER_DRAFT_REVIEW} e.g. AES-256 (broker-level)",
                    "field_level":      False,
                    "encrypted_fields": [],
                },
                "data_retention_compliance": f"{MARKER_DRAFT_REVIEW} Applicable regulation, e.g. GDPR Art. 17",
            },
            "required": True,
        },

        # Section 9
        "observability": {
            "description": "Monitoring, alerting, and tracing expectations.",
            "content": {
                "metrics": [
                    {"name": "event.published.count", "type": "Counter",   "description": f"Total {event_name} events published"},
                    {"name": "consumer.lag",           "type": "Gauge",     "description": "Consumer group processing lag"},
                    {"name": "event.processing.time",  "type": "Histogram", "description": "Consumer-side end-to-end processing duration"},
                ],
                "key_dashboards": [],
                "alerting_rules": [
                    {
                        "alert_name":           "ConsumerLagHigh",
                        "condition":            "consumer_lag > 10000 for 5 minutes",
                        "severity":             "Warning",
                        "notification_channel": f"{MARKER_DRAFT_REVIEW} Alert Slack channel",
                    },
                    {
                        "alert_name":           "DLTMessageReceived",
                        "condition":            f"messages on {topic}.dlt > 0",
                        "severity":             "Critical",
                        "notification_channel": f"{MARKER_DRAFT_REVIEW} Alert Slack channel",
                    },
                ],
                "distributed_tracing": {
                    "enabled":        True,
                    "trace_header":   "traceparent",
                    "tracing_system": f"{MARKER_DRAFT_REVIEW} Jaeger | Zipkin | OpenTelemetry",
                },
                "logging_requirements": (
                    "Log event_id and correlation_id at INFO level on both publish and consume."
                ),
            },
            "required": False,
        },

        # Section 10
        "testing": {
            "description": "Testing strategy for event production, consumption, schema, and failure scenarios.",
            "content": {
                "contract_testing": {
                    "tool":            f"{MARKER_DRAFT_REVIEW} Pact | Spring Cloud Contract | Custom",
                    "producer_tests":  f"{MARKER_DRAFT_REVIEW} How producer validates output against contract",
                    "consumer_tests":  f"{MARKER_DRAFT_REVIEW} How each consumer validates event handling",
                },
                "schema_validation": {
                    "validation_point": "At publish time via schema registry",
                    "reject_on_invalid": True,
                },
                "integration_test_environment": f"{MARKER_DRAFT_REVIEW} e.g. staging-kafka-cluster",
                "sample_test_events":           [],
                "chaos_testing": {
                    "enabled":   False,
                    "scenarios": [],
                },
            },
            "required": False,
        },

        # Section 11
        "dependencies": {
            "description": "Relationships to other events, services, and documents.",
            "content": {
                "upstream_events":   [],
                "downstream_events": [],
                "saga_participation": {
                    "saga_name":          "",
                    "saga_step":          "",
                    "compensating_event": "",
                },
                "related_apis":      [],
                "event_flow_diagram": "",
            },
            "required": False,
        },

        "attachments": {
            "description": "AsyncAPI spec files, Avro/Protobuf schemas, sample payloads.",
            "files": [],
        },
        "change_log": {
            "description": "All changes to this contract must be logged before the version is incremented.",
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


def _infer_payload_fields(event_name: str) -> List[dict]:
    """
    Derive a starter payload field list from the event name.

    This function currently returns a universal placeholder.

    TODO: Implement domain-aware field inference here (5-10 lines).

    You have access to the event_name (e.g. "order.created", "payment.failed").
    Consider: should you parse the action verb to add status/error fields?
    Should you derive entity ID fields from the noun (e.g. "order" → "order_id")?
    Should you inspect the FRD's data_requirements to pull entity fields directly?

    The choice shapes every AEC produced by this generator — a good inference
    saves authors significant scaffolding time for common event patterns.

    Returns:
        list of field dicts matching the AEC template payload_schema.fields shape:
        {"name": str, "type": str, "description": str, "required": bool,
         "constraints": str, "example": str}
    """
    # Starter: one required entity-id field + one placeholder
    noun    = event_name.split(".")[0] if "." in event_name else event_name
    id_name = f"{noun}_id"
    return [
        {
            "name":        id_name,
            "type":        "string",
            "description": f"Unique identifier of the {noun}",
            "required":    True,
            "constraints": "format: uuid",
            "example":     "550e8400-e29b-41d4-a716-446655440000",
        },
        {
            "name":        f"{MARKER_DRAFT_REVIEW} field_name",
            "type":        "",
            "description": "",
            "required":    True,
            "constraints": "",
            "example":     "",
        },
    ]
