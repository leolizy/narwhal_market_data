---
name: sdlc-doc-intake
description: "Interactive SDLC document intake workflow. Use this skill when the user wants to create a new document or update an existing one across any of the 20 SDLC document types: PC, FRD, NFR, PSD, AEC, API, DC, DBC, MDC, HLD, CICD, DBAD, TSI, NFTS, DG, UT, NFRAR, MVP, RTM, DD. Guides the user section-by-section, accepts file uploads, generates JSON output to knowledge/artifact/, MD + HTML output to doc/, archives older versions to archive/, stages signed-off docs to knowledge/staging/, and produces a downstream chain update flagging report."
---

# SDLC Document Intake — Workflow Instructions

## Environment

- **Base directory:** `.`
- **CLI module:** `knowledge/sdlc_chain/cli.py`
- **Invoke CLI as:** `python3 knowledge/sdlc_chain/cli.py <command> [args]`
  (run from the base directory above)
- **JSON artifact files go to:** `knowledge/artifact/[subdir]/` (`.json` extension)
- **Markdown files go to:** `knowledge/req_doc/md/[subdir]/` (`.md` extension)
- **HTML files go to:** `knowledge/req_doc/html/[subdir]/` (`.html` extension, same base name as `.md`)
- **Archived older versions go to:** `archive/[subdir]/` (same structure as `knowledge/artifact/`)
- **Staged (signed-off) documents go to:** `knowledge/staging/[subdir]/` (same structure as `knowledge/artifact/`)

---

## Doc Type Reference Table

| # | Code | Name | Template dir | YAML template | README file | Layer |
|---|------|------|-------------|---------------|-------------|-------|
| 1 | PC | Platform Canon | `00_general` | `00-pc_template.yaml` | `00-pc_README.md` | 0 |
| 2 | FRD | Functional Requirements | `10_function` | `11-frd_template.yaml` | `11-frd_README.md` | 1 |
| 3 | NFR | Non-Functional Requirements | `20_non_function` | `21-nfr_template.yaml` | `21-nfr_README.md` | 1 |
| 4 | PSD | Product Specification | `30_logical` | `31-psd_template.yaml` | `31-psd_README.md` | 2 |
| 5 | AEC | Async Event Contract | `40_contract` | `41-aec_template.yaml` | `41-aec_README.md` | 3 |
| 6 | API | API Specification (OpenAPI) | `40_contract` | `42-api_schemas.yaml` | `42-api_README.md` | 3 |
| 7 | DC | Data Contract | `40_contract` | `43-dc_template.yaml` | `43-dc_README.md` | 3 |
| 8 | DBC | Database Contract | `40_contract` | `44-dbc_template.yaml` | `44-dbc_README.md` | 3 |
| 9 | MDC | Market Data Contract | `50_external_contract` | `51-mdc_template.yaml` | `51-mdc_README.md` | 3 |
| 10 | HLD | High-Level Design | `60_architecture` | `61-hld_template.yaml` | `61-hld_README.md` | 3 |
| 11 | CICD | CI/CD Framework | `70_nf_implementation` | `73-cicd_template.yaml` | `73-cicd_README.md` | 3 |
| 12 | DBAD | Database Architecture | `70_nf_implementation` | `74-dbad_template.yaml` | `74-dbad_README.md` | 3 |
| 13 | TSI | Technical System Integration | `60_architecture` | `62-tsi_template.yaml` | `62-tsi_README.md` | 3 |
| 14 | NFTS | Non-Functional Test Spec | `70_nf_implementation` | `71-nfts_template.yaml` | `71-nfts_README.md` | 4 |
| 15 | DG | Deployment Guide | `70_nf_implementation` | `72-dg_template.yaml` | `72-dg_README.md` | 4 |
| 16 | UT | Unit Test Document | `80_test` | `81-ut_template.yaml` | `81-ut_README.md` | 4 |
| 17 | NFRAR | NFR Analysis Report | `80_test` | `82-nfrar_template.yaml` | `82-nfrar_README.md` | 4 |
| 18 | MVP | Minimum Viable Product | `90_project` | `91-mvp_template.yaml` | `91-mvp_README.md` | 5 |
| 19 | RTM | Requirements Traceability Matrix | `90_project` | `92-rtm_template.yaml` | `92-rtm_README.md` | 5 |
| 20 | DD | Data Dictionary | `90_project` | `93-dd_template.yaml` | *(no README)* | 5 |

