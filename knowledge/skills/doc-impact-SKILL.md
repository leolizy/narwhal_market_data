---
name: doc-impact
description: "Show the downstream impact of changing a specific document type. Uses BFS traversal to display all affected documents, their hop distances, and whether they currently exist. Use before updating a doc to understand the blast radius."
---

# Doc Impact Analysis

## Purpose

Before updating a document, show the full downstream impact — every doc
that would need review or update as a result.  Combines `downstream` BFS
traversal with `list-existing` to show which affected docs actually exist
(and therefore need updating) vs which are missing (and can be deferred).

## Environment

- **Base directory:** `.`
- **CLI:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`

## Workflow

### Step 1 — Identify the document type

If the user provides a doc type (e.g., `/doc-impact NFR`), use it directly.
Otherwise, ask:

```
Which document type are you planning to change?
  PC, FRD, NFR, PSD, AEC, API, DC, DBC, MDC, HLD, TSI, CICD, DBAD,
  NFTS, DG, UT, NFRAR, MVP, RTM, DD
```

### Step 2 — Run downstream traversal

```bash
python3 knowledge/sdlc_chain/cli.py downstream [DOC_TYPE]
```

Parse the JSON output. Each downstream entry has:
- `doc_type` — affected type
- `layer` — layer number (0-5)
- `hop_count` — distance from source
- `immediate_parent` — which doc feeds into this one

### Step 3 — Cross-reference with existing docs

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

For each downstream doc type, check if an artifact exists.

### Step 4 — Present impact analysis

```
## Impact Analysis: Changing [DOC_TYPE]

Source: [DOC_TYPE] (Layer [N])
Total downstream docs affected: [count]

### Hop 1 — Direct children
| Type | Layer | Exists? | Document ID | Action needed |
|------|-------|---------|-------------|---------------|
| PSD  | 2     | ✅ Yes  | PSD-0001    | Review & update |
| ...  | ...   | ...     | ...         | ...           |

### Hop 2 — Indirect dependents
| Type | Layer | Via | Exists? | Document ID | Action needed |
|------|-------|----|---------|-------------|---------------|
| AEC  | 3     | PSD | ⬜ No  | —           | Create when ready |
| ...  | ...   | ... | ...     | ...         | ...           |

### Hop 3+ — Aggregators
| Type | Layer | Via | Exists? | Document ID | Action needed |
|------|-------|----|---------|-------------|---------------|
| MVP  | 5     | NFTS | ⬜ No | —           | Deferred |
```

### Step 5 — Section-level impact (for NFR and FRD)

If the source is **NFR**, show the NFR Section → Downstream Impact Map:

```
### NFR Section Impact

Which NFR sections changed? This determines which downstream docs
need the most attention:

| NFR Section               | Affected docs        |
|---------------------------|----------------------|
| performance_requirements  | HLD, CICD, NFTS      |
| availability_reliability  | HLD, CICD, DG, NFTS  |
| security_requirements     | HLD, CICD, NFTS      |
| scalability_requirements  | HLD, CICD, DBAD, NFTS|
| data_requirements         | DBAD, NFTS           |
| integration_requirements  | HLD, TSI, NFTS       |
| deployment_requirements   | CICD, DG             |
| monitoring_observability  | HLD, TSI, DG         |
| compliance_regulatory     | CICD, NFTS           |
| maintainability_operability| DG, NFTS            |
```

If the source is **FRD**, show the FRD Section → Downstream Impact Map:

```
### FRD Section Impact

Which FRD sections changed?

| FRD Section                       | Affected docs      |
|-----------------------------------|--------------------|
| functional_requirements           | PSD, UT, RTM       |
| event_triggers                    | AEC, PSD           |
| module_interface.apis_provided    | API, DBC           |
| module_interface.events_published | AEC                |
| data_requirements.entities        | DC, PSD, DD        |
| business_rules                    | PSD, DBC           |
| acceptance_criteria               | PSD, UT            |
| nonfunctional_requirements        | NFR (cross-branch) |
```

### Step 6 — Recommend action

```
Recommended workflow:
  1. Update [DOC_TYPE] first
  2. Then update existing downstream docs in layer order:
     → [list existing downstream docs by layer]
  3. Use /nfr-refresh or /sdlc-doc-intake to propagate changes
```

## Rules

1. **Read-only** — never create or modify files.
2. Always show hop distance — it tells the user how far the ripple extends.
3. For NFR and FRD changes, always show the section-level impact map.
4. Recommend processing in layer order (not random).
5. Flag existing docs that need updating vs missing docs that can be deferred.
