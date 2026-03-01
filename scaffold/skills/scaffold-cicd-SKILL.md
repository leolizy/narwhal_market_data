---
name: scaffold-cicd
description: "Generate CI/CD pipeline configuration files from CICD and DG knowledge artifacts."
---

# Scaffold CI/CD Pipelines

## Purpose

Generate CI/CD pipeline definitions and deployment configuration files
based on the CICD Framework and Deployment Guide knowledge artifacts.

## Environment

- **Base directory:** `.`
- **Knowledge artifacts (read-only):** `knowledge/artifact/70_nf_implementation/`
- **Output directories:** `scaffold/ci/`, `scaffold/config/`

## Prerequisites

- CICD artifact must exist (required)
- DG artifact is optional but recommended for deployment targets

## Workflow

### Step 1 — Read CICD artifact

Find and read the CICD artifact JSON. Extract:
- `sections.pipeline_stages` — build, test, deploy stages
- `sections.environments` — dev, staging, production
- `sections.quality_gates` — lint, test coverage, security scan thresholds
- `sections.triggers` — branch patterns, PR events, schedules

### Step 2 — Read DG artifact (if exists)

Find and read DG artifact. Extract:
- `sections.deployment_targets` — cloud provider, container orchestration
- `sections.rollback_procedures` — rollback strategy
- `sections.health_checks` — readiness/liveness probes
- `sections.container_specs` — Dockerfile requirements

### Step 3 — Propose pipeline files

Based on the artifacts, propose a file list:

```
scaffold/ci/
├── ci.yml                # Main CI pipeline
├── cd.yml                # Deployment pipeline (if DG exists)
└── quality-gates.yml     # Quality gate definitions

scaffold/config/
├── Dockerfile            # Container build (if DG specifies containers)
├── docker-compose.yml    # Local development stack
└── env.template          # Environment variable template
```

Present each file with a brief description of what it will contain.

### Step 4 — Get confirmation and write

After user confirmation, generate each file with:
- Traceability header citing CICD and/or DG doc IDs
- Stage/job definitions matching the CICD artifact structure
- Environment-specific configuration from DG

### Step 5 — Report

Show what was created, source doc references, and recommended next steps.

## Rules

1. Never write outside `scaffold/`.
2. Always include traceability headers.
3. Match pipeline platform to what CICD artifact specifies (GitHub Actions, GitLab CI, etc.).
4. If CICD is missing, report the gap — do not scaffold partial pipelines.
5. Always get user confirmation before writing.
6. Quality gate thresholds must match CICD artifact values exactly.
