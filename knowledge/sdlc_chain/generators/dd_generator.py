"""All-artifacts → Data Dictionary (DD) generator.

Mines every recognised SDLC artifact type (FRD, PSD, DC, MDC, …) and
synthesises a single DD scaffold.

Entry point
-----------
    generate_dd(artifacts, sequence, system_name, today)

Where ``artifacts`` is a list of loaded artifact dicts.  Callers should
inject a ``_source_path`` key into each dict so provenance is recorded,
though the generator functions correctly without it.
"""
from datetime import date
from typing import Any, Dict, List, Optional

from ..config import (
    DRAFT_VERSION,
    MARKER_AUTO_COMPLETE,
    MARKER_AUTO_REVIEW,
    MARKER_DRAFT_REVIEW,
    STATUS_DRAFT,
)
from ..naming import generate_dd_id, to_pascal_case


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _doc_id(art: dict) -> str:
    """Extract the document_id string from an artifact dict."""
    m = art.get("metadata", {})
    return (
        m.get("document_id")
        or m.get("id")                               # K8s-envelope may use metadata.id
        or art.get("document", {}).get("document_id", "")
    ) or "UNKNOWN"


def _doc_prefix(art: dict) -> str:
    """Return the doc-type prefix from the document_id (e.g. 'FRD', 'DC')."""
    did = _doc_id(art)
    return did.split("-")[0] if did and did != "UNKNOWN" else "UNKNOWN"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_dd(
    artifacts: List[dict],
    sequence: int = 1,
    system_name: str = "System",
    today: Optional[str] = None,
) -> dict:
    """
    Generate a Data Dictionary scaffold from the full SDLC artifact suite.

    Args:
        artifacts:   List of loaded artifact dicts (any doc type).  Each dict
                     may carry a ``_source_path`` key for provenance.
        sequence:    Numeric sequence for the DD document ID (1 → DD-0001).
        system_name: Short system / project name used in the document title.
        today:       ISO 8601 date string; defaults to today's date.

    Returns:
        Fully structured DD dict aligned with 93-dd_template.yaml.
    """
    if today is None:
        today = date.today().isoformat()

    # Classify artifacts by doc-type prefix
    by_type: Dict[str, List[dict]] = {}
    for art in artifacts:
        prefix = _doc_prefix(art)
        by_type.setdefault(prefix, []).append(art)

    frds = by_type.get("FRD", [])
    psds = by_type.get("PSD", [])
    dcs  = by_type.get("DC",  [])
    mdcs = by_type.get("MDC", [])

    doc_id = generate_dd_id(sequence)

    return {
        "kind": "DataDictionary",
        "metadata":                    _build_metadata(doc_id, system_name, today, artifacts),
        "introduction":                _build_introduction(system_name, artifacts),
        "data_domains":                _build_domains(frds, psds, dcs),
        "data_elements_catalog":       _build_elements(dcs, frds),
        "entity_relationship_summary": _build_er_summary(frds, dcs),
        "code_tables":                 _build_code_tables(),
        "data_glossary":               _build_glossary(dcs, frds),
        "data_lineage":                _build_lineage(dcs, mdcs),
        "data_quality_rules":          _build_quality_rules(dcs),
        "attachments":                 [],
        "change_log": [
            {
                "version": DRAFT_VERSION,
                "date": today,
                "author": MARKER_AUTO_REVIEW,
                "changes": (
                    f"Initial scaffold auto-generated from {len(artifacts)} SDLC artifacts "
                    f"({len(frds)} FRDs, {len(psds)} PSDs, {len(dcs)} DCs, {len(mdcs)} MDCs)."
                ),
            }
        ],
    }


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _build_metadata(
    doc_id: str,
    system_name: str,
    today: str,
    artifacts: List[dict],
) -> dict:
    related = sorted(set(
        _doc_id(a) for a in artifacts
        if _doc_id(a) not in ("UNKNOWN", "")
    ))
    return {
        "document_id": doc_id,
        "title": f"{system_name} Data Dictionary & Glossary",
        "version": DRAFT_VERSION,
        "status": STATUS_DRAFT,
        "classification": "Internal",
        "created_date": today,
        "last_updated": today,
        "author": MARKER_DRAFT_REVIEW,
        "reviewer": MARKER_DRAFT_REVIEW,
        "approver": MARKER_DRAFT_REVIEW,
        "system_name": system_name,
        "system_version": MARKER_AUTO_COMPLETE,
        "related_documents": related,
    }


