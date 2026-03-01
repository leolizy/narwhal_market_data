"""NFTS + DG + NFRAR → MVP Delivery Task List generator.

Produces an MVP scaffold by deriving workstreams from NFTS test types,
DG deployment procedures, and NFRAR remediation items.

Entry point
-----------
    generate_mvp(nfts, dg, nfrar, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_mvp_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or "UNKNOWN"


def generate_mvp(
    nfts: Optional[dict] = None,
    dg: Optional[dict] = None,
    nfrar: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate an MVP scaffold aligned with 91-mvp_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_mvp_id(sequence)
    related = [_doc_id(a) for a in [nfts, dg, nfrar] if a and _doc_id(a) != "UNKNOWN"]

    workstreams = _build_workstreams(nfts, dg, nfrar)

    return {
        "kind": "MinimumViableProductPlan",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} MVP Delivery Task List",
            "version": DRAFT_VERSION,
            "status": STATUS_DRAFT,
            "classification": "Internal",
            "created_date": today,
            "last_updated": today,
            "author": MARKER_DRAFT_REVIEW,
            "product_owner": MARKER_DRAFT_REVIEW,
            "tech_lead": MARKER_DRAFT_REVIEW,
            "release_target": MARKER_DRAFT_REVIEW,
            "related_documents": related,
        },
        "mvp_objective": {"content": MARKER_DRAFT_REVIEW},
        "success_criteria": [
            {"criterion": MARKER_DRAFT_REVIEW, "metric": MARKER_AUTO_COMPLETE, "target": MARKER_AUTO_COMPLETE},
        ],
        "scope": {
            "in_scope": [],
            "out_of_scope": [],
            "assumptions": [],
        },
        "tasks": {"workstreams": workstreams},
        "dependencies_and_risks": {
            "dependencies": [],
            "risks": [],
        },
        "timeline": {"milestones": []},
        "definition_of_done": {"checklist": []},
        "communication": {
            "standup_cadence": MARKER_DRAFT_REVIEW,
            "status_report_frequency": MARKER_AUTO_COMPLETE,
            "escalation_path": MARKER_AUTO_COMPLETE,
        },
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from NFTS, DG, NFRAR."}],
    }


def _build_workstreams(nfts: Optional[dict], dg: Optional[dict], nfrar: Optional[dict]) -> list:
    workstreams = []
    task_seq = 1

    # Workstream from NFTS test types
    if nfts:
        test_tasks = []
        for section_key in ["performance_testing", "security_testing", "reliability_availability_testing", "scalability_testing"]:
            section = nfts.get(section_key, {})
            if section:
                test_tasks.append({
                    "id": f"MVP-T{task_seq:03d}",
                    "title": f"Execute {section_key.replace('_', ' ').title()}",
                    "description": MARKER_DRAFT_REVIEW,
                    "owner": MARKER_DRAFT_REVIEW,
                    "priority": "High",
                    "estimate": MARKER_AUTO_COMPLETE,
                    "status": "Not Started",
                    "blocked_by": [],
                    "acceptance_criteria": MARKER_AUTO_COMPLETE,
                    "notes": "",
                })
                task_seq += 1
        if test_tasks:
            workstreams.append({"workstream_name": "Non-Functional Testing", "tasks": test_tasks})

    # Workstream from DG deployment procedure
    if dg:
        deploy_tasks = [{
            "id": f"MVP-T{task_seq:03d}",
            "title": "Validate Deployment Procedure",
            "description": "Execute deployment guide in staging environment and verify all steps.",
            "owner": MARKER_DRAFT_REVIEW,
            "priority": "High",
            "estimate": MARKER_AUTO_COMPLETE,
            "status": "Not Started",
            "blocked_by": [],
            "acceptance_criteria": MARKER_AUTO_COMPLETE,
            "notes": "",
        }]
        task_seq += 1
        deploy_tasks.append({
            "id": f"MVP-T{task_seq:03d}",
            "title": "Validate Rollback Procedure",
            "description": "Test rollback procedure to confirm recovery capability.",
            "owner": MARKER_DRAFT_REVIEW,
            "priority": "High",
            "estimate": MARKER_AUTO_COMPLETE,
            "status": "Not Started",
            "blocked_by": [],
            "acceptance_criteria": MARKER_AUTO_COMPLETE,
            "notes": "",
        })
        task_seq += 1
        workstreams.append({"workstream_name": "Deployment Readiness", "tasks": deploy_tasks})

    # Workstream from NFRAR remediation items
    if nfrar:
        recs = nfrar.get("recommendations", {}).get("key_recommendations", [])
        if recs:
            remediation_tasks = []
            for rec in recs[:5]:
                rec_text = rec if isinstance(rec, str) else rec.get("recommendation", MARKER_DRAFT_REVIEW) if isinstance(rec, dict) else str(rec)
                remediation_tasks.append({
                    "id": f"MVP-T{task_seq:03d}",
                    "title": f"Address: {rec_text[:60]}",
                    "description": rec_text,
                    "owner": MARKER_DRAFT_REVIEW,
                    "priority": "Medium",
                    "estimate": MARKER_AUTO_COMPLETE,
                    "status": "Not Started",
                    "blocked_by": [],
                    "acceptance_criteria": MARKER_AUTO_COMPLETE,
                    "notes": "",
                })
                task_seq += 1
            workstreams.append({"workstream_name": "NFRAR Remediation", "tasks": remediation_tasks})

    # Default workstream if nothing was derived
    if not workstreams:
        workstreams.append({
            "workstream_name": MARKER_DRAFT_REVIEW,
            "tasks": [{
                "id": "MVP-T001",
                "title": MARKER_DRAFT_REVIEW,
                "description": MARKER_DRAFT_REVIEW,
                "owner": MARKER_DRAFT_REVIEW,
                "priority": "High",
                "estimate": MARKER_AUTO_COMPLETE,
                "status": "Not Started",
                "blocked_by": [],
                "acceptance_criteria": MARKER_AUTO_COMPLETE,
                "notes": "",
            }],
        })

    return workstreams
