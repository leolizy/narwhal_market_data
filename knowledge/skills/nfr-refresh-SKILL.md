---
name: nfr-refresh
description: >
  Refresh the NFR and all downstream subsidiary documents after an NFR update.
  Compares the new NFR version against the previous one, maps changed sections
  to the 9 transitive downstream doc types (HLD, CICD, DBAD, TSI, NFTS, DG, NFRAR,
  MVP, RTM), then guides section-level updates for each affected existing doc
  in hop-count order. Use this skill when the NFR has been updated and the user
  wants all downstream documents kept in sync.
---

# NFR Refresh — Propagate NFR Changes to All Downstream Documents

## Environment

- **Base directory:** `.`
- **CLI module:** `knowledge/sdlc_chain/cli.py`
- **Invoke CLI as:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`
  (run from the base directory)
- **NFR artifacts:** `knowledge/artifact/20_non_function/NFR-*.json`
- **Archive before overwrite:** `python3 knowledge/sdlc_chain/cli.py archive [PATH]`

---

## NFR Section → Downstream Impact Map

Use this map throughout the skill to determine which downstream doc types are
affected when a given NFR section changes.

| NFR Section | Directly Affected Types |
|-------------|------------------------|
| `performance_requirements` | HLD, CICD, NFTS |
| `availability_reliability` | HLD, CICD, DG, NFTS |
| `security_requirements` | HLD, CICD, NFTS |
| `scalability_requirements` | HLD, CICD, DBAD, NFTS |
| `data_requirements` | DBAD, NFTS |
| `integration_requirements` | HLD, TSI, NFTS |
| `deployment_requirements` | CICD, DG |
| `monitoring_observability` | HLD, TSI, DG |
| `compliance_regulatory` | CICD, NFTS |
| `maintainability_operability` | DG, NFTS |

Docs at hop 2+ (NFRAR, MVP, RTM) are always flagged for review whenever ANY
hop-1 or hop-2 doc is updated — they aggregate NFR outcomes and must reflect
current test results and traceability.

---

## Downstream Processing Order (always follow this order)

1. **Hop 1 — direct NFR children:** HLD, CICD, DBAD, TSI
2. **Hop 2 — indirect (via hop-1 docs):** NFTS, DG
3. **Hop 3 — aggregators:** NFRAR, MVP, RTM

Never process a hop before the previous hop is complete. This ensures that
hop-2 docs reflect already-updated hop-1 content.

---

## PHASE 1 — Startup: Load NFR Versions

### Step 1a — Scan all existing documents

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

Store the full result. Extract all NFR entries from it.

### Step 1b — Identify the current (latest) NFR

From the list-existing output, find all artifacts of type `NFR` and sort by
version descending to find the latest. Show the user:

```
Current NFR on record:
  ID:       [NFR-NNNN]
  Title:    [title]
  Version:  [X.Y]
  Status:   [status]
  Path:     knowledge/artifact/20_non_function/[filename]
```

If no NFR exists, tell the user:

```
No NFR found in knowledge/artifact/20_non_function/.

Please create an NFR first using /sdlc-doc-intake before running a refresh.
```

Stop here.

### Step 1c — Identify the new NFR version to refresh from

Ask the user:

```
What is the source of the updated NFR?

  a. A new version has already been saved to knowledge/artifact/ — use the latest on disk
  b. Upload or paste new NFR content
  c. Provide a file path to the new version

Reply with a, b, or c:
```

**If (a):** Use the artifact already found in Step 1b. Skip to Step 1e.

**If (b):** Accept pasted content. Write it to `knowledge/.tmp/nfr_new.json`. Detect type:

```bash
python3 knowledge/sdlc_chain/cli.py detect knowledge/.tmp/nfr_new.json
```

Confirm: "I detected this as an NFR document with ID [ID] v[VER]. Is that correct?"

**If (c):** Accept the path. Detect type the same way. Confirm with the user.

### Step 1d — Accept and save the new NFR (options b and c only)

If the user provides new content (b or c) and it is confirmed as an NFR:

1. Archive the existing NFR first:

```bash
python3 knowledge/sdlc_chain/cli.py archive [EXISTING_NFR_PATH]
```

Confirm the archive succeeded. Do not proceed if it fails.

2. Ask the user for the new version number (suggest incrementing minor: e.g. `0.1` → `0.2`).

3. Write the new artifact JSON:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import dump_json
from pathlib import Path

with open('knowledge/.tmp/nfr_new.json', encoding='utf-8') as f:
    doc = json.load(f)

# Update version in metadata
doc.setdefault('metadata', {})['version'] = '[NEW_VERSION]'
doc['metadata']['last_updated'] = '[TODAY_YYYY-MM-DD]'

out_path = '[ARTIFACT_PATH]'
dump_json(doc, out_path)
print(json.dumps({'path': out_path, 'status': 'ok'}))
"
```

