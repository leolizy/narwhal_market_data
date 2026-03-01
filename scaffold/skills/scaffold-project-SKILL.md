---
name: scaffold-project
description: "Generate the overall project directory structure and module layout from HLD and TSI knowledge artifacts."
---

# Scaffold Project Structure

## Purpose

Generate the project's directory layout, module boundaries, and initial files
based on the High-Level Design (HLD) and Technical System Integration (TSI)
knowledge artifacts.

## Environment

- **Base directory:** `.`
- **Scaffold CLI:** `python3 scaffold/build_chain/cli.py <command> [args]`
- **Knowledge artifacts (read-only):** `knowledge/artifact/60_architecture/`
- **Output directory:** `scaffold/src/`

## Prerequisites

- HLD artifact must exist (required)
- TSI artifact is optional but recommended for integration points

## Workflow

### Step 1 — Read HLD artifact

Find and read the HLD artifact JSON from `knowledge/artifact/60_architecture/`.
Extract:
- `sections.system_architecture` — overall architecture pattern
- `sections.module_design` or equivalent — module list, boundaries
- `sections.technology_stack` — language, framework, runtime choices
- `metadata.document_id` and `metadata.version` — for traceability

### Step 2 — Read TSI artifact (if exists)

Find and read TSI artifact. Extract:
- `sections.integration_points` — external service boundaries
- `sections.service_topology` — how modules connect
- `sections.shared_components` — cross-module utilities

### Step 3 — Propose directory layout

Based on HLD modules and TSI integration points, propose:

```
scaffold/src/
├── [module_a]/           # From HLD module list
│   ├── __init__.py       # Adapt to detected language
│   └── ...
├── [module_b]/
├── shared/               # Cross-module utilities (from TSI)
│   └── __init__.py
└── README.md             # Architecture overview
```

Present the proposed tree to the user. Include:
- Module names and their purpose (from HLD)
- Technology choices (from HLD)
- Integration boundaries (from TSI)

### Step 4 — Get confirmation

Ask the user to confirm the proposed layout before writing any files.

### Step 5 — Write files

For each module directory:
1. Create the directory
2. Create an entry point file with traceability header
3. Create a module-level README or docstring explaining the module's purpose

Write `scaffold/src/README.md` summarising the overall architecture.

### Step 6 — Report

```
Scaffolded project structure from HLD-NNNN vX.Y:
  Created [N] module directories
  Created [N] entry point files
  Created scaffold/src/README.md

Next steps:
  → /scaffold-cicd to generate CI/CD pipeline configs
  → /scaffold-db to generate database schemas
  → /scaffold-api to generate API route stubs
```

## Rules

1. Never write outside `scaffold/`.
2. Always include traceability headers in generated files.
3. Adapt file extensions and entry points to the technology stack specified in HLD.
4. If HLD is missing, report the gap and recommend creating it first.
5. Always get user confirmation before writing.
6. Do not generate business logic — only structure and stubs.
