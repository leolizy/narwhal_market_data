"""Knowledge artifact reader — parse SDLC docs from the knowledge branch (read-only)."""
import json
import subprocess
import re
from pathlib import Path

from . import config


def list_knowledge_artifacts(base_dir: str) -> list[dict]:
    """Discover all knowledge artifacts via the knowledge CLI.

    Returns a list of dicts with: doc_type, document_id, relative_path, directory.
    """
    cli_path = str(Path(base_dir) / config.KNOWLEDGE_CLI)
    result = subprocess.run(
        ["python3", cli_path, "list-existing"],
        capture_output=True, text=True, cwd=base_dir, timeout=30,
    )
    if result.returncode != 0:
        return []

    try:
        data = json.loads(result.stdout)
        # Handle both {"documents": [...]} and flat [...] formats
        if isinstance(data, dict):
            return data.get("documents", [])
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, TypeError):
        return []


def read_artifact(file_path: str) -> dict | None:
    """Read and parse a single knowledge artifact JSON file.

    Returns the parsed dict with kind, metadata, and sections.
    Returns None if the file cannot be read or parsed.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return None


def extract_artifact_summary(artifact: dict) -> dict:
    """Extract key summary fields from a parsed artifact.

    Returns: {kind, document_id, version, status, section_keys, related_documents}
    """
    metadata = artifact.get("metadata", {})
    return {
        "kind": artifact.get("kind", artifact.get("openapi", "unknown")),
        "document_id": metadata.get("document_id", "unknown"),
        "version": metadata.get("version", "unknown"),
        "status": metadata.get("status", "unknown"),
        "section_keys": list(artifact.get("sections", {}).keys()),
        "related_documents": metadata.get("related_documents", []),
    }


def group_by_layer(artifacts: list[dict]) -> dict[str, list[dict]]:
    """Group artifact entries by SDLC layer.

    Uses the scaffold order to determine layer groupings.
    Returns {layer_name: [artifact_entries]}.
    """
    layer_map = {
        "HLD": "architecture", "TSI": "architecture",
        "CICD": "architecture", "DBAD": "architecture",
        "API": "contracts", "AEC": "contracts",
        "DC": "contracts", "DBC": "contracts", "MDC": "contracts",
        "DG": "deploy_test", "UT": "deploy_test", "NFTS": "deploy_test",
        "PC": "root", "FRD": "requirements", "NFR": "requirements",
        "PSD": "specification",
        "MVP": "aggregators", "RTM": "aggregators", "DD": "aggregators",
        "NFRAR": "deploy_test",
    }
    groups: dict[str, list[dict]] = {}
    for entry in artifacts:
        doc_type = entry.get("doc_type", "")
        layer = layer_map.get(doc_type, "other")
        groups.setdefault(layer, []).append(entry)
    return groups


def get_scaffoldable_artifacts(base_dir: str) -> list[dict]:
    """Get knowledge artifacts that have scaffold mappings.

    Returns only artifacts whose doc_type is in SCAFFOLD_MAP,
    sorted by SCAFFOLD_ORDER.
    """
    all_artifacts = list_knowledge_artifacts(base_dir)
    # Filter to only artifact entries (not rendered docs)
    artifact_entries = [
        a for a in all_artifacts
        if a.get("directory", "").startswith("knowledge/artifact")
    ]
    # Filter to scaffoldable types
    scaffoldable = [
        a for a in artifact_entries
        if a.get("doc_type") in config.SCAFFOLD_MAP
    ]
    # Sort by scaffold order
    order_index = {t: i for i, t in enumerate(config.SCAFFOLD_ORDER)}
    scaffoldable.sort(key=lambda a: order_index.get(a.get("doc_type", ""), 999))
    return scaffoldable


def parse_traceability_header(file_path: str) -> list[dict]:
    """Parse the traceability header from a scaffold-generated file.

    Returns list of {doc_id, version} dicts found in Source: lines.
    """
    try:
        with open(file_path, "r") as f:
            # Only check first 10 lines for the header
            head = "".join(f.readline() for _ in range(10))
    except (FileNotFoundError, PermissionError):
        return []

    results = []
    for match in re.finditer(config.TRACEABILITY_PATTERN, head):
        sources_str = match.group(1)
        for source in sources_str.split(","):
            source = source.strip()
            parts = source.split()
            doc_id = parts[0] if parts else ""
            version = parts[1].lstrip("v") if len(parts) > 1 else ""
            if doc_id:
                results.append({"doc_id": doc_id, "version": version})
    return results
