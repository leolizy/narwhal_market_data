"""SDLC document generators.

Each generator takes upstream artifact dicts and produces a scaffold dict
aligned with the corresponding YAML template.

The batch orchestrator ``generate_contracts_from_frd`` coordinates all five
contract generators (AEC, API, DC, DBC, MDC) from a single FRD dict.
"""
from datetime import date
from typing import Any, Dict, Optional

from .aec_generator import generate_aec
from .api_generator import generate_api_contract
from .cicd_generator import generate_cicd
from .dbad_generator import generate_dbad
from .dbc_generator import generate_dbc
from .dc_generator import generate_dc
from .dd_generator import generate_dd
from .dg_generator import generate_dg
from .frd_generator import generate_frd
from .hld_generator import generate_hld
from .mdc_generator import generate_mdc
from .mvp_generator import generate_mvp
from .nfrar_generator import generate_nfrar
from .nfts_generator import generate_nfts
from .tsi_generator import generate_tsi

from ._contract_helpers import extract_common as _extract_common
from ..config import DRAFT_VERSION
from ..naming import (
    generate_aec_filename,
    generate_api_filename,
    generate_dc_filename,
    generate_dbc_filename,
    generate_mdc_filename,
)

__all__ = [
    "generate_aec",
    "generate_api_contract",
    "generate_cicd",
    "generate_contracts_from_frd",
    "generate_dbad",
    "generate_dbc",
    "generate_dc",
    "generate_dd",
    "generate_dg",
    "generate_frd",
    "generate_hld",
    "generate_mdc",
    "generate_mvp",
    "generate_nfrar",
    "generate_nfts",
    "generate_tsi",
]


# ---------------------------------------------------------------------------
# Batch contract orchestrator
# ---------------------------------------------------------------------------

def generate_contracts_from_frd(
    frd: dict,
    sequence_start: int = 1,
    today: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate all five contract documents from a single FRD dict.

    Inspects ``frd["module_interface"]`` and ``frd["data_requirements"]`` to
    derive per-contract scaffolds.  Missing or placeholder fields are filled
    with MARKER_DRAFT_REVIEW so authors know exactly what to complete.

    Args:
        frd:            FRD dict as produced by frd_generator.generate_frd().
        sequence_start: Starting sequence number for document IDs (e.g. 1
                        produces AEC-0001, DC-0001, DBC-0001, MDC-0001).
        today:          ISO 8601 date string; defaults to today's date.

    Returns:
        {
            "AEC":       list[dict]  — one AEC per published event
            "API":       dict        — one OpenAPI 3.1 scaffold per module
            "DC":        list[dict]  — one DC per source-of-truth entity
            "DBC":       dict        — one DBC per module service boundary
            "MDC":       list[dict]  — one MDC per external data source
            "filenames": {
                "AEC": list[str],
                "API": str,
                "DC":  list[str],
                "DBC": str,
                "MDC": list[str],
            }
        }
    """
    if today is None:
        today = date.today().isoformat()

    common = _extract_common(frd, today)

    mi = frd.get("module_interface", {})
    events_raw = mi.get("events_published", [])
    dr = frd.get("data_requirements", {})
    entities_raw = dr.get("entities", [])

    # Entities where this module is the source of truth
    owned_entities = [
        e for e in entities_raw
        if isinstance(e, dict) and e.get("ownership") in ("SourceOfTruth", "")
    ]

    # --- AEC: one per published event (minimum one scaffold) ---
    aec_list, aec_filenames = [], []
    events = [e for e in events_raw if e]
    if events:
        for idx, evt in enumerate(events, start=sequence_start):
            evt_name = evt if isinstance(evt, str) else evt.get("event", f"{common['module_slug']}.event")
            aec_list.append(generate_aec(frd, evt_name, idx, today))
            aec_filenames.append(generate_aec_filename(idx, evt_name, DRAFT_VERSION, "yaml"))
    else:
        default_event = f"{common['module_slug']}.created"
        aec_list.append(generate_aec(frd, default_event, sequence_start, today))
        aec_filenames.append(generate_aec_filename(sequence_start, common["module_name"], DRAFT_VERSION, "yaml"))

    # --- API: one OpenAPI 3.1 scaffold per module ---
    api = generate_api_contract(frd, sequence_start, today)
    api_filename = generate_api_filename(common["frd_id"], common["module_name"])

    # --- DC: one per source-of-truth entity (minimum one scaffold) ---
    dc_list, dc_filenames = [], []
    if owned_entities:
        for seq, entity in enumerate(owned_entities, start=sequence_start):
            entity_name = entity.get("entity_name", common["module_name"])
            dc_list.append(generate_dc(frd, entity, seq, today))
            dc_filenames.append(generate_dc_filename(seq, entity_name, DRAFT_VERSION, "yaml"))
    else:
        dc_list.append(generate_dc(frd, {}, sequence_start, today))
        dc_filenames.append(generate_dc_filename(sequence_start, common["module_name"], DRAFT_VERSION, "yaml"))

    # --- DBC: one per module service boundary ---
    dbc = generate_dbc(frd, sequence_start, today)
    dbc_filename = generate_dbc_filename(sequence_start, common["module_name"], DRAFT_VERSION, "yaml")

    # --- MDC: one per external data source (minimum one scaffold) ---
    mdc_list, mdc_filenames = [], []
    external_sources = dr.get("external_sources", [])
    if external_sources:
        for seq, source in enumerate(external_sources, start=sequence_start):
            source_name = source.get("source_name", common["module_name"]) if isinstance(source, dict) else common["module_name"]
            mdc_list.append(generate_mdc(frd, source if isinstance(source, dict) else {}, seq, today))
            mdc_filenames.append(generate_mdc_filename(seq, source_name, DRAFT_VERSION, "yaml"))
    else:
        mdc_list.append(generate_mdc(frd, {}, sequence_start, today))
        mdc_filenames.append(generate_mdc_filename(sequence_start, common["module_name"], DRAFT_VERSION, "yaml"))

    return {
        "AEC": aec_list,
        "API": api,
        "DC": dc_list,
        "DBC": dbc,
        "MDC": mdc_list,
        "filenames": {
            "AEC": aec_filenames,
            "API": api_filename,
            "DC": dc_filenames,
            "DBC": dbc_filename,
            "MDC": mdc_filenames,
        },
    }
