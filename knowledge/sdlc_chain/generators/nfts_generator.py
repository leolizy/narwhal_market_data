"""NFR + CICD + DBAD + TSI → Non-Functional Test Specification (NFTS) generator.

Produces an NFTS scaffold by deriving test scenarios from NFR catalog items
and aligning with CICD quality gates, DBAD performance baselines, and TSI
tech stack for test environment configuration.

Entry point
-----------
    generate_nfts(nfr, cicd, dbad, tsi, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_nfts_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or "UNKNOWN"


def _extract_nfr_items(nfr: Optional[dict], *categories: str) -> List[dict]:
    if not nfr:
        return []
    catalog = nfr.get("nfr_catalog", nfr.get("nonfunctional_requirements", {}))
    if not isinstance(catalog, dict):
        return []
    items = []
    for cat in categories:
        reqs = catalog.get(cat, [])
        if isinstance(reqs, list):
            for r in reqs:
                if isinstance(r, dict):
                    items.append(r)
    return items


def generate_nfts(
    nfr: Optional[dict] = None,
    cicd: Optional[dict] = None,
    dbad: Optional[dict] = None,
    tsi: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate an NFTS scaffold aligned with 71-nfts_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_nfts_id(sequence)
    related = {
        "nfr_ref": _doc_id(nfr) if nfr else MARKER_AUTO_COMPLETE,
        "cicd_ref": _doc_id(cicd) if cicd else MARKER_AUTO_COMPLETE,
        "dbad_ref": _doc_id(dbad) if dbad else MARKER_AUTO_COMPLETE,
        "tsi_ref": _doc_id(tsi) if tsi else MARKER_AUTO_COMPLETE,
        "additional": [],
    }

    perf_items = _extract_nfr_items(nfr, "performance_requirements", "performance")
    sec_items = _extract_nfr_items(nfr, "security_requirements", "security")
    avail_items = _extract_nfr_items(nfr, "availability_reliability", "availability", "reliability")
    scale_items = _extract_nfr_items(nfr, "scalability_requirements", "scalability")

    return {
        "kind": "NonFunctionalTestSpec",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} Non-Functional Test Specification",
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
            "purpose": f"Defines non-functional test scenarios, acceptance criteria, and execution approach for {system_name}.",
            "system_under_test": system_name,
            "scope": {"in_scope": [], "out_of_scope": []},
            "definitions_and_acronyms": [],
        },
        "references": [],
        "test_strategy": {
            "approach": MARKER_DRAFT_REVIEW,
            "test_types_included": ["Performance", "Security", "Reliability", "Scalability"],
            "nft_execution_sequence": MARKER_DRAFT_REVIEW,
        },
        "entry_exit_criteria": {
            "entry_criteria": [],
            "exit_criteria": [],
            "suspension_criteria": MARKER_AUTO_COMPLETE,
            "resumption_criteria": MARKER_AUTO_COMPLETE,
        },
        "test_environment": {
            "environment_name": MARKER_DRAFT_REVIEW,
            "environment_type": MARKER_DRAFT_REVIEW,
            "hardware_specifications": MARKER_AUTO_COMPLETE,
            "software_and_middleware": MARKER_AUTO_COMPLETE,
            "network_topology": MARKER_AUTO_COMPLETE,
            "test_tools": [],
            "environment_differences_from_production": MARKER_DRAFT_REVIEW,
        },
        "test_data": {
            "data_volume_requirements": MARKER_DRAFT_REVIEW,
            "data_generation_approach": MARKER_AUTO_COMPLETE,
            "data_reset_strategy": MARKER_AUTO_COMPLETE,
        },
        "performance_testing": {
            "baseline_metrics": [],
            "workload_models": [],
            "test_scenarios": _build_test_scenarios(perf_items, "PERF"),
            "monitoring_metrics": [],
        },
        "security_testing": {
            "security_framework_references": [],
            "threat_model_reference": MARKER_AUTO_COMPLETE,
            "security_test_scenarios": _build_test_scenarios(sec_items, "SEC"),
            "vulnerability_acceptance_thresholds": MARKER_DRAFT_REVIEW,
        },
        "reliability_availability_testing": {
            "availability_targets": MARKER_DRAFT_REVIEW,
            "reliability_test_scenarios": _build_test_scenarios(avail_items, "REL"),
        },
        "scalability_testing": {
            "scalability_objectives": MARKER_DRAFT_REVIEW,
            "scalability_test_scenarios": _build_test_scenarios(scale_items, "SCALE"),
        },
        "usability_testing": {
            "accessibility_standard": MARKER_AUTO_COMPLETE,
            "usability_test_scenarios": [],
        },
        "compatibility_testing": {
            "browser_compatibility": MARKER_AUTO_COMPLETE,
            "device_compatibility": MARKER_AUTO_COMPLETE,
            "integration_compatibility": MARKER_AUTO_COMPLETE,
        },
        "defect_management": {
            "severity_classification": MARKER_DRAFT_REVIEW,
            "defect_tracking_tool": MARKER_DRAFT_REVIEW,
            "defect_label_convention": MARKER_AUTO_COMPLETE,
            "retest_policy": MARKER_AUTO_COMPLETE,
        },
        "roles_and_responsibilities": [],
        "risks_and_mitigations": [],
        "reporting": [],
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from NFR, CICD, DBAD, TSI."}],
    }


def _build_test_scenarios(nfr_items: List[dict], prefix: str) -> list:
    """Convert NFR catalog items into test scenario stubs."""
    scenarios = []
    for i, item in enumerate(nfr_items[:10], 1):
        nfr_id = item.get("id", item.get("nfr_id", f"{prefix}-{i:03d}"))
        stmt = item.get("requirement", item.get("statement", MARKER_DRAFT_REVIEW))
        threshold = item.get("acceptance_criteria", item.get("threshold", MARKER_DRAFT_REVIEW))
        scenarios.append({
            "scenario_id": f"NFT-{prefix}-{i:03d}",
            "nfr_reference": nfr_id,
            "description": stmt[:200] if isinstance(stmt, str) else str(stmt)[:200],
            "acceptance_criteria": threshold,
            "test_approach": MARKER_DRAFT_REVIEW,
            "expected_result": MARKER_AUTO_COMPLETE,
            "priority": "High",
        })
    if not scenarios:
        scenarios.append({
            "scenario_id": f"NFT-{prefix}-001",
            "nfr_reference": MARKER_AUTO_COMPLETE,
            "description": MARKER_DRAFT_REVIEW,
            "acceptance_criteria": MARKER_DRAFT_REVIEW,
            "test_approach": MARKER_DRAFT_REVIEW,
            "expected_result": MARKER_AUTO_COMPLETE,
            "priority": "High",
        })
    return scenarios
