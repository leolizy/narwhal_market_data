---
name: scaffold-tests
description: "Generate test harness stubs from UT and NFTS knowledge artifacts."
---

# Scaffold Tests

## Purpose

Generate unit test file stubs and performance test scaffolds based on the
Unit Test Specification (UT) and Non-Functional Test Spec (NFTS) knowledge
artifacts.

## Environment

- **Base directory:** `.`
- **Knowledge artifacts (read-only):**
  - `knowledge/artifact/80_test/` (UT, NFRAR)
  - `knowledge/artifact/70_nf_implementation/` (NFTS)
- **Output directories:** `scaffold/tests/unit/`, `scaffold/tests/performance/`

## Prerequisites

- UT artifact for unit test stubs
- NFTS artifact for performance test scaffolds
- At least one of UT or NFTS is required

## Workflow

### Step 1 — Read UT artifact(s)

Find and read UT artifact JSON. Extract:
- `sections.test_cases` — test case definitions with expected behaviors
- `sections.test_fixtures` — setup/teardown requirements
- `sections.coverage_targets` — minimum coverage thresholds

### Step 2 — Read NFTS artifact (if exists)

Find and read NFTS artifact. Extract:
- `sections.performance_scenarios` — load test scenarios
- `sections.benchmarks` — response time, throughput targets
- `sections.stress_tests` — stress test parameters

### Step 3 — Propose test files

```
scaffold/tests/unit/
├── test_[module_a].py        # Unit tests per module
├── test_[module_b].py
├── conftest.py               # Shared fixtures
└── __init__.py

scaffold/tests/performance/
├── load_[scenario_a].py      # Load test per scenario
├── load_[scenario_b].py
└── config.yml                # Performance test configuration
```

Present each file with test case count and coverage mapping.

### Step 4 — Get confirmation and write

Generate each file with traceability headers. Unit test stubs include:
- Test function with descriptive name from UT test case
- Docstring referencing the test case ID and requirement
- `assert` placeholder or `pytest.skip("Not implemented")`

### Step 5 — Report

Show created files, test case counts, and coverage mapping.

## Rules

1. Never write outside `scaffold/`.
2. Always include traceability headers.
3. Match test framework to HLD technology stack (pytest, Jest, Go test, etc.).
4. Every UT test case must have a corresponding test stub.
5. Every NFTS scenario must have a corresponding load test stub.
6. Always get user confirmation before writing.
7. All test stubs start as skipped/placeholder — never mark as passing.