def _build_introduction(system_name: str, artifacts: List[dict]) -> dict:
    return {
        "purpose": (
            f"This Data Dictionary defines all data elements, entities, domains, and "
            f"business terms used within the {system_name} system. "
            f"It serves as the authoritative reference for data governance, integration, "
            f"and development teams."
        ),
        "scope": (
            f"Covers all data elements sourced from {len(artifacts)} SDLC artifacts "
            f"including functional requirements, product specifications, and data contracts."
        ),
        "audience": (
            "Data engineers, backend developers, data governance teams, "
            "and business analysts."
        ),
        "how_to_use": (
            "Navigate by domain (Section 3) to find related elements, "
            "or search the Data Elements Catalog (Section 4) by element name or ID. "
            "See the Glossary (Section 7) for business term definitions."
        ),
    }


def _build_domains(
    frds: List[dict],
    psds: List[dict],
    dcs: List[dict],
) -> List[dict]:
    """
    Derive logical data domains.

    Primary:   One domain per PSD (each PSD represents one functional module).
    Supplement: DC data_product_identification.domain for any additional domains
                not already covered by the PSD set.
    """
    domains: List[dict] = []
    seq = 1

    for psd in psds:
        meta = psd.get("metadata", {})
        domains.append({
            "domain_id": f"DOM-{seq:02d}",
            "domain_name": meta.get("title", MARKER_DRAFT_REVIEW),
            "description": MARKER_AUTO_REVIEW,
            "owner": meta.get("author", MARKER_DRAFT_REVIEW),
            "related_modules": [_doc_id(psd)],
        })
        seq += 1

    # Supplement with DC-declared domains not already represented
    existing_names = {d["domain_name"].lower() for d in domains}
    for dc in dcs:
        dpi = dc.get("data_product_identification", {})
        domain = dpi.get("domain", "")
        if not domain or domain.lower() in existing_names:
            continue
        existing_names.add(domain.lower())
        domains.append({
            "domain_id": f"DOM-{seq:02d}",
            "domain_name": domain,
            "description": dpi.get("subdomain", MARKER_AUTO_REVIEW),
            "owner": dpi.get("owner_team", MARKER_DRAFT_REVIEW),
            "related_modules": [_doc_id(dc)],
        })
        seq += 1

    if not domains:
        domains.append({
            "domain_id": "DOM-01",
            "domain_name": MARKER_DRAFT_REVIEW,
            "description": MARKER_DRAFT_REVIEW,
            "owner": MARKER_DRAFT_REVIEW,
            "related_modules": [],
        })

    return domains


