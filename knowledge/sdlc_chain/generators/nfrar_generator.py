"""NFTS + NFR → NFR Acceptance Report (NFRAR) generator.

Produces an NFRAR scaffold by mapping NFR catalog items and NFTS test
scenarios into acceptance evaluation rows.

Entry point
-----------
    generate_nfrar(nfts, nfr, sequence, system_name, today)
"""
from datetime import date
from typing import List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_nfrar_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or "UNKNOWN"


def generate_nfrar(
    nfts: Optional[dict] = None,
    nfr: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate an NFRAR scaffold aligned with 82-nfrar_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_nfrar_id(sequence)
    related = [_doc_id(a) for a in [nfts, nfr] if a and _doc_id(a) != "UNKNOWN"]

    # Build result rows from NFTS test scenarios
    results = _build_results(nfts, nfr)

    return {
        "kind": "NFRAnalysisReport",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} NFR Acceptance Report",
            "version": DRAFT_VERSION,
            "status": STATUS_DRAFT,
            "classification": "Internal",
            "created_date": today,
            "last_updated": today,
            "author": MARKER_DRAFT_REVIEW,
            "reviewer": MARKER_DRAFT_REVIEW,
            "approver": MARKER_DRAFT_REVIEW,
            "nfr_category": "All",
            "related_documents": related,
        },
        "executive_summary": {
            "overall_verdict": MARKER_DRAFT_REVIEW,
            "total_nfrs_evaluated": len(results),
            "passed": 0,
            "failed": 0,
            "conditionally_accepted": 0,
            "deferred": 0,
            "summary_narrative": MARKER_DRAFT_REVIEW,
        },
        "scope_and_objectives": {
            "nfr_category": "All",
            "system_under_test": system_name,
            "module_or_component": MARKER_DRAFT_REVIEW,
            "evaluation_objectives": [],
            "in_scope": [],
            "out_of_scope": [],
            "baseline_reference": MARKER_AUTO_COMPLETE,
        },
        "acceptance_criteria_reference": _build_criteria_ref(nfr),
        "test_environment": {
            "environment_name": MARKER_DRAFT_REVIEW,
            "infrastructure": MARKER_AUTO_COMPLETE,
            "software_stack": MARKER_AUTO_COMPLETE,
            "test_data": MARKER_AUTO_COMPLETE,
            "tools_used": [],
            "deviations_from_production": MARKER_DRAFT_REVIEW,
        },
        "test_execution_summary": {
            "test_cycle": MARKER_DRAFT_REVIEW,
            "execution_start_date": MARKER_AUTO_COMPLETE,
            "execution_end_date": MARKER_AUTO_COMPLETE,
            "total_test_duration": MARKER_AUTO_COMPLETE,
            "executed_by": MARKER_DRAFT_REVIEW,
            "interruptions_or_reruns": [],
        },
        "detailed_test_results": results,
        "risk_assessment": [],
        "recommendations": {
            "overall_recommendation": MARKER_DRAFT_REVIEW,
            "key_recommendations": [],
        },
        "sign_off": [],
        "appendices": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated from NFTS and NFR."}],
    }


def _build_criteria_ref(nfr: Optional[dict]) -> list:
    if not nfr:
        return [{"nfr_id": MARKER_AUTO_COMPLETE, "title": MARKER_DRAFT_REVIEW, "acceptance_threshold": MARKER_DRAFT_REVIEW}]
    catalog = nfr.get("nfr_catalog", nfr.get("nonfunctional_requirements", {}))
    if not isinstance(catalog, dict):
        return []
    criteria = []
    for cat, items in catalog.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            criteria.append({
                "nfr_id": item.get("id", item.get("nfr_id", MARKER_AUTO_COMPLETE)),
                "title": item.get("requirement", item.get("statement", MARKER_DRAFT_REVIEW))[:120],
                "acceptance_threshold": item.get("acceptance_criteria", item.get("threshold", MARKER_DRAFT_REVIEW)),
                "category": cat,
            })
    return criteria or [{"nfr_id": MARKER_AUTO_COMPLETE, "title": MARKER_DRAFT_REVIEW, "acceptance_threshold": MARKER_DRAFT_REVIEW}]


def _build_results(nfts: Optional[dict], nfr: Optional[dict]) -> list:
    results = []
    # Try to pull test scenarios from NFTS
    if nfts:
        for section_key in ["performance_testing", "security_testing", "reliability_availability_testing", "scalability_testing"]:
            section = nfts.get(section_key, {})
            scenarios = section.get("test_scenarios", section.get("security_test_scenarios", section.get("reliability_test_scenarios", section.get("scalability_test_scenarios", []))))
            if isinstance(scenarios, list):
                for sc in scenarios:
                    if not isinstance(sc, dict):
                        continue
                    results.append({
                        "nfr_id": sc.get("nfr_reference", MARKER_AUTO_COMPLETE),
                        "nfr_title": sc.get("description", MARKER_DRAFT_REVIEW)[:120],
                        "acceptance_threshold": sc.get("acceptance_criteria", MARKER_DRAFT_REVIEW),
                        "actual_result": MARKER_AUTO_COMPLETE,
                        "verdict": MARKER_DRAFT_REVIEW,
                        "evidence": MARKER_AUTO_COMPLETE,
                        "observations": MARKER_AUTO_COMPLETE,
                        "conditions_or_waivers": "",
                        "remediation_plan": "",
                        "linked_defects": [],
                    })
    if not results:
        results.append({
            "nfr_id": MARKER_AUTO_COMPLETE,
            "nfr_title": MARKER_DRAFT_REVIEW,
            "acceptance_threshold": MARKER_DRAFT_REVIEW,
            "actual_result": MARKER_AUTO_COMPLETE,
            "verdict": MARKER_DRAFT_REVIEW,
            "evidence": MARKER_AUTO_COMPLETE,
            "observations": MARKER_AUTO_COMPLETE,
        })
    return results
