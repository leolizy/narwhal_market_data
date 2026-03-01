---
name: mvp-update
description: >
  Update the open MVP task list whenever a new version of a linked document is
  submitted. Diffs old vs new functional requirements (FR-NNN level), updates
  outstanding task statuses, adds tasks for new FRs, and flags orphaned tasks
  for FRs that were removed or significantly changed. Use this skill when the
  user submits a new version of an FRD or other upstream document and wants the
  MVP kept in sync.
---

# MVP Update — Sync MVP Task List with New Document Version

## Environment

- **Base directory:** `.`
- **CLI module:** `knowledge/sdlc_chain/cli.py`
- **Invoke CLI as:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`
  (run from the base directory)
- **MVP artifacts:** `knowledge/artifact/90_project/MVP-[NNNN]_*.json`
- **Archive before overwrite:** `python3 knowledge/sdlc_chain/cli.py archive [PATH]`

---

## When to Use This Skill

Trigger this skill when:
- The user says they "submitted", "updated", or "published" a new version of a document
- The user says a new FRD version is available and wants the MVP synced
- The user uploads a new document version and asks to update the MVP
- `/sdlc-doc-intake` has just completed an update to an FRD linked to the open MVP

---

## PHASE 1 — Startup: Find Open MVP

Run the list-existing command:

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

Store the full result. Then find the open MVP by loading each MVP document
and checking its `metadata.status`:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import load_json

OPEN_STATUSES = {'Draft', 'In Review', 'Approved', 'Active'}
mvp_paths = [PATHS_FROM_LIST_EXISTING]

open_mvps = []
for p in mvp_paths:
    try:
        d = load_json(p)
        status = d.get('metadata', {}).get('status', '')
        if status in OPEN_STATUSES:
            open_mvps.append({
                'path': p,
                'id': d.get('metadata', {}).get('document_id', '?'),
                'status': status,
                'title': d.get('metadata', {}).get('title', ''),
                'scoped_frd': d.get('metadata', {}).get('scoped_frd', ''),
                'version': d.get('metadata', {}).get('version', '')
            })
    except Exception:
        pass

print(json.dumps(open_mvps))
"
```

### If no open MVP found

Tell the user:

```
No open MVP found. There is no active MVP task list to update.

Use /mvp-create to start a new MVP plan.
```

Stop here.

### If one open MVP found

Store its path, ID, version, and `scoped_frd` for use throughout.

Display:

```
Found open MVP:
  ID:         [MVP-NNNN]
  Title:      [title]
  Version:    [version]
  Status:     [status]
  Scoped FRD: [FRD-ID]
  Path:       knowledge/artifact/90_project/[filename]
```

---

## PHASE 2 — Identify the New Document Version

Ask the user:

```
Which document has a new version to sync into the MVP?

  a. Upload or paste the new document content
  b. Provide a file path to the new version
  c. Select from the project's existing documents

Reply with a, b, or c:
```

### If (c) — Select from existing

Use the `list-existing` output. Show only documents whose type matches the
MVP's `scoped_frd` or other documents linked in `metadata.related_documents`.
Present as a numbered list.

### If (a) or (b) — User provides content/path

Accept the path or pasted content. Detect document type:

```bash
python3 knowledge/sdlc_chain/cli.py detect [FILE_PATH]
```

Confirm: "I detected this as a [TYPE] document with ID [ID] v[VER]. Is that correct?"

### Document type validation

This skill only updates MVP tasks from **FRD-level** documents. If the detected
document is not an FRD, warn the user:

```
⚠️  This is a [TYPE] document, not an FRD. MVP tasks are anchored at FRD level
(FR-NNN functional requirements).

The MVP can still note this document was updated, but no task-level sync is
possible for [TYPE] documents.

Options:
  1. Log a change_log note that [TYPE] [ID] was updated (no task changes)
  2. Cancel

Which would you like?
```

