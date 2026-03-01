"""
CLI helper for the SDLC document intake skill.

Commands:
  template <DOC_TYPE>    — Extract template sections and README guidance as JSON
  list-existing          — Scan artifact/ and doc/ for existing YAML documents
  downstream <DOC_TYPE>  — Get all transitive downstream doc types via BFS

Usage (from repository root):
  python3 knowledge/sdlc_chain/cli.py template PC
  python3 knowledge/sdlc_chain/cli.py list-existing
  python3 knowledge/sdlc_chain/cli.py downstream FRD
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

# Default base_dir: three levels up from this file → repository root
# (knowledge/sdlc_chain/cli.py → sdlc_chain → knowledge → root)
DEFAULT_BASE_DIR = str(Path(__file__).parent.parent.parent.resolve())

# Add knowledge/ to Python path so `from sdlc_chain import ...` resolves correctly
_KNOWLEDGE_DIR = str(Path(__file__).parent.parent.resolve())
if _KNOWLEDGE_DIR not in sys.path:
    sys.path.insert(0, _KNOWLEDGE_DIR)

# Synthetic section returned for the API doc type (OpenAPI spec, not section-structured)
_API_SYNTHETIC_SECTION = {
    "section": "openapi_spec",
    "required": True,
    "guidance": (
        "Full OpenAPI 3.x specification. Describe your API paths, request/response "
        "schemas, authentication mechanisms, and any reusable components. "
        "Reference: OAS 3.0 — info, paths, components, security."
    ),
    "key_fields": ["openapi", "info", "paths", "components", "security"],
}


# ---------------------------------------------------------------------------
# Template command
# ---------------------------------------------------------------------------

def run_template(doc_type: str, base_dir: str) -> None:
    """Print JSON describing the sections of a doc type's YAML template."""
    from sdlc_chain import config
    from sdlc_chain.yaml_utils import load_yaml

    if doc_type not in config.YAML_TEMPLATES:
        _err(f"Unknown doc type '{doc_type}'. Valid types: {sorted(config.YAML_TEMPLATES)}")

    yaml_template_file = config.YAML_TEMPLATES[doc_type]
    template_dir = config.TEMPLATE_PATHS[doc_type]
    yaml_path = Path(base_dir) / config.TEMPLATE_DIR / template_dir / yaml_template_file

    # --- Special case: API doc type uses an OpenAPI schema file, not a section template ---
    if doc_type == "API":
        result = {
            "doc_type": "API",
            "yaml_template_path": str(yaml_path),
            "sections": [_API_SYNTHETIC_SECTION],
            "readme_guidance": _read_readme(doc_type, base_dir, config),
        }
        print(json.dumps(result, indent=2))
        return

    if not yaml_path.exists():
        _err(f"Template file not found: {yaml_path}")

    raw = load_yaml(str(yaml_path))
    sections = _extract_sections(raw)

    result = {
        "doc_type": doc_type,
        "yaml_template_path": str(yaml_path),
        "sections": sections,
        "readme_guidance": _read_readme(doc_type, base_dir, config),
    }
    print(json.dumps(result, indent=2))


def _extract_sections(raw: dict) -> list:
    """
    Extract section descriptors from a flat-structure YAML template dict.

    Each top-level key that maps to a dict becomes a section. The metadata
    key gets special treatment (flat fields, no description/required).
    """
    sections = []
    for key, value in raw.items():
        if not isinstance(value, dict):
            continue  # skip string/list top-level keys (comments parsed as scalars, etc.)

        if key == "metadata":
            sections.append({
                "section": "metadata",
                "required": True,
                "guidance": "Document identity, ownership, version, and lifecycle metadata.",
                "key_fields": [k for k in value.keys()],
            })
            continue

        guidance = value.get("description", "")
        # description may be a multi-line string — normalise whitespace for JSON
        if isinstance(guidance, str):
            guidance = " ".join(guidance.split())

        required = value.get("required", False)
        key_fields = [k for k in value.keys() if k not in ("description", "required")]

        sections.append({
            "section": key,
            "required": bool(required),
            "guidance": guidance,
            "key_fields": key_fields,
        })

    return sections


