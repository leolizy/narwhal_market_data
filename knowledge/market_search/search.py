#!/usr/bin/env python3
"""CLI entry point for market data search.

Usage:
    python3 knowledge/market_search/search.py list-exchanges
    python3 knowledge/market_search/search.py sources <EXCHANGE_CODE>
    python3 knowledge/market_search/search.py all-sources
"""

import json
import os
import sys

# Ensure knowledge/ is on sys.path so imports resolve.
_KNOWLEDGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _KNOWLEDGE_DIR not in sys.path:
    sys.path.insert(0, _KNOWLEDGE_DIR)

from market_search.exchanges.registry import get_adapter, list_exchanges


def cmd_list_exchanges():
    """Print JSON list of all registered exchanges."""
    data = []
    for ex in list_exchanges():
        data.append({
            "exchange_code": ex["exchange_code"],
            "exchange_name": ex["exchange_name"],
            "data_categories": ex["data_categories"],
        })
    print(json.dumps(data, indent=2))


def cmd_sources(code: str):
    """Print JSON with public URLs and data categories for one exchange."""
    try:
        adapter = get_adapter(code)
    except KeyError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(adapter.summary(), indent=2))


def cmd_all_sources():
    """Print JSON with all exchanges and their public URLs."""
    print(json.dumps(list_exchanges(), indent=2))


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps({"error": "Usage: search.py <list-exchanges|sources|all-sources> [args]"}),
            file=sys.stderr,
        )
        sys.exit(1)

    command = sys.argv[1]

    if command == "list-exchanges":
        cmd_list_exchanges()
    elif command == "sources":
        if len(sys.argv) < 3:
            print(
                json.dumps({"error": "Usage: search.py sources <EXCHANGE_CODE>"}),
                file=sys.stderr,
            )
            sys.exit(1)
        cmd_sources(sys.argv[2])
    elif command == "all-sources":
        cmd_all_sources()
    else:
        print(
            json.dumps({"error": f"Unknown command '{command}'. Use list-exchanges, sources, or all-sources."}),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