4. Validate:

```bash
python3 knowledge/sdlc_chain/cli.py validate NFR [NEW_NFR_PATH]
```

Report any validation errors to the user. Continue unless there are required-section failures.

5. Regenerate MD and HTML for the NFR itself:

```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from sdlc_chain.generators.html_renderer import render_md_file_to_html
from pathlib import Path

# Write the Markdown for the NFR doc
# (render from JSON using the same section structure)
"
```

Render Markdown using the NFR section fields from the JSON. Write to
`knowledge/req_doc/md/20_non_function/[filename].md` and the HTML to `knowledge/req_doc/html/20_non_function/[filename].html`.

### Step 1e — Load both NFR versions for diffing

Load the **previous** NFR version (from archive/ if one exists, otherwise treat
all sections as new) and the **current** NFR version:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import load_json

def extract_sections(path):
    try:
        d = load_json(path)
    except Exception:
        import yaml
        with open(path, encoding='utf-8') as f:
            d = yaml.safe_load(f)
    spec = d.get('spec', d)
    # Return a dict of section_name → serialized content (for diffing)
    sections = {}
    for k, v in spec.items():
        if k not in ('document', 'metadata'):
            sections[k] = json.dumps(v, sort_keys=True)
    return sections

current_sections = extract_sections('[CURRENT_NFR_PATH]')

# Try to find previous version in archive/
import os
from pathlib import Path
archive_dir = Path('archive/20_non_function')
prev_sections = {}
prev_version = None
if archive_dir.exists():
    candidates = sorted(archive_dir.glob('NFR-*.json'), reverse=True)
    if candidates:
        prev_sections = extract_sections(str(candidates[0]))
        prev_d = load_json(str(candidates[0]))
        prev_version = prev_d.get('metadata', {}).get('version', '?')

# Compute changed sections
changed = []
added = []
removed = []
unchanged = []

all_keys = set(current_sections) | set(prev_sections)
for k in sorted(all_keys):
    if k not in prev_sections:
        added.append(k)
    elif k not in current_sections:
        removed.append(k)
    elif current_sections[k] != prev_sections[k]:
        changed.append(k)
    else:
        unchanged.append(k)

result = {
    'current_version': '[CURRENT_VERSION]',
    'prev_version': prev_version,
    'changed_sections': changed,
    'added_sections': added,
    'removed_sections': removed,
    'unchanged_sections': unchanged
}
print(json.dumps(result))
"
```

Store the diff result for use in Phase 2.

---

## PHASE 2 — Scan Downstream Documents

### Step 2a — Find all existing downstream docs

From the `list-existing` output (Phase 1), extract documents of these types:
`CICD`, `DBAD`, `TSI`, `NFTS`, `DG`, `NFRAR`, `MVP`, `RTM`.

For each found document, load its metadata to check the NFR version it
references:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import load_json

downstream_paths = [LIST_OF_PATHS]
result = []
for p in downstream_paths:
    try:
        d = load_json(p)
        meta = d.get('metadata', {})
        related = meta.get('related_documents', [])
        # related_documents may be a list of strings or dicts
        nfr_refs = [r for r in related if 'NFR' in str(r)]
        result.append({
            'path': p,
            'doc_type': meta.get('doc_type', '?'),
            'doc_id': meta.get('document_id', '?'),
            'title': meta.get('title', ''),
            'version': meta.get('version', '?'),
            'status': meta.get('status', '?'),
            'nfr_refs': nfr_refs
        })
    except Exception as e:
        result.append({'path': p, 'error': str(e)})

print(json.dumps(result))
"
```

### Step 2b — Determine staleness

A downstream doc is **stale** if:
- Its `related_documents` does NOT include the current NFR ID + version, OR
- The NFR sections it depends on (per the Impact Map) have changed.

A downstream doc is **not affected** if:
- No sections in its impact-map subset changed between NFR versions.

Build a staleness list: `{doc_type, doc_id, path, version, stale: bool, reason: str}`.

---

## PHASE 3 — Impact Analysis Report

Present the full impact analysis to the user before touching anything:

```
## NFR Refresh Impact Report
## NFR [NFR-ID] — v[PREV_VER] → v[CURRENT_VER]

NFR sections changed: [N]
  CHANGED:   [section_name], [section_name], ...
  ADDED:     [section_name], ...  (or "none")
  REMOVED:   [section_name], ...  (or "none")
  UNCHANGED: [N] sections (no action needed)

─────────────────────────────────────────────────────────────────────
HOP 1 — Direct NFR children
─────────────────────────────────────────────────────────────────────

  CICD  [CICD-NNNN] v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Affected by: performance_requirements, security_requirements, ...

  DBAD  [DBAD-NNNN] v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Affected by: scalability_requirements, data_requirements

  TSI   [TSI-NNNN]  v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Affected by: integration_requirements, monitoring_observability

─────────────────────────────────────────────────────────────────────
HOP 2 — Indirect (via hop-1 docs)
─────────────────────────────────────────────────────────────────────

  NFTS  [NFTS-NNNN] v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Always needs review when any hop-1 doc changes.

  DG    [DG-NNNN]   v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Affected by: availability_reliability, deployment_requirements, ...

─────────────────────────────────────────────────────────────────────
HOP 3 — Aggregators
─────────────────────────────────────────────────────────────────────

  NFRAR [NFRAR-NNNN] v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Flag for review — aggregates NFR test results.

  MVP   [MVP-NNNN]   v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Flag for review — may reference NFR-derived acceptance criteria.

  RTM   [RTM-NNNN]   v[X.Y]  [STALE / UP TO DATE / NOT FOUND]
        Flag for review — traceability matrix includes NFR rows.

─────────────────────────────────────────────────────────────────────
NOT FOUND: [list of types with no existing artifact]
─────────────────────────────────────────────────────────────────────

Proposed refresh plan:
  ✏️  Update [N] stale docs (content update + archive + re-render)
  🔍 Flag  [N] docs for review  (note added, no content change)
  ✅ Skip  [N] docs already up to date
  ➕ Create [N] docs not yet started (optional — skip unless user requests)

Proceed with refresh? (yes / yes for stale only / select specific types / no)
```

Wait for explicit user confirmation before proceeding.

Accept responses like:
- `yes` — proceed with all stale + flag-for-review
- `yes for stale only` — update stale docs, skip flag-only docs
- `CICD, NFTS` — update only named doc types
- `no` — abort

Store the confirmed list of doc types to process.

---

## PHASE 4 — Refresh Loop (Hop-by-Hop)

Process docs in hop order: hop-1 first, then hop-2, then hop-3.
Within each hop, process alphabetically: CICD → DBAD → TSI, then DG → NFTS, then NFRAR → MVP → RTM.

For each doc type in the confirmed list:

### 4A — If the doc EXISTS and is STALE (content update)

**Step 4A-1: Load the existing doc**

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import load_json
doc = load_json('[DOC_PATH]')
print(json.dumps(doc))
"
```

**Step 4A-2: Show the user which sections need updating**

Based on the NFR Impact Map, list the specific sections in this doc type
that are derived from the changed NFR sections. Show the current content
of each affected section (first 200 chars) and what changed in the NFR.

Example for CICD after `security_requirements` changed:
```
Updating CICD-NNNN — sections driven by changed NFR areas:

  Section: quality_gates.security_checks
  Current: "[first 200 chars of current content]..."
  NFR changed: security_requirements now includes [summary of change]

  Section: pipeline_stages (security stage)
  Current: "[first 200 chars]..."
  NFR changed: [summary]

Please provide the updated content for each section, or reply "keep"
to leave a section unchanged.
```

**Step 4A-3: Collect updated section content from the user**

For each affected section, accept the user's input. If the user replies
"keep" or leaves blank, preserve the existing content.

**Step 4A-4: Update the doc in memory**

Apply the user-provided section updates to the loaded JSON. Also update:
- `metadata.version` — increment minor version (e.g. `0.3` → `0.4`)
- `metadata.last_updated` — today's date
- `metadata.related_documents` — replace or add the current NFR reference in the flat list:
  `"NFR-[ID] v[CURRENT_VER]"`
- `metadata.tags` — preserve existing tags
- `metadata.supersedes` — preserve existing value
- `change_log` — append entry:
  ```json
  {
    "version": "[new version]",
    "date": "[TODAY]",
    "author": "nfr-refresh skill",
    "changes": "Refreshed from NFR-[ID] v[CURRENT_VER]: updated [section_names]."
  }
  ```

**Step 4A-5: Archive → Write → Validate → Render**

1. Archive the existing file:

```bash
python3 knowledge/sdlc_chain/cli.py archive [DOC_PATH]
```

Confirm success before writing. If archive fails, stop and report.

2. Write the updated doc to `knowledge/.tmp/nfr_refresh_[TYPE].json` using the Write tool.

3. Write JSON artifact:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import dump_json

with open('knowledge/.tmp/nfr_refresh_[TYPE].json', encoding='utf-8') as f:
    doc = json.load(f)

dump_json(doc, '[DOC_PATH]')
print(json.dumps({'path': '[DOC_PATH]', 'status': 'ok'}))
"
```

