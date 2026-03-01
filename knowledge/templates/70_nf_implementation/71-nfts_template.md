# Non-Functional Test Specification (NFTS)

| Field             | Value                                                                 |
|-------------------|-----------------------------------------------------------------------|
| Document ID       | NFTS-[NNNN]                                                          |
| Title             |                                                                       |
| Version           |                                                                       |
| Status            | Draft / In Review / Approved / Superseded / Retired                  |
| Classification    | Public / Internal / Confidential / Restricted                        |
| Created Date      |                                                                       |
| Last Updated      |                                                                       |
| Author            |                                                                       |
| Reviewer          |                                                                       |
| Approver          |                                                                       |
| NFR Reference     |                                                                       |
| Test Plan Ref     |                                                                       |
| SRS / FRD Ref     |                                                                       |
| HLD Ref           |                                                                       |

---

## 1. Introduction

### 1.1 Purpose

> **Guidance:** Briefly describe the goal of this NFTS and the system or component it covers. State what decisions this
document supports (e.g., NFT sign-off, go/no-go decision) and its relationship to the parent Test Plan.

[Content here]

---

### 1.2 System Under Test

> **Guidance:** Identify the application, service, or component being tested. Include version, release, environment
details, and any component boundaries. Specify what is explicitly excluded from NFT scope.

| Attribute         | Details                     |
|-------------------|-----------------------------|
| System / Service  |                             |
| Release Version   |                             |
| Component Scope   |                             |
| Excluded Items    |                             |

---

### 1.3 Scope of Non-Functional Testing

> **Guidance:** Enumerate the non-functional quality attributes that are **in scope** for this specification. Explicitly
state what is **out of scope** to avoid ambiguity. Use ISO 25010 quality attributes as a reference (Performance
Efficiency, Security, Reliability, Usability, Compatibility, Maintainability, Portability).

**In Scope:**

| # | Quality Attribute          | Rationale                        |
|---|----------------------------|----------------------------------|
| 1 |                            |                                  |
| 2 |                            |                                  |

**Out of Scope:**

| # | Quality Attribute / Area   | Reason Excluded                  |
|---|----------------------------|----------------------------------|
| 1 |                            |                                  |

---

### 1.4 Definitions and Acronyms

> **Guidance:** Define all technical terms, metrics units, and acronyms used in this document. Include NFT-specific
terms such as TPS, P95, RTO, RPO, MTTR, MTBF.

| Term / Acronym    | Definition                                                            |
|-------------------|-----------------------------------------------------------------------|
| TPS               | Transactions Per Second                                               |
| P95               | 95th Percentile Response Time                                        |
| RTO               | Recovery Time Objective                                               |
| RPO               | Recovery Point Objective                                              |
| MTTR              | Mean Time to Recovery                                                 |
| MTBF              | Mean Time Between Failures                                            |
|                   |                                                                       |

---

## 2. References

> **Guidance:** List all documents, standards, and frameworks that inform this NFTS. Every NFR referenced in test
acceptance criteria must be traceable to a document listed here.

| Document ID   | Title                                | Version | Location / Link |
|---------------|--------------------------------------|---------|-----------------|
|               | Non-Functional Requirements (NFR)   |         |                 |
|               | Test Plan (TP)                       |         |                 |
|               | SRS / FRD                            |         |                 |
|               | HLD / Architecture Document          |         |                 |
|               | ISO/IEC/IEEE 29119-3 (Test Documentation) |    |                 |
|               | ISO 25010 (Software Quality Model)   |         |                 |
|               | OWASP Top 10                         |         |                 |

---

## 3. Test Strategy

### 3.1 Overall Approach

> **Guidance:** Describe the overarching NFT approach — tool-driven vs manual, dedicated environment vs shared,
continuous vs milestone-based testing. Include the philosophy behind test prioritisation (risk-based,
NFR-criticality-based, etc.).

[Content here]

---

### 3.2 Test Types Included

