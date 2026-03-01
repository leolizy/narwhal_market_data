"""
CLI helper for the Scaffold branch — scaffold status, artifact summary, sync check.

Commands:
  artifact-summary    — Scan knowledge artifacts and display a structured summary
  scaffold-status     — Show what has been scaffolded vs what is pending
  sync-check          — Detect stale scaffold output that needs regeneration

Usage (from repository root):
  python3 scaffold/build_chain/cli.py artifact-summary
  python3 scaffold/build_chain/cli.py scaffold-status
  python3 scaffold/build_chain/cli.py sync-check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Default base_dir: three levels up from this file → repository root
# (scaffold/build_chain/cli.py → build_chain → scaffold → root)
DEFAULT_BASE_DIR = str(Path(__file__).parent.parent.parent.resolve())

# Add scaffold/ to Python path so `from build_chain import ...` resolves correctly
_BODY_DIR = str(Path(__file__).parent.parent.resolve())
if _BODY_DIR not in sys.path:
    sys.path.insert(0, _BODY_DIR)


# ---------------------------------------------------------------------------
# artifact-summary
# ---------------------------------------------------------------------------

def run_artifact_summary(base_dir: str) -> None:
    """Scan knowledge artifacts and print a structured JSON summary."""
    from build_chain import reader

    artifacts = reader.list_knowledge_artifacts(base_dir)

    # Filter to artifact entries only (not rendered docs)
    artifact_entries = [
        a for a in artifacts
        if a.get("directory", "").startswith("knowledge/artifact")
    ]

    summaries = []
    for entry in artifact_entries:
        rel_path = entry.get("relative_path", "")
        abs_path = str(Path(base_dir) / rel_path)
        parsed = reader.read_artifact(abs_path)
        if parsed:
            summary = reader.extract_artifact_summary(parsed)
            summary["relative_path"] = rel_path
            summaries.append(summary)

    # Group by layer
    groups = reader.group_by_layer(artifact_entries)

    output = {
        "total_artifacts": len(summaries),
        "scaffoldable": len([
            s for s in summaries
            if s["document_id"].split("-")[0] in (
                "HLD", "TSI", "CICD", "DG", "DBAD", "DC",
                "API", "AEC", "DBC", "MDC", "UT", "NFTS"
            )
        ]),
        "by_layer": {layer: len(entries) for layer, entries in groups.items()},
        "artifacts": summaries,
    }
    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# scaffold-status
# ---------------------------------------------------------------------------

def run_scaffold_status(base_dir: str) -> None:
    """Show what has been scaffolded vs what is pending."""
    from build_chain import reader, scaffolder

    scaffoldable = reader.get_scaffoldable_artifacts(base_dir)
    report = scaffolder.scaffold_status_report(base_dir, scaffoldable)
    print(json.dumps(report, indent=2))


# ---------------------------------------------------------------------------
# sync-check
# ---------------------------------------------------------------------------

def run_sync_check(base_dir: str) -> None:
    """Detect stale scaffold output that needs regeneration."""
    from build_chain import reader, scaffolder

    scaffoldable = reader.get_scaffoldable_artifacts(base_dir)
    report = scaffolder.scaffold_status_report(base_dir, scaffoldable)

    sync_result = {
        "stale_files": report.get("stale", []),
        "total_scaffolded": len(report.get("scaffolded", [])),
        "total_pending": len(report.get("pending", [])),
        "total_stale": len(report.get("stale", [])),
    }

    if sync_result["total_stale"] == 0:
        sync_result["message"] = "All scaffolded files are up to date."
    else:
        sync_result["message"] = (
            f"{sync_result['total_stale']} file(s) reference outdated "
            f"knowledge artifact versions. Re-scaffold to update."
        )

    print(json.dumps(sync_result, indent=2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Narwhal Scaffold Branch CLI — scaffold management",
    )
    parser.add_argument(
        "--base-dir", default=DEFAULT_BASE_DIR,
        help="Repository root directory (default: auto-detected)",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "artifact-summary",
        help="Scan knowledge artifacts and display a structured summary",
    )
    subparsers.add_parser(
        "scaffold-status",
        help="Show what has been scaffolded vs what is pending",
    )
    subparsers.add_parser(
        "sync-check",
        help="Detect stale scaffold output that needs regeneration",
    )

    args = parser.parse_args()

    if args.command == "artifact-summary":
        run_artifact_summary(args.base_dir)
    elif args.command == "scaffold-status":
        run_scaffold_status(args.base_dir)
    elif args.command == "sync-check":
        run_sync_check(args.base_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
