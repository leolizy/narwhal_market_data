"""Chain configuration, document type registry, template paths, output directories."""
from pathlib import Path

# Base paths (relative to narwhal_doc root)
TEMPLATE_DIR = "knowledge/templates"
ARTIFACT_DIR = "knowledge/artifact"
DOC_DIR = "knowledge/req_doc"
DOC_MD_DIR = "knowledge/req_doc/md"
DOC_HTML_DIR = "knowledge/req_doc/html"
ARCHIVE_DIR = "archive"
STAGING_DIR = "staging"
TRACKER_FILENAME_YAML = "OUTSTANDING_ITEMS.yaml"
TRACKER_FILENAME_MD = "OUTSTANDING_ITEMS.md"

# Document chain order: parent → list of child types
# Represents both the Functional Hierarchy and Non-Functional Hierarchy
CHAIN_ORDER = [
    # Functional Hierarchy: PC → FRD → PSD → Contracts → Tests
    ("PC", ["FRD", "NFR"]),
    ("FRD", ["PSD"]),
    ("NFR", ["HLD", "CICD", "DBAD", "TSI"]),
    ("PSD", ["AEC", "API", "DC", "DBC", "MDC"]),

    # Contract layer
    ("AEC", ["UT"]),
    ("API", ["UT"]),
    ("DC", ["UT"]),
    ("DBC", ["UT"]),
    ("MDC", ["UT"]),

    # Architecture layer
    ("CICD", ["NFTS", "DG"]),
    ("DBAD", ["NFTS"]),
    ("TSI", ["NFTS"]),

    # Non-functional implementation layer
    ("NFTS", ["NFRAR", "MVP", "RTM"]),
    ("DG", ["MVP", "RTM"]),

    # Project facilitation (aggregators)
    ("UT", ["MVP", "RTM"]),
    ("NFRAR", ["MVP", "RTM"]),
]

# Document type → template directory mapping
TEMPLATE_PATHS = {
    "PC": "00_general",
    "FRD": "10_function",
    "NFR": "20_non_function",
    "PSD": "30_logical",
    "AEC": "40_contract",
    "API": "40_contract",
    "DC": "40_contract",
    "DBC": "40_contract",
    "MDC": "50_external_contract",
    "CICD": "70_nf_implementation",
    "DBAD": "70_nf_implementation",
    "HLD": "60_architecture",
    "TSI": "60_architecture",
    "NFTS": "70_nf_implementation",
    "DG": "70_nf_implementation",
    "UT": "80_test",
    "NFRAR": "80_test",
    "MVP": "90_project",
    "RTM": "90_project",
    "DD": "90_project",
}

# Document type → README filename
README_FILES = {
    "PC": "00-pc_README.md",
    "FRD": "11-frd_README.md",
    "NFR": "21-nfr_README.md",
    "PSD": "31-psd_README.md",
    "AEC": "41-aec_README.md",
    "API": "42-api_README.md",
    "DC": "43-dc_README.md",
    "DBC": "44-dbc_README.md",
    "MDC": "51-mdc_README.md",
    "CICD": "73-cicd_README.md",
    "DBAD": "74-dbad_README.md",
    "HLD": "61-hld_README.md",
    "TSI": "62-tsi_README.md",
    "NFTS": "71-nfts_README.md",
    "DG": "72-dg_README.md",
    "UT": "81-ut_README.md",
    "NFRAR": "82-nfrar_README.md",
    "MVP": "91-mvp_README.md",
    "RTM": "92-rtm_README.md",
    # DD has no README file on disk — intentionally omitted
}

# Document type → YAML template filename
YAML_TEMPLATES = {
    "PC": "00-pc_template.yaml",
    "FRD": "11-frd_template.yaml",
    "NFR": "21-nfr_template.yaml",
    "PSD": "31-psd_template.yaml",
    "AEC": "41-aec_template.yaml",
    "API": "42-api_schemas.yaml",
    "DC": "43-dc_template.yaml",
    "DBC": "44-dbc_template.yaml",
    "MDC": "51-mdc_template.yaml",
    "CICD": "73-cicd_template.yaml",
    "DBAD": "74-dbad_template.yaml",
    "HLD": "61-hld_template.yaml",
    "TSI": "62-tsi_template.yaml",
    "NFTS": "71-nfts_template.yaml",
    "DG": "72-dg_template.yaml",
    "UT": "81-ut_template.yaml",
    "NFRAR": "82-nfrar_template.yaml",
    "MVP": "91-mvp_template.yaml",
    "RTM": "92-rtm_template.yaml",
    "DD": "93-dd_template.yaml",
}