4. Validate:

```bash
python3 knowledge/sdlc_chain/cli.py validate [DOC_TYPE] [DOC_PATH]
```

Report errors. Continue on warnings; stop on missing-required-section errors
and ask the user to resolve before proceeding.

5. Render Markdown + HTML for the doc. Use the same section structure as the
template defines. Write `.md` to `knowledge/req_doc/md/[template_dir]/[filename].md` and
`.html` to `knowledge/req_doc/html/[template_dir]/[filename].html`:

```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from sdlc_chain.generators.html_renderer import render_md_file_to_html
from pathlib import Path

html = render_md_file_to_html('[FULL_MD_PATH]', '[DOCUMENT_TITLE]')
Path('[FULL_HTML_PATH]').write_text(html, encoding='utf-8')
print('html written')
"
```

**Step 4A-6: Confirm completion**

After writing all three files, report:
```
✅ [DOC_TYPE]-[ID] updated: v[OLD] → v[NEW]
   JSON:  knowledge/artifact/[dir]/[filename].json
   MD:    knowledge/req_doc/md/[dir]/[filename].md
   HTML:  knowledge/req_doc/html/[dir]/[filename].html
   Archived: archive/[dir]/[old filename]
```

---

### 4B — If the doc EXISTS but is FLAG-ONLY (review note, no content change)

Load the doc, append a note to its `change_log` only:

```json
{
  "version": "[same version — no increment]",
  "date": "[TODAY]",
  "author": "nfr-refresh skill",
  "changes": "REVIEW REQUIRED — NFR-[ID] updated to v[CURRENT_VER]. Verify alignment with changed sections: [section_names]."
}
```

Update `metadata.last_updated` to today. Archive + write + re-render the doc.

---

### 4C — If the doc does NOT EXIST

Do not create it automatically. Report:

```
⚠️  [DOC_TYPE] — no artifact found. Skipping.
    To create it, run /sdlc-doc-intake and select [DOC_TYPE].
```

---

## PHASE 5 — Summary Report

After processing all docs, present the full summary:

```
## NFR Refresh Complete

  NFR:     [NFR-ID] v[PREV_VER] → v[CURRENT_VER]
  Date:    [TODAY]
  Trigger: [N] NFR sections changed

NFR sections changed:
  [list of section names]

Downstream refresh results:

  HOP 1
  ──────────────────────────────────────────────────────────────
  ✅ CICD  [CICD-NNNN]  v[OLD] → v[NEW]  updated
  ✅ DBAD  [DBAD-NNNN]  v[OLD] → v[NEW]  updated
  ⏭️  TSI   — not found, skipped

  HOP 2
  ──────────────────────────────────────────────────────────────
  ✅ NFTS  [NFTS-NNNN]  v[OLD] → v[NEW]  updated
  🔍 DG    [DG-NNNN]    v[X.Y]  flagged for review

  HOP 3
  ──────────────────────────────────────────────────────────────
  🔍 NFRAR [NFRAR-NNNN] v[X.Y]  flagged for review
  🔍 MVP   [MVP-NNNN]   v[X.Y]  flagged for review
  ⏭️  RTM   — not found, skipped

Summary:
  ✅ [N] documents updated (content refresh)
  🔍 [N] documents flagged for review
  ⏭️  [N] documents not found (use /sdlc-doc-intake to create)

Files written:
  [list of all updated knowledge/artifact/doc/html paths]

Archived versions:
  [list of all archive/ paths]

Next steps:
  → Review the 🔍 flagged documents for alignment with NFR v[CURRENT_VER]
  → Create missing doc types with /sdlc-doc-intake if required
  → Run /sdlc-doc-intake on any doc needing deeper structural changes
```

---

## Important Rules

1. **Always process in hop-count order** — hop 1 before hop 2 before hop 3. Never skip ahead.
2. **Never overwrite without archiving first** — confirm archive success before every write.
3. **Never modify any doc without explicit user confirmation** — present the impact report in Phase 3 and wait for approval.
4. **Never auto-create missing downstream docs** — only flag them; creation is done via `/sdlc-doc-intake`.
5. **Never touch MVP tasks with status "Done"** — if MVP is in the refresh list, only add a change_log note; do not alter task statuses.
6. **Always write temp JSON via the Write tool** — never embed doc content in shell strings.
7. **If archive fails, stop** — report the error and do not overwrite without a successful archive.
8. **Preserve all non-NFR-derived fields** — only update sections that are driven by changed NFR sections; leave all other content unchanged.
9. **Always regenerate both MD and HTML** after a JSON update — never leave them out of sync.
10. **If a section update from the user is blank or "keep", preserve existing content** — never silently zero out a section.
