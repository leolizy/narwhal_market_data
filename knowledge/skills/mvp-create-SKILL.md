---
name: mvp-create
description: >
  Create a new MVP (Minimum Viable Product) task list scoped to a specific FRD.
  Tasks are anchored at FRD functional requirement (FR-NNN) level. Enforces a
  single open MVP constraint — aborts if an open MVP already exists. Use this skill
  when the user wants to create an MVP plan, open a new MVP list, or start MVP
  tracking for a functional scope.
---

# MVP Create — New MVP Task List

## Environment

- **Base directory:** `.`
- **CLI module:** `knowledge/sdlc_chain/cli.py`
- **Invoke CLI as:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`
  (run from the base directory)
- **JSON artifact files go to:** `knowledge/artifact/90_project/` (`.json` extension)
- **Markdown files go to:** `knowledge/req_doc/md/90_project/` (`.md` extension)
- **HTML files go to:** `knowledge/req_doc/html/90_project/` (`.html` extension, same base name as `.md`)
- **MVP naming:** `MVP-[NNNN]_[ShortTitle]_v[X.Y].json`

---

## Key Constraint: One Open MVP at a Time

A project may only have **one open MVP**. "Open" means status is any of:
`Draft`, `In Review`, `Approved`, `Active`.

If an open MVP already exists when this skill is invoked, you MUST abort and
tell the user which MVP is open before allowing any other action.

---

## PHASE 1 — Startup: Scan for Open MVP

Run the list-existing command first:

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

Store the full result for use throughout.

Then extract MVP documents from the output (type = "MVP"). For each, load its JSON
and check the `metadata.status` field:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import load_json

OPEN_STATUSES = {'Draft', 'In Review', 'Approved', 'Active'}
mvp_paths = [PATHS_FROM_LIST_EXISTING]  # substitute actual paths

open_mvps = []
for p in mvp_paths:
    try:
        d = load_json(p)
        status = d.get('metadata', {}).get('status', '')
        if status in OPEN_STATUSES:
            open_mvps.append({'path': p, 'id': d.get('metadata', {}).get('document_id', '?'), 'status': status, 'title': d.get('metadata', {}).get('title', '')})
    except Exception as e:
        pass

print(json.dumps(open_mvps))
"
```

### If an open MVP is found

Stop immediately and tell the user:

```
⛔ An open MVP already exists:

  ID:     [MVP-NNNN]
  Title:  [title]
  Status: [status]
  Path:   knowledge/artifact/90_project/[filename]

Only one open MVP is allowed at a time.

Options:
  1. Use /mvp-update to update the existing MVP with new document versions
  2. Manually change the existing MVP's status to "Completed" or "Retired" first,
     then re-run /mvp-create

Which would you like to do?
```

Do NOT proceed with MVP creation until the conflict is resolved.

### If no open MVP found

Continue to Phase 2.

---

## PHASE 2 — Select Scope FRD

Display available FRDs from the `list-existing` output:

```
## Select Scope FRD

The MVP task list will be anchored to functional requirements (FR-NNN) from a
specific FRD. Which FRD should this MVP cover?

Available FRDs:
  1. FRD-NPH-0001  CanonicalEntityManagement  v0.2  knowledge/artifact/10_function/...
  2. FRD-NPH-0002  DataIngestion              v0.4  knowledge/artifact/10_function/...
  ...

Enter a number or the FRD document ID (e.g. "FRD-NPH-0002"):
```

If the user provides a file path directly, accept it. If they mention an FRD by name,
match it from the list. Confirm the selection before proceeding.

---

## PHASE 3 — Load FRD and Extract Functional Requirements

Load the selected FRD and extract all functional areas and requirements:

```bash
python3 -c "
import sys, json, yaml
sys.path.insert(0, '.')

path = '[SELECTED_FRD_PATH]'

# Try JSON first, fall back to YAML
try:
    from sdlc_chain.yaml_utils import load_json
    d = load_json(path)
except Exception:
    with open(path, encoding='utf-8') as f:
        d = yaml.safe_load(f)

# Handle both flat and K8s-envelope formats
doc = d.get('spec', d)
fr_block = doc.get('functional_requirements', {})
areas = fr_block.get('functional_areas', []) if isinstance(fr_block, dict) else []

result = []
for area in areas:
    area_entry = {
        'area_id': area.get('area_id', ''),
        'area_name': area.get('area_name', ''),
        'requirements': []
    }
    for req in area.get('requirements', []):
        area_entry['requirements'].append({
            'id': req.get('id', ''),
            'statement': req.get('statement', '')[:120],
            'priority': req.get('priority', ''),
        })
    result.append(area_entry)

doc_meta = doc.get('document', {})
print(json.dumps({'frd_id': doc_meta.get('document_id', '?'), 'areas': result}))
"
```

Present the extracted requirements to the user in a structured list:

