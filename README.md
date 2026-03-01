# Narwhal — SDLC Doc-to-Code Repository

Narwhal is a structured **SDLC documentation management system** that generates, validates, and maintains a complete tree of software development lifecycle documents. It uses YAML/Markdown templates with a Python CLI to enforce document dependencies, versioning, and rendering.

## Repository Structure

```
├── knowledge/              # Documentation, templates, scripts, and generated artifacts
│   ├── SKILL.md            # Main workflow guide (SDLC tree builder)
│   ├── AGENTS.md           # Agent system prompt and guidelines
│   ├── sdlc_chain/         # Core CLI — generators, parsers, config, validation
│   ├── market_search/      # Financial market data search utilities
│   ├── templates/          # YAML + Markdown templates for all 20 doc types
│   ├── skills/             # Skill definitions (all workflows + dashboard tools)
│   ├── artifact/           # Generated JSON document artifacts
│   └── req_doc/            # Rendered output (md/ and html/)
│
├── .claude/                # Claude Code configuration (hooks, agents)
├── requirements.txt
└── README.md
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

Requires **Python 3.8+** and **PyYAML**.

## Usage

All commands run from the repository root.

### Core CLI

```bash
# List all existing documents and their status
python3 knowledge/sdlc_chain/cli.py list-existing

# Extract a blank template as JSON for a document type
python3 knowledge/sdlc_chain/cli.py template <DOC_TYPE>

# Validate a document against its template
python3 knowledge/sdlc_chain/cli.py validate <DOC_TYPE> <ARTIFACT_PATH>

# Archive an existing artifact before overwriting
python3 knowledge/sdlc_chain/cli.py archive <PATH>

# Auto-detect the document type of a file
python3 knowledge/sdlc_chain/cli.py detect <FILE_PATH>

# Show downstream dependencies of a document type
python3 knowledge/sdlc_chain/cli.py downstream <DOC_TYPE>

# Generate a module mapping template
python3 knowledge/sdlc_chain/cli.py mapping-template <PC_PATH> <PROJECT_CODE>
```

### Market Data Search

```bash
python3 knowledge/market_search/search.py list-exchanges
python3 knowledge/market_search/search.py sources <EXCHANGE_CODE>
python3 knowledge/market_search/search.py all-sources
```

## Document Types

Narwhal manages **20 SDLC document types** across 6 hierarchical layers:

| Layer | Documents | Description |
|-------|-----------|-------------|
| 0 | **PC** | Platform Canon — root document |
| 1 | **FRD**, **NFR** | Functional & Non-Functional Requirements |
| 2 | **PSD** | Product Specification Document |
| 3 | **AEC**, **API**, **DC**, **DBC**, **MDC**, **HLD**, **CICD**, **DBAD**, **TSI** | Contracts, Architecture & Implementation |
| 4 | **UT**, **NFRAR**, **NFTS**, **DG** | Testing & Deployment |
| 5 | **MVP**, **RTM**, **DD** | Project Aggregators |

Documents are created in layer order — no downstream document can be generated before its parents exist.

## Workflow

1. **Start with the Platform Canon (PC)** — the root document defining project scope
2. **Walk the tree** — use `list-existing` to see what's missing, then create documents layer by layer
3. **Generate artifacts** — each document is saved as JSON in `knowledge/artifact/`
4. **Render outputs** — Markdown and HTML are written to `knowledge/req_doc/md/` and `knowledge/req_doc/html/`
5. **Archive before update** — always archive an existing artifact before overwriting with a new version
6. **Validate** — the CLI validates every artifact against its template schema

## Templates

Each document type has a template set in `knowledge/templates/`:

- `*_template.yaml` — YAML structure template (schema)
- `*_template.md` — Markdown rendering template
- `*_README.md` — User guidance for that document type

## Claude Code Integration

This repository includes Claude Code skills for interactive document creation:

- **sdlc-doc-intake** — Guided workflow to create any SDLC document
- **mvp-create / mvp-update** — MVP-specific workflows
- **nfr-refresh** — NFR update workflow
- **doc-status / doc-diff / doc-impact** — Dashboard and analysis tools
- **pre-generate / project-refresh** — Preflight checks and health reports