If the user selects option 1, skip to Phase 5 (record a changelog entry only).
If the document IS an FRD, continue to Phase 3.

---

## PHASE 3 — Load and Diff FRD Versions

### Step 3a — Load the new FRD

```bash
python3 -c "
import sys, json, yaml
sys.path.insert(0, '.')

path = '[NEW_FRD_PATH]'
try:
    from sdlc_chain.yaml_utils import load_json
    d = load_json(path)
except Exception:
    with open(path, encoding='utf-8') as f:
        d = yaml.safe_load(f)

doc = d.get('spec', d)
fr_block = doc.get('functional_requirements', {})
areas = fr_block.get('functional_areas', []) if isinstance(fr_block, dict) else []

new_reqs = {}
for area in areas:
    for req in area.get('requirements', []):
        fr_id = req.get('id', '')
        new_reqs[fr_id] = {
            'id': fr_id,
            'statement': req.get('statement', ''),
            'priority': req.get('priority', ''),
            'area_id': area.get('area_id', ''),
            'area_name': area.get('area_name', ''),
            'acceptance_criteria': [ac.get('statement', '') for ac in req.get('acceptance_criteria', [])]
        }

doc_meta = d.get('document', doc.get('document', {}))
result = {
    'frd_id': doc_meta.get('document_id', '?'),
    'version': doc_meta.get('version', '?'),
    'requirements': new_reqs
}
print(json.dumps(result))
"
```

### Step 3b — Extract current MVP tasks (indexed by linked_fr)

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import load_json

mvp = load_json('[MVP_PATH]')
tasks_by_fr = {}
for ws in mvp.get('tasks', {}).get('workstreams', []):
    for task in ws.get('tasks', []):
        fr_id = task.get('linked_fr', '')
        if fr_id:
            tasks_by_fr[fr_id] = {
                'task_id': task.get('id', ''),
                'title': task.get('title', ''),
                'status': task.get('status', ''),
                'linked_frd': task.get('linked_frd', ''),
                'workstream': ws.get('workstream_name', '')
            }

print(json.dumps({'tasks_by_fr': tasks_by_fr, 'total_tasks': len(tasks_by_fr)}))
"
```

### Step 3c — Determine scope

Check whether the new FRD ID matches `metadata.scoped_frd` of the open MVP.

- **If it matches:** full diff — compare all FRs
- **If it does NOT match:** partial diff — only compare FRs that appear in the MVP as `linked_fr` values for tasks with `linked_frd == [this FRD ID]`

### Step 3d — Run the diff

Compare `new_reqs` (from new FRD) against `tasks_by_fr` (from MVP) to produce:

**A. NEW requirements** — FR IDs in `new_reqs` that have NO matching task in `tasks_by_fr` for this FRD.

**B. REMOVED requirements** — FR IDs in `tasks_by_fr` (with `linked_frd` = this FRD) that do NOT appear in `new_reqs`.

**C. MODIFIED requirements** — FR IDs present in both, where the `statement` has changed by more than 20 characters (rough threshold for substantive change).

**D. UNCHANGED requirements** — FR IDs present in both with no material statement change.

Build a summary of findings before making any changes.

---

## PHASE 4 — Present Diff Report and Confirm Changes

Present the diff to the user before touching anything:

```
## MVP Sync Report — [FRD-ID] v[OLD_VER] → v[NEW_VER]

Comparing [N] MVP tasks against [M] functional requirements in the new FRD.

FINDING           COUNT  DETAILS
──────────────────────────────────────────────────────────────────
NEW (add task)    [N]    FR-NNN: [title excerpt]
                         FR-NNN: [title excerpt]

REMOVED (orphan)  [N]    T-NNN → FR-NNN: [title excerpt] — status: [current status]
                         T-NNN → FR-NNN: [title excerpt] — status: [current status]

