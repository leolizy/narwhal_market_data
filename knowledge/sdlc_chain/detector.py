"""Auto-detect document type from a YAML/JSON file's structure.

All doc types use K8s-style envelope format with ``kind`` at the top
level.  Detection prefers the ``kind`` field when present, then falls
back to structure-based or prefix-based heuristics.

Detection rules (evaluated in order):
  (envelope) - kind maps to doc type via KIND_MAP
  PC    - kind == "PlatformCanon" (legacy: apiVersion + spec key)
  FRD    - document.type == "FunctionalRequirements", functional_requirements key
  NFR    - document.type == "NonFunctionalRequirements", nonfunctional_requirements key
  PSD    - metadata.document_id starts with "PSD-", function_overview.function_type
  AEC    - metadata.document_id starts with "AEC-"
  API    - top-level openapi key (OpenAPI spec) OR metadata.document_id starts with "API-"
  DC     - metadata.document_id starts with "DC-"
  DBC    - metadata.document_id starts with "DBC-"
  HLD    - metadata.document_id starts with "HLD-"
  CICD   - metadata.document_id starts with "CICD-"
  DBAD   - metadata.document_id starts with "DBAD-"
  TSI    - metadata.document_id starts with "TSI-"
  NFTS   - metadata.document_id starts with "NFTS-"
  DG     - metadata.document_id starts with "DG-"
  UT     - metadata.document_id starts with "UT-", unit_under_test key
  NFRAR  - metadata.document_id starts with "NFRAR-"
  MVP    - metadata.document_id starts with "MVP-"
  RTM    - metadata.document_id starts with "RTM-"
  DD     - metadata.document_id starts with "DD-"
"""

from __future__ import annotations

from .yaml_utils import load_yaml

# Maps K8s-style ``kind`` values to doc type codes.
KIND_MAP: dict[str, str] = {
    "PlatformCanon": "PC",
    "FunctionalRequirements": "FRD",
    "NonFunctionalRequirements": "NFR",
    "HighLevelDesign": "HLD",
    "CICDFramework": "CICD",
    "DatabaseArchitectureDesign": "DBAD",
    "TechnicalSystemIntegration": "TSI",
    "NonFunctionalTestSpec": "NFTS",
    "DeploymentGuide": "DG",
    "NFRAnalysisReport": "NFRAR",
    "MinimumViableProductPlan": "MVP",
    "RequirementsTraceabilityMatrix": "RTM",
}

_VALID_API_VERSIONS = {"sdlc/v1", "sdlc.alphlaion.com/v1"}