**Artifact output subdirectory** = the template dir column above (e.g. PC → `knowledge/artifact/00_general/`).

---

## Chain Order (direct parent → children)

```
PC  → FRD, NFR
FRD  → PSD
NFR  → HLD, CICD, DBAD, TSI
PSD  → AEC, API, DC, DBC, MDC
AEC, API, DC, DBC, MDC → UT
CICD → NFTS, DG
DBAD → NFTS
TSI  → NFTS
NFTS → NFRAR, MVP, RTM
DG   → MVP, RTM
UT   → MVP, RTM
NFRAR → MVP, RTM
```

---

## ID Generation Rules

| Doc type | ID pattern | Filename pattern (artifact JSON / doc MD / doc HTML) |
|----------|-----------|------------------------------------------------------|
| PC | `PC-[PROJECT]-[NNNN]` | `PC-[PROJECT]-[NNNN]_[ShortTitle]_v[X.Y].json / .md / .html` |
| FRD | `FRD-[PROJECT]-[NNNN]` | `FRD-[PROJECT]-[NNNN]_[ShortTitle]_v[X.Y].json / .md / .html` |
| PSD | `PSD-[NNNN]` | `PSD-[NNNN]_[ShortTitle]_v[X.Y].json / .md / .html` |
| UT | `UT-[NNNN]` | `UT-[NNNN]_[FunctionName]_v[X.Y].json / .md / .html` |
| MDC | `MDC-[NNNN]` | `MDC-[NNNN]_[SourceName]_v[X.Y].json / .md / .html` |
| All others | `[TYPE]-[NNNN]` | `[TYPE]-[NNNN]_[ShortTitle]_v[X.Y].json / .md / .html` |

- `[PROJECT]` = 2–5 uppercase letters (e.g. `NPH`)
- `[NNNN]` = 4-digit sequence starting at 0001
- `[ShortTitle]` = PascalCase, max 40 chars
- `[X.Y]` = semantic version (e.g. `0.1` for drafts, `1.0` for initial approved)

Determine the next sequence number by counting existing docs of the same type from the `list-existing` output (cached from Phase 1 startup).

---

## PHASE 1 — Startup: Scan + Mode and Document Type Selection

**Run this first, before showing any menu:**

```bash
python3 knowledge/sdlc_chain/cli.py list-existing
```

Store the result. You will reference this JSON throughout all subsequent phases
(sequence numbering, pre-fill analysis, FRD PC lookup, and the chain report).
Do NOT re-run it unless the user explicitly adds or removes a document mid-session.

---

Present this exact menu:

```
I'll help you create or update an SDLC document. Which mode do you need?

  1. Create a new document
  2. Update an existing document

Reply with 1 or 2.
```

### If mode = 1 (New document)

Present the 19 doc types grouped by layer:

```
Which document type do you want to create?

  Layer 0 — Business & Decisions:
     1. PC   Platform Canon
    19. DD    Design Decisions

  Layer 1 — Requirements:
     2. FRD   Functional Requirements Document
     3. NFR   Non-Functional Requirements

  Layer 2 — Specification:
     4. PSD   Product Specification Document

  Layer 3 — Contracts & Architecture:
     5. AEC   Async Event Contract
     6. API   API Specification (OpenAPI)
     7. DC    Data Contract
     8. DBC   Database Contract
     9. MDC   Market Data Contract
    10. CICD  CI/CD Framework
    11. DBAD  Database Architecture Design
    12. TSI   Technical System Integration

  Layer 4 — Implementation & Testing:
    13. NFTS  Non-Functional Test Specification
    14. DG    Deployment Guide
    15. UT    Unit Test Document
    16. NFRAR NFR Analysis Report

  Layer 5 — Project Facilitation:
    17. MVP   Minimum Viable Product Plan
    18. RTM   Requirements Traceability Matrix

Enter a number or the doc type code (e.g. "PC"):
```

### If mode = 2 (Update existing document)

Ask:

```
How would you like to provide the document to update?

  a. Upload or paste the file content
  b. Scan the project for existing documents

Reply with a or b.
```

**If (b):** Use the `list-existing` output cached from the Phase 1 startup run.
Present results as a numbered list. If empty, tell the user no existing documents
were found and fall back to option (a).

**If (a):** Ask the user to paste the YAML content or provide a file path. Read the
content. Detect the document type using the CLI:

```bash
python3 knowledge/sdlc_chain/cli.py detect [FILE_PATH]
```

Confirm: "I detected this as a [TYPE] document with ID [ID]. Is that correct?"

---

## PHASE 2 — Template Loading and Pre-fill Analysis

Once you know the doc type, run the template command silently:

```bash
python3 knowledge/sdlc_chain/cli.py template [DOC_TYPE]
```

Read the JSON output. Use the `sections` array as your Q&A roadmap and the `readme_guidance` for section-level context. Do NOT show the raw JSON to the user.

### FRD special case

If creating an FRD AND the `list-existing` output contains a PC document:

Tell the user: "I found a PC at [path]. Would you like me to use the PC generator to pre-populate the FRD draft? (yes/no)"

**If yes:**
1. Ask which PC to use (if multiple).
2. Show the user the PC's functional requirement IDs:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, '.')
   from sdlc_chain.parsers.pc_parser import load_pc
   pc = load_pc('[PC_PATH]')
   for r in pc.functional_requirements:
       print(r.id, ':', r.statement[:80])
   "
   ```
3. Generate a mapping template scaffold and show it to the user:
   ```bash
   python3 knowledge/sdlc_chain/cli.py mapping-template [PC_PATH] [PROJECT_CODE]
   ```
   Ask the user to rename the placeholder module and split requirements into
   logical modules before continuing.
4. Once modules are defined, invoke the FRD generator:
   ```bash
   python3 -c "
   import sys, json
   sys.path.insert(0, '.')
   from sdlc_chain.parsers.pc_parser import load_pc
   from sdlc_chain.models import ModuleMapping
   from sdlc_chain.generators.frd_generator import generate_frd

   pc = load_pc('[PC_PATH]')
   module = ModuleMapping(
       module_code='[MODULE_CODE]',    # still used for requirement grouping
       module_name='[MODULE_NAME]',
       requirements=[PC_REQ_IDS],
       functions=[],
   )
   frd = generate_frd(pc, module, project_code='[PROJECT_CODE]', sequence=[SEQ])
   print(json.dumps(frd))
   "
   ```
   Capture the JSON output as your starting draft.
5. In Phase 3, focus specifically on resolving sections marked `[AUTO - Review]` and `[DRAFT - Needs Review]`.

**If no or no PC exists:** proceed with standard template-based Q&A for all sections.

### Update mode: Processed Report

When updating an existing document, before asking any questions, produce this comparison table:

```
## Pre-fill Analysis — [DOC_TYPE] [DOC_ID]

I've mapped your existing content to the template sections:

SECTION               STATUS        NOTES
──────────────────────────────────────────────────────────────
metadata              complete      All required fields present
executive_summary     complete      Content found
objectives            incomplete    1 item; success_measure empty
problem_statement     missing       No content detected
scope                 partial       in_scope present, out_of_scope empty
requirements          complete      3 functional, 1 NFR, 0 constraints
risks                 missing       No items found

Sections that need your input: objectives (success_measure),
problem_statement, scope (out_of_scope), risks.

Shall I work through only the missing/incomplete sections, or all sections?
```

---

## PHASE 3 — Section-by-Section Q&A

Work through sections using the groupings below. For doc types with fewer than
4 sections (e.g. DD), go one section at a time.

### PC groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` — title, project code, author, reviewer, approver, classification, related doc IDs, tags, supersedes |
| G2 | `executive_summary` + `problem_statement` |
| G3 | `objectives` — each with its success measure |
| G4 | `scope` — in-scope, out-of-scope, domain definitions |
| G5 | `stakeholders` + `current_state` + `future_state` |
| G6 | `requirements` — functional, NFR, and constraints separately |
| G7 | `assumptions_and_constraints` + `risks` + `dependencies` |
| G8 | `success_metrics` + `glossary` (optional) |

### FRD groupings

| Group | Sections |
|-------|----------|
| G1 | `document` (metadata) |
| G2 | `introduction` + `purpose` + `business_context` |
| G3 | `scope` + `definitions` |
| G4 | `actors` + `functional_overview` + `event_triggers` |
| G5 | `functional_requirements` (per functional area) |
| G6 | `business_rules` + `exception_scenarios` |
| G7 | `cross_module_interactions` + `data_requirements` |
| G8 | `nonfunctional_requirements` + `dependencies` + `assumptions` + `constraints` |
| G9 | `traceability` + `acceptance_criteria` |
| G10 | `open_issues` + `approvals` (optional review) |