def _build_elements(dcs: List[dict], frds: List[dict]) -> List[dict]:
    """
    Build the data elements catalog.

    Primary source:   DC schema_definition.fields — already typed and constrained.
    Secondary source: FRD data_requirements.entities — entity-level stubs for
                      anything not yet in a formal data contract.
    """
    elements: List[dict] = []
    seen_names: set = set()
    seq = 1

    # --- Primary: DC fields ---
    for dc in dcs:
        dc_id = _doc_id(dc)
        dpi = dc.get("data_product_identification", {})
        domain_hint = (
            dpi.get("domain")
            or dc.get("contract_overview", {}).get("entity")
            or dc_id
        )
        for field in dc.get("schema_definition", {}).get("fields", []):
            name = field.get("field_name", "")
            if not name or name in seen_names:
                continue
            seen_names.add(name)
            constraints = field.get("constraints", "") or ""
            elements.append({
                "element_id":    f"DE-{seq:04d}",
                "element_name":  name,
                "display_name":  name.replace("_", " ").title(),
                "domain":        domain_hint,
                "definition":    field.get("description", MARKER_DRAFT_REVIEW),
                "data_type":     field.get("data_type", MARKER_DRAFT_REVIEW),
                "format":        MARKER_AUTO_COMPLETE,
                "length":        MARKER_AUTO_COMPLETE,
                "allowed_values": field.get("allowed_values", []),
                "nullable":      field.get("nullable", True),
                "unique":        False,
                "primary_key":   "PK" in constraints,
                "foreign_key":   "FK" in constraints,
                "sensitivity":   field.get("classification", "Internal"),
                "pii":           field.get("pii", False),
                "business_rules": field.get("semantic", MARKER_AUTO_COMPLETE),
                "example_values": [],
                "source_document": dc_id,
            })
            seq += 1

    # --- Secondary: FRD entity stubs ---
    for frd in frds:
        frd_id = _doc_id(frd)
        for ent in frd.get("data_requirements", {}).get("entities", []):
            name = ent.get("entity_name", "")
            stub_key = name.lower().replace(" ", "_")
            if not stub_key or stub_key in seen_names:
                continue
            seen_names.add(stub_key)
            elements.append({
                "element_id":    f"DE-{seq:04d}",
                "element_name":  stub_key,
                "display_name":  name,
                "domain":        MARKER_AUTO_REVIEW,
                "definition":    ent.get("description", MARKER_DRAFT_REVIEW),
                "data_type":     MARKER_DRAFT_REVIEW,
                "format":        MARKER_AUTO_COMPLETE,
                "length":        MARKER_AUTO_COMPLETE,
                "allowed_values": [],
                "nullable":      True,
                "unique":        False,
                "primary_key":   False,
                "foreign_key":   False,
                "sensitivity":   ent.get("sensitivity", "Internal"),
                "pii":           False,
                "business_rules": MARKER_AUTO_COMPLETE,
                "example_values": [],
                "source_document": frd_id,
            })
            seq += 1

    if not elements:
        elements.append({
            "element_id":   "DE-0001",
            "element_name": MARKER_DRAFT_REVIEW,
            "display_name": MARKER_DRAFT_REVIEW,
            "domain":       MARKER_DRAFT_REVIEW,
            "definition":   MARKER_DRAFT_REVIEW,
            "data_type":    MARKER_DRAFT_REVIEW,
        })

    return elements


def _build_er_summary(frds: List[dict], dcs: List[dict]) -> List[dict]:
    """
    Scaffold entity relationship stubs from FRD entity lists.

    Entities are listed in FRD order; relationships are sequential stubs
    that authors replace with real cardinality and type.
    """
    entities: List[str] = []
    seen: set = set()

    for frd in frds:
        for ent in frd.get("data_requirements", {}).get("entities", []):
            name = ent.get("entity_name", "")
            if name and name not in seen:
                seen.add(name)
                entities.append(name)

    if len(entities) < 2:
        return []

    return [
        {
            "relationship_id": f"REL-{i:03d}",
            "parent_entity":   entities[i - 1],
            "child_entity":    entities[i],
            "relationship_type": MARKER_DRAFT_REVIEW,
            "cardinality":       MARKER_DRAFT_REVIEW,
            "on_delete":         MARKER_AUTO_COMPLETE,
            "on_update":         MARKER_AUTO_COMPLETE,
        }
        for i in range(1, len(entities))
    ]


def _build_code_tables() -> List[dict]:
    """Return a placeholder code-table entry for authors to populate."""
    return [
        {
            "code_table_id":   "CT-001",
            "code_table_name": MARKER_DRAFT_REVIEW,
            "description":     MARKER_DRAFT_REVIEW,
            "owner":           MARKER_DRAFT_REVIEW,
            "codes":           [],
        }
    ]


def _build_glossary(dcs: List[dict], frds: List[dict]) -> List[dict]:
    """
    Compile the data glossary.

    Primary source:   DC semantic_definitions.business_glossary.
    Secondary source: FRD definitions.terms.
    """
    terms: List[dict] = []
    seen: set = set()
    seq = 1

    for dc in dcs:
        dc_id = _doc_id(dc)
        sem = dc.get("semantic_definitions", {})
        bg = (
            sem.get("business_glossary", []) if isinstance(sem, dict)
            else sem if isinstance(sem, list)
            else []
        )
        for g in bg:
            if not isinstance(g, dict):
                continue
            term = g.get("term", "")
            if not term or term.lower() in seen:
                continue
            seen.add(term.lower())
            terms.append({
                "term_id":       f"TRM-{seq:03d}",
                "term":          term,
                "definition":    g.get("definition", MARKER_DRAFT_REVIEW),
                "context":       MARKER_AUTO_REVIEW,
                "synonyms":      g.get("synonyms", []),
                "related_terms": [],
                "source":        dc_id,
                "category":      "Business",
            })
            seq += 1

    for frd in frds:
        frd_id = _doc_id(frd)
        defs = frd.get("definitions", {})
        term_list = defs.get("terms", []) if isinstance(defs, dict) else []
        for entry in term_list:
            if not isinstance(entry, dict):
                continue
            term = entry.get("term", entry.get("name", ""))
            definition = entry.get("definition", entry.get("description", MARKER_DRAFT_REVIEW))
            if not term or term.lower() in seen:
                continue
            seen.add(term.lower())
            terms.append({
                "term_id":       f"TRM-{seq:03d}",
                "term":          term,
                "definition":    definition,
                "context":       MARKER_AUTO_REVIEW,
                "synonyms":      [],
                "related_terms": [],
                "source":        frd_id,
                "category":      "Business",
            })
            seq += 1

    return terms


