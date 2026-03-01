"""NFR → Database Architecture Design (DBAD) generator.

Produces a DBAD scaffold from NFR artifacts, mapping data, scalability,
and security requirements into database design decisions.

Entry point
-----------
    generate_dbad(nfr, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_dbad_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or "UNKNOWN"


def _extract_nfr_items(nfr: Optional[dict], *categories: str) -> List[str]:
    if not nfr:
        return []
    catalog = nfr.get("nfr_catalog", nfr.get("nonfunctional_requirements", {}))
    if not isinstance(catalog, dict):
        return []
    items = []
    for cat in categories:
        reqs = catalog.get(cat, [])
        if isinstance(reqs, list):
            for r in reqs[:3]:
                stmt = r.get("requirement", r.get("statement", "")) if isinstance(r, dict) else str(r)
                if stmt:
                    items.append(stmt[:150])
    return items


def generate_dbad(
    nfr: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate a DBAD scaffold aligned with 74-dbad_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_dbad_id(sequence)
    related = []
    if nfr and _doc_id(nfr) != "UNKNOWN":
        related.append(_doc_id(nfr))

    data_reqs = _extract_nfr_items(nfr, "data_requirements", "data")
    scale_reqs = _extract_nfr_items(nfr, "scalability_requirements", "scalability")
    sec_reqs = _extract_nfr_items(nfr, "security_requirements", "security")
    avail_reqs = _extract_nfr_items(nfr, "availability_reliability", "availability")

    return {
        "kind": "DatabaseArchitectureDesign",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} Database Architecture Design",
            "project_name": system_name,
            "version": DRAFT_VERSION,
            "status": STATUS_DRAFT,
            "classification": "Internal",
            "created_date": today,
            "last_updated": today,
            "author": MARKER_DRAFT_REVIEW,
            "reviewer": MARKER_DRAFT_REVIEW,
            "approver": MARKER_DRAFT_REVIEW,
            "related_documents": related,
        },
        "introduction": {
            "purpose": f"Defines the database architecture, data model, and data management strategy for {system_name}.",
            "scope": MARKER_DRAFT_REVIEW,
            "definitions_and_acronyms": [],
            "references": [],
        },
        "architecture_overview": {
            "summary": MARKER_DRAFT_REVIEW,
            "technology_stack": MARKER_DRAFT_REVIEW,
            "architecture_pattern": MARKER_DRAFT_REVIEW,
            "deployment_topology": MARKER_AUTO_COMPLETE,
        },
        "logical_data_model": {
            "entity_relationship_diagram": MARKER_AUTO_COMPLETE,
            "entity_descriptions": [],
            "relationships": [],
            "nfr_data_inputs": data_reqs or [MARKER_AUTO_COMPLETE],
        },
        "physical_data_model": {
            "schema_organization": MARKER_DRAFT_REVIEW,
            "table_definitions": [],
            "naming_conventions": MARKER_DRAFT_REVIEW,
            "data_types_and_standards": MARKER_AUTO_COMPLETE,
        },
        "indexing_strategy": {"index_design": [], "indexing_guidelines": MARKER_DRAFT_REVIEW},
        "data_access_patterns": {
            "query_patterns": [],
            "connection_management": MARKER_DRAFT_REVIEW,
            "orm_and_data_access_layer": MARKER_AUTO_COMPLETE,
        },
        "partitioning_and_sharding": {
            "partitioning_strategy": MARKER_DRAFT_REVIEW,
            "sharding_strategy": MARKER_AUTO_COMPLETE,
            "nfr_scalability_inputs": scale_reqs or [MARKER_AUTO_COMPLETE],
        },
        "security_and_access_control": {
            "authentication": MARKER_DRAFT_REVIEW,
            "authorization": MARKER_DRAFT_REVIEW,
            "encryption": MARKER_DRAFT_REVIEW,
            "data_masking_and_anonymization": MARKER_AUTO_COMPLETE,
            "audit_logging": MARKER_DRAFT_REVIEW,
            "nfr_security_inputs": sec_reqs or [MARKER_AUTO_COMPLETE],
        },
        "backup_and_recovery": {
            "backup_strategy": MARKER_DRAFT_REVIEW,
            "recovery_objectives": MARKER_DRAFT_REVIEW,
            "recovery_procedures": MARKER_AUTO_COMPLETE,
            "disaster_recovery": MARKER_DRAFT_REVIEW,
            "nfr_availability_inputs": avail_reqs or [MARKER_AUTO_COMPLETE],
        },
        "performance_and_optimization": {
            "capacity_planning": MARKER_DRAFT_REVIEW,
            "performance_baselines": MARKER_AUTO_COMPLETE,
            "optimization_techniques": [],
            "configuration_tuning": MARKER_AUTO_COMPLETE,
        },
        "migration_and_versioning": {
            "migration_tool": MARKER_DRAFT_REVIEW,
            "migration_strategy": MARKER_DRAFT_REVIEW,
            "seed_and_reference_data": MARKER_AUTO_COMPLETE,
        },
        "monitoring_and_alerting": {
            "monitoring_tools": MARKER_DRAFT_REVIEW,
            "key_metrics": [],
            "alerting_and_escalation": MARKER_AUTO_COMPLETE,
        },
        "high_availability": {
            "replication_topology": MARKER_DRAFT_REVIEW,
            "failover_procedures": MARKER_AUTO_COMPLETE,
            "maintenance_windows": MARKER_AUTO_COMPLETE,
        },
        "data_lifecycle_management": {
            "data_retention": MARKER_DRAFT_REVIEW,
            "archival_strategy": MARKER_AUTO_COMPLETE,
            "data_purging": MARKER_AUTO_COMPLETE,
        },
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from NFR."}],
    }