### NFR groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `introduction` + `scope` |
| G3 | `nonfunctional_requirements` (by category: performance, reliability, security, etc.) |
| G4 | `compliance` + `constraints` |
| G5 | `priorities` + `traceability` |

### PSD groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `function_overview` (function_type / archetype) |
| G3 | `data_model` + `field_definitions` |
| G4 | `ui_specification` (if applicable) |
| G5 | `process_flow` + `business_rules` |
| G6 | `acceptance_criteria` + `traceability` |

### Contract-layer types (AEC, DC, DBC) groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `overview` / `purpose` |
| G3 | Core content (events / fields / schema — varies by type) |
| G4 | `versioning` + `compatibility` |
| G5 | `examples` + `validation_rules` |

### MDC (Market Data Contract) groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `contract_overview` + `data_product_identification` |
| G3 | `input_and_source_location` (source systems, delivery mechanisms, formats, authentication, public URLs) |
| G4 | `source_data_catalog` (L1) + `dataset_extraction_plan` (L2, incl. per-dataset write path behaviour) |
| G5 | `canonical_key_resolution` (L3: composite key derivation, 6 canonical key columns, per-dataset key resolution, entity resolution mechanics) |
| G6 | `field_extraction_spec` (L4: per-dataset, per-field mapping tables) |
| G7 | `end_result` (L5: DC-0004 snapshot mockups per dataset) + `semantic_definitions` (glossary + business rules) |
| G8 | `data_quality_standards` + `service_level_agreements` |
| G9 | `access_and_security` + `lineage_and_dependencies` (incl. `canonical_entity_integration` ref PSD-0002, `search_mode` per consumer) |
| G10 | `versioning_and_compatibility` + `sample_fixture` + `support_and_communication` + `change_log` |

**MDC special case — market-search integration:**
Only use market-search when the user provides just the desired market (exchange name or code) without full source details. If the user already has specific source URLs, delivery mechanisms, and formats, skip market-search and proceed directly with the MDC intake.

If market-search is needed, run:
```bash
python3 knowledge/market_search/search.py sources [EXCHANGE_CODE]
```
Use the discovered URLs to pre-populate the `input_and_source_location.source_systems[]` entries in G3. Map exchange metadata to `canonical_key_fields` (per PSD-0002) and set `entity_resolution.canonical_key_ref` to `PSD-0002`.

### API grouping

Work through the OpenAPI spec top-down:
`info` → `servers` → `paths` (endpoint by endpoint) → `components` → `security`.

### Architecture-layer types (CICD, DBAD, TSI) groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `overview` + `principles` |
| G3 | Core architecture content (pipeline stages / schema design / integration map) |
| G4 | `environment_configuration` |
| G5 | `risks` + `decisions` |

### NFTS groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `scope` + `objectives` |
| G3 | `test_categories` (performance, security, reliability — one at a time) |
| G4 | `tools_and_environment` |
| G5 | `acceptance_criteria` + `reporting` |

### DG groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `prerequisites` + `environment_setup` |
| G3 | `deployment_steps` (step by step) |
| G4 | `rollback_procedure` |
| G5 | `verification_checklist` |

### UT groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `unit_under_test` + `test_objectives` |
| G3 | `test_cases` (per case) |
| G4 | `mocking_strategy` + `coverage_targets` |

### NFRAR groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `executive_summary` + `scope` |
| G3 | `findings` (per NFR category) |
| G4 | `recommendations` + `risk_register` |

### MVP groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `objectives` + `success_criteria` |
| G3 | `included_features` + `excluded_features` |
| G4 | `release_plan` + `risks` |

### RTM groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `traceability_matrix` (requirement by requirement) |
| G3 | `coverage_summary` + `gaps` |

### DD groupings

| Group | Sections |
|-------|----------|
| G1 | `metadata` |
| G2 | `decision` (one at a time: context, options, outcome, rationale) |

### Per-section Q&A format

For each group, follow this pattern:

1. Announce the section: `## Section: [Name] ([N] of [total])`
2. Quote the guidance: `> **Guidance:** [guidance text from template]`
3. Ask open, section-level questions in prose (NOT field-by-field)
4. After the user answers, confirm your interpretation:
   ```
   Got it. I'll capture:
     [field]: [value]
     [field]: [value]

   Does that look right, or would you like to add anything?
   ```