```
## Functional Requirements in [FRD-ID]

  FA-1: Source Onboarding
    FR-001 [Must]  System shall support onboarding of multiple external data sources...
    FR-002 [Must]  System shall support configurable source adapters...

  FA-2: Automated Processing
    FR-003 [Must]  System shall schedule and execute automated ingestion jobs...
    ...

Total: [N] functional requirements across [M] functional areas.

Which requirements should this MVP cover?
  a. All of them  (default)
  b. Select specific functional areas (by FA-N)
  c. Select specific requirements (by FR-NNN)

Reply with a, b, or c:
```

### If (b) — Select by functional area

List the area IDs and names. Ask user to enter comma-separated area IDs (e.g., `FA-1, FA-3`).
Filter to those areas only.

### If (c) — Select specific requirements

Ask user to enter comma-separated FR IDs (e.g., `FR-001, FR-003, FR-007`).
Filter to those requirements only. Preserve their functional area grouping.

### If (a) — All requirements

Proceed with all areas and requirements. No filtering needed.

Confirm the final selection:

```
Got it. I'll build the MVP task list from:
  [N] requirements across [M] functional areas:
  - FA-1: Source Onboarding (FR-001, FR-002)
  - FA-3: Automated Processing (FR-003)
  ...

Does that look right? (yes/no)
```

---

## PHASE 4 — Collect MVP Metadata

Ask the following questions in groups. Do NOT ask field by field — use open-ended prose.

### Group 1 — Identity

```
## MVP Details (1 of 3)

What is the title and objective for this MVP?

Tell me:
- A short title (e.g., "Data Ingestion MVP — Sprint 5")
- The single overarching goal of this delivery cycle (1-2 sentences)
- The target release or sprint name (e.g., "Sprint 12", "v1.0-beta")
- Author name, reviewer, approver, product owner, and tech lead (if known)
```

After user answers, confirm:

```
Got it. I'll capture:
  title:          [title]
  mvp_objective:  [objective]
  release_target: [sprint/release]
  author:         [name]
  reviewer:       [name]
  approver:       [name]
  product_owner:  [name]
  tech_lead:      [name]

Does that look right?
```

### Group 2 — Success Criteria and Scope

```
## MVP Details (2 of 3)

What does success look like, and what are the boundaries?

Tell me:
- 2–4 measurable success criteria (quantifiable where possible)
- What is explicitly OUT of scope for this MVP
- Any key assumptions
```

After user answers, confirm captured values.

### Group 3 — Timeline and Risks

```
## MVP Details (3 of 3)

Timeline and risks:

Tell me:
- 3–6 key milestones with target dates (YYYY-MM-DD)
- Any known risks or blockers that could delay delivery
- Any external dependencies (other teams, APIs, vendors)
```

After user answers, confirm captured values.

---

## PHASE 5 — Generate MVP Document

After all sections are confirmed, announce: "Generating your MVP document…"

### Task scaffolding from functional requirements

Build the `tasks.workstreams` array automatically from the selected FRD requirements.
Each functional area becomes one workstream. Each FR becomes one task:

```
workstream_name: [FA-N area_name]
tasks:
  - id: T-[NNN]          # sequential across all workstreams, starting at T-001
    title: [FR-NNN]: [first 80 chars of FR statement]
    description: [full FR statement]
    linked_fr: [FR-NNN]              # KEY FIELD — used by mvp-update
    linked_frd: [FRD-ID]             # e.g. FRD-NPH-0002
    owner: ""                        # to be assigned
    priority: [map FR priority: Must→P1-High, Should→P2-Medium, Could→P3-Low, Won't→Deferred]
    estimate: ""
    status: "Not Started"
    blocked_by: ""
    acceptance_criteria: []          # copy FR acceptance_criteria if present
    notes: ""
```

Priority mapping from FR priority to task priority:
- `Must` → `P1-High`
- `Should` → `P2-Medium`
- `Could` → `P3-Low`
- `Won't` / not set → `P3-Low`

### Document ID generation

Count existing MVP documents from `list-existing` output.
`MVP-[NNNN]` where NNNN = (count + 1) zero-padded to 4 digits.

### Output paths

```
JSON:  knowledge/artifact/90_project/MVP-[NNNN]_[ShortTitle]_v0.1.json
MD:    knowledge/req_doc/md/90_project/MVP-[NNNN]_[ShortTitle]_v0.1.md
HTML:  knowledge/req_doc/html/90_project/MVP-[NNNN]_[ShortTitle]_v0.1.html
```

Tell the user all three paths before writing. Ask for confirmation.

### Writing the files

**Step 1 — Assemble the full document dict** in memory:

```json
{
  "metadata": {
    "document_id": "MVP-NNNN",
    "title": "[title]",
    "version": "0.1",
    "status": "Draft",
    "classification": "Internal",
    "created_date": "[YYYY-MM-DD]",
    "last_updated": "[YYYY-MM-DD]",
    "author": "[author]",
    "reviewer": "[reviewer]",
    "approver": "[approver]",
    "product_owner": "[product_owner]",
    "tech_lead": "[tech_lead]",
    "release_target": "[release_target]",
    "related_documents": ["[FRD-ID]"],
    "tags": [],
    "supersedes": "",
    "scoped_frd": "[FRD-ID]",
    "scoped_frd_path": "[relative path to FRD artifact]"
  },
  "mvp_objective": { "content": "[objective]" },
  "success_criteria": { "items": [...] },
  "scope": { "in_scope": [...], "out_of_scope": [...], "assumptions": [...] },
  "tasks": { "workstreams": [...] },
  "dependencies_and_risks": { "dependencies": [...], "risks": [...] },
  "timeline": { "milestones": [...] },
  "definition_of_done": {
    "checklist": [
      "Code reviewed and merged",
      "Unit tests passing",
      "Acceptance criteria verified",
      "No critical or high-severity bugs open",
      "Documentation updated (if applicable)"
    ]
  },
  "change_log": [
    {
      "version": "0.1",
      "date": "[YYYY-MM-DD]",
      "author": "[author]",
      "changes": "Initial MVP task list created from [FRD-ID]"
    }
  ]
}
```

**Step 2 — Write temp JSON:**

Use the Write tool to save to `/tmp/mvp_draft.json`.

**Step 3 — Write JSON artifact:**

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import dump_json
from pathlib import Path

with open('/tmp/mvp_draft.json', encoding='utf-8') as f:
    doc = json.load(f)

path = '[FULL JSON PATH]'
Path(path).parent.mkdir(parents=True, exist_ok=True)
dump_json(doc, path)
print(json.dumps({'path': path, 'status': 'ok'}))
"
```

**Step 4 — Write Markdown** using the Write tool. Render as follows:

```markdown
# MVP Plan — [title]

| Field | Value |
|-------|-------|
| Document ID | [id] |
| Version | 0.1 |
| Status | Draft |
| Scoped FRD | [FRD-ID] |
| Release Target | [release_target] |
| Author | [author] |
| Created | [YYYY-MM-DD] |

---

## Objective

[mvp_objective.content]

---

## Success Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| [criterion] | [metric] | [target] |

---

## Scope

**In Scope:**
[in_scope items as bullet list]

**Out of Scope:**
[out_of_scope items as bullet list]

**Assumptions:**
[assumptions as bullet list]

---

## Task List

### [Workstream Name] (FA-N)

| Task ID | FR Ref | Title | Priority | Status | Owner | Estimate |
|---------|--------|-------|----------|--------|-------|----------|
| T-001 | FR-001 | [title] | P1-High | Not Started | — | — |
| T-002 | FR-002 | [title] | P1-High | Not Started | — | — |

[repeat per workstream]

**Summary:** [N] tasks total — [N] Not Started, 0 In Progress, 0 Done

---

## Dependencies & Risks

**Dependencies:**
[list]

**Risks:**
[list]

---

## Timeline

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| [milestone] | [date] | [owner] | On Track |

---

## Definition of Done

[checklist items as checkbox list]

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [date] | [author] | Initial MVP task list created from [FRD-ID] |
```

**Step 5 — Generate HTML:**

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

## PHASE 6 — Summary Report

After writing all files, present a completion summary:

```
## MVP Created Successfully

  Document ID:  MVP-NNNN
  Title:        [title]
  Scoped FRD:   [FRD-ID]
  Tasks:        [N] tasks across [M] workstreams

  Files written:
    knowledge/artifact/90_project/[filename].json
    knowledge/req_doc/md/90_project/[filename].md
    knowledge/req_doc/html/90_project/[filename].html

Task breakdown:
  [FA-1] Source Onboarding:          [N] tasks
  [FA-2] Automated Processing:       [N] tasks
  ...

Next steps:
  - Assign owners and estimates to each task
  - Use /mvp-update whenever a new version of [FRD-ID] is submitted
    to automatically sync outstanding task statuses
```

---

## Important Rules

1. **Never create a new MVP if an open MVP already exists.** Always block at Phase 1 and explain the options.
2. **Never write files without confirming output paths with the user first.**
3. **Every task MUST have a `linked_fr` field** pointing to its source FR-NNN ID — this is the foreign key used by the update skill.
4. **Every task MUST have a `linked_frd` field** pointing to the source FRD document ID.
5. **`metadata.scoped_frd` and `metadata.scoped_frd_path`** must be set — these anchor the MVP to its source FRD.
6. **Never generate downstream chain report for MVP** — MVP is a Layer 5 terminal document.
7. **Use today's date** for `created_date` and `last_updated`.
8. **Always write temp JSON via the Write tool** before invoking Python — never embed doc data in shell strings.