def _read_readme(doc_type: str, base_dir: str, config) -> str:
    """Read up to 3000 chars of the README for a doc type. Returns '' if missing."""
    if doc_type not in config.README_FILES:
        return ""
    try:
        readme_path = config.get_readme_path(base_dir, doc_type)
        text = readme_path.read_text(encoding="utf-8")
        return text[:3000]
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# List-existing command
# ---------------------------------------------------------------------------

def run_list_existing(base_dir: str) -> None:
    """Print JSON listing all .json/.yaml files found in artifact/ and doc/."""
    from sdlc_chain import detector
    from sdlc_chain.yaml_utils import load_yaml, load_json

    base = Path(base_dir)
    # artifact/ holds .json (new format) and legacy .yaml
    # doc/md/ holds rendered Markdown; doc/html/ holds rendered HTML
    search_dirs = [base / "artifact", base / "doc" / "md", base / "doc" / "html", base / "staging"]
    documents = []

    for directory in search_dirs:
        if not directory.exists():
            continue
        dir_label = directory.name  # "artifact", "doc", or "staging"
        candidates = sorted(
            list(directory.rglob("*.json")) + list(directory.rglob("*.yaml"))
        )
        for doc_file in candidates:
            detected_type = "UNKNOWN"
            doc_id = ""
            try:
                ext = doc_file.suffix.lower()
                data = load_json(str(doc_file)) if ext == ".json" else load_yaml(str(doc_file))
                detected_type = detector.detect_document_type(data)
                meta = data.get("metadata") or {}
                doc_id = (
                    meta.get("document_id", "")
                    or meta.get("id", "")
                    or ""
                )
            except Exception:
                detected_type = "ERROR"

            documents.append({
                "path": str(doc_file),
                "relative_path": str(doc_file.relative_to(base)),
                "doc_type": detected_type,
                "document_id": str(doc_id) if doc_id else "",
                "directory": dir_label,
            })

    print(json.dumps({"documents": documents}, indent=2))


# ---------------------------------------------------------------------------
# Downstream command
# ---------------------------------------------------------------------------

def run_downstream(doc_type: str) -> None:
    """Print JSON listing all transitive downstream doc types via BFS."""
    from sdlc_chain.config import CHAIN_ORDER, get_chain_layer

    # Build adjacency map
    adjacency: dict[str, list[str]] = {}
    for parent, children in CHAIN_ORDER:
        adjacency[parent] = children

    if doc_type not in adjacency and doc_type not in {
        child for children in adjacency.values() for child in children
    }:
        _err(f"Unknown doc type '{doc_type}'.")

    # BFS from direct children of source (source itself is not included)
    # Track (node, hop_count, immediate_parent) in the queue
    initial_children = adjacency.get(doc_type, [])
    queue = [(child, 1, doc_type) for child in initial_children]
    visited: set[str] = set()
    ordered: list[dict] = []

    while queue:
        current, hop, parent = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        ordered.append({
            "doc_type": current,
            "layer": get_chain_layer(current),
            "hop_count": hop,
            "immediate_parent": parent,
        })
        for child in adjacency.get(current, []):
            if child not in visited:
                queue.append((child, hop + 1, current))

    print(json.dumps({
        "source_doc_type": doc_type,
        "all_downstream": ordered,
        "count": len(ordered),
    }, indent=2))


# ---------------------------------------------------------------------------
# Detect command
# ---------------------------------------------------------------------------