> **Guidance:** List all non-functional test types and their execution status for this cycle. Include rationale for any
test types marked as Deferred or Not Applicable.

| Test Type                     | Status                           | Rationale / Notes          |
|-------------------------------|----------------------------------|----------------------------|
| Performance (Baseline)        | Active / Deferred / N/A          |                            |
| Load Testing                  | Active / Deferred / N/A          |                            |
| Stress Testing                | Active / Deferred / N/A          |                            |
| Endurance / Soak Testing      | Active / Deferred / N/A          |                            |
| Spike Testing                 | Active / Deferred / N/A          |                            |
| Security Testing              | Active / Deferred / N/A          |                            |
| Reliability & Availability    | Active / Deferred / N/A          |                            |
| Scalability Testing           | Active / Deferred / N/A          |                            |
| Usability Testing             | Active / Deferred / N/A          |                            |
| Compatibility Testing         | Active / Deferred / N/A          |                            |
| Maintainability Testing       | Active / Deferred / N/A          |                            |
| Disaster Recovery Testing     | Active / Deferred / N/A          |                            |

---

### 3.3 NFT Execution Sequence

> **Guidance:** Define the recommended execution order. Note dependencies — for example, a performance baseline must be
established before stress testing, and security scanning should occur before load testing to avoid false positives.

```
[Baseline] → [Load] → [Stress] → [Soak] → [Spike]
[Security Scan (SAST)] → [Security Test (DAST)] → parallel with load testing if safe
[Reliability / Failover] → [DR Testing]

```

[Describe dependencies and sequencing rationale here]

---

## 4. Entry and Exit Criteria

### 4.1 Entry Criteria

> **Guidance:** All conditions below must be satisfied before NFT execution commences. If entry criteria cannot be met,
the NFT lead must formally escalate with documented risk acceptance.

| # | Criterion                                                              | Owner         | Status      |
|---|------------------------------------------------------------------------|---------------|-------------|
| 1 | Functional regression test pass rate ≥ 95%                            |               |             |
| 2 | NFT environment provisioned and verified against spec                  |               |             |
| 3 | Test data loaded to required volumes                                   |               |             |
| 4 | NFR acceptance criteria formally agreed with stakeholders              |               |             |
| 5 | Test tools licensed, configured, and smoke-tested                      |               |             |
| 6 | Monitoring and alerting active in NFT environment                      |               |             |
|   |                                                                        |               |             |

---

### 4.2 Exit Criteria

> **Guidance:** All conditions below must be met for NFT to be declared complete. Any criterion not met must be formally
risk-accepted by the approver.

| # | Criterion                                                              | Owner         | Status      |
|---|------------------------------------------------------------------------|---------------|-------------|
| 1 | All P1/P2 performance NFRs met within agreed thresholds               |               |             |
| 2 | Zero Critical and High security vulnerabilities unresolved             |               |             |
| 3 | All P1 NFT defects resolved or risk-accepted with documented approval  |               |             |
| 4 | Final NFT Report reviewed and approved                                 |               |             |
| 5 | Sign-off obtained from Test Manager and relevant stakeholders          |               |             |
|   |                                                                        |               |             |

---

### 4.3 Suspension Criteria *(Optional)*

> **Guidance:** Define conditions that warrant pausing NFT execution (e.g., critical production incident, environment
failure affecting > 50% of test scenarios).

[Content here]

---

### 4.4 Resumption Criteria *(Optional)*

> **Guidance:** Define conditions that must be satisfied before NFT execution resumes after suspension.

[Content here]

---

## 5. Test Environment

### 5.1 Environment Overview

> **Guidance:** Identify the environment by name and type. All NFT results are only valid for the environment documented
in this section. Any deviation must be flagged.

| Attribute                | Details                                              |
|--------------------------|------------------------------------------------------|
| Environment Name         |                                                      |
| Environment Type         | Dedicated / Shared / Cloud-Provisioned / On-Premise  |
| Environment Owner        |                                                      |
| Managed By               |                                                      |

---

### 5.2 Hardware Specifications