MODIFIED (review) [N]    T-NNN → FR-NNN: [title excerpt] — status: [current status]
                         Statement changed from: "[old first 60 chars]..."
                         Statement changed to:   "[new first 60 chars]..."

UNCHANGED         [N]    (no action needed)

DONE (protected)  [N]    Tasks already marked Done — not touched regardless of changes

Proposed actions:
  ✅ Add [N] new tasks for new FRs (status: Not Started)
  ⚠️  Flag [N] orphaned tasks (FR removed from FRD) → mark Deferred with note
  🔍 Flag [N] tasks for review (FR statement changed materially)
  ✔️  Leave [N] Done tasks untouched

Apply these changes? (yes/no)
  Or enter specific numbers to skip (e.g. "yes, but skip orphaned")
```

Wait for explicit confirmation before making any changes.

### Special rules for task status during update

| Change Type | Current Task Status | Action |
|-------------|---------------------|--------|
| FR removed | Done | **Never touch** — completed work stands |
| FR removed | Not Started | Mark `Deferred`, add note: "FR removed in [FRD-ID] v[VER]" |
| FR removed | In Progress / Blocked | Mark `Deferred`, add note with warning, flag for user decision |
| FR modified | Done | **Never touch** — completed work stands |
| FR modified | Not Started / Blocked | Add note: "FR statement changed in v[VER] — review acceptance criteria" |
| FR modified | In Progress | Add note: "FR statement changed in v[VER] — verify work still aligned" |
| FR new | — | Create new task, status: Not Started |

---

## PHASE 5 — Apply Changes to MVP Document

After user confirms, load the full MVP document and apply all changes in memory.

### For each NEW FR → add task

Find the correct workstream (by `area_name`). If the area doesn't exist as a
workstream yet, create a new workstream entry. Append a new task:

```json
{
  "id": "T-[NEXT_SEQUENTIAL_NUMBER]",
  "title": "[FR-NNN]: [first 80 chars of new FR statement]",
  "description": "[full FR statement]",
  "linked_fr": "[FR-NNN]",
  "linked_frd": "[FRD-ID]",
  "owner": "",
  "priority": "[mapped from FR priority]",
  "estimate": "",
  "status": "Not Started",
  "blocked_by": "",
  "acceptance_criteria": ["[from new FR if present]"],
  "notes": "Added in MVP update — new FR in [FRD-ID] v[NEW_VER]"
}
```

The next task ID = max existing T-NNN number + 1, zero-padded to 3 digits.

### For each REMOVED FR → flag task as Deferred

Locate the task by `linked_fr` ID. If its status is NOT "Done":
- Set `status` = `"Deferred"`
- Append to `notes`: `"[DATE] — FR [FR-NNN] removed from [FRD-ID] v[NEW_VER]. Task deferred."`

If status IS "Done": do not modify.

### For each MODIFIED FR → add review note

Locate the task by `linked_fr` ID. If its status is NOT "Done":
- Append to `notes`: `"[DATE] — FR [FR-NNN] statement changed in [FRD-ID] v[NEW_VER]. Review acceptance criteria."`
- If `acceptance_criteria` in the FR has changed, update the task's `acceptance_criteria` with the new values (only if task is Not Started or Blocked — not if In Progress).

If status IS "Done": do not modify.

### Update MVP metadata

```json
{
  "metadata": {
    "version": "[increment minor: e.g. 0.1 → 0.2]",
    "last_updated": "[today YYYY-MM-DD]",
    "related_documents": ["[FRD-ID]", "[NEW_FRD if different]"],
    "tags": "[preserve existing]",
    "supersedes": "[preserve existing]"
  }
}
```

### Add change_log entry

```json
{
  "version": "[new version]",
  "date": "[today YYYY-MM-DD]",
  "author": "mvp-update skill",
  "changes": "Synced with [FRD-ID] v[NEW_VER]: added [N] tasks, deferred [N] tasks, flagged [N] for review."
}
```

---

## PHASE 6 — Write Updated Files

### Step 6a — Archive existing MVP

```bash
python3 knowledge/sdlc_chain/cli.py archive [CURRENT_MVP_JSON_PATH]
```

Confirm the archive succeeded before writing anything new.

### Step 6b — Write temp JSON

Use the Write tool to save updated document to `/tmp/mvp_update.json`.

### Step 6c — Write JSON artifact (overwrite)

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import dump_json
from pathlib import Path

with open('/tmp/mvp_update.json', encoding='utf-8') as f:
    doc = json.load(f)

path = '[SAME MVP JSON PATH]'
dump_json(doc, path)
print(json.dumps({'path': path, 'status': 'ok'}))
"
```