5. Once confirmed, move to the next group.

Build the document structure in memory as you go. Do NOT write files during Q&A.

**Update mode:** In update mode, only ask about sections that are missing or incomplete (from the Processed Report), unless the user asks to review all.

---

## PHASE 4 — Document Generation

After all sections are confirmed, announce: "Generating your [DOC_TYPE] document…"

### Document ID generation

- Use the sequence number = 1 + count of existing docs of this type in `list-existing` output.
- PC: `PC-[PROJECT]-[NNNN]` e.g. `PC-NPH-0001`
- FRD: `FRD-[PROJECT]-[NNNN]` e.g. `FRD-NPH-0001`
- All others: `[TYPE]-[NNNN]` e.g. `PSD-0001`

### Output paths

JSON: `knowledge/artifact/[template_dir]/[filename].json`
MD:   `knowledge/req_doc/md/[template_dir]/[filename].md`
HTML: `knowledge/req_doc/html/[template_dir]/[filename].html`

Tell the user all three paths before writing. Ask for confirmation.

### Writing the files

**Step 1 — Write doc data to a temp JSON file using the Write tool:**

Use the Write tool to save the complete document dict as JSON to:
`knowledge/.tmp/sdlc_draft_[DOC_TYPE].json`

This avoids shell-escaping issues with special characters in user content.

**Step 2 — Archive old version (update mode only):**

Before overwriting in update mode, archive the existing file first:

```bash
python3 knowledge/sdlc_chain/cli.py archive [EXISTING JSON PATH]
```

The CLI will copy the old version to `archive/[subdir]/[filename]` and print the
destination path. Confirm the archive was successful before proceeding.

**Step 3 — Write JSON artifact:**

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.yaml_utils import dump_json
from pathlib import Path

with open('knowledge/.tmp/sdlc_draft_[DOC_TYPE].json', encoding='utf-8') as f:
    doc_data = json.load(f)

json_path = '[FULL JSON PATH]'
Path(json_path).parent.mkdir(parents=True, exist_ok=True)
dump_json(doc_data, json_path)
print(json.dumps({'json': json_path, 'status': 'ok'}))
"
```

**Step 4 — Write Markdown using the Write tool** with the rendered content
(see rendering rules below). Write directly to the MD path.

**Step 5 — Generate HTML from the Markdown:**

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

The HTML file shares the same base name as the Markdown file, just with `.html`.
Example: `knowledge/req_doc/html/00_general/PC-NPH-0001_NarwhalProductHub_v0.3.html`

### Validation step

After writing the JSON, always validate it before proceeding to Phase 5:

```bash
python3 knowledge/sdlc_chain/cli.py validate [DOC_TYPE] [JSON_PATH]
```

If `errors` is non-empty, report them to the user and ask how to proceed.
If only `warnings`, report them but continue to Phase 5.

### Staging (sign-off)

When the user explicitly indicates the document is **signed off / approved**,
offer to move it to staging:

```
The document looks complete. Would you like to stage it for sign-off approval?
This copies [filename].json to knowledge/staging/[subdir]/ to mark it as ready for review.
Reply yes/no.
```

If yes, run:

```bash
python3 knowledge/sdlc_chain/cli.py stage [FULL JSON PATH]
```

Report the destination path from the CLI output. The original in `knowledge/artifact/` is
unchanged — staging is a copy, not a move.

### K8s-style envelope format (CRITICAL — applies to ALL doc types)

ALL artifacts must be written in **K8s-style envelope format** with
`kind` at the top level, followed by `metadata` and the document's
content sections. The flat template is for reading guidance only.

```json
{
  "kind": "<KindName>",
  "metadata": { ... },
  "<section_1>": { ... },
  "<section_2>": { ... }
}
```

Kind values by doc type:

| Doc Type | `kind` Value                    |
|----------|---------------------------------|
| PC       | `PlatformCanon`                 |
| FRD      | `FunctionalRequirements`        |
| NFR      | `NonFunctionalRequirements`     |
| HLD      | `HighLevelDesign`               |
| CICD     | `CICDFramework`                 |
| DBAD     | `DatabaseArchitectureDesign`    |
| TSI      | `TechnicalSystemIntegration`    |
| NFTS     | `NonFunctionalTestSpec`         |
| DG       | `DeploymentGuide`               |
| NFRAR    | `NFRAnalysisReport`             |
| MVP      | `MinimumViableProductPlan`      |
| RTM      | `RequirementsTraceabilityMatrix` |

### FRD Markdown rendering

For FRD, generate Markdown using the existing renderer (reads from the temp file
written in Step 1):

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from sdlc_chain.generators.md_renderer import render_frd_markdown

with open('knowledge/.tmp/sdlc_draft_FRD.json', encoding='utf-8') as f:
    frd_dict = json.load(f)

md = render_frd_markdown(frd_dict)
with open('[MD_PATH]', 'w', encoding='utf-8') as f:
    f.write(md)
print('done')
"
```

