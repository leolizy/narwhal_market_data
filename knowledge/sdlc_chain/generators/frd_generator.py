"""PC → FRD generation: transforms PC content into FRD YAML structure."""
from datetime import date
from typing import Dict, List, Optional, Tuple

from ..models import PcDocument, ModuleMapping, FunctionMapping
from ..naming import (
    generate_frd_id, generate_frd_filename, generate_fr_id,
    generate_fr_sub_id, generate_ac_fr_id, generate_fa_id,
)
from ..config import (
    DRAFT_VERSION, STATUS_DRAFT, MARKER_AUTO_REVIEW,
    MARKER_AUTO_COMPLETE, MARKER_DRAFT_REVIEW,
)


def generate_frd(
    pc: PcDocument,
    module: ModuleMapping,
    project_code: str,
    sequence: int = 1,
    today: Optional[str] = None,
) -> dict:
    """
    Generate a single FRD YAML dict for one module.

    Returns a dict matching the frd_template.yaml structure.
    """
    if today is None:
        today = date.today().isoformat()

    frd_id = generate_frd_id(project_code, sequence)

    # Phase 1: Identify relevant PC content for this module
    module_reqs = [
        req for req in pc.functional_requirements
        if req.id in module.requirements
    ]

    # Collect BO-xxx IDs referenced by this module's requirements
    relevant_objectives = set()
    for req in module_reqs:
        for bo_id in req.traces_to:
            if bo_id:
                relevant_objectives.add(bo_id)

    # Phase 2: Build FRD metadata
    document = {
        "document_id": frd_id,
        "module_code": module.module_code,
        "title": f"{module.module_name} - Functional Requirements",
        "version": DRAFT_VERSION,
        "status": STATUS_DRAFT,
        "classification": pc.classification or "Internal",
        "created_date": today,
        "last_updated": today,
        "author": pc.owners.get("author", "") if pc.owners else "",
        "reviewer": pc.owners.get("reviewer", "") if pc.owners else "",
        "approver": pc.owners.get("approver", "") if pc.owners else "",
        "parent_pc": pc.id,
        "related_documents": [pc.id],
        "tags": list(pc.tags) if pc.tags else [],
        "supersedes": "",
    }

    # Phase 3: Overview (merged Introduction + Purpose)
    overview = {
        "description": (
            "Introduce the module and state this document's purpose in one place. "
            "Identify the module's role within the broader system, reference the parent "
            "PC, and clarify who should use this document and for what decisions. "
            "Reference: IEEE 830 Section 1.1 — Purpose."
        ),
        "summary": (
            f"This document defines the functional requirements for the "
            f"{module.module_name} module of the {pc.title} initiative. "
            f"It is derived from the parent PC ({pc.id}) and captures "
            f"the detailed functional behavior required for design, "
            f"development, and testing of this module."
        ),
        "purpose": (
            f"This FRD specifies the functional behavior of the "
            f"{module.module_name} module. It serves as the primary "
            f"reference for architects (HLD/LLD), developers, and QA "
            f"engineers working on this module. Decisions regarding "
            f"functional scope, acceptance criteria, and business rules "
            f"for {module.module_name} should be resolved using this document."
        ),
        "audience": (
            f"{MARKER_AUTO_COMPLETE} List primary readers: architects, developers, "
            f"QA lead, product owner"
        ),
        "required": True,
    }

    # Phase 4: Scope
    scope_in = [
        f"{MARKER_AUTO_REVIEW} {item}" for item in pc.scope_in if item
    ] or [f"{MARKER_DRAFT_REVIEW} Define in-scope items for {module.module_name}"]
    scope_out = [
        f"{MARKER_AUTO_REVIEW} {item}" for item in pc.scope_out if item
    ] or [f"{MARKER_DRAFT_REVIEW} Define out-of-scope items for {module.module_name}"]

    scope = {
        "description": (
            "Define the boundary of this FRD — what is covered and what is explicitly "
            "excluded. This prevents scope creep and clarifies ownership between "
            "modules. Reference: IEEE 830 Section 1.2 — Scope."
        ),
        "in_scope": scope_in,
        "out_of_scope": scope_out,
        "required": True,
    }

    # Phase 5: Definitions from glossary
    def_items = [
        {"term": g.term, "definition": g.definition}
        for g in pc.glossary if g.term
    ]
    definitions = {
        "description": (
            "Define domain-specific terms, acronyms, and abbreviations used in this "
            "document. Include terms inherited from the parent PC only if their "
            "meaning is refined or extended at the module level. "
            "Reference: IEEE 830 Section 1.4 — Definitions."
        ),
        "items": def_items or [{"term": "", "definition": ""}],
        "required": False,
    }

    # Phase 6: Business context
    parent_obj_ids = sorted(relevant_objectives)
    obj_summaries = [
        f"{o.id}: {o.statement}"
        for o in pc.objectives if o.id in relevant_objectives
    ]
    bc_content = (
        f"This module supports the following parent PC objectives: "
        f"{'; '.join(obj_summaries)}."
    ) if obj_summaries else (
        f"{MARKER_DRAFT_REVIEW} Link this module to parent PC business objectives."
    )

    business_context = {
        "description": (
            "Describe the business drivers, expected outcomes, and value proposition "
            "for this module. Reference the parent PC business objectives (BO-NNN) "
            "that this module supports. This section bridges business intent to "
            "functional behavior."
        ),
        "content": bc_content,
        "parent_objectives": parent_obj_ids,
        "required": True,
    }

    # Phase 7: Actors from PC stakeholders
    actor_items = [
        {
            "actor": s.get("stakeholder", ""),
            "type": "",
            "role": s.get("role", ""),
            "responsibility": s.get("responsibility", ""),
        }
        for s in pc.stakeholders if s.get("stakeholder")
    ]
    actors = {
        "description": (
            "Identify all human actors, system actors, and stakeholders that interact "
            "with or are affected by this module. Distinguish between primary actors "
            "(who initiate actions) and secondary actors (who support or are notified). "
            "Reference: IEEE 830 Section 2.2 — User Characteristics."
        ),
        "items": actor_items or [
            {"actor": "", "type": "", "role": "", "responsibility": ""}
        ],
        "required": True,
    }

    # Phase 8: Functional overview
    functional_overview = {
        "description": (
            "Provide a high-level summary of the module's capabilities, major process "
            "flows, and how it fits within the overall system. Include or reference a "
            "context diagram or high-level flow if available. "
            "Reference: IEEE 830 Section 2 — Overall Description."
        ),
        "content": (
            f"{MARKER_DRAFT_REVIEW} The {module.module_name} module "
            f"encompasses {len(module_reqs)} functional requirements "
            f"organized into functional areas as defined below. "
            f"Provide a narrative summary of the module's major capabilities."
        ),
        "diagrams": [],
        "required": True,
    }

    # Phase 9: Event triggers (placeholder)
    event_triggers = {
        "description": (
            "List the events (user actions, system events, scheduled triggers, or "
            "external signals) that initiate processing within this module. Each "
            "trigger should map to one or more functional requirements."
        ),
        "items": [
            {
                "trigger_id": "ET-001",
                "event": f"{MARKER_DRAFT_REVIEW} Define event trigger",
                "source": "",
                "triggered_requirements": [],
            }
        ],
        "required": True,
    }

    # Phase 10: Functional requirements — core mapping
    functional_areas, fr_id_map = _build_functional_requirements(module_reqs)

    functional_requirements = {
        "description": (
            "The core of the FRD. Each requirement must be uniquely identified, "
            "prioritized (MoSCoW), and traceable to a parent PC requirement. Group "
            "related requirements under a functional area heading. Each requirement "
            "should be testable and unambiguous. "
            "Reference: IEEE 830 Section 3 — Specific Requirements; BABOK Section 7."
        ),
        "functional_areas": functional_areas,
        "required": True,
    }

    # Phase 11: Business rules (placeholder)
    business_rules = {
        "description": (
            "Define the business rules that govern functional behavior within this "
            "module. Business rules are constraints on operations, computations, "
            "or data that must be enforced by the system. Each rule should be "
            "uniquely identified for traceability."
        ),
        "items": [
            {
                "id": "BRL-001",
                "rule": f"{MARKER_DRAFT_REVIEW} Define business rules for this module",
                "applies_to": [],
            }
        ],
        "required": True,
    }

    # Phase 12: Exception scenarios (placeholder)
    exception_scenarios = {
        "description": (
            "Document known exception and error scenarios — conditions where normal "
            "processing cannot continue. For each, specify the trigger condition, "
            "expected system behavior, and user-visible outcome."
        ),
        "items": [
            {
                "id": "EX-001",
                "scenario": f"{MARKER_DRAFT_REVIEW} Define exception scenario",
                "trigger_condition": "",
                "expected_behavior": "",
                "user_outcome": "",
            }
        ],
        "required": True,
    }

    # Phase 13: Cross-module interactions (placeholder)
    cross_module_interactions = {
        "description": (
            "Identify all interactions this module has with other modules or external "
            "systems. Specify the direction of data flow and the nature of the "
            "interaction. This section is critical for impact analysis when changes "
            "are proposed."
        ),
        "items": [
            {
                "module": "",
                "interaction_type": "",
                "direction": "",
                "description": f"{MARKER_DRAFT_REVIEW} Define cross-module interactions",
                "interface_reference": "",
            }
        ],
        "required": True,
    }

    # Phase 14: Data requirements (entities only — field-level belongs in DC/DBC)
    data_requirements = {
        "description": (
            "Define the key data entities this module creates, reads, updates, or "
            "deletes at a high level. This is a functional view — detailed schema and "
            "field definitions belong in DC/DBC documents. Include ownership and "
            "sensitivity to guide data stewardship decisions. "
            "Reference: IEEE 830 Section 3.2 — Functions."
        ),
        "entities": [
            {
                "entity_name": "",
                "description": f"{MARKER_DRAFT_REVIEW} Define data entities",
                "crud": "",
                "ownership": "",  # SourceOfTruth | Consumer | Cache
                "sensitivity": "",
            }
        ],
        "data_retention": f"{MARKER_DRAFT_REVIEW} Define data retention policy",
        "required": True,
    }

    # Phase 15: NFRs with functional impact
    nfr_items = []
    for idx, nfr in enumerate(pc.nonfunctional_requirements, start=1):
        if nfr.statement:
            nfr_items.append({
                "id": f"NFR-FM-{idx:03d}",
                "category": nfr.category or "",
                "statement": nfr.statement,
                "target_metric": nfr.target_metric or "",
                "functional_impact": (
                    f"{MARKER_AUTO_COMPLETE} Describe how this NFR impacts "
                    f"functional design for {module.module_name}"
                ),
            })
    if not nfr_items:
        nfr_items = [{
            "id": "NFR-FM-001",
            "category": "",
            "statement": f"{MARKER_DRAFT_REVIEW} Define module-level NFRs",
            "target_metric": "",
            "functional_impact": "",
        }]

    nonfunctional_requirements = {
        "description": (
            "Non-functional requirements that have a direct impact on functional "
            "design for this module. System-wide NFRs live in the parent PC or a "
            "dedicated NFR document — include here only those that require specific "
            "functional accommodations within this module. "
            "Reference: IEEE 830 Section 3.3 — Performance Requirements."
        ),
        "items": nfr_items,
        "required": True,
    }

    # Phase 16: Dependencies
    dep_items = []
    for idx, dep in enumerate(pc.dependencies, start=1):
        dep_str = str(dep) if dep else ""
        if dep_str:
            dep_items.append({
                "id": f"DEP-{idx:03d}",
                "dependency": f"{MARKER_AUTO_REVIEW} {dep_str}",
                "type": "",
                "owner": "",
                "impact_if_unavailable": "",
            })
    if not dep_items:
        dep_items = [{
            "id": "DEP-001",
            "dependency": f"{MARKER_DRAFT_REVIEW} Define dependencies",
            "type": "",
            "owner": "",
            "impact_if_unavailable": "",
        }]

    dependencies = {
        "description": (
            "External or internal dependencies that could affect delivery or "
            "functionality of this module. Include system dependencies, team "
            "dependencies, data dependencies, and third-party service dependencies."
        ),
        "items": dep_items,
        "required": True,
    }

    # Phase 17: Assumptions & Constraints (merged)
    asm_items = []
    for idx, asm in enumerate(pc.assumptions, start=1):
        asm_str = str(asm) if asm else ""
        if asm_str:
            asm_items.append({
                "id": f"ASM-{idx:03d}",
                "assumption": f"{MARKER_AUTO_REVIEW} {asm_str}",
                "validation_method": "",
                "impact_if_false": "",
            })
    if not asm_items:
        asm_items = [{
            "id": "ASM-001",
            "assumption": f"{MARKER_DRAFT_REVIEW} Define assumptions",
            "validation_method": "",
            "impact_if_false": "",
        }]

    con_items = []
    for idx, con in enumerate(pc.constraints, start=1):
        if con.statement:
            con_items.append({
                "id": f"CON-{idx:03d}",
                "constraint": f"{MARKER_AUTO_REVIEW} {con.statement}",
                "type": con.type or "",
                "rationale": "",
            })
    for idx2, cs in enumerate(pc.constraint_statements, start=len(con_items) + 1):
        cs_str = str(cs) if cs else ""
        if cs_str:
            con_items.append({
                "id": f"CON-{idx2:03d}",
                "constraint": f"{MARKER_AUTO_REVIEW} {cs_str}",
                "type": "",
                "rationale": "",
            })
    if not con_items:
        con_items = [{
            "id": "CON-001",
            "constraint": f"{MARKER_DRAFT_REVIEW} Define constraints",
            "type": "",
            "rationale": "",
        }]

    assumptions_and_constraints = {
        "description": (
            "Assumptions: conditions believed to be true but not yet confirmed — "
            "documenting them creates accountability for validation. "
            "Constraints: hard boundaries that limit solution design choices — "
            "non-negotiable technical mandates, regulatory requirements, or budget/"
            "timeline restrictions. Preferences belong in HLD, not here. "
            "Reference: BABOK Section 6.3; IEEE 830 Section 2.5."
        ),
        "assumptions": asm_items,
        "constraints": con_items,
        "required": True,
    }

    # Phase 15: Module interface — what this module exposes
    # (APIs it provides, events it publishes, data it owns as source of truth)
    module_interface = _build_module_interface(module)

    # Phase 19: Traceability matrix
    trace_matrix = []
    for area in functional_areas:
        for req in area.get("requirements", []):
            pc_refs = req.get("traces_to_pc", [])
            fr_ids = [req["id"]]
            for sub in req.get("sub_requirements", []):
                if sub.get("id"):
                    fr_ids.append(sub["id"])
            trace_matrix.append({
                "pc_requirement": pc_refs[0] if pc_refs else "",
                "frd_requirements": fr_ids,
                "downstream_artifacts": [],
                "notes": "",
            })
    if not trace_matrix:
        trace_matrix = [{
            "pc_requirement": "",
            "frd_requirements": [],
            "downstream_artifacts": [],
            "notes": "",
        }]

    traceability = {
        "description": (
            "Maps each FRD requirement to its originating PC requirement and "
            "downstream artifacts (HLD sections, LLD modules, test cases) for "
            "impact analysis and coverage tracking."
        ),
        "matrix": trace_matrix,
        "required": True,
    }

    # Phase 20: Module-level acceptance criteria (placeholder)
    acceptance_criteria = {
        "description": (
            "Module-level acceptance criteria that define the conditions under which "
            "this module is considered complete and ready for handover. These are "
            "higher-level than individual requirement acceptance criteria and may "
            "include integration, performance, and user acceptance conditions."
        ),
        "items": [
            {
                "id": "MAC-001",
                "criteria": (
                    f"{MARKER_DRAFT_REVIEW} Define module-level acceptance criteria "
                    f"for {module.module_name}"
                ),
                "verification_method": "",
            }
        ],
        "required": True,
    }

    # Phase 21: Open issues (empty)
    open_issues = {
        "description": (
            "Track unresolved questions, decisions pending, or ambiguities that "
            "require clarification before the FRD can be finalized. Each issue "
            "should have an owner and a target resolution date."
        ),
        "items": [],
        "required": False,
    }

    # Phase 22: Approvals
    approvals = {
        "description": (
            "Formal sign-off from accountable stakeholders. The FRD cannot move "
            "to Approved status without the required approvals recorded here."
        ),
        "items": [
            {"role": "Business Analyst / Author", "name": "", "decision": "", "signature": "", "date": ""},
            {"role": "Technical Lead / Architect", "name": "", "decision": "", "signature": "", "date": ""},
            {"role": "QA Lead", "name": "", "decision": "", "signature": "", "date": ""},
            {"role": "Product Owner", "name": "", "decision": "", "signature": "", "date": ""},
        ],
        "required": True,
    }

    # Phase 23: Change log
    change_log = {
        "entries": [
            {
                "version": DRAFT_VERSION,
                "date": today,
                "author": "sdlc_chain (auto-generated)",
                "summary": f"Initial draft generated from {pc.id}",
            }
        ],
    }

    # Phase 24: Attachments
    attachments = {
        "items": [],
    }

    # Assemble full FRD — section order matches template v2.0
    frd = {
        "kind": "FunctionalRequirements",
        "metadata": document,
        # Context
        "overview": overview,
        "scope": scope,
        "definitions": definitions,
        "business_context": business_context,
        # Actors
        "actors": actors,
        "functional_overview": functional_overview,
        # Spec
        "event_triggers": event_triggers,
        "functional_requirements": functional_requirements,
        "business_rules": business_rules,
        "exception_scenarios": exception_scenarios,
        # Interface
        "module_interface": module_interface,
        "cross_module_interactions": cross_module_interactions,
        "data_requirements": data_requirements,
        # NFR
        "nonfunctional_requirements": nonfunctional_requirements,
        # Assurance
        "traceability": traceability,
        "acceptance_criteria": acceptance_criteria,
        # Management
        "assumptions_and_constraints": assumptions_and_constraints,
        "dependencies": dependencies,
        "open_issues": open_issues,
        # Governance
        "approvals": approvals,
        "change_log": change_log,
        "attachments": attachments,
    }

    return frd


