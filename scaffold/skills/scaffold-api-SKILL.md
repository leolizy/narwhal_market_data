---
name: scaffold-api
description: "Generate API route stubs and event handler scaffolds from API and AEC knowledge artifacts."
---

# Scaffold API & Events

## Purpose

Generate API server route stubs, request/response types, and async event
handler scaffolds based on the API Specification and Async Event Contract
knowledge artifacts.

## Environment

- **Base directory:** `.`
- **Knowledge artifacts (read-only):**
  - `knowledge/artifact/40_contract/` (API, AEC)
- **Output directories:** `scaffold/src/api/`, `scaffold/src/events/`

## Prerequisites

- API artifact must exist for route generation
- AEC artifact must exist for event handler generation
- At least one of API or AEC is required

## Workflow

### Step 1 — Read API artifact

Find and read the API artifact JSON. For OpenAPI-style docs, extract:
- `paths` — API endpoints, methods, parameters
- `components.schemas` — request/response type definitions
- `security` — authentication mechanisms
- `info` — API version, base path

### Step 2 — Read AEC artifact(s) (if exist)

Find and read AEC artifacts. Extract:
- `sections.event_definitions` — event types, schemas, triggers
- `sections.message_formats` — payload structures
- `sections.channels` — queues, topics, exchanges
- `sections.consumer_contracts` — handler requirements

### Step 3 — Propose API stubs

```
scaffold/src/api/
├── routes/
│   ├── [resource_a].py       # Route handlers per API path group
│   └── [resource_b].py
├── schemas/
│   ├── [schema_a].py         # Request/response types from components
│   └── [schema_b].py
├── middleware/
│   └── auth.py               # Auth middleware from security spec
└── __init__.py

scaffold/src/events/
├── handlers/
│   ├── [event_a]_handler.py  # Event handler stubs from AEC
│   └── [event_b]_handler.py
├── schemas/
│   └── [event]_schema.py     # Message schemas from AEC
└── __init__.py
```

Present each file with its source endpoint/event and brief description.

### Step 4 — Get confirmation and write

Generate each file with traceability headers. Route stubs include:
- Function signature with typed parameters
- Docstring referencing the API path and method
- Placeholder return with correct response type

### Step 5 — Report

Show created files, endpoint counts, and recommended next steps.

## Rules

1. Never write outside `scaffold/`.
2. Always include traceability headers.
3. Match framework to HLD technology stack (FastAPI, Express, Gin, etc.).
4. Route stubs must cover every path in the API artifact.
5. Event handlers must cover every event type in AEC artifact.
6. Always get user confirmation before writing.
7. Do not implement business logic — stubs only with correct types.