### All other doc types — Markdown rendering

For all types except FRD, render Markdown by iterating sections:

```
# [DOC TYPE NAME] — [Document Title]

| Field | Value |
|-------|-------|
| Document ID | [id] |
| Title | [title] |
| Version | [version] |
| Status | [status] |
| Created | [created_date] |
| Author | [author] |

---

## 1. [Section Name]

> **Guidance:** [guidance from template]

[section content]

---

## Change Log

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| [ver] | [date] | [author] | [summary] |
```

### Update mode: version increment

When updating an existing document:
- Increment minor version: `1.0` → `1.1`, `2.3` → `2.4`
- Set `last_updated` to today's date
- Add a new change_log entry summarising what was changed
- Overwrite the original file (confirm with user first)

---

## PHASE 5 — Chain Update Flagging Report

After writing the files, automatically run:

```bash
python3 knowledge/sdlc_chain/cli.py downstream [DOC_TYPE]
```

Reference the `list-existing` output cached from Phase 1 to check which downstream
types already have documents.

### Priority calculation

Use the `hop_count` field from the downstream command output directly:

| hop_count | Priority |
|-----------|---------|
| 1 | HIGH |
| 2 | MEDIUM |
| 3+ | LOW |

### Report format

```
## Chain Update Flagging Report

You created/updated: [DOC_TYPE] [DOC_ID]

The following downstream documents may need review:

PRIORITY  DOC TYPE  DOCUMENT ID         STATUS      IMMEDIATE PARENT
────────────────────────────────────────────────────────────────────────
HIGH      FRD       FRD-NPH-ING-0001    EXISTS      PC
HIGH      NFR       —                   NOT FOUND   PC
MEDIUM    PSD       —                   NOT FOUND   FRD
LOW       AEC       —                   NOT FOUND   PSD
...

RECOMMENDED ACTIONS:
  1. [HIGH priority existing docs] — review and update as needed
  2. [HIGH priority not-found docs] — create if applicable to this change
  3. No immediate action needed for LOW priority docs

⚠️  No documents were automatically modified.
    All downstream changes require manual review.
    Use this skill again to create or update any of the above documents.
```

**EXISTS** = found in `list-existing` output. Show the relative path.
**NOT FOUND** = no document of that type exists yet in the project.

---

## Important Rules

1. **Never write files without asking the user to confirm the paths first.**
2. **In update mode, always archive the existing file (Step 2) before overwriting. Confirm the archive succeeded.**
3. **In update mode, always confirm before overwriting an existing file.**
4. **The chain flagging report is informational only — never auto-generate downstream docs.**
5. **Always state clearly at the end of the report: "No documents were automatically modified."**
6. **ALL doc types must use the K8s envelope format (`kind/metadata/sections`), not the flat template format. See the Kind values table for the `kind` value per doc type.**
7. **For the FRD generator special case, only use it when: doc type is FRD AND a PC exists AND the user agrees.**
8. **If any CLI command fails, report the error to the user and ask how to proceed.**
9. **Always run `list-existing` once at Phase 1 startup and reuse that cached output throughout — do not re-run mid-session.**
10. **Always write doc data to a temp JSON file (Write tool) before invoking Python — never paste dict repr into shell strings.**
11. **Always validate the generated JSON (Phase 4 validation step) before proceeding to Phase 5.**
12. **Artifact output is always `.json` — never write `.yaml` to `knowledge/artifact/`. Templates in `template/` remain YAML for guidance only.**
13. **Always generate both MD and HTML outputs to `doc/`. The HTML file has the same base name as the MD file.**
14. **Staging is a copy operation — the original in `knowledge/artifact/` is preserved. Only stage when the user explicitly requests it.**