> **Guidance:** Document the server/VM specifications for all nodes in the NFT environment. Include CPU, RAM, storage,
and network bandwidth.

| Role                  | CPU     | RAM     | Storage | OS      | Count |
|-----------------------|---------|---------|---------|---------|-------|
| Application Server    |         |         |         |         |       |
| Database Server       |         |         |         |         |       |
| Load Balancer         |         |         |         |         |       |
| Cache Layer           |         |         |         |         |       |
| Load Generator        |         |         |         |         |       |

---

### 5.3 Software and Middleware

> **Guidance:** List all software components and middleware versions in the test environment. Version mismatches with
production must be documented as known risks.

| Component             | Version         | Configuration Notes          |
|-----------------------|-----------------|------------------------------|
|                       |                 |                              |

---

### 5.4 Network Topology

> **Guidance:** Describe the network configuration — bandwidth, latency constraints, firewalls, proxies, load balancers,
and CDN configuration relevant to NFT.

[Content here — include topology diagram reference if available]

---

### 5.5 Test Tools

> **Guidance:** List all tools used for test execution, monitoring, and analysis. Include licensing status and version.

| Tool                  | Purpose                             | Version | License Status |
|-----------------------|-------------------------------------|---------|----------------|
|                       | Load & Performance Test Execution   |         |                |
|                       | Real-time Monitoring & Metrics      |         |                |
|                       | Security Scanning (DAST)            |         |                |
|                       | Security Scanning (SAST)            |         |                |
|                       | Defect Tracking                     |         |                |
|                       | Test Results Dashboard              |         |                |

---

### 5.6 Known Differences from Production

> **Guidance:** Document every known difference between the NFT environment and production. This is critical for
accurately interpreting and contextualising test results.

| Attribute             | NFT Environment        | Production              | Impact on Results       |
|-----------------------|------------------------|-------------------------|-------------------------|
|                       |                        |                         |                         |

---

## 6. Test Data Requirements

### 6.1 Data Volume Requirements

> **Guidance:** Specify minimum record counts per entity required to simulate realistic production conditions.
Under-seeded data is a leading cause of misleading performance results.

| Entity / Table        | Minimum Record Count   | Rationale                |
|-----------------------|------------------------|--------------------------|
|                       |                        |                          |

---

### 6.2 Data Generation Approach

> **Guidance:** Describe how test data will be created — production anonymization, synthetic generation, or seeded
datasets. Note PII handling and compliance requirements (e.g., GDPR, PDPA).

[Content here]

---

### 6.3 Data Reset Strategy

> **Guidance:** Define how data will be reset between test runs to ensure repeatability and prevent test pollution.

[Content here]

---

## 7. Performance Testing Specification

### 7.1 Baseline Metrics

> **Guidance:** Document current or expected baseline performance metrics. If no baseline exists, note that baseline
establishment is an explicit objective of the first test run.

| Metric                           | Baseline Value         | Source / Date             |
|----------------------------------|------------------------|---------------------------|
| Average Response Time (ms)       |                        |                           |
| P95 Response Time (ms)           |                        |                           |
| P99 Response Time (ms)           |                        |                           |
| Throughput (TPS)                 |                        |                           |
| Error Rate (%)                   |                        |                           |

---

### 7.2 Workload Models

> **Guidance:** Define the user and transaction workload for each test scenario. A workload model specifies concurrent
users, transaction mix, ramp-up/sustain/ramp-down durations, and think time.

| Workload ID | Scenario Name              | Concurrent Users | Transaction Mix (%)       | Ramp-Up (min) | Sustain (min) | Think Time (sec) |
|-------------|----------------------------|------------------|---------------------------|---------------|---------------|------------------|
| WL-001      |                            |                  |                           |               |               |                  |
| WL-002      |                            |                  |                           |               |               |                  |

---

### 7.3 Performance Test Scenarios

> **Guidance:** Document each test scenario with full acceptance criteria traceable to the NFR document. Every metric
threshold must have an NFR reference — thresholds without an NFR source are assumptions and must be flagged.

