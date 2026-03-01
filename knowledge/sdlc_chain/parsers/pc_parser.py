"""Parse a PC YAML file (K8s-style apiVersion/kind/metadata/spec) into a PcDocument dataclass."""
from typing import Any, Dict, List, Optional

from ..models import (
    PcAcceptanceCriterion, PcConstraint, PcDocument,
    PcFunctionalRequirement, PcGlossaryItem,
    PcNonFunctionalRequirement, PcObjective, PcSubRequirement,
)
from ..yaml_utils import load_yaml, safe_get

_META_KEYS = {"description", "required"}


def _strip_meta(section: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(section, dict):
        return {}
    return {k: v for k, v in section.items() if k not in _META_KEYS}


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


def _filter_strings(items: Optional[List[Any]]) -> List[str]:
    if not isinstance(items, list):
        return []
    return [str(item) for item in items if not _is_empty(item)]


def _filter_dicts(items: Optional[List[Any]]) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    result = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if any(not _is_empty(v) for v in item.values()):
            result.append(item)
    return result


def _parse_objectives(section: Optional[Dict[str, Any]]) -> List[PcObjective]:
    clean = _strip_meta(section)
    raw_items = clean.get("items", [])
    if not isinstance(raw_items, list):
        return []
    results = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        obj_id = item.get("id", "")
        statement = item.get("statement", "")
        if _is_empty(statement) and _is_empty(obj_id):
            continue
        results.append(PcObjective(
            id=obj_id or "",
            statement=statement or "",
            success_measure=item.get("success_measure", "") or "",
        ))
    return results


def _parse_acceptance(items: Optional[List[Any]]) -> List[PcAcceptanceCriterion]:
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        ac_id = item.get("id", "")
        statement = item.get("statement", "")
        if _is_empty(statement) and _is_empty(ac_id):
            continue
        results.append(PcAcceptanceCriterion(id=ac_id or "", statement=statement or ""))
    return results


def _parse_sub_requirements(items: Optional[List[Any]]) -> List[PcSubRequirement]:
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        sr_id = item.get("id", "")
        statement = item.get("statement", "")
        if _is_empty(statement) and _is_empty(sr_id):
            continue
        results.append(PcSubRequirement(id=sr_id or "", statement=statement or ""))
    return results


def _parse_functional(items: Optional[List[Any]]) -> List[PcFunctionalRequirement]:
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        req_id = item.get("id", "")
        statement = item.get("statement", "")
        if _is_empty(statement) and _is_empty(req_id):
            continue
        results.append(PcFunctionalRequirement(
            id=req_id or "",
            type=item.get("type", "functional") or "functional",
            statement=statement or "",
            priority=item.get("priority", "") or "",
            traces_to=_filter_strings(item.get("traces_to")),
            acceptance=_parse_acceptance(item.get("acceptance")),
            sub_requirements=_parse_sub_requirements(item.get("sub_requirements")),
        ))
    return results


def _parse_nonfunctional(items: Optional[List[Any]]) -> List[PcNonFunctionalRequirement]:
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        req_id = item.get("id", "")
        statement = item.get("statement", "")
        if _is_empty(statement) and _is_empty(req_id):
            continue
        results.append(PcNonFunctionalRequirement(
            id=req_id or "",
            type=item.get("type", "nonfunctional") or "nonfunctional",
            category=item.get("category", "") or "",
            statement=statement or "",
            priority=item.get("priority", "") or "",
            target_metric=item.get("target_metric", "") or "",
            acceptance=_parse_acceptance(item.get("acceptance")),
        ))
    return results


def _parse_constraints_req(items: Optional[List[Any]]) -> List[PcConstraint]:
    if not isinstance(items, list):
        return []
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        req_id = item.get("id", "")
        statement = item.get("statement", "")
        if _is_empty(statement) and _is_empty(req_id):
            continue
        results.append(PcConstraint(
            id=req_id or "",
            type=item.get("type", "constraint") or "constraint",
            statement=statement or "",
            priority=item.get("priority", "") or "",
        ))
    return results


def _parse_glossary(section: Optional[Dict[str, Any]]) -> List[PcGlossaryItem]:
    clean = _strip_meta(section)
    raw_items = clean.get("items", [])
    if not isinstance(raw_items, list):
        return []
    results = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        term = item.get("term", "")
        definition = item.get("definition", "")
        if _is_empty(term) and _is_empty(definition):
            continue
        results.append(PcGlossaryItem(term=term or "", definition=definition or ""))
    return results


def _parse_traceability(section: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    clean = _strip_meta(section)
    raw_matrix = clean.get("matrix", [])
    if not isinstance(raw_matrix, list):
        return []
    results = []
    for item in raw_matrix:
        if not isinstance(item, dict):
            continue
        req_id = item.get("requirement_id", "")
        if _is_empty(req_id):
            continue
        results.append({
            "requirement_id": req_id or "",
            "traces_to_objective": item.get("traces_to_objective", "") or "",
            "traces_to_downstream": _filter_strings(item.get("traces_to_downstream")),
        })
    return results


def load_pc(path: str) -> PcDocument:
    """Load a PC YAML file and return a populated PcDocument."""
    data = load_yaml(path)
    return parse_pc(data)


def parse_pc(data: dict) -> PcDocument:
    """Parse an already-loaded dict into a PcDocument."""
    api_version = data.get("apiVersion", "")
    kind = data.get("kind", "")
    if api_version != "sdlc/v1":
        raise ValueError(f"Unsupported apiVersion '{api_version}'; expected 'sdlc/v1'")
    if kind != "PlatformCanon":
        raise ValueError(f"Unsupported kind '{kind}'; expected 'PlatformCanon'")

    meta = data.get("metadata") or {}
    owners_raw = meta.get("owners") or {}
    owners = {k: str(v) for k, v in owners_raw.items() if not _is_empty(v)}

    spec = data.get("spec") or {}

    exec_section = _strip_meta(spec.get("executive_summary"))
    executive_summary = exec_section.get("content", "") or ""

    objectives = _parse_objectives(spec.get("objectives"))

    prob_section = _strip_meta(spec.get("problem_statement"))
    problem_statement = prob_section.get("content", "") or ""

    scope_section = _strip_meta(spec.get("scope"))
    scope_in = _filter_strings(scope_section.get("in_scope"))
    scope_out = _filter_strings(scope_section.get("out_of_scope"))
    scope_defs = _filter_strings(scope_section.get("domain_definitions"))

    stakeholders_section = _strip_meta(spec.get("stakeholders"))
    stakeholders = _filter_dicts(stakeholders_section.get("items"))

    current_section = _strip_meta(spec.get("current_state"))
    current_state = _filter_strings(current_section.get("items"))

    future_section = _strip_meta(spec.get("future_state"))
    future_vision = future_section.get("vision", "") or ""
    future_outcomes = _filter_strings(future_section.get("target_outcomes"))

    req_section = _strip_meta(spec.get("requirements"))
    functional_reqs = _parse_functional(req_section.get("functional"))
    nonfunctional_reqs = _parse_nonfunctional(req_section.get("nonfunctional"))
    constraint_reqs = _parse_constraints_req(req_section.get("constraints"))

    ac_section = _strip_meta(spec.get("assumptions_and_constraints"))
    assumptions = _filter_strings(ac_section.get("assumptions"))
    constraint_statements = _filter_strings(ac_section.get("constraints"))

    risks_section = _strip_meta(spec.get("risks"))
    risks = _filter_dicts(risks_section.get("items"))

    sm_section = _strip_meta(spec.get("success_metrics"))
    success_metrics = _filter_dicts(sm_section.get("items"))

    dep_section = _strip_meta(spec.get("dependencies"))
    dependencies = _filter_strings(dep_section.get("items"))

    glossary = _parse_glossary(spec.get("glossary"))
    traceability_matrix = _parse_traceability(spec.get("traceability"))

    return PcDocument(
        id=meta.get("id", "") or "",
        title=meta.get("title", "") or "",
        version=meta.get("version", "") or "",
        status=meta.get("status", "") or "",
        classification=meta.get("classification", "") or "",
        created_date=meta.get("created_date", "") or "",
        last_updated=meta.get("last_updated", "") or "",
        owners=owners,
        related_documents=_filter_strings(meta.get("related_documents")),
        tags=_filter_strings(meta.get("tags")),
        executive_summary=executive_summary,
        objectives=objectives,
        problem_statement=problem_statement,
        scope_in=scope_in,
        scope_out=scope_out,
        scope_domain_definitions=scope_defs,
        stakeholders=stakeholders,
        current_state=current_state,
        future_state_vision=future_vision,
        future_state_outcomes=future_outcomes,
        functional_requirements=functional_reqs,
        nonfunctional_requirements=nonfunctional_reqs,
        constraints=constraint_reqs,
        assumptions=assumptions,
        constraint_statements=constraint_statements,
        risks=risks,
        success_metrics=success_metrics,
        dependencies=dependencies,
        glossary=glossary,
        traceability_matrix=traceability_matrix,
    )


def validate_pc(pc: PcDocument) -> List[str]:
    """Return a list of validation warnings/errors for the PC."""
    issues = []

    if _is_empty(pc.id):
        issues.append("metadata.id is missing")
    if _is_empty(pc.title):
        issues.append("metadata.title is missing")
    if _is_empty(pc.version):
        issues.append("metadata.version is missing")
    if _is_empty(pc.status):
        issues.append("metadata.status is missing")

    if not pc.owners:
        issues.append("metadata.owners is empty")

    if _is_empty(pc.executive_summary):
        issues.append("spec.executive_summary.content is empty")
    if not pc.objectives:
        issues.append("spec.objectives has no items")
    if _is_empty(pc.problem_statement):
        issues.append("spec.problem_statement.content is empty")
    if not pc.scope_in:
        issues.append("spec.scope.in_scope is empty")

    if not pc.functional_requirements:
        issues.append("spec.requirements.functional has no items")

    for req in pc.functional_requirements:
        if _is_empty(req.statement):
            issues.append(f"Functional requirement '{req.id}' has an empty statement")
        if _is_empty(req.priority):
            issues.append(f"Functional requirement '{req.id}' has no priority")
        if not req.traces_to:
            issues.append(f"Functional requirement '{req.id}' does not trace to any objective")

    return issues
