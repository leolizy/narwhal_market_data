# UT-0001: Unit Test Document — Policy & Governance

## Document Overview

The Unit Test Document (UT) is a structured record that defines, tracks, and reports unit-level test coverage for a
single testable function or method. It serves as the lowest-granularity testing artifact in the SDLC documentation
hierarchy, sitting beneath the Test Plan (TP) and alongside the Test Case Document (TC).

Within the SDLC, the UT document fulfills three roles. First, it provides traceability from individual function behavior
back to functional requirements. Second, it serves as a communication bridge between developers who author unit tests
and QA engineers who validate coverage completeness. Third, it creates an auditable record of what was tested, how, and
with what results — supporting both code review processes and regression analysis.

The UT document sits in the document hierarchy as follows:

```
Test Plan (TP)
  └── Test Case Document (TC)  — per feature/module
        └── Unit Test Document (UT) — per function/method

```

## Document Dependencies

### Upstream Documents (Dependencies)

- AEC-0001, API-0001, DBC-0001, DC-0001

### Downstream Documents (Depend on This)

- MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming & ID Convention

**ID Format:** `UT-[NNNN]`

The prefix `UT` stands for "Unit Test." The four-digit sequential number is assigned per project or per module,
depending on the organization's preference.

**Examples:** UT-0001, UT-0042, UT-0310

**Test Case IDs within a UT document** follow the pattern `UT-[NNNN]-TC[NN]`, allowing each test case to be uniquely
identifiable across the entire test suite. For example, the third test case in UT-0001 would be `UT-0001-TC03`.

**File Naming Convention:**

```
UT-[NNNN]_[FunctionName]_v[X.Y].[ext]

```

Examples:
- `UT-0001_calculateDiscount_v1.0.yaml`
- `UT-0001_calculateDiscount_v1.0.md`

**Version Numbering:** Semantic Major.Minor format.
- **Major** increment: Structural changes (new test cases added, test cases removed, preconditions changed).
- **Minor** increment: Content updates within existing structure (updated expected values, corrected test data, added
  notes).

## Scope & Granularity

One UT document covers exactly **one testable unit** — a single function or method. This is the atomic level of testing
documentation.

**When to create a new UT document:**
- A new function is written that contains non-trivial logic (conditionals, calculations, transformations, side effects).
- An existing function is significantly refactored such that its behavior contract changes.

**When to update an existing UT document (rather than create a new one):**
- The function's internal implementation changes but its external contract (inputs, outputs, side effects) remains the
  same.
- New edge cases are discovered that require additional test cases.
- Defects reveal missing test coverage.

**When a UT document is NOT required:**
- Trivial getters/setters with no logic.
- Auto-generated code (unless it contains custom logic).
- Functions that are purely delegation (pass-through calls with no transformation).

**Relationship to parent documents:**
- A UT document should reference its parent TC document (if one exists) or the relevant FRD/LLD requirement IDs.
- Multiple UT documents for functions within the same module can be grouped under a single TC document.

## Section-by-Section Explanation

### Metadata

**Purpose:** Provide identification, ownership, and lifecycle tracking for the document.

**What to include:** Document ID, title (should include the function name), version, status, classification level,
dates, author/reviewer/approver names, and cross-references to related documents (FRD, LLD, TC).

**What NOT to include:** Test results (those go in Section 6). Do not put implementation details in metadata.

**Required:** Yes.

### Unit Under Test

**Purpose:** Precisely identify what is being tested so there is zero ambiguity.

**What to include:** The function name, the class or module it belongs to, its full signature (parameters and return
type), a one-sentence purpose statement, the source file path, and a version reference (git commit hash or branch).

**What NOT to include:** The full source code of the function. This document references the function, it does not
duplicate it.

**Example:**
- Function Name: `calculateDiscount`
- Module/Class: `pricing.DiscountEngine`
- Signature: `calculateDiscount(price: float, customerTier: str) -> float`
- Purpose: "Applies a tier-based percentage discount to the given price and returns the discounted amount."

**Required:** Yes.

### Dependencies & Test Environment

**Purpose:** Make explicit every external dependency the function has, and document how each will be handled during
testing. This is critical for test isolation and reproducibility.

**What to include:** For each dependency — its name, whether it is direct (called by the function) or indirect (called
by something the function calls), the handling strategy (mocked, stubbed, faked, or used as real), and a justification
for that choice. Also include the test framework, runtime version, OS, and any special configuration (environment
variables, feature flags).

**What NOT to include:** Dependencies of other functions not under test. Infrastructure-level dependencies that are
handled by the CI/CD pipeline rather than the test code.

**Required:** Yes.

### Preconditions

**Purpose:** Define the state that must exist before any test case can execute. This ensures test reproducibility and
prevents false failures due to missing setup.

**What to include:** Each precondition as a statement of required state, paired with the setup method (fixture, mock,
database seed, etc.).

**What NOT to include:** Test-case-specific setup. Preconditions here apply to ALL test cases in the document.
Case-specific setup goes in the Arrange section of each test case.

**Required:** Yes.

### Test Cases