| Scenario ID | Test Type     | Workload Ref | NFR Ref | Avg RT (ms) | P95 RT (ms) | P99 RT (ms) | Error Rate (%) | Throughput (TPS) | CPU (%) | Memory (%) | Priority |
|-------------|---------------|--------------|---------|-------------|-------------|-------------|----------------|------------------|---------|------------|----------|
| PERF-001    | Baseline      |              |         |             |             |             |                |                  |         |            | P1       |
| PERF-002    | Load Test     |              |         |             |             |             |                |                  |         |            | P1       |
| PERF-003    | Stress Test   |              |         |             |             |             |                |                  |         |            | P1       |
| PERF-004    | Soak Test     |              |         |             |             |             |                |                  |         |            | P2       |
| PERF-005    | Spike Test    |              |         |             |             |             |                |                  |         |            | P2       |

---

### 7.4 Monitoring Metrics

> **Guidance:** Define the metrics that must be collected during performance test execution. Missing monitoring data
invalidates test results.

**Server-Level Metrics:** CPU utilization (%), Memory utilization (%), Disk I/O (MB/s), Network I/O (MB/s), Swap usage
(%)

**Application-Level Metrics:** Active thread count, Connection pool utilization, Garbage collection frequency and pause
time, Error log rate

**Database-Level Metrics:** Query execution time (avg / P95), Lock wait count, Active connection count, Cache hit ratio

---

## 8. Security Testing Specification

### 8.1 Security Framework References

> **Guidance:** List the security standards governing this testing scope. Common references include OWASP Top 10, OWASP
ASVS (Application Security Verification Standard), PCI-DSS, and ISO 27001.

| Standard / Framework              | Version / Year    | Applicability                 |
|-----------------------------------|-------------------|-------------------------------|
| OWASP Top 10                      |                   |                               |
| OWASP ASVS                        |                   | Level: 1 / 2 / 3              |
|                                   |                   |                               |

---

### 8.2 Threat Model Reference *(Optional)*

> **Guidance:** Reference the threat model document if one exists. If no threat model exists, note that risk-based test
selection is based on OWASP Top 10 default priorities.

[Content here]

---

### 8.3 Security Test Scenarios

> **Guidance:** List security test scenarios by OWASP/ASVS category. Specify the test methodology (SAST, DAST, manual
penetration testing, code review) and tool for each scenario.

| Scenario ID | Category                    | Description                  | Methodology     | Tool  | NFR Ref | Acceptance Criteria              | Priority |
|-------------|-----------------------------|------------------------------ |-----------------|-------|---------|----------------------------------|----------|
| SEC-001     | Authentication              |                              | DAST            |       |         |                                  | P1       |
| SEC-002     | Authorization               |                              | Manual          |       |         |                                  | P1       |
| SEC-003     | Injection (SQL/XSS)         |                              | DAST + SAST     |       |         |                                  | P1       |
| SEC-004     | Sensitive Data Exposure     |                              | DAST            |       |         |                                  | P1       |
| SEC-005     | Security Misconfiguration   |                              | SAST + Manual   |       |         |                                  | P2       |
| SEC-006     | Session Management          |                              | Manual          |       |         |                                  | P2       |
| SEC-007     | Logging & Monitoring        |                              | Manual          |       |         |                                  | P2       |

---

### 8.4 Vulnerability Acceptance Thresholds

> **Guidance:** Define the maximum tolerable open vulnerabilities by severity at exit. Critical vulnerabilities must
always be zero at exit gate.

| Severity    | Max Open at Exit | Notes                                            |
|-------------|------------------|--------------------------------------------------|
| Critical    | 0                | Zero tolerance — test cannot exit with any open  |
| High        | 0                | Must be resolved or formally risk-accepted       |
| Medium      |                  |                                                  |
| Low         |                  |                                                  |

---

## 9. Reliability and Availability Testing Specification

### 9.1 Availability Targets

