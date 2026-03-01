---
name: build-status
description: "Dashboard showing what has been scaffolded vs what knowledge artifacts are available but not yet scaffolded."
---

# Build Status Dashboard

## Purpose

Show a read-only dashboard of the scaffold branch scaffolding progress:
what has been generated, what is pending, and what is stale.

## Environment

- **Base directory:** `.`
- **Scaffold CLI:** `python3 scaffold/build_chain/cli.py scaffold-status`

## Workflow

### Step 1 — Run scaffold status

```bash
python3 scaffold/build_chain/cli.py scaffold-status
```

Parse the JSON output containing `scaffolded`, `pending`, and `stale` arrays.

### Step 2 — Build the dashboard

```
## Scaffold Branch — Scaffold Status

Progress: [N] / [M] scaffoldable artifacts   [progress bar] [pct]%

### Scaffolded
| Doc Type | Doc ID | Version | Files Generated |
|----------|--------|---------|-----------------|
| HLD | HLD-0001 | v0.1 | scaffold/src/README.md, scaffold/src/module_a/... |

### Pending (knowledge artifact exists, not yet scaffolded)
| Doc Type | Doc ID | Scaffold Action | Output Dir |
|----------|--------|-----------------|------------|
| API | API-0001 | api_routes | scaffold/src/api/ |

### Stale (knowledge updated since last scaffold)
| File | Source Doc | Scaffold Version | Current Version |
|------|-----------|--------------|-----------------|
| scaffold/src/... | HLD-0001 | v0.1 | v0.3 |
```

### Step 3 — Recommended actions

Based on status:
- **Pending items** → suggest which `/scaffold-*` skill to run next
- **Stale items** → recommend re-running the relevant scaffold skill
- **All done** → confirm scaffold is complete and current

### Step 4 — Offer next steps

```
What would you like to do?
  → /scaffold-project to scaffold from HLD/TSI
  → /scaffold-cicd to scaffold CI/CD pipelines
  → /sync-check for detailed staleness analysis
```

## Rules

1. This skill is **read-only** — never create or modify files.
2. Run `scaffold-status` exactly once.
3. Always show all three sections (scaffolded, pending, stale).
4. Always show recommended next actions.