def run_detect(path: str) -> None:
    """Detect the document type of a YAML or JSON file and print JSON result."""
    from sdlc_chain import detector
    from sdlc_chain.yaml_utils import load_yaml, load_json

    file_path = Path(path)
    if not file_path.exists():
        _err(f"File not found: {path}")

    ext = file_path.suffix.lower()
    if ext == ".json":
        data = load_json(str(file_path))
        doc_type = detector.detect_document_type(data)
    else:
        doc_type = detector.detect_from_file(str(file_path))

    print(json.dumps({"path": path, "doc_type": doc_type}, indent=2))


# ---------------------------------------------------------------------------
# Validate command
# ---------------------------------------------------------------------------

def run_validate(doc_type: str, path: str, base_dir: str) -> None:
    """Validate a YAML document against its template's required sections."""
    from sdlc_chain import config
    from sdlc_chain.yaml_utils import load_yaml

    file_path = Path(path)
    if not file_path.exists():
        _err(f"File not found: {path}")

    if doc_type not in config.YAML_TEMPLATES:
        _err(f"Unknown doc type '{doc_type}'. Valid types: {sorted(config.YAML_TEMPLATES)}")

    # Load the document (JSON or YAML)
    try:
        from sdlc_chain.yaml_utils import load_json
        ext = file_path.suffix.lower()
        doc_data = load_json(str(file_path)) if ext == ".json" else load_yaml(str(file_path))
    except Exception as exc:
        _err(f"Failed to parse document: {exc}")

    # Load the template to find required sections
    template_path = config.get_template_path(base_dir, doc_type, config.YAML_TEMPLATES[doc_type])
    errors: list[str] = []
    warnings: list[str] = []

    if doc_type == "API":
        # OpenAPI: just check the openapi key exists
        if "openapi" not in doc_data:
            errors.append("Missing top-level 'openapi' key (expected for API/OpenAPI spec)")
    elif template_path.exists():
        try:
            template = load_yaml(str(template_path))
        except Exception as exc:
            _err(f"Failed to parse template: {exc}")

        for key, value in template.items():
            if not isinstance(value, dict):
                continue
            required = value.get("required", False)
            present = key in doc_data
            content = doc_data.get(key)

            if required and not present:
                errors.append(f"Missing required section: '{key}'")
            elif required and present:
                # Check if the section has any non-empty content
                if content is None or content == {} or content == [] or content == "":
                    warnings.append(f"Required section '{key}' is present but empty")

    # Check document ID format
    meta = doc_data.get("metadata") or doc_data.get("meta") or {}
    if isinstance(meta, dict):
        doc_id = meta.get("document_id", "") or meta.get("id", "")
        if doc_id and not str(doc_id).startswith(doc_type + "-"):
            if doc_type not in ("PC",):  # PC uses apiVersion/kind, not document_id
                warnings.append(
                    f"document_id '{doc_id}' does not start with '{doc_type}-'"
                )

    status = "valid" if not errors else "invalid"
    print(json.dumps({
        "path": path,
        "doc_type": doc_type,
        "status": status,
        "errors": errors,
        "warnings": warnings,
    }, indent=2))


# ---------------------------------------------------------------------------
# Mapping-template command
# ---------------------------------------------------------------------------

def run_mapping_template(pc_path: str, project_code: str, base_dir: str) -> None:
    """Generate a module mapping template YAML from a PC file and print it."""
    import yaml as _yaml
    from sdlc_chain.parsers.pc_parser import load_pc
    from sdlc_chain.mapping import generate_mapping_template

    pc_file = Path(pc_path)
    if not pc_file.exists():
        _err(f"PC file not found: {pc_path}")

    try:
        pc = load_pc(str(pc_file))
    except Exception as exc:
        _err(f"Failed to parse PC: {exc}")

    mapping = generate_mapping_template(pc, project_code)
    print(_yaml.dump(mapping, default_flow_style=False, sort_keys=False, allow_unicode=True))


# ---------------------------------------------------------------------------
# Archive command
# ---------------------------------------------------------------------------