def _build_lineage(dcs: List[dict], mdcs: List[dict]) -> List[dict]:
    """
    Build data lineage stubs.

    DCs contribute internal source-system entries from lineage_and_dependencies.
    MDCs contribute external market-data sources from input_and_source_location.
    """
    lineage: List[dict] = []
    seq = 1

    for dc in dcs:
        dc_id = _doc_id(dc)
        lin = dc.get("lineage_and_dependencies", {})
        for src in lin.get("source_systems", []):
            if not isinstance(src, dict):
                continue
            lineage.append({
                "mapping_id":       f"LIN-{seq:03d}",
                "source_system":    src.get("system", MARKER_DRAFT_REVIEW),
                "source_field":     MARKER_AUTO_COMPLETE,
                "transformation":   src.get("description", MARKER_AUTO_COMPLETE),
                "target_system":    "Narwhal",
                "target_field":     MARKER_AUTO_COMPLETE,
                "target_element_id": MARKER_AUTO_COMPLETE,
                "frequency":        MARKER_AUTO_COMPLETE,
                "source_document":  dc_id,
            })
            seq += 1

    for mdc in mdcs:
        mdc_id = _doc_id(mdc)
        dpi = mdc.get("data_product_identification", {})
        product_name = dpi.get("product_name", mdc_id)
        for src in mdc.get("input_and_source_location", {}).get("source_systems", []):
            if not isinstance(src, dict):
                continue
            lineage.append({
                "mapping_id":       f"LIN-{seq:03d}",
                "source_system":    f"{product_name} / {src.get('source_id', MARKER_DRAFT_REVIEW)}",
                "source_field":     MARKER_AUTO_COMPLETE,
                "transformation":   src.get("description", MARKER_AUTO_COMPLETE),
                "target_system":    "Narwhal",
                "target_field":     MARKER_AUTO_COMPLETE,
                "target_element_id": MARKER_AUTO_COMPLETE,
                "frequency":        src.get("delivery_mechanism", MARKER_AUTO_COMPLETE),
                "source_document":  mdc_id,
            })
            seq += 1

    return lineage


def _build_quality_rules(dcs: List[dict]) -> List[dict]:
    """
    Compile data quality rules from DC data_quality_standards.quality_dimensions.

    Each quality dimension becomes a DQR entry; authors fill in target_elements
    and tighten rule_expression beyond the threshold value.
    """
    rules: List[dict] = []
    seen: set = set()
    seq = 1

    for dc in dcs:
        dc_id = _doc_id(dc)
        dqs = dc.get("data_quality_standards", {})
        dims = (
            dqs.get("quality_dimensions", []) if isinstance(dqs, dict)
            else dqs if isinstance(dqs, list)
            else []
        )
        for dim in dims:
            if not isinstance(dim, dict):
                continue
            name = dim.get("dimension", dim.get("rule_name", ""))
            if not name or name in seen:
                continue
            seen.add(name)
            rules.append({
                "rule_id":              f"DQR-{seq:03d}",
                "rule_name":            name,
                "description":          dim.get("metric", dim.get("description", MARKER_DRAFT_REVIEW)),
                "target_elements":      [],
                "rule_type":            "quality_dimension",
                "rule_expression":      dim.get("threshold", MARKER_AUTO_COMPLETE),
                "severity":             "Error",
                "action_on_failure":    MARKER_AUTO_COMPLETE,
                "measurement_frequency": dim.get("measurement_frequency", MARKER_AUTO_COMPLETE),
                "source_document":      dc_id,
            })
            seq += 1

    return rules
