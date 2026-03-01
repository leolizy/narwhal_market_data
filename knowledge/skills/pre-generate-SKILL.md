---
name: pre-generate
description: "Run a preflight checklist before generating an SDLC document. Verifies all parent docs exist, checks for stale upstream versions, and confirms required inputs are available. Use before /sdlc-doc-intake to catch problems early."
---

# Pre-Generate Checklist

## Purpose

Before creating or updating a document, verify that all prerequisites
are met.  Catches missing parents, stale upstream content, and missing
inputs *before* you invest time in generation.

## Environment

- **Base directory:** `.`
- **CLI:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`

## Workflow

### Step 1 — Identify target document type

If the user provides a doc type (e.g., `/pre-generate PSD`), use it.
Otherwise, ask:

```
Which document type are you about to create or update?
  PC, FRD, NFR, PSD, AEC, API, DC, DBC, MDC, HLD, TSI, CICD, DBAD,
  NFTS, DG, UT, NFRAR, MVP, RTM, DD
```

### Step 2 — Check parent prerequisites

Use the prerequisite map below to identify required parent docs:

```
PC: no prerequisites
FRD: requires PC
NFR: requires PC
PSD: requires FRD
AEC, API, DC, DBC, MDC: require PSD
HLD, CICD, DBAD, TSI: require NFR
NFTS: requires CICD + DBAD + TSI
DG: requires CICD
UT: requires at least one of (AEC, API, DC, DBC, MDC)
NFRAR: requires NFTS
MVP, RTM: require at least one of (NFTS, DG, UT)
DD: no prerequisites (aggregator)
```

Run:

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

For each required parent, check if an artifact exists.

### Step 3 — Check template availability

```bash
python3 knowledge/sdlc_chain/cli.py template [DOC_TYPE]
```

Verify the template loads without errors.  List required sections.

### Step 4 — Check for existing version

If an artifact already exists for this doc type, flag it:
- Note the current version
- Remind to run `archive` before overwriting
- Show when it was last updated (from metadata if readable)

### Step 5 — Present checklist

```
## Pre-Generate Checklist: [DOC_TYPE]

### Prerequisites
| Check | Status | Details |
|-------|--------|---------|
| Parent: PC exists | ✅ Pass | PC-NPH-0001 v0.3 |
| Parent: FRD exists | ✅ Pass | FRD-NPH-0001 v0.2 |
| Template available | ✅ Pass | 12 sections defined |
| No existing artifact | ✅ Pass | First creation |

### Required Sections (from template)
1. metadata (required)
2. executive_summary (required)
3. functional_requirements (required)
4. ...

### Parent Content to Surface
When creating this doc, surface these parent sections:
| Parent Doc | Sections to Reference |
|-----------|----------------------|
| FRD-NPH-0001 | functional_requirements, event_triggers, data_requirements |
| PC-NPH-0001 | module_registry, integration_points |

### Ready to Generate?
✅ All checks passed — safe to proceed with /sdlc-doc-intake [DOC_TYPE]
```

Or if checks fail:

```
### Ready to Generate?
❌ Blocked — 2 prerequisite(s) missing:
  → Create CICD first (required parent for NFTS)
  → Create DBAD first (required parent for NFTS)

Use /sdlc-doc-intake CICD to create the missing parent.
```

### Step 6 — Offer next steps

```
What would you like to do?
  → /sdlc-doc-intake [DOC_TYPE] — proceed with generation
  → /doc-impact [DOC_TYPE] — see downstream impact first
  → /pre-generate [PARENT_TYPE] — check a missing parent
```

## Rules

1. **Read-only** — never create or modify files.
2. Always check ALL prerequisites, not just the first missing one.
3. Show parent content sections that should drive the new doc's content.
4. If an existing artifact will be overwritten, always flag the archive step.
5. List template sections so the user knows what to prepare.
