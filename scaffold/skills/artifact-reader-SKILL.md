---
name: read-artifacts
description: "Scan and summarise all knowledge artifacts — the scaffold agent's view into the documentation branch."
---

# Knowledge Artifact Reader

## Purpose

Parse all knowledge branch artifacts and present a structured summary.
This is the scaffold agent's primary tool for understanding what documentation
exists and what can be scaffolded.

## Environment

- **Base directory:** `.`
- **Scaffold CLI:** `python3 scaffold/build_chain/cli.py <command> [args]`
- **Knowledge CLI (read-only):** `python3 knowledge/sdlc_chain/cli.py list-existing`

## Workflow

### Step 1 — Run artifact summary

```bash
python3 scaffold/build_chain/cli.py artifact-summary
```

Parse the JSON output. It contains:
- `total_artifacts` — count of all knowledge artifacts
- `scaffoldable` — count of artifacts with scaffold mappings
- `by_layer` — artifact counts grouped by SDLC layer
- `artifacts` — detailed list with kind, document_id, version, status, section_keys

### Step 2 — Present the overview

```
## Knowledge Artifacts — Summary

Total artifacts: [N]
Scaffoldable (Layer 3+): [N]

| Layer | Count | Doc Types |
|-------|-------|-----------|
| root | [N] | PC |
| requirements | [N] | FRD, NFR |
| specification | [N] | PSD |
| architecture | [N] | HLD, TSI, CICD, DBAD |
| contracts | [N] | API, AEC, DC, DBC, MDC |
| deploy_test | [N] | DG, UT, NFTS, NFRAR |
| aggregators | [N] | MVP, RTM, DD |
```

### Step 3 — Show scaffoldable artifacts detail

For each scaffoldable artifact, show:

```
| Doc ID | Type | Version | Status | Scaffold Action | Output Dir |
|--------|------|---------|--------|-----------------|------------|
| HLD-0001 | HLD | v0.1 | Draft | project_layout | scaffold/src/ |
| CICD-0001 | CICD | v0.2 | Approved | ci_pipeline | scaffold/ci/ |
```

### Step 4 — Identify gaps

List any scaffold-relevant doc types that are missing:

```
Missing knowledge artifacts (cannot scaffold yet):
  → HLD not found — needed for /scaffold-project
  → API not found — needed for /scaffold-api
  → UT not found — needed for /scaffold-tests

Recommendation: Switch to knowledge branch and create these docs first.
  → /switch-knowledge then /sdlc-doc-intake
```

### Step 5 — Offer next steps

```
What would you like to do?
  → /scaffold-project to generate project structure from HLD/TSI
  → /scaffold-cicd to generate CI/CD configs
  → /build-status for a scaffold progress dashboard
```

## Rules

1. This skill is **read-only** — never create or modify files.
2. Run `artifact-summary` exactly once.
3. Always show the layer overview table.
4. Always identify scaffoldable artifacts and gaps.
5. Never read artifacts from outside `knowledge/`.
