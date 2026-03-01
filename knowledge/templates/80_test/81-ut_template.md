# Unit Test Document

| Field            | Value                                                        |
|------------------|--------------------------------------------------------------|
| Document ID      | UT-[NNNN]                                                    |
| Title            |                                                              |
| Version          |                                                              |
| Status           | Draft / In Review / Approved / Superseded / Retired          |
| Classification   | Public / Internal / Confidential / Restricted                |
| Created Date     |                                                              |
| Last Updated     |                                                              |
| Author           |                                                              |
| Reviewer         |                                                              |
| Approver         |                                                              |
| Related Documents|                                                              |

---

## 1. Unit Under Test

> **Guidance:** Identify the exact function or method being tested. Include the module/class it belongs to, its
signature, and a brief description of its responsibility.

| Field              | Value                                           |
|--------------------|-------------------------------------------------|
| Function Name      |                                                 |
| Module / Class     |                                                 |
| Function Signature |                                                 |
| Purpose            |                                                 |
| Source File        |                                                 |
| Source Version     |                                                 |

---

## 2. Dependencies & Test Environment

> **Guidance:** List all dependencies the unit relies on and how they will be handled (mocked, stubbed, or used as-is).
Define the test environment configuration.

### 2.1 Dependencies

| Dependency Name | Type (Direct/Indirect) | Handling (Mocked/Stubbed/Faked/Real) | Justification |
|-----------------|------------------------|--------------------------------------|---------------|
|                 |                        |                                      |               |

### 2.2 Test Environment

| Field                  | Value                                     |
|------------------------|-------------------------------------------|
| Test Framework         |                                           |
| Runtime                |                                           |
| OS                     |                                           |
| Special Configuration  |                                           |

---

## 3. Preconditions

> **Guidance:** Define the state that must be true before any test case in this document can execute. This includes data
setup, system state, and any assumptions.

| # | Precondition | Setup Method |
|---|-------------|--------------|
| 1 |             |              |

---

## 4. Test Cases

> **Guidance:** Define individual test cases for the unit under test. Each test case should cover one specific behavior
or scenario. Follow the Arrange-Act-Assert pattern. Cover: happy path, edge cases, boundary values, error handling, and
negative scenarios.

### Test Case: [UT-NNNN-TC01] — [Title]

| Field                | Value                                                   |
|----------------------|---------------------------------------------------------|
| Test Case ID         |                                                         |
| Title                |                                                         |
| Category             | Happy Path / Edge Case / Boundary / Negative / Error Handling |
| Priority             | Critical / High / Medium / Low                          |
| Description          |                                                         |
| Linked Requirement   |                                                         |

**Arrange:**

> Set up the test data, mocks, and initial state.

| Input Parameter | Value | Description |
|-----------------|-------|-------------|
|                 |       |             |

| Mock | Configuration |
|------|---------------|
|      |               |

**Initial State:**

[Describe the starting state here]

**Act:**

> The specific function call or action being tested.

```
[e.g., result = calculateDiscount(100.0, "gold")]

```

**Assert:**

> The expected outcome and how it is verified.

| Field             | Value                                          |
|-------------------|-------------------------------------------------|
| Expected Result   |                                                 |
| Assertion Type    | Equality / Inequality / Exception / State Change / Side Effect |
| Tolerance         |                                                 |

**Postconditions:**

[Any state that should be true after the test — optional]

**Notes:**

[Additional context or clarification — optional]

---

*(Copy the test case block above for each additional test case: TC02, TC03, etc.)*

---

## 5. Coverage Requirements

> **Guidance:** Define the expected test coverage metrics for the unit under test. Specify targets and measurement
method.

| Metric                  | Target  |
|-------------------------|---------|
| Line Coverage           |         |
| Branch Coverage         |         |
| Mutation Score          |         |
| Coverage Tool           |         |

**Excluded Lines:**

| Line(s) | Justification |
|---------|---------------|
|         |               |

---

## 6. Execution Results

> **Guidance:** Record the results of test execution. This section is filled in after test runs. Include pass/fail
status, execution time, and any defects discovered.

| Field               | Value                      |
|---------------------|----------------------------|
| Last Execution Date |                            |
| Executed By         |                            |
| Environment         |                            |

### 6.1 Summary

| Metric          | Count |
|-----------------|-------|
| Total Cases     |       |
| Passed          |       |
| Failed          |       |
| Skipped         |       |
| Blocked         |       |
| Execution Time  |       |

### 6.2 Failures

| Test Case ID | Actual Result | Defect ID | Root Cause |
|-------------|---------------|-----------|------------|
|             |               |           |            |

### 6.3 Coverage Achieved

| Metric          | Achieved |
|-----------------|----------|
| Line Coverage   |          |
| Branch Coverage |          |

---

## 7. Risks & Assumptions

> **Guidance:** Document any risks to test validity and assumptions made during test design. Flag areas where testing
may be insufficient.

### Risks

| Risk | Mitigation |
|------|-----------|
|      |           |

### Assumptions

| # | Assumption |
|---|-----------|
| 1 |           |

---

## 8. Attachments

> **Guidance:** Supporting files such as test data files, mock configuration files, or coverage reports.

| Filename | Description | Location |
|----------|-------------|----------|
|          |             |          |

---

## 9. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
|         |      |        |         |
