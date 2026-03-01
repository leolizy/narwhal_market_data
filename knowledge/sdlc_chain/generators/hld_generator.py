"""NFR/FRD → High-Level Design (HLD) generator.

Produces an HLD scaffold from NFR and FRD artifacts, mapping
non-functional requirements into architectural design decisions.

Entry point
-----------
    generate_hld(nfr, frd, sequence, system_name, today)
"""
from datetime import date
from typing import Any, Dict, List, Optional

from ..config import DRAFT_VERSION, MARKER_AUTO_COMPLETE, MARKER_AUTO_REVIEW, MARKER_DRAFT_REVIEW, STATUS_DRAFT
from ..naming import generate_hld_id


def _doc_id(art: dict) -> str:
    m = art.get("metadata", {})
    return m.get("document_id") or m.get("id") or art.get("document", {}).get("document_id", "") or "UNKNOWN"


def generate_hld(
    nfr: Optional[dict] = None,
    frd: Optional[dict] = None,
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """Generate an HLD scaffold aligned with 61-hld_template.yaml."""
    if today is None:
        today = date.today().isoformat()

    doc_id = generate_hld_id(sequence)
    related = [_doc_id(a) for a in [nfr, frd] if a and _doc_id(a) != "UNKNOWN"]

    return {
        "kind": "HighLevelDesign",
        "metadata": {
            "document_id": doc_id,
            "title": f"{system_name} High-Level Design",
            "version": DRAFT_VERSION,
            "status": STATUS_DRAFT,
            "classification": "Internal",
            "created_date": today,
            "last_updated": today,
            "author": MARKER_DRAFT_REVIEW,
            "reviewer": MARKER_DRAFT_REVIEW,
            "approver": MARKER_DRAFT_REVIEW,
            "project_name": system_name,
            "system_name": system_name,
            "related_documents": related,
        },
        "introduction": _build_introduction(system_name),
        "design_goals_and_constraints": _build_design_goals(nfr),
        "system_architecture_overview": _build_arch_overview(),
        "component_design": _build_components(),
        "technology_stack": _build_tech_stack(),
        "data_architecture": _build_data_arch(),
        "integration_architecture": _build_integration_arch(),
        "security_architecture": _build_security_arch(nfr),
        "deployment_architecture": _build_deployment_arch(),
        "observability_and_operations": _build_observability(nfr),
        "design_decisions": [],
        "risks_and_mitigations": [],
        "future_considerations": [],
        "glossary": [],
        "attachments": [],
        "change_log": [{"version": DRAFT_VERSION, "date": today, "author": MARKER_AUTO_REVIEW, "changes": "Initial scaffold auto-generated."}],
    }


def _build_introduction(system_name: str) -> dict:
    return {
        "purpose": f"This document describes the high-level architectural design of the {system_name} system.",
        "scope": MARKER_DRAFT_REVIEW,
        "intended_audience": "Architects, tech leads, senior developers",
        "references": [],
    }


def _build_design_goals(nfr: Optional[dict]) -> dict:
    goals = []
    if nfr:
        catalog = nfr.get("nfr_catalog", nfr.get("nonfunctional_requirements", {}))
        if isinstance(catalog, dict):
            for cat, items in catalog.items():
                if isinstance(items, list):
                    for item in items[:2]:
                        stmt = item.get("requirement", item.get("statement", "")) if isinstance(item, dict) else str(item)
                        if stmt:
                            goals.append({"goal": stmt[:120], "source": f"NFR.{cat}"})
    if not goals:
        goals.append({"goal": MARKER_DRAFT_REVIEW, "source": MARKER_AUTO_COMPLETE})
    return {"design_goals": goals, "design_constraints": [], "assumptions": []}


def _build_arch_overview() -> dict:
    return {
        "architecture_style": MARKER_DRAFT_REVIEW,
        "architecture_diagram": MARKER_AUTO_COMPLETE,
        "narrative": MARKER_DRAFT_REVIEW,
    }


def _build_components() -> list:
    return [{
        "component_id": "COMP-001",
        "component_name": MARKER_DRAFT_REVIEW,
        "description": MARKER_DRAFT_REVIEW,
        "responsibilities": [],
        "interfaces": [],
        "dependencies": [],
        "technology_stack": MARKER_AUTO_COMPLETE,
    }]


def _build_tech_stack() -> dict:
    return {"stack_summary": MARKER_DRAFT_REVIEW, "technology_decisions": []}


def _build_data_arch() -> dict:
    return {"data_model": MARKER_DRAFT_REVIEW, "data_flow": MARKER_AUTO_COMPLETE, "data_storage_strategy": MARKER_DRAFT_REVIEW}


def _build_integration_arch() -> dict:
    return {"internal_integrations": [], "external_integrations": [], "integration_diagram": MARKER_AUTO_COMPLETE}


def _build_security_arch(nfr: Optional[dict]) -> dict:
    sec = {}
    if nfr:
        catalog = nfr.get("nfr_catalog", nfr.get("nonfunctional_requirements", {}))
        if isinstance(catalog, dict):
            sec_reqs = catalog.get("security_requirements", catalog.get("security", []))
            if isinstance(sec_reqs, list):
                sec["nfr_security_inputs"] = [
                    item.get("requirement", str(item))[:120] for item in sec_reqs[:5] if isinstance(item, dict)
                ]
    return {
        "authentication": MARKER_DRAFT_REVIEW,
        "authorization": MARKER_DRAFT_REVIEW,
        "data_protection": MARKER_DRAFT_REVIEW,
        "threat_model_summary": MARKER_AUTO_COMPLETE,
        **sec,
    }


def _build_deployment_arch() -> dict:
    return {
        "infrastructure_overview": MARKER_DRAFT_REVIEW,
        "deployment_diagram": MARKER_AUTO_COMPLETE,
        "deployment_strategy": MARKER_DRAFT_REVIEW,
        "environments": [],
    }


def _build_observability(nfr: Optional[dict]) -> dict:
    return {
        "monitoring": MARKER_DRAFT_REVIEW,
        "logging": MARKER_DRAFT_REVIEW,
        "alerting": MARKER_AUTO_COMPLETE,
        "sla_slo_sli": MARKER_DRAFT_REVIEW,
    }
