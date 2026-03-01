"""FRD → Design by Contract (DBC) generator.

Produces a DBC scaffold for a module's service boundary, aligned with
44-dbc_template.yaml.

Entry point
-----------
    generate_dbc(frd, sequence, today)
"""
from datetime import date
from typing import Optional

from ..config import (
    DRAFT_VERSION,
    MARKER_AUTO_COMPLETE,
    MARKER_AUTO_REVIEW,
    MARKER_DRAFT_REVIEW,
    STATUS_DRAFT,
)
from ..naming import generate_dbc_id
from ._contract_helpers import extract_common


def generate_dbc(
    frd: dict,
    sequence: int = 1,
    today: Optional[str] = None,
) -> dict:
    """
    Scaffold one DBC (Design by Contract) document for the module's service boundary.

    Args:
        frd:      Source FRD dict.
        sequence: Numeric sequence for DBC-NNNN.
        today:    ISO date string; defaults to today.
    """
    if today is None:
        today = date.today().isoformat()
    common = extract_common(frd, today)
    return _generate_dbc(common, frd, sequence)


# ---------------------------------------------------------------------------
# Private implementation
# ---------------------------------------------------------------------------

def _generate_dbc(common: dict, frd: dict, sequence: int) -> dict:
    """Build a full DBC scaffold dict aligned with 44-dbc_template.yaml."""
    frd_id      = common["frd_id"]
    module_name = common["module_name"]
    today       = common["today"]
    dbc_id      = generate_dbc_id(sequence)

    fa          = frd.get("functional_requirements", {}).get("functional_areas", [])
    contracts   = _extract_dbc_contracts(dbc_id, fa)
    trace       = _build_dbc_traceability(dbc_id, fa, frd_id)

    overview    = frd.get("overview", {}).get("summary", "")
    bc_parent   = frd.get("business_context", {}).get("parent_objectives", [])

    return {
        "kind": "DesignByContract",
        "metadata": {
            "document_id":    dbc_id,
            "title":          f"{module_name} Design by Contract Specification",
            "version":        DRAFT_VERSION,
            "status":         STATUS_DRAFT,
            "classification": common["classification"],
            "created_date":   today,
            "last_updated":   today,
            "author":         common["author"],
            "reviewer":       common["reviewer"],
            "approver":       common["approver"],
            "related_documents": [frd_id],
        },

        # Section 1
        "introduction": {
            "description": (
                "High-level overview of the service/API boundary this specification covers, "
                "including its role in the system, the rationale for applying DbC, and how "
                "this document should be consumed by developers and QA."
            ),
            "content": (
                overview
                or f"{MARKER_DRAFT_REVIEW} Describe the {module_name} service boundary, its role "
                   f"in the system, and how DbC principles are applied to its operations."
            ),
            "required": True,
        },

        # Section 2
        "service_boundary": {
            "description": (
                "Exact boundary of the service or API this specification governs, "
                "including protocol and upstream/downstream dependencies."
            ),
            "service_name":           module_name,
            "bounded_context":        f"{MARKER_AUTO_REVIEW} {', '.join(bc_parent) if bc_parent else module_name}",
            "protocol":               f"{MARKER_DRAFT_REVIEW} REST | gRPC | GraphQL | Message Queue | Event Bus",
            "upstream_dependencies":  [],
            "downstream_consumers":   [],
            "content":                f"{MARKER_DRAFT_REVIEW} Describe the external interface surface of {module_name}",
            "required":               True,
        },

        # Section 3
        "glossary": {
            "description": "Domain-specific terms and DbC vocabulary used in this document.",
            "terms": [
                {"term": "Precondition",     "definition": "A condition that MUST be true before an operation is invoked. The caller is responsible for satisfying it."},
                {"term": "Postcondition",    "definition": "A condition the service GUARANTEES to be true after successful execution, provided all preconditions were met."},
                {"term": "Invariant",        "definition": "A condition that must ALWAYS hold for the service, regardless of which operation is called."},
                {"term": module_name,        "definition": f"{MARKER_DRAFT_REVIEW} Define {module_name} in business terms"},
            ],
            "required": True,
        },

        # Section 4 — core of the DBC
        "contract_catalogue": {
            "description": (
                "Each entry defines one operation or endpoint with its full DbC specification: "
                "preconditions (caller's obligations), postconditions (service's obligations on success), "
                "error postconditions (service's obligations on failure), and the operation signature."
            ),
            "contracts": contracts,
            "required":  True,
        },

        # Section 5
        "service_invariants": {
            "description": (
                "Conditions that must ALWAYS hold true for the service regardless of which "
                "operation is called. Invariants are checked before and after every public operation."
            ),
            "invariants": [
                {
                    "id":                   "INV-001",
                    "condition":            f"{MARKER_DRAFT_REVIEW} Define a fundamental integrity guarantee for {module_name}",
                    "scope":                f"{MARKER_DRAFT_REVIEW} Global | Per-Entity | Per-Session",
                    "rationale":            "",
                    "verification_method":  f"{MARKER_DRAFT_REVIEW} Runtime assertion | Integration test | Monitor",
                }
            ],
            "required": True,
        },

        # Section 6
        "contract_inheritance": {
            "description": (
                "How contracts relate to parent or composed services. Under DbC inheritance: "
                "subtypes may weaken preconditions and strengthen postconditions (LSP)."
            ),
            "inherited_contracts": [],
            "required":            False,
        },

        # Section 7
        "verification_strategy": {
            "description": "How each contract (preconditions, postconditions, invariants) will be verified.",
            "approaches": [
                {
                    "contract_id":       f"{dbc_id}-C001",
                    "verification_type": f"{MARKER_DRAFT_REVIEW} Unit Test | Integration Test | Runtime Assertion | Contract Test | Monitor",
                    "test_case_reference": f"{MARKER_AUTO_COMPLETE} UT document ID once created",
                    "automation_status": "Planned",
                    "notes":             "",
                }
            ],
            "required": True,
        },

        # Section 8
        "failure_modes": {
            "description": (
                "Blame model: precondition violations are the caller's fault; "
                "postcondition and invariant violations are the service's fault."
            ),
            "failure_cases": [
                {
                    "scenario":          f"{MARKER_DRAFT_REVIEW} e.g. Invalid input violates PRE-001",
                    "violated_contract": f"{MARKER_DRAFT_REVIEW} PRE/POST/EPOST/INV reference",
                    "blame":             f"{MARKER_DRAFT_REVIEW} Caller | Service | Infrastructure",
                    "diagnostic_action": f"{MARKER_DRAFT_REVIEW} Log | Alert | Circuit-break",
                    "escalation_path":   "",
                }
            ],
            "required": True,
        },

        # Section 9
        "assumptions_constraints": {
            "description": "Operating environment assumptions and constraints that bound the contracts.",
            "assumptions": [
                {
                    "id":               "ASM-001",
                    "assumption":       f"{MARKER_DRAFT_REVIEW} Define assumption",
                    "impact_if_invalid": "",
                }
            ],
            "constraints": [
                {
                    "id":         "CON-001",
                    "constraint": f"{MARKER_DRAFT_REVIEW} Define constraint",
                    "rationale":  "",
                }
            ],
            "required": True,
        },

        # Section 10
        "traceability": {
            "description": "Maps each contract to its originating requirement, design decision, and test cases.",
            "matrix":   trace,
            "required": True,
        },

        "attachments": {
            "description": "Sequence diagrams, state diagrams, schema definitions, or formal notation.",
            "files":       [],
            "required":    False,
        },
        "change_log": {
            "description": "Version history tracking all changes to this specification.",
            "entries": [
                {
                    "version": DRAFT_VERSION,
                    "date":    today,
                    "author":  "sdlc_chain (auto-generated)",
                    "changes": f"Initial draft scaffolded from {frd_id}",
                }
            ],
            "required": True,
        },
    }


