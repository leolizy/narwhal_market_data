"""NFR → Technology Stack Inventory (TSI) generator.

Produces a TSI scaffold from NFR artifacts, mapping integration,
monitoring, and security requirements into a tech stack registry.

Entry point
-----------
    generate_tsi(nfr, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_tsi_id


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


def generate_tsi(
    nfr: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate a TSI scaffold aligned with 62-tsi_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_tsi_id(sequence)
    related = []
    if nfr and _doc_id(nfr) != "UNKNOWN":
        related.append(_doc_id(nfr))

    integration_reqs = _extract_nfr_items(nfr, "integration_requirements", "integration")
    monitoring_reqs = _extract_nfr_items(nfr, "monitoring_observability", "monitoring")
    sec_reqs = _extract_nfr_items(nfr, "security_requirements", "security")

    return {
        "kind": "TechnicalSystemIntegration",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} Technology Stack Inventory",
            "version": DRAFT_VERSION,
            "status": STATUS_DRAFT,
            "classification": "Internal",
            "created_date": today,
            "last_updated": today,
            "author": MARKER_DRAFT_REVIEW,
            "reviewer": MARKER_DRAFT_REVIEW,
            "approver": MARKER_DRAFT_REVIEW,
            "system_name": system_name,
            "system_id": MARKER_AUTO_COMPLETE,
            "related_documents": related,
        },
        "executive_summary": {"content": MARKER_DRAFT_REVIEW},
        "system_context": {
            "content": MARKER_DRAFT_REVIEW,
            "system_boundary": MARKER_AUTO_COMPLETE,
            "architecture_style": MARKER_DRAFT_REVIEW,
            "context_diagram_ref": MARKER_AUTO_COMPLETE,
            "upstream_systems": [],
            "downstream_systems": [],
            "nfr_integration_inputs": integration_reqs or [MARKER_AUTO_COMPLETE],
        },
        "technology_stack_summary": {
            "categories": [
                {"category_name": "Presentation Layer", "technologies": []},
                {"category_name": "Application Layer", "technologies": []},
                {"category_name": "Data Layer", "technologies": []},
                {"category_name": "Infrastructure Layer", "technologies": []},
                {"category_name": "Security Layer", "technologies": []},
                {"category_name": "Observability Layer", "technologies": []},
                {"category_name": "CI/CD Layer", "technologies": []},
                {"category_name": "Integration Layer", "technologies": []},
            ],
        },
        "technology_registry": [],
        "version_compatibility_matrix": {"content": MARKER_AUTO_COMPLETE, "matrix_entries": []},
        "licensing_summary": {"content": MARKER_AUTO_COMPLETE, "license_entries": []},
        "eol_deprecation_tracker": {"content": MARKER_AUTO_COMPLETE, "entries": []},
        "security_considerations": {
            "content": MARKER_DRAFT_REVIEW,
            "vulnerability_scanning_tool": MARKER_DRAFT_REVIEW,
            "last_scan_date": MARKER_AUTO_COMPLETE,
            "critical_vulnerabilities": 0,
            "security_notes": MARKER_AUTO_COMPLETE,
            "nfr_security_inputs": sec_reqs or [MARKER_AUTO_COMPLETE],
        },
        "architecture_decision_references": [],
        "dependency_map": {"content": MARKER_AUTO_COMPLETE, "diagram_ref": MARKER_AUTO_COMPLETE, "critical_dependencies": []},
        "operational_notes": {
            "content": MARKER_AUTO_COMPLETE,
            "nfr_monitoring_inputs": monitoring_reqs or [MARKER_AUTO_COMPLETE],
        },
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from NFR."}],
    }