> **Guidance:** Define agreed availability and recovery targets from NFR / SLA documents. All thresholds must be
traceable to an NFR entry.

| Metric                                      | Target Value   | NFR Reference |
|---------------------------------------------|----------------|---------------|
| Target Uptime (%)                           |                |               |
| Max Planned Downtime (hrs/month)            |                |               |
| Max Unplanned Downtime per Incident (min)   |                |               |
| Recovery Time Objective (RTO) (min)         |                |               |
| Recovery Point Objective (RPO) (min)        |                |               |
| MTBF (Mean Time Between Failures)           |                |               |
| MTTR (Mean Time to Recovery)                |                |               |

---

### 9.2 Reliability Test Scenarios

> **Guidance:** Define failure injection and recovery scenarios. Include method of failure injection (process kill,
network partition, node shutdown, database outage) and expected system behavior.

| Scenario ID | Test Type             | Failure Injection Method           | Expected Behavior                    | Acceptance Criteria        | NFR Ref | Priority |
|-------------|------------------------|-----------------------------------|--------------------------------------|----------------------------|---------|----------|
| REL-001     | Failover               |                                   |                                      |                            |         | P1       |
| REL-002     | Recovery               |                                   |                                      |                            |         | P1       |
| REL-003     | Data Integrity         |                                   |                                      |                            |         | P1       |
| REL-004     | Disaster Recovery      |                                   |                                      |                            |         | P2       |
| REL-005     | Chaos Engineering      |                                   |                                      |                            |         | P2       |

---

## 10. Scalability Testing Specification *(Optional)*

### 10.1 Scalability Objectives

> **Guidance:** Describe the scaling behavior expected (horizontal, vertical, auto-scale) and what the tests aim to
validate — e.g., linear scaling up to N nodes, auto-scale trigger latency, degradation curve under over-capacity load.

[Content here]

---

### 10.2 Scalability Test Scenarios

> **Guidance:** Define step-load scenarios with increasing concurrency levels to identify the scaling breakpoint and
degradation profile.

| Scenario ID | Description              | Scaling Type          | Load Steps (Concurrent Users)    | Acceptance Criteria        | NFR Ref |
|-------------|--------------------------|------------------------|----------------------------------|----------------------------|---------|
| SCALE-001   |                          | Horizontal             |                                  |                            |         |
| SCALE-002   |                          | Auto-Scale             |                                  |                            |         |

---

## 11. Usability Testing Specification *(Optional)*

### 11.1 Accessibility Standard

> **Guidance:** State the accessibility compliance target (e.g., WCAG 2.1 Level AA). This governs automated and manual
accessibility test criteria.

Accessibility Standard: ______________________

---

### 11.2 Usability Test Scenarios

> **Guidance:** Define usability tasks with participant profiles and measurable success criteria. Avoid subjective
acceptance criteria — use task completion rate, error rate, and time-on-task.

| Scenario ID | Task Description             | Participant Profile   | Success Metric                    | NFR Ref |
|-------------|------------------------------|------------------------|-----------------------------------|---------|
| USA-001     |                              |                        | Task completion rate ≥ 90%        |         |
| USA-002     |                              |                        |                                   |         |

---

## 12. Compatibility Testing Specification *(Optional)*

### 12.1 Browser Compatibility

> **Guidance:** List the browsers and versions to be tested. Use "latest-N" notation where N = number of versions behind
current.

| Browser       | Version(s)    | Priority  |
|---------------|---------------|-----------|
| Chrome        | latest, -1    | P1        |
| Firefox       | latest, -1    | P1        |
| Safari        | latest        | P1        |
| Edge          | latest        | P2        |

---

### 12.2 Device and OS Compatibility

> **Guidance:** List device types and OS versions relevant to the user population. Prioritize by market share data.

| Device Type   | OS / Version         | Priority  |
|---------------|----------------------|-----------|
|               |                      |           |

---

### 12.3 Integration Compatibility

> **Guidance:** List external systems and APIs whose compatibility with the current release must be validated.

