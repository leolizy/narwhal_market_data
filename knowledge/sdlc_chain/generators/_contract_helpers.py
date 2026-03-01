"""Shared helpers for contract generators (AEC, API, DC, DBC, MDC).

These utilities are used by all five contract generators to extract
common metadata from a source FRD dict.
"""


def extract_common(frd: dict, today: str) -> dict:
    """Pull reusable context from an FRD dict into a flat common dict."""
    meta = frd.get("metadata", {})
    raw_title = meta.get("title", "")
    module_name = raw_title.replace(" - Functional Requirements", "").strip() or "Module"
    return {
        "frd_id":        meta.get("document_id", "FRD-UNKNOWN"),
        "module_name":   module_name,
        "module_code":   meta.get("module_code", ""),
        "module_slug":   module_name.lower().replace(" ", "."),
        "author":        meta.get("author", ""),
        "reviewer":      meta.get("reviewer", ""),
        "approver":      meta.get("approver", ""),
        "classification": meta.get("classification", "Internal"),
        "parent_pc":    meta.get("parent_pc", ""),
        "today":         today,
    }
