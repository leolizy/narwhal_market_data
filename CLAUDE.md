# Narwhal — SDLC Doc-to-Code System

This repository has two isolated branches with independent agents and skills.

## Branches

### Knowledge Branch (documentation)
- **Agent:** `knowledge/AGENTS.md`
- **Skills:** `knowledge/SKILL.md`, `knowledge/skills/*.md`
- **Scope:** Create, update, validate SDLC documentation artifacts
- **Write access:** `knowledge/` only
- **Read access:** `knowledge/` and `scaffold/` (read-only access to scaffold)

### Scaffold Branch (code generation)
- **Agent:** `scaffold/AGENTS.md`
- **Skills:** `scaffold/SKILL.md`, `scaffold/skills/*.md`
- **Scope:** Analyse knowledge artifacts, generate project scaffolding and code
- **Write access:** `scaffold/` only
- **Read access:** `scaffold/` and `knowledge/` (read-only access to knowledge)

## Branch Activation

You **must** activate a branch before working. Use one of:

| Command | Action |
|---------|--------|
| `/switch-knowledge` | Activate Knowledge branch — documentation work |
| `/switch-scaffold` | Activate Scaffold branch — code scaffolding work |

If no branch is active, prompt the user:

```
No branch is active. Which branch do you want to work in?
  → /switch-knowledge — create/update SDLC documentation
  → /switch-scaffold — generate project scaffolding from documentation
```

## Isolation Rules

1. Each branch has its own `AGENTS.md`, skills, and CLI tools.
2. Write access is branch-scoped. The active branch is recorded in `.claude/.branch_lock`.
3. **PreToolUse hooks** enforce write isolation — writing to the other branch is blocked.
4. Both branches can **read** the other's files freely.
5. Skills do **not** cross branch boundaries (except `/switch-knowledge` and `/switch-scaffold`).
6. Agents must **never** modify the other branch's documents, skills, or configuration.

## Quick Reference

- Knowledge CLI: `python3 knowledge/sdlc_chain/cli.py <command> [args]`
- Scaffold CLI: `python3 scaffold/build_chain/cli.py <command> [args]`
- Branch lock file: `.claude/.branch_lock` (contains `knowledge` or `scaffold`)