def run_archive(path: str, base_dir: str) -> None:
    """Copy a document to the archive/ directory, preserving its subdirectory structure.

    The source file stays in place. The archive copy records the older version
    before a new version overwrites it in artifact/.
    """
    from sdlc_chain import config, detector
    from sdlc_chain.yaml_utils import load_yaml, load_json

    src = Path(path).resolve()
    if not src.exists():
        _err(f"File not found: {path}")

    ext = src.suffix.lower()
    try:
        data = load_json(str(src)) if ext == ".json" else load_yaml(str(src))
        doc_type = detector.detect_document_type(data)
    except Exception as exc:
        _err(f"Could not load/detect document: {exc}")

    if doc_type == "UNKNOWN" or doc_type not in config.TEMPLATE_PATHS:
        _err(f"Cannot determine doc type for archiving (detected: {doc_type})")

    dest = config.get_archive_path(base_dir, doc_type, src.name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dest))

    print(json.dumps({
        "status": "archived",
        "source": str(src),
        "archived_to": str(dest),
        "doc_type": doc_type,
    }, indent=2))


# ---------------------------------------------------------------------------
# Stage command
# ---------------------------------------------------------------------------

def run_generate_dd(base_dir: str, system_name: str) -> None:
    """Load all existing artifacts, generate a DD scaffold, and write JSON + MD + HTML."""
    from sdlc_chain import config, detector
    from sdlc_chain.generators import generate_dd
    from sdlc_chain.generators.md_renderer import render_dd_markdown
    from sdlc_chain.generators.html_renderer import render_markdown_to_html
    from sdlc_chain.naming import generate_dd_filename
    from sdlc_chain.yaml_utils import load_yaml, load_json

    base = Path(base_dir)
    artifact_dir = base / "artifact"

    # Collect all artifacts
    artifacts: list[dict] = []
    if artifact_dir.exists():
        for doc_file in sorted(
            list(artifact_dir.rglob("*.json")) + list(artifact_dir.rglob("*.yaml"))
        ):
            try:
                ext = doc_file.suffix.lower()
                data = load_json(str(doc_file)) if ext == ".json" else load_yaml(str(doc_file))
                doc_type = detector.detect_document_type(data)
                if doc_type not in ("UNKNOWN", "ERROR", "DD"):
                    data["_source_path"] = str(doc_file)
                    artifacts.append(data)
            except Exception:
                continue

    # Generate DD
    dd = generate_dd(artifacts, sequence=1, system_name=system_name)

    # Determine filenames
    version = dd.get("metadata", {}).get("version", config.DRAFT_VERSION)
    json_name = generate_dd_filename(1, system_name, version, "json")
    md_name = generate_dd_filename(1, system_name, version, "md")
    html_name = generate_dd_filename(1, system_name, version, "html")

    # Write JSON artifact
    json_path = config.get_artifact_path(base_dir, "DD", json_name)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    import json as _json
    json_path.write_text(_json.dumps(dd, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write MD
    md_content = render_dd_markdown(dd)
    md_path = config.get_doc_md_path(base_dir, "DD", md_name)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md_content, encoding="utf-8")

    # Write HTML
    html_content = render_markdown_to_html(md_content, title=dd.get("metadata", {}).get("title", "Data Dictionary"))
    html_path = config.get_doc_html_path(base_dir, "DD", html_name)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_content, encoding="utf-8")

    print(json.dumps({
        "status": "generated",
        "artifacts_consumed": len(artifacts),
        "system_name": system_name,
        "files": {
            "json": str(json_path),
            "md": str(md_path),
            "html": str(html_path),
        },
    }, indent=2))


