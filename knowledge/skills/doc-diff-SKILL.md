---
name: doc-diff
description: "Compare two versions of an SDLC document side-by-side. Shows added, removed, and changed sections between an artifact and its archived predecessor. Use before updating a doc to see what changed."
---

# Doc Diff — Version Comparison

## Purpose

Compare the current artifact version of a document against a previous
(archived) version, highlighting what sections changed, what was added,
and what was removed.  Useful for change review and impact assessment.

## Environment

- **Base directory:** `.`
- **CLI:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`

## Workflow

### Step 1 — Identify the document

If the user provides a path or doc type (e.g., `/doc-diff NFR`), use it.
Otherwise, ask:

```
Which document do you want to compare?
  Provide a doc type (e.g., NFR) or a file path.
```

### Step 2 — Find versions to compare

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

Locate:
- **Current version:** artifact JSON for the given doc type
- **Previous version:** matching file in `archive/` directory

If no archive exists, report:

```
No archived version found for [DOC_TYPE].
Only the current version exists — nothing to compare.
```

If multiple archive versions exist, compare the current artifact against
the most recent archive (highest version number).

### Step 3 — Load and diff

Load both JSON files. For each top-level section in the K8s envelope
(`metadata`, then each key under `sections`):

1. **Section exists in both** → deep-compare values
2. **Section only in current** → mark as ADDED
3. **Section only in archive** → mark as REMOVED

For changed sections, identify:
- **Field-level changes** — which specific fields changed
- **List-level changes** — items added/removed from arrays
- **Value changes** — old value → new value

### Step 4 — Present diff

```
## Document Diff: [DOC_TYPE]

Current:  [filename] (v[X.Y])
Previous: [filename] (v[A.B])

### Metadata Changes
| Field | Previous | Current | Change |
|-------|----------|---------|--------|
| version | v0.1 | v0.2 | Updated |
| status | Draft | In Review | Updated |
| last_updated | 2025-01-01 | 2025-02-15 | Updated |

### Section Changes

#### ✅ Unchanged sections (N)
executive_summary, scope_boundaries, ...

#### ✏️ Modified sections (N)
| Section | Changes |
|---------|---------|
| performance_requirements | 2 fields changed, 1 item added |
| security_requirements | 1 field changed |

##### performance_requirements — Details
| Field / Item | Previous | Current |
|-------------|----------|---------|
| response_time_p99 | 500ms | 200ms |
| + throughput_target | — | 10,000 rps |

#### ➕ Added sections (N)
| Section | Fields |
|---------|--------|
| monitoring_observability | 5 fields |

#### ➖ Removed sections (N)
| Section | Note |
|---------|------|
| legacy_integration | Was 3 fields |
```

### Step 5 — Impact assessment

After showing the diff, cross-reference changes with the downstream
impact map:

```
### Change Impact

Changed sections that affect downstream docs:
| Changed Section | Downstream Impact |
|----------------|-------------------|
| performance_requirements | HLD, CICD, NFTS |
| security_requirements | HLD, CICD, NFTS |

Recommendation:
  → Review HLD, CICD, NFTS for alignment with these changes
  → Use /doc-impact [DOC_TYPE] for full blast radius
```

## Rules

1. **Read-only** — never create or modify files.
2. Always show the version numbers being compared.
3. Group changes by severity: modified sections first, then added, then removed.
4. For modified sections, always show field-level detail.
5. Always finish with the impact assessment linking changes to downstream docs.
6. If comparing NFR or FRD, use the section-level impact maps from `/doc-impact`.