# Document type → Markdown template filename
MD_TEMPLATES = {
    "PC": "00-pc_template.md",
    "FRD": "11-frd_template.md",
    "NFR": "21-nfr_template.md",
    "PSD": "31-psd_template.md",
    "AEC": "41-aec_template.md",
    "DC": "43-dc_template.md",
    "DBC": "44-dbc_template.md",
    "MDC": "51-mdc_template.md",
    "CICD": "73-cicd_template.md",
    "DBAD": "74-dbad_template.md",
    "HLD": "61-hld_template.md",
    "TSI": "62-tsi_template.md",
    "NFTS": "71-nfts_template.md",
    "DG":   "72-dg_template.md",
    "UT":   "81-ut_template.md",
    "NFRAR": "82-nfrar_template.md",
    "MVP": "91-mvp_template.md",
    "RTM": "92-rtm_template.md",
    "DD": "93-dd_template.md",
}

# Version constants
DRAFT_VERSION = "0.1"
INITIAL_APPROVED_VERSION = "1.0"

# Marker strings
MARKER_AUTO_REVIEW = "[AUTO - Review]"
MARKER_AUTO_COMPLETE = "[AUTO - To be completed]"
MARKER_DRAFT_REVIEW = "[DRAFT - Needs Review]"

# Document statuses
STATUS_DRAFT = "Draft"
STATUS_IN_REVIEW = "InReview"
STATUS_APPROVED = "Approved"
STATUS_DEPRECATED = "Deprecated"

# Resolution states for proposed documents
RESOLUTION_PENDING = "pending"
RESOLUTION_CREATE = "create"
RESOLUTION_NOT_REQUIRED = "not_required"

# PSD archetypes
ARCHETYPE_DATA_PAGE = "DATA_PAGE"
ARCHETYPE_PROCESS_FLOW = "PROCESS_FLOW"
ARCHETYPE_STATUS_GROUP = "STATUS_GROUP"
VALID_ARCHETYPES = {ARCHETYPE_DATA_PAGE, ARCHETYPE_PROCESS_FLOW, ARCHETYPE_STATUS_GROUP}


def get_template_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the full path to a template file."""
    return Path(base_dir) / TEMPLATE_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_readme_path(base_dir: str, doc_type: str) -> Path:
    """Get the full path to a document type's README."""
    return get_template_path(base_dir, doc_type, README_FILES[doc_type])


def get_artifact_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the output path for a generated draft document under artifact/."""
    return Path(base_dir) / ARTIFACT_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_doc_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the output path for an approved document under doc/.

    Deprecated: prefer get_doc_md_path() or get_doc_html_path() for
    format-specific output directories.
    """
    return Path(base_dir) / DOC_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_doc_md_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the output path for a rendered Markdown document under doc/md/."""
    return Path(base_dir) / DOC_MD_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_doc_html_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the output path for a rendered HTML document under doc/html/."""
    return Path(base_dir) / DOC_HTML_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_archive_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the path for an archived (older version) document under archive/."""
    return Path(base_dir) / ARCHIVE_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_staging_path(base_dir: str, doc_type: str, filename: str) -> Path:
    """Get the path for a signed-off document waiting for approval under staging/."""
    return Path(base_dir) / STAGING_DIR / TEMPLATE_PATHS[doc_type] / filename


def get_downstream_types(doc_type: str) -> list:
    """Get the list of downstream document types for a given type."""
    for parent, children in CHAIN_ORDER:
        if parent == doc_type:
            return children
    return []


def get_chain_layer(doc_type: str) -> int:
    """Get the layer number for a document type in the SDLC hierarchy.

    Layer 0: Platform Canon (PC)
    Layer 1: Functional & Non-Functional Requirements (FRD, NFR)
    Layer 2: Product Specification (PSD)
    Layer 3: Architecture & Contracts (AEC, API, DC, DBC, CICD, DBAD, TSI)
    Layer 4: Testing & Validation (UT, NFRAR, NFTS, DG)
    Layer 5: Project Facilitation (MVP, RTM)
    """
    layer_map = {
        "PC": 0,
        "FRD": 1, "NFR": 1,
        "PSD": 2,
        "AEC": 3, "API": 3, "DC": 3, "DBC": 3, "MDC": 3, "HLD": 3, "CICD": 3, "DBAD": 3, "TSI": 3,
        "UT": 4, "NFRAR": 4, "NFTS": 4, "DG": 4,
        "MVP": 5, "RTM": 5,
        "DD": 0,
    }
    return layer_map.get(doc_type, -1)