def run_stage(path: str, base_dir: str) -> None:
    """Copy a signed-off document to the staging/ directory for approval handoff.

    Preserves the same subdirectory structure as artifact/. The original file
    remains in place; staging/ acts as a holding area before final promotion.
    """
    from sdlc_chain import config, detector
    from sdlc_chain.yaml_utils import load_yaml, load_json

    src = Path(path).resolve()
    if not src.exists():
        _err(f"File not found: {path}")

    ext = src.suffix.lower()
    try:
        data = load_json(str(src)) if ext == ".json" else load_yaml(str(src))
        doc_type = detector.detect_document_type(data)
    except Exception as exc:
        _err(f"Could not load/detect document: {exc}")

    if doc_type == "UNKNOWN" or doc_type not in config.TEMPLATE_PATHS:
        _err(f"Cannot determine doc type for staging (detected: {doc_type})")

    dest = config.get_staging_path(base_dir, doc_type, src.name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dest))

    print(json.dumps({
        "status": "staged",
        "source": str(src),
        "staged_to": str(dest),
        "doc_type": doc_type,
    }, indent=2))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _err(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="SDLC Chain CLI helper for the document intake skill"
    )
    parser.add_argument(
        "--base-dir",
        default=DEFAULT_BASE_DIR,
        help="Path to narwhal_doc root (default: auto-detected from script location)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # template
    t_parser = subparsers.add_parser("template", help="Get template sections for a doc type")
    t_parser.add_argument("doc_type", help="Doc type abbreviation, e.g. PC, FRD, NFR")

    # list-existing
    subparsers.add_parser("list-existing", help="Scan artifact/ and doc/ for YAML documents")

    # downstream
    d_parser = subparsers.add_parser("downstream", help="Get all transitive downstream doc types")
    d_parser.add_argument("doc_type", help="Source doc type abbreviation, e.g. PC, FRD")

    # detect
    det_parser = subparsers.add_parser("detect", help="Detect the document type of a YAML file")
    det_parser.add_argument("path", help="Path to the YAML file")

    # validate
    v_parser = subparsers.add_parser("validate", help="Validate a YAML document against its template")
    v_parser.add_argument("doc_type", help="Expected doc type, e.g. PC, FRD")
    v_parser.add_argument("path", help="Path to the YAML file to validate")

    # mapping-template
    mt_parser = subparsers.add_parser(
        "mapping-template",
        help="Generate a module mapping template YAML from a PC file",
    )
    mt_parser.add_argument("pc_path", help="Path to the PC YAML file")
    mt_parser.add_argument("project_code", help="Project code, e.g. NPH")

    # archive
    ar_parser = subparsers.add_parser(
        "archive",
        help="Copy an older version document to the archive/ directory",
    )
    ar_parser.add_argument("path", help="Path to the document file (.json or .yaml)")

    # stage
    st_parser = subparsers.add_parser(
        "stage",
        help="Copy a signed-off document to the staging/ directory",
    )
    st_parser.add_argument("path", help="Path to the document file (.json or .yaml)")

    # generate-dd
    dd_parser = subparsers.add_parser(
        "generate-dd",
        help="Generate a Data Dictionary from all existing artifacts",
    )
    dd_parser.add_argument("system_name", help="System/project name, e.g. Narwhal")

    args = parser.parse_args()

    # Add knowledge/ to sys.path so `sdlc_chain` is importable
    knowledge_dir = str((Path(args.base_dir) / "knowledge").resolve())
    if knowledge_dir not in sys.path:
        sys.path.insert(0, knowledge_dir)

    try:
        if args.command == "template":
            run_template(args.doc_type.upper(), args.base_dir)
        elif args.command == "list-existing":
            run_list_existing(args.base_dir)
        elif args.command == "downstream":
            run_downstream(args.doc_type.upper())
        elif args.command == "detect":
            run_detect(args.path)
        elif args.command == "validate":
            run_validate(args.doc_type.upper(), args.path, args.base_dir)
        elif args.command == "mapping-template":
            run_mapping_template(args.pc_path, args.project_code.upper(), args.base_dir)
        elif args.command == "archive":
            run_archive(args.path, args.base_dir)
        elif args.command == "stage":
            run_stage(args.path, args.base_dir)
        elif args.command == "generate-dd":
            run_generate_dd(args.base_dir, args.system_name)
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