def detect_document_type(data: dict) -> str:
    """Detect document type from parsed YAML/JSON data.

    Returns one of: 'PC', 'FRD', 'NFR', 'PSD', 'AEC', 'API', 'MDC', 'DC', 'DBC',
                    'HLD', 'CICD', 'DBAD', 'TSI', 'NFTS', 'DG', 'UT', 'NFRAR',
                    'MVP', 'RTM', 'DD', or 'UNKNOWN'.
    """
    if not isinstance(data, dict):
        return "UNKNOWN"

    # ------------------------------------------------------------------
    # 0. K8s envelope detection (applies to ALL doc types)
    #    If kind is present and maps via KIND_MAP, use it directly.
    #    Also accepts legacy docs that include apiVersion.
    # ------------------------------------------------------------------
    kind = data.get("kind", "")
    if kind in KIND_MAP and "metadata" in data:
        return KIND_MAP[kind]

    # ------------------------------------------------------------------
    # 1. PC - Platform Canon (legacy envelope with apiVersion + spec key)
    # ------------------------------------------------------------------
    api_version = data.get("apiVersion", "")
    if (
        api_version in _VALID_API_VERSIONS
        and kind == "PlatformCanon"
        and "metadata" in data
        and "spec" in data
    ):
        return "PC"

    # ------------------------------------------------------------------
    # 2. FRD - Functional Requirements Document
    #    Required: document.type == "FunctionalRequirements"
    #              functional_requirements key present
    # ------------------------------------------------------------------
    document = data.get("document")
    if (
        isinstance(document, dict)
        and document.get("type") == "FunctionalRequirements"
        and "functional_requirements" in data
    ):
        return "FRD"

    # ------------------------------------------------------------------
    # 3. NFR - Non-Functional Requirements Document
    #    Required: document.type == "NonFunctionalRequirements"
    #              nonfunctional_requirements key present
    # ------------------------------------------------------------------
    if (
        isinstance(document, dict)
        and document.get("type") == "NonFunctionalRequirements"
        and "nonfunctional_requirements" in data
    ):
        return "NFR"

    # Get metadata once for subsequent checks
    metadata = data.get("metadata")
    doc_id = ""
    if isinstance(metadata, dict):
        doc_id = metadata.get("document_id", "")

    # ------------------------------------------------------------------
    # 4. PSD - Program/System Design
    #    Required: metadata.document_id starts with "PSD-"
    #              function_overview key with function_type sub-key
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("PSD-"):
        func_overview = data.get("function_overview")
        if isinstance(func_overview, dict) and "function_type" in func_overview:
            return "PSD"

    # ------------------------------------------------------------------
    # 5. AEC - Architecture & Engineering Checklist
    #    Required: metadata.document_id starts with "AEC-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("AEC-"):
        return "AEC"

    # ------------------------------------------------------------------
    # 6. API - OpenAPI specification or API document
    #    Required: top-level openapi key OR metadata.document_id starts with "API-"
    # ------------------------------------------------------------------
    if "openapi" in data or (isinstance(doc_id, str) and doc_id.startswith("API-")):
        return "API"

    # ------------------------------------------------------------------
    # 7a. MDC - Market Data Contract
    #     Required: metadata.document_id starts with "MDC-"
    #     Note: Must be checked BEFORE DC to avoid MDC- matching DC- prefix
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("MDC-"):
        return "MDC"

    # ------------------------------------------------------------------
    # 7. DC - Data Contracts
    #    Required: metadata.document_id starts with "DC-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("DC-"):
        return "DC"

    # ------------------------------------------------------------------
    # 8. DBC - Database Checklist
    #    Required: metadata.document_id starts with "DBC-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("DBC-"):
        return "DBC"

    # ------------------------------------------------------------------
    # 9. HLD - High-Level Design
    #    Required: metadata.document_id starts with "HLD-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("HLD-"):
        return "HLD"

    # ------------------------------------------------------------------
    # 10. CICD - CI/CD Pipeline
    #     Required: metadata.document_id starts with "CICD-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("CICD-"):
        return "CICD"

    # ------------------------------------------------------------------
    # 10. DBAD - Database Architecture Design
    #     Required: metadata.document_id starts with "DBAD-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("DBAD-"):
        return "DBAD"

    # ------------------------------------------------------------------
    # 11. TSI - Technical System Integration
    #     Required: metadata.document_id starts with "TSI-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("TSI-"):
        return "TSI"

    # ------------------------------------------------------------------
    # 12. NFTS - Non-Functional Test Specification
    #     Required: metadata.document_id starts with "NFTS-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("NFTS-"):
        return "NFTS"

    # ------------------------------------------------------------------
    # 13. DG - Deployment Guide
    #     Required: metadata.document_id starts with "DG-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("DG-"):
        return "DG"

    # ------------------------------------------------------------------
    # 14. UT - Unit Test Specification
    #     Required: metadata.document_id starts with "UT-"
    #               unit_under_test key present
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("UT-"):
        if "unit_under_test" in data:
            return "UT"

    # ------------------------------------------------------------------
    # 13. NFRAR - Non-Functional Requirements Analysis Report
    #     Required: metadata.document_id starts with "NFRAR-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("NFRAR-"):
        return "NFRAR"

    # ------------------------------------------------------------------
    # 14. MVP - Minimum Viable Product
    #     Required: metadata.document_id starts with "MVP-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("MVP-"):
        return "MVP"

    # ------------------------------------------------------------------
    # 15. RTM - Requirements Traceability Matrix
    #     Required: metadata.document_id starts with "RTM-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("RTM-"):
        return "RTM"

    # ------------------------------------------------------------------
    # 16. DD - Design Decisions
    #     Required: metadata.document_id starts with "DD-"
    # ------------------------------------------------------------------
    if isinstance(doc_id, str) and doc_id.startswith("DD-"):
        return "DD"

    return "UNKNOWN"


def detect_from_file(path: str) -> str:
    """Load a YAML file and detect its document type.

    Parameters
    ----------
    path : str
        Filesystem path to a YAML document.

    Returns
    -------
    str
        A document type string (e.g. 'PC', 'NFR', 'NFTS', 'DG') or 'UNKNOWN'.
    """
    data = load_yaml(path)
    return detect_document_type(data)
