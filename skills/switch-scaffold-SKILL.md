---
name: switch-scaffold
description: "Activate the Scaffold branch for code scaffolding work. Sets branch lock and loads scaffold agent context."
---

# Switch to Scaffold Branch

## Purpose

Activate the Scaffold branch so that all subsequent work is scoped to
code generation and scaffolding within `scaffold/`.

## Workflow

### Step 1 — Set branch lock

Write the string `scaffold` to `.claude/.branch_lock`:

```bash
echo "scaffold" > .claude/.branch_lock
```

### Step 2 — Confirm activation

```
Scaffold branch activated.

  Agent context: scaffold/AGENTS.md
  Skills: scaffold/SKILL.md, scaffold/skills/*.md
  Write scope: scaffold/ only
  CLI: python3 scaffold/build_chain/cli.py <command>

  Use /read-artifacts to scan knowledge documentation.
  Use /build-status for a dashboard of scaffolded vs pending items.
```

### Step 3 — Load agent context

Read `scaffold/AGENTS.md` and `scaffold/SKILL.md` to load the full scaffold
branch context, scaffold mapping, and available skills.

## Rules

1. Always write the lock file before doing any other work.
2. If already on the scaffold branch, confirm and skip re-activation.
3. Never write to `knowledge/` while the scaffold branch is active.
