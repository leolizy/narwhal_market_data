"""CICD + NFR → Deployment Guide (DG) generator.

Produces a DG scaffold from CICD pipeline design and NFR deployment/
availability requirements.

Entry point
-----------
    generate_dg(cicd, nfr, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_dg_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or "UNKNOWN"


def generate_dg(
    cicd: Optional[dict] = None,
    nfr: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate a DG scaffold aligned with 72-dg_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_dg_id(sequence)
    related = [_doc_id(a) for a in [cicd, nfr] if a and _doc_id(a) != "UNKNOWN"]

    # Extract deployment strategy from CICD if available
    deploy_strategy = MARKER_DRAFT_REVIEW
    rollback_info = MARKER_DRAFT_REVIEW
    if cicd:
        cd = cicd.get("continuous_delivery", {})
        if cd.get("deployment_strategies"):
            deploy_strategy = cd["deployment_strategies"]
        if cd.get("rollback_and_recovery"):
            rollback_info = cd["rollback_and_recovery"]

    return {
        "kind": "DeploymentGuide",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} Deployment Guide",
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
            "purpose": f"Step-by-step deployment procedures, rollback plans, and operational runbook for {system_name}.",
            "system_overview": MARKER_DRAFT_REVIEW,
            "scope": MARKER_DRAFT_REVIEW,
            "target_audience": "DevOps engineers, SREs, release managers",
            "definitions_and_acronyms": [],
            "references": [],
        },
        "deployment_architecture": {
            "topology": MARKER_DRAFT_REVIEW,
            "component_inventory": [],
            "dependency_map": MARKER_AUTO_COMPLETE,
        },
        "environment_configuration": {
            "environment_matrix": [],
            "configuration_management": MARKER_DRAFT_REVIEW,
            "secrets_management": MARKER_DRAFT_REVIEW,
            "infrastructure_as_code": MARKER_AUTO_COMPLETE,
        },
        "pre_deployment_checklist": {
            "artifact_validation": [],
            "environment_readiness": [],
            "dependency_readiness": [],
            "approval_and_communication": [],
        },
        "deployment_procedure": {
            "deployment_strategy": deploy_strategy,
            "automated_deployment": MARKER_DRAFT_REVIEW,
            "manual_deployment": MARKER_AUTO_COMPLETE,
            "database_migration": MARKER_DRAFT_REVIEW,
        },
        "post_deployment_verification": {
            "smoke_tests": [],
            "health_checks": [],
            "monitoring_verification": MARKER_DRAFT_REVIEW,
            "traffic_validation": MARKER_AUTO_COMPLETE,
            "signoff": MARKER_DRAFT_REVIEW,
        },
        "rollback_procedure": {
            "rollback_decision_criteria": MARKER_DRAFT_REVIEW,
            "rollback_steps": rollback_info if isinstance(rollback_info, list) else [],
            "database_rollback": MARKER_DRAFT_REVIEW,
            "post_rollback_verification": MARKER_AUTO_COMPLETE,
            "rollback_communication": MARKER_AUTO_COMPLETE,
        },
        "troubleshooting_guide": {
            "common_issues": [],
            "diagnostic_commands": [],
            "log_locations": [],
        },
        "communication_plan": {
            "routine_deployment": MARKER_DRAFT_REVIEW,
            "incident_during_deployment": MARKER_DRAFT_REVIEW,
        },
        "maintenance_windows": {
            "standard_deployment_windows": MARKER_DRAFT_REVIEW,
            "blackout_periods": [],
            "emergency_deployment": MARKER_AUTO_COMPLETE,
        },
        "disaster_recovery": {
            "recovery_objectives": MARKER_DRAFT_REVIEW,
            "recovery_procedures": MARKER_AUTO_COMPLETE,
            "backup_references": [],
        },
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from CICD and NFR."}],
    }
