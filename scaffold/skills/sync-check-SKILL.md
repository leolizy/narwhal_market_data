---
name: sync-check
description: "Detect when knowledge artifacts have been updated since the last scaffold, flagging stale scaffold output."
---

# Sync Check

## Purpose

Compare scaffold output files against current knowledge artifact versions.
Flag any generated files that reference outdated document versions,
indicating they need regeneration.

## Environment

- **Base directory:** `.`
- **Scaffold CLI:** `python3 scaffold/build_chain/cli.py sync-check`

## Workflow

### Step 1 — Run sync check

```bash
python3 scaffold/build_chain/cli.py sync-check
```

Parse the JSON output containing:
- `stale_files` — files with version mismatches
- `total_scaffolded` — count of scaffolded artifacts
- `total_pending` — count of pending artifacts
- `total_stale` — count of stale files
- `message` — human-readable summary

### Step 2 — Present results

If no stale files:

```
## Sync Check — All Clear

All [N] scaffolded files are up to date with their knowledge sources.
No regeneration needed.
```

If stale files found:

```
## Sync Check — [N] Stale File(s) Found

| File | Source Doc | Scaffolded From | Current Version | Action |
|------|-----------|-----------------|-----------------|--------|
| scaffold/src/api/routes.py | API-0001 | v0.1 | v0.3 | Re-run /scaffold-api |
| scaffold/ci/ci.yml | CICD-0001 | v0.2 | v0.4 | Re-run /scaffold-cicd |
```

### Step 3 — Recommend actions

Group stale files by scaffold skill and recommend:

```
Recommended actions:
  → /scaffold-api — 3 files need regeneration (API-0001 updated to v0.3)
  → /scaffold-cicd — 1 file needs regeneration (CICD-0001 updated to v0.4)
```

## Rules

1. This skill is **read-only** — never create or modify files.
2. Run `sync-check` exactly once.
3. Always show the staleness summary, even if empty.
4. Group recommendations by scaffold skill.
5. Show exact version numbers (old vs current).
