---
name: switch-knowledge
description: "Activate the Knowledge branch for documentation work. Sets branch lock and loads knowledge agent context."
---

# Switch to Knowledge Branch

## Purpose

Activate the Knowledge branch so that all subsequent work is scoped to
documentation creation, updates, and validation within `knowledge/`.

## Workflow

### Step 1 — Set branch lock

Write the string `knowledge` to `.claude/.branch_lock`:

```bash
echo "knowledge" > .claude/.branch_lock
```

### Step 2 — Confirm activation

```
Knowledge branch activated.

  Agent context: knowledge/AGENTS.md
  Skills: knowledge/SKILL.md, knowledge/skills/*.md
  Write scope: knowledge/ only
  CLI: python3 knowledge/sdlc_chain/cli.py <command>

  Use /doc-status for a quick dashboard of SDLC tree progress.
  Use /sdlc-doc-intake to create or update a document.
```

### Step 3 — Load agent context

Read `knowledge/AGENTS.md` and `knowledge/SKILL.md` to load the full
knowledge branch context, conventions, and available skills.

## Rules

1. Always write the lock file before doing any other work.
2. If already on the knowledge branch, confirm and skip re-activation.
3. Never write to `scaffold/` while the knowledge branch is active.