def _build_module_interface(module: "ModuleMapping") -> dict:
    """
    Generate a placeholder module_interface section for a newly created FRD.

    This section declares what the module *exposes* at a high level.
    Detailed integration specs (INT-NNN entries with protocol, SLA, DBC/AEC
    references) belong in the PSD integration_points section — see
    _build_integration_points() in psd_generator.py.  Authors populate
    api_spec_reference (DBC-NNNN) and schema_reference (AEC-NNNN) here only
    after those downstream contracts have been drafted.
    """
    return {
        "description": (
            "Declare what this module exposes: APIs provided, domain events published, "
            "and data entities owned as source of truth. Detailed integration specs "
            "live in the PSD integration_points section; populate api_spec_reference "
            "and schema_reference once the corresponding DBC/AEC docs are drafted."
        ),
        "apis_provided": [],
        "events_published": [],
        "data_owned": [],
        "required": False,
    }


def _build_functional_requirements(module_reqs) -> Tuple[List[dict], Dict[str, str]]:
    """
    Build FRD functional_areas from PC requirements.

    Returns (functional_areas list, fr_id_map: {pc_req_id: frd_fr_id}).
    """
    functional_areas = []
    fr_id_map = {}  # PC-NNN → FR-NNN
    fr_counter = 1
    fa_counter = 1

    for br in module_reqs:
        fr_id = generate_fr_id(fr_counter)
        fr_id_map[br.id] = fr_id

        # Map acceptance criteria
        mapped_ac = []
        for ac_idx, ac in enumerate(br.acceptance, start=1):
            if ac.statement:
                mapped_ac.append({
                    "id": generate_ac_fr_id(fr_id, ac_idx),
                    "statement": ac.statement,
                })

        # Map sub-requirements
        mapped_sub = []
        for sub_idx, sub in enumerate(br.sub_requirements, start=1):
            if sub.statement:
                mapped_sub.append({
                    "id": generate_fr_sub_id(fr_counter, sub_idx),
                    "statement": sub.statement,
                })

        area = {
            "area_id": generate_fa_id(fa_counter),
            "area_name": (br.statement[:60] if br.statement else f"Area {fa_counter}"),
            "requirements": [{
                "id": fr_id,
                "statement": br.statement or "",
                "priority": br.priority or "",
                "traces_to_pc": [br.id],
                "acceptance_criteria": mapped_ac or [
                    {"id": generate_ac_fr_id(fr_id, 1), "statement": ""}
                ],
                "sub_requirements": mapped_sub,
            }],
        }
        functional_areas.append(area)
        fr_counter += 1
        fa_counter += 1

    return functional_areas, fr_id_map


def get_frd_metadata(frd: dict) -> dict:
    """Extract metadata fields from an FRD dict."""
    return frd.get("metadata", {})