**Purpose:** The core of the document. Each test case verifies one specific behavior of the unit under test.

**What to include:** A unique test case ID, descriptive title, category (happy path, edge case, boundary, negative,
error handling), priority, description of what is being verified, traceability to a requirement, and the full
Arrange-Act-Assert structure.

**What NOT to include:** Multiple behaviors in a single test case. Each test case must test exactly one thing. If you
find yourself writing "and" in a test case title, split it.

**Categories explained:**
- **Happy Path:** The function receives valid, typical inputs and produces the expected output.
- **Edge Case:** Unusual but valid inputs (empty strings, single-element lists, maximum values).
- **Boundary:** Values at exact boundaries (0, max int, threshold values).
- **Negative:** Invalid inputs that should be rejected or handled gracefully.
- **Error Handling:** Scenarios where the function should raise exceptions or return error indicators.

**Required:** Yes. At minimum, one happy path and one negative/error handling test case.

### Coverage Requirements

**Purpose:** Set measurable targets for how thoroughly the unit is tested.

**What to include:** Line coverage target, branch coverage target, optionally mutation score target, the coverage
measurement tool, and any lines explicitly excluded from coverage with justification.

**What NOT to include:** Coverage results (those go in Section 6). This section defines targets, not outcomes.

**Example targets:** Line coverage 90%, Branch coverage 85%.

**Required:** Yes.

### Execution Results

**Purpose:** Record the outcome of running the test cases. This section transforms the document from a test design
artifact into a test evidence artifact.

**What to include:** Execution date, who or what ran the tests (person or CI pipeline), environment,
pass/fail/skip/blocked counts, execution time, details of any failures (actual result, linked defect ID, root cause),
and coverage achieved.

**What NOT to include:** Historical results from previous runs (those are tracked via the Change Log). This section
reflects the most recent execution only.

**Required:** No (optional until tests are executed; required once execution occurs).

### Risks & Assumptions

**Purpose:** Document anything that limits test validity or areas where coverage may be insufficient.

**What to include:** Risks such as "mocked database may not reflect production behavior" with mitigations, and
assumptions such as "input validation is handled by the caller."

**What NOT to include:** Project-level risks. Keep this focused on testing risks for this specific function.

**Required:** No (optional, but strongly recommended for functions with complex dependencies or shared state).

### Attachments

**Purpose:** Link to supporting files that complement the document.

**What to include:** Test data files, mock configuration files, coverage reports, screenshots of coverage tool output.

**What NOT to include:** The source code itself or unrelated project files.

**Required:** No.

### Change Log

**Purpose:** Maintain a history of all modifications to this document.

**What to include:** Version number, date, author, and a summary of what changed.

**Required:** Yes.

## Update Triggers

### Creation Triggers

- A new function with non-trivial logic is implemented and ready for unit testing.
- An existing function is refactored to the point where its behavior contract changes (new parameters, different return
  type, changed side effects).
- A defect post-mortem identifies a function that lacked any unit test documentation.

### Update Triggers

- A new test case is added (e.g., discovered edge case, new requirement mapped to this function).
- Test data or expected results change due to a requirement update.
- A dependency handling strategy changes (e.g., switching from mocked to real database).
- Execution results are recorded after a test run.
- A defect reveals missing coverage, prompting additional test cases.

### Review Triggers

- Prior to each major release, all UT documents for modified functions should be re-reviewed.
- When the function's parent module undergoes a design review.
- When a test failure pattern suggests the test design may be flawed.

### Retirement Triggers

- The function under test is deleted or deprecated.
- The function is merged into another function (the UT document for the surviving function should be updated instead).
- The function is moved to a different module and a new UT document is created for it in the new context.

## Roles & Responsibilities

| Role       | Responsibility                                                                 |
|------------|--------------------------------------------------------------------------------|
| **Author** | Developer who implements the function or the designated test author. Responsible for writing and maintaining the UT document alongside the test code. |
| **Reviewer** | A peer developer or QA engineer who reviews the document for completeness, correctness of test design, and adequate coverage. |
| **Approver** | Tech lead, QA lead, or designated approver who signs off that the unit test documentation meets team standards. |
| **Maintainer** | The current code owner of the function. Accountable for keeping the UT document in sync when the function changes. |

## Quality Checklist

Before submitting the UT document for review, verify the following:

- [ ] Document ID follows the `UT-[NNNN]` naming convention
- [ ] Unit Under Test section fully identifies the function (name, module, signature, purpose, source file)
- [ ] All dependencies are listed with handling strategy and justification
- [ ] Preconditions are documented and setup methods specified
- [ ] At least one Happy Path test case exists
- [ ] At least one Negative or Error Handling test case exists
- [ ] All test cases follow Arrange-Act-Assert structure
- [ ] Each test case has a unique ID following `UT-[NNNN]-TC[NN]` format
- [ ] Each test case is linked to a requirement (where applicable)
- [ ] Coverage targets are defined
- [ ] Related documents (FRD, LLD, TC) are cross-referenced
- [ ] Change Log is updated with current version entry
- [ ] Document has been reviewed by at least one peer