def _extract_dbc_contracts(dbc_id: str, functional_areas: list) -> list:
    """
    Derive DBC contract entries from FRD functional areas.

    Each functional requirement becomes one contract entry with placeholder
    preconditions and postconditions.  Callers fill in the invariant details;
    the FR statement provides enough context to bootstrap meaningful prompts.
    """
    contracts = []
    c_idx = 1

    for area in functional_areas:
        for req in area.get("requirements", []):
            fr_id     = req.get("id", f"FR-{c_idx:03d}")
            statement = req.get("statement", "")
            operation = statement[:80] if statement and MARKER_DRAFT_REVIEW not in statement else f"Operation {c_idx}"
            contract_id = f"{dbc_id}-C{c_idx:03d}"

            contracts.append({
                "contract_id":        contract_id,
                "operation_name":     operation,
                "operation_signature": f"{MARKER_DRAFT_REVIEW} methodName(params): ReturnType",
                "description":        statement or f"{MARKER_DRAFT_REVIEW} Describe the business purpose of this operation",
                "content":            "",

                "preconditions": {
                    "description": "Conditions that MUST be true before this operation is invoked. The caller is responsible.",
                    "items": [
                        {
                            "id":                f"PRE-{c_idx:03d}-001",
                            "condition":         f"{MARKER_DRAFT_REVIEW} Define precondition for: {operation[:50]}",
                            "rationale":         "",
                            "violation_response": f"{MARKER_DRAFT_REVIEW} e.g. HTTP 400 | IllegalArgumentException",
                        }
                    ],
                    "required": True,
                },

                "postconditions": {
                    "description": "Conditions the service GUARANTEES after successful execution.",
                    "items": [
                        {
                            "id":           f"POST-{c_idx:03d}-001",
                            "condition":    f"{MARKER_DRAFT_REVIEW} Define postcondition for: {operation[:50]}",
                            "rationale":    "",
                            "verifiable_by": f"{MARKER_AUTO_COMPLETE} UT test case ID once created",
                        }
                    ],
                    "required": True,
                },

                "error_postconditions": {
                    "description": "Conditions the service guarantees when the operation fails.",
                    "items": [
                        {
                            "id":              f"EPOST-{c_idx:03d}-001",
                            "error_condition":  "Any unhandled exception",
                            "guaranteed_state": "No partial writes; transaction rolled back",
                            "error_code":       f"{MARKER_DRAFT_REVIEW} HTTP 500 | gRPC INTERNAL | InternalException",
                            "rationale":        "Atomicity must be preserved on failure",
                        }
                    ],
                    "required": True,
                },

                "input_output": {
                    "description": "Input parameters and output response structure.",
                    "input_schema":  f"{MARKER_AUTO_COMPLETE} Reference API or DC schema",
                    "output_schema": f"{MARKER_AUTO_COMPLETE} Reference API or DC schema",
                    "required":      True,
                },
            })
            c_idx += 1

    # Fallback if FRD has no functional areas yet
    if not contracts:
        contracts.append({
            "contract_id":        f"{dbc_id}-C001",
            "operation_name":     f"{MARKER_DRAFT_REVIEW} Operation name",
            "operation_signature": f"{MARKER_DRAFT_REVIEW} methodName(params): ReturnType",
            "description":        f"{MARKER_DRAFT_REVIEW} Describe the business purpose of this operation",
            "content":            "",
            "preconditions":      {"description": "Conditions the caller must satisfy.", "items": [{"id": "PRE-001-001", "condition": f"{MARKER_DRAFT_REVIEW}", "rationale": "", "violation_response": ""}], "required": True},
            "postconditions":     {"description": "Conditions the service guarantees on success.", "items": [{"id": "POST-001-001", "condition": f"{MARKER_DRAFT_REVIEW}", "rationale": "", "verifiable_by": ""}], "required": True},
            "error_postconditions": {"description": "Conditions the service guarantees on failure.", "items": [{"id": "EPOST-001-001", "error_condition": "Any unhandled exception", "guaranteed_state": "No partial writes", "error_code": "", "rationale": ""}], "required": True},
            "input_output":       {"description": "Input/output schema references.", "input_schema": f"{MARKER_DRAFT_REVIEW}", "output_schema": f"{MARKER_DRAFT_REVIEW}", "required": True},
        })

    return contracts


def _build_dbc_traceability(dbc_id: str, functional_areas: list, frd_id: str) -> list:
    """Build the traceability matrix linking DBC contracts back to FRD requirements."""
    matrix = []
    c_idx  = 1
    for area in functional_areas:
        for req in area.get("requirements", []):
            pc_refs = req.get("traces_to_pc", [])
            matrix.append({
                "contract_id":      f"{dbc_id}-C{c_idx:03d}",
                "requirement_id":   req.get("id", ""),
                "frd_reference":    frd_id,
                "pc_reference":    pc_refs[0] if pc_refs else "",
                "design_reference": f"{MARKER_AUTO_COMPLETE} PSD reference once created",
                "test_case_ids":    [],
            })
            c_idx += 1

    if not matrix:
        matrix.append({
            "contract_id":      f"{dbc_id}-C001",
            "requirement_id":   "",
            "frd_reference":    frd_id,
            "pc_reference":    "",
            "design_reference": f"{MARKER_AUTO_COMPLETE} PSD reference once created",
            "test_case_ids":    [],
        })

    return matrix
