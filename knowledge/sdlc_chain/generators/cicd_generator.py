"""NFR → CI/CD Framework (CICD) generator.

Produces a CICD scaffold from NFR artifacts, mapping performance,
security, and deployment requirements into pipeline design.

Entry point
-----------
    generate_cicd(nfr, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_cicd_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or "UNKNOWN"


def _extract_nfr_items(nfr: Optional[dict], *categories: str) -> List[str]:
    """Extract requirement statements from NFR catalog categories."""
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


def generate_cicd(
    nfr: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate a CICD scaffold aligned with 73-cicd_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_cicd_id(sequence)
    related = []
    if nfr and _doc_id(nfr) != "UNKNOWN":
        related.append(_doc_id(nfr))

    perf_reqs = _extract_nfr_items(nfr, "performance_requirements", "performance")
    sec_reqs = _extract_nfr_items(nfr, "security_requirements", "security")
    deploy_reqs = _extract_nfr_items(nfr, "deployment_requirements", "availability_reliability")

    return {
        "kind": "CICDFramework",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} CI/CD Framework & Handbook",
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
            "purpose": f"Defines the CI/CD pipeline design, quality gates, and deployment strategy for {system_name}.",
            "scope": MARKER_DRAFT_REVIEW,
            "target_audience": "DevOps engineers, developers, release managers",
            "definitions_and_acronyms": [],
            "references": [],
        },
        "principles_and_strategy": {
            "core_principles": [],
            "ci_cd_maturity_model": MARKER_DRAFT_REVIEW,
            "strategic_goals": [],
        },
        "source_control_strategy": {
            "branching_strategy": MARKER_DRAFT_REVIEW,
            "commit_standards": MARKER_AUTO_COMPLETE,
            "code_review_policy": MARKER_DRAFT_REVIEW,
        },
        "continuous_integration": {
            "build_pipeline": MARKER_DRAFT_REVIEW,
            "build_standards": MARKER_AUTO_COMPLETE,
            "automated_testing_in_ci": MARKER_DRAFT_REVIEW,
            "artifact_management": MARKER_AUTO_COMPLETE,
            "nfr_performance_inputs": perf_reqs or [MARKER_AUTO_COMPLETE],
        },
        "continuous_delivery": {
            "deployment_pipeline": MARKER_DRAFT_REVIEW,
            "environment_strategy": MARKER_DRAFT_REVIEW,
            "deployment_strategies": MARKER_DRAFT_REVIEW,
            "release_management": MARKER_AUTO_COMPLETE,
            "rollback_and_recovery": MARKER_DRAFT_REVIEW,
            "nfr_deployment_inputs": deploy_reqs or [MARKER_AUTO_COMPLETE],
        },
        "quality_gates": {
            "gate_definitions": [],
            "approval_workflows": MARKER_DRAFT_REVIEW,
            "compliance_and_audit": MARKER_AUTO_COMPLETE,
        },
        "security": {
            "pipeline_security": MARKER_DRAFT_REVIEW,
            "application_security_scanning": MARKER_DRAFT_REVIEW,
            "supply_chain_security": MARKER_AUTO_COMPLETE,
            "nfr_security_inputs": sec_reqs or [MARKER_AUTO_COMPLETE],
        },
        "monitoring_and_feedback": {
            "pipeline_monitoring": MARKER_DRAFT_REVIEW,
            "deployment_monitoring": MARKER_AUTO_COMPLETE,
            "dora_metrics": MARKER_AUTO_COMPLETE,
            "feedback_loops": [],
        },
        "pipeline_templates": {
            "standard_pipeline_definitions": [],
            "shared_libraries_and_reusable_components": [],
            "naming_conventions": MARKER_AUTO_COMPLETE,
        },
        "roles_and_responsibilities": {"raci_matrix": [], "team_ownership": []},
        "exception_process": {"exception_handling": MARKER_DRAFT_REVIEW, "escalation_matrix": []},
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from NFR."}],
    }
