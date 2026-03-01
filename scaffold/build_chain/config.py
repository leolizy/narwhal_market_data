"""Build chain configuration — scaffold mapping, paths, processing order."""
from pathlib import Path

# Base paths (relative to repository root)
BODY_DIR = "scaffold"
BODY_SRC = "scaffold/src"
BODY_CONFIG = "scaffold/config"
BODY_CI = "scaffold/ci"
BODY_DB = "scaffold/db"
BODY_TESTS = "scaffold/tests"
BODY_TESTS_UNIT = "scaffold/tests/unit"
BODY_TESTS_PERF = "scaffold/tests/performance"
BODY_TMP = "scaffold/.tmp"

# Knowledge paths (read-only)
KNOWLEDGE_ARTIFACT_DIR = "knowledge/artifact"
KNOWLEDGE_CLI = "knowledge/sdlc_chain/cli.py"

# SDLC doc type -> scaffold action and output directory
SCAFFOLD_MAP = {
    "HLD":  {"action": "project_layout",    "output": BODY_SRC,        "description": "Project architecture, module layout"},
    "TSI":  {"action": "integration_points", "output": BODY_SRC,        "description": "Integration points, service boundaries"},
    "CICD": {"action": "ci_pipeline",        "output": BODY_CI,         "description": "CI/CD pipeline configs"},
    "DG":   {"action": "deployment_config",  "output": BODY_CONFIG,     "description": "Deployment configs, Docker, K8s manifests"},
    "DBAD": {"action": "db_schema",          "output": BODY_DB,         "description": "Database schemas, migration scaffolds"},
    "DC":   {"action": "data_models",        "output": BODY_SRC,        "description": "Data models, type definitions"},
    "API":  {"action": "api_routes",         "output": BODY_SRC + "/api",    "description": "API route stubs, OpenAPI server scaffolds"},
    "AEC":  {"action": "event_handlers",     "output": BODY_SRC + "/events", "description": "Event handler stubs, message schemas"},
    "DBC":  {"action": "db_contracts",       "output": BODY_SRC,        "description": "DB contract implementations, repository stubs"},
    "MDC":  {"action": "market_adapters",    "output": BODY_SRC,        "description": "Market data adapter stubs"},
    "UT":   {"action": "unit_tests",         "output": BODY_TESTS_UNIT, "description": "Unit test stubs, test fixtures"},
    "NFTS": {"action": "perf_tests",         "output": BODY_TESTS_PERF, "description": "Performance/load test scaffolds"},
}

# Processing order: follows SDLC layer dependencies
# Architecture -> Contracts -> Testing
SCAFFOLD_ORDER = [
    # Layer 3 — Architecture
    "HLD", "TSI", "CICD", "DBAD",
    # Layer 3 — Contracts
    "API", "AEC", "DC", "DBC", "MDC",
    # Layer 4 — Deploy & Test
    "DG", "UT", "NFTS",
]

# Traceability header pattern (regex for parsing)
TRACEABILITY_PATTERN = r"Source:\s+([\w-]+(?:\s+v[\d.]+)?(?:,\s*[\w-]+(?:\s+v[\d.]+)?)*)"

# Comment syntax by file extension
COMMENT_STYLES = {
    ".py":   "#",
    ".yaml": "#",
    ".yml":  "#",
    ".sh":   "#",
    ".toml": "#",
    ".ts":   "//",
    ".js":   "//",
    ".go":   "//",
    ".rs":   "//",
    ".java": "//",
    ".sql":  "--",
    ".html": "<!-- {} -->",
    ".xml":  "<!-- {} -->",
    ".md":   "<!-- {} -->",
}


def get_comment_prefix(file_ext: str) -> str:
    """Return the line comment prefix for a file extension."""
    style = COMMENT_STYLES.get(file_ext, "//")
    if "{}" in style:
        return style  # Template-based (HTML/XML)
    return style


def get_scaffold_path(base_dir: str, relative: str) -> Path:
    """Get absolute path for a scaffold output file."""
    return Path(base_dir) / relative


def get_scaffold_info(doc_type: str) -> dict | None:
    """Get scaffold mapping for a knowledge doc type."""
    return SCAFFOLD_MAP.get(doc_type)