| External System   | API Version  | Test Method            | Acceptance Criteria   |
|-------------------|--------------|------------------------|-----------------------|
|                   |              |                        |                       |

---

## 13. Defect Management for NFT

### 13.1 NFT Severity Classification

> **Guidance:** Use NFT-specific severity definitions below. Generic functional defect severities are not appropriate
for non-functional failures — an NFT defect must describe NFR breach impact.

| Severity    | Definition                                                                          | Example                                                     |
|-------------|-------------------------------------------------------------------------------------|-------------------------------------------------------------|
| P1 Critical | SLA-breaching failure or system unavailability under target load                   | Response time > 3× SLA threshold under normal load         |
| P2 High     | Significant NFR breach but system remains partially functional                      | P95 response time exceeds SLA by 20–50%                    |
| P3 Medium   | NFR breach under edge-case conditions only                                          | Performance degrades under spike load beyond target users  |
| P4 Low      | Cosmetic / minor deviation with negligible end-user impact                          | Response time 5% above target during off-peak hours        |

---

### 13.2 Defect Tracking

| Attribute                  | Details                              |
|----------------------------|--------------------------------------|
| Defect Tracking Tool       |                                      |
| NFT Label Convention       | e.g., [NFT], [PERF], [SEC]          |
| Retest Policy              |                                      |
| Defect Review Cadence      |                                      |

---

## 14. Roles and Responsibilities

> **Guidance:** Define who is accountable for each NFT activity. Every activity must have a named owner — unassigned
responsibilities are a leading cause of NFT delays.

| Role                         | Responsibilities                                                     | Assigned To |
|------------------------------|----------------------------------------------------------------------|-------------|
| Performance Test Engineer    | Design and execute performance scripts; analyse and report results   |             |
| Security Test Engineer       | Execute SAST/DAST scans; manage vulnerability reporting              |             |
| NFT Lead / QA Lead           | Own NFT plan, coordinate execution, manage exit criteria             |             |
| Test Manager                 | Review and approve NFTS; sign off exit report                        |             |
| DevOps / Infrastructure      | Provision and maintain NFT environment; configure monitoring         |             |
| System Architect             | Validate NFT results against architecture expectations               |             |
| Project Manager              | NFT schedule management; stakeholder communication                   |             |

---

## 15. Risks and Mitigations

> **Guidance:** Document NFT-specific risks. Common sources include: environment instability, insufficient test data
volumes, production environment differences, tool licensing constraints, and tight execution windows.

| Risk ID  | Description                                  | Likelihood    | Impact        | Mitigation                        | Owner |
|----------|----------------------------------------------|---------------|---------------|-----------------------------------|-------|
| RISK-001 |                                              | High/Med/Low  | High/Med/Low  |                                   |       |
| RISK-002 |                                              |               |               |                                   |       |

---

## 16. Reporting Requirements

> **Guidance:** Define NFT reports, their frequency, audience, and format. Reports must be produced regardless of
whether results pass or fail — stakeholders need visibility throughout.

| Report Type                        | Frequency                   | Audience                          | Format                         |
|------------------------------------|-----------------------------|-----------------------------------|--------------------------------|
| NFT Execution Progress Report      | Daily during execution      | QA Lead, Project Manager          | Email / Dashboard              |
| Performance Test Results Report    | Per scenario batch          | QA Lead, Architect, DevOps        | Wiki / PDF                     |
| Security Test Summary Report       | At security scan completion | QA Lead, Security, CISO           | PDF / Secure Wiki              |
| Final NFT Completion Report        | Once — at exit gate         | All stakeholders, Sign-off chain  | Formal PDF Report              |

---

## Attachments

> **Guidance:** Reference all supporting materials — test scripts, monitoring dashboards, baseline reports, screenshots,
and evidence artifacts.

| File Name             | Description                         | Location / Link |
|-----------------------|-------------------------------------|-----------------|
|                       |                                     |                 |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0     |      |        | Initial draft |
|         |      |        |         |
