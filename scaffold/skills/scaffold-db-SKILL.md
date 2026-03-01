---
name: scaffold-db
description: "Generate database schema files and migration scaffolds from DBAD and DC knowledge artifacts."
---

# Scaffold Database

## Purpose

Generate database schemas, migration files, and ORM model stubs based on
the Database Architecture Design (DBAD) and Data Contract (DC) knowledge
artifacts.

## Environment

- **Base directory:** `.`
- **Knowledge artifacts (read-only):**
  - `knowledge/artifact/70_nf_implementation/` (DBAD)
  - `knowledge/artifact/40_contract/` (DC)
- **Output directory:** `scaffold/db/`

## Prerequisites

- DBAD artifact must exist (required)
- DC artifact is optional but provides field-level detail

## Workflow

### Step 1 — Read DBAD artifact

Find and read the DBAD artifact JSON. Extract:
- `sections.database_design` — table/collection designs, relationships
- `sections.indexing_strategy` — index definitions
- `sections.partitioning` — sharding/partitioning schemes
- `sections.technology` — database engine (PostgreSQL, MongoDB, etc.)

### Step 2 — Read DC artifact(s) (if exist)

Find and read DC artifacts. Extract:
- `sections.data_entities` — entity definitions, field types, constraints
- `sections.validation_rules` — data validation requirements
- `sections.relationships` — foreign keys, references

### Step 3 — Propose schema files

```
scaffold/db/
├── migrations/
│   └── 001_initial_schema.sql   # DDL from DBAD table designs
├── models/
│   └── [entity].py              # ORM stubs from DC entities
└── seeds/
    └── seed_template.sql        # Seed data template
```

Present the proposed files with table names, key fields, and relationships.

### Step 4 — Get confirmation and write

Generate each file with traceability headers.

### Step 5 — Report

Show created files, table counts, and recommended next steps.

## Rules

1. Never write outside `scaffold/`.
2. Always include traceability headers.
3. Match database engine to what DBAD specifies (SQL dialect, ORM choice).
4. If DBAD is missing, report the gap — do not scaffold partial schemas.
5. Always get user confirmation before writing.
6. Constraints and indexes must match DBAD specifications exactly.