### Step 6d — Write updated Markdown

Render the same Markdown structure as defined in the mvp-create skill's Phase 5.
Write to the same `.md` path (overwrite). Update the task table to reflect new statuses.

**Task status column rendering:**
- `Not Started` → `Not Started`
- `In Progress` → `🔄 In Progress`
- `Done` → `✅ Done`
- `Blocked` → `⛔ Blocked`
- `Deferred` → `~~Deferred~~`

**Add a "Changes in this update" section** at the top (below the header table):

```markdown
## Changes in This Update (v[NEW_VER])

Synced with **[FRD-ID] v[FRD_VER]** on [DATE].

| Change | FR Ref | Task | Details |
|--------|--------|------|---------|
| ➕ Added | FR-NNN | T-NNN | New functional requirement |
| ⚠️ Deferred | FR-NNN | T-NNN | FR removed from FRD |
| 🔍 Review needed | FR-NNN | T-NNN | FR statement changed |
```

### Step 6e — Regenerate HTML

```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from sdlc_chain.generators.html_renderer import render_md_file_to_html
from pathlib import Path

html = render_md_file_to_html('[FULL MD PATH]', '[DOCUMENT TITLE]')
Path('[FULL HTML PATH]').write_text(html, encoding='utf-8')
print('html written')
"
```

---

## PHASE 7 — Summary Report

After writing all files, present:

```
## MVP Updated Successfully

  MVP:          [MVP-NNNN] v[OLD] → v[NEW]
  Synced with:  [FRD-ID] v[FRD_VER]
  Updated:      [DATE]

Changes applied:
  ➕ [N] new tasks added        (status: Not Started)
  ⚠️  [N] tasks deferred         (FR removed from FRD)
  🔍 [N] tasks flagged for review (FR statement changed)
  ✅ [N] Done tasks protected    (not touched)
  — [N] tasks unchanged

Current task summary:
  Not Started:  [N]
  In Progress:  [N]
  Done:         [N]
  Blocked:      [N]
  Deferred:     [N]

Files updated:
  knowledge/artifact/90_project/[filename].json
  knowledge/req_doc/md/90_project/[filename].md
  knowledge/req_doc/html/90_project/[filename].html

Archived previous version to:
  knowledge/artifact/90_project/[old filename]

Action required:
  → Assign owners/estimates to the [N] newly added tasks
  → Review the [N] flagged tasks for alignment with updated FRD
```

---

## Important Rules

1. **Never modify tasks with status "Done"** — completed work is protected from all sync operations.
2. **Always archive the existing MVP before overwriting** — confirm archive success before writing.
3. **Never auto-approve changes** — always present the diff report and wait for explicit user confirmation.
4. **Only update tasks whose `linked_frd` matches the submitted document** — never touch tasks from other FRDs.
5. **Preserve all non-linked task fields** (owner, estimate, blocked_by) during update — only change status and notes.
6. **Task IDs (T-NNN) are never renumbered** — new tasks append from the highest existing ID.
7. **Only FRD documents trigger task-level sync** — other doc type updates only add a changelog note.
8. **Always write temp JSON via the Write tool** before invoking Python — never embed doc content in shell strings.
9. **If archive fails, stop and report the error** — do not overwrite without a successful archive.
