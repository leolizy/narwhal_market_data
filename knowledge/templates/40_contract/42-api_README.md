# API-0001: API Contract Policy — OpenAPI Framework

## Purpose

This document defines the policy, structure, and governance for API contracts under the SDLC documentation framework.
Each API endpoint is treated as **one contract**. All contracts belonging to the same **Functional Requirements Document
(FRD)** are aggregated into a **single OpenAPI specification file**.

---

## Document Dependencies

### Upstream Documents (Dependencies)

- PSD-0001

### Downstream Documents (Depend on This)

- UT-0001, MVP-0001, RTM-0001

### Impact of Changes

- Changes to this document may impact downstream requirements, design, testing, and project delivery activities.

## Naming Convention

| Artifact | Format | Example |
|---|---|---|
| Aggregated Contract File | `<FRD-ID>_<domain>_api_contract.yaml` | `FRD-2024-001_order-management_api_contract.yaml` |
| Individual API Contract | Path + OperationId inside the aggregated file | `GET /orders/{orderId}` → `getOrderById` |
| Version Tag | Semantic Versioning (`MAJOR.MINOR.PATCH`) | `1.2.0` |

---

## Aggregation Rule

- **1 FRD → 1 Aggregated OpenAPI YAML file**
- Each `path + method` combination inside the file = 1 API contract
- Cross-FRD shared schemas go into a `_shared_schemas.yaml` referenced via `$ref`

---

## Contract Sections (per API)

Each API contract (path + method) MUST include:

| Section | Required | Description |
|---|---|---|
| `operationId` | ✅ | Unique identifier across the entire spec |
| `summary` | ✅ | One-line purpose |
| `description` | ✅ | Detailed behaviour, business rules, FRD traceability |
| `tags` | ✅ | Domain grouping (maps to FRD module) |
| `parameters` | Conditional | Path, query, header params with full schema |
| `requestBody` | Conditional | For POST/PUT/PATCH with schema + examples |
| `responses` | ✅ | All expected HTTP status codes with schema |
| `x-frd-reference` | ✅ | Custom extension linking to FRD ID + section |
| `x-contract-owner` | ✅ | Team / individual accountable |
| `x-sla` | Recommended | Latency, throughput, availability targets |
| `security` | ✅ | Auth scheme(s) applicable |

---

## Versioning & Change Triggers

| Change Type | Version Bump | Approval |
|---|---|---|
| New field (additive, optional) | MINOR | Contract Owner |
| Breaking change (remove field, rename, type change) | MAJOR | Architecture Review Board |
| Bug fix / description correction | PATCH | Contract Owner |
| New API added to existing FRD | MINOR | Contract Owner + FRD Author |

---

## Governance

- Contracts MUST be reviewed via PR before merge.
- Breaking changes require a **deprecation notice** (min 2 sprint cycles).
- All contracts MUST pass OpenAPI linting (`spectral` ruleset enforced in CI).
- Consumer teams MUST be notified of MAJOR version changes.

---

## Directory Structure

```
api-contracts/
├── API_CONTRACT_POLICY.md          # This policy
├── _shared_schemas.yaml            # Cross-FRD reusable schemas
├── FRD-2024-001_order-management_api_contract.yaml
├── FRD-2024-002_user-management_api_contract.yaml
└── ...

```
