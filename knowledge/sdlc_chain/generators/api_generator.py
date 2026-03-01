"""FRD → OpenAPI 3.1 API Contract generator.

Produces an OpenAPI 3.1 scaffold from FRD module interface and functional
requirements, aligned with the project's API contract convention.

Entry point
-----------
    generate_api_contract(frd, sequence, today)
"""
from datetime import date
from typing import Optional

from ..config import (
    DRAFT_VERSION,
    MARKER_AUTO_COMPLETE,
    MARKER_AUTO_REVIEW,
    MARKER_DRAFT_REVIEW,
    STATUS_DRAFT,
)
from ..naming import to_pascal_case
from ._contract_helpers import extract_common


def generate_api_contract(
    frd: dict,
    sequence: int = 1,
    today: Optional[str] = None,
) -> dict:
    """
    Scaffold one OpenAPI 3.1 API contract document.

    Args:
        frd:      Source FRD dict.
        sequence: Unused for API IDs (filename uses FRD ID + domain name)
                  but kept for signature consistency.
        today:    ISO date string; defaults to today.
    """
    if today is None:
        today = date.today().isoformat()
    common = extract_common(frd, today)
    apis = frd.get("module_interface", {}).get("apis_provided", [])
    return _generate_api_contract(common, apis, frd)


# ---------------------------------------------------------------------------
# Private implementation
# ---------------------------------------------------------------------------

def _generate_api_contract(common: dict, apis: list, frd: dict) -> dict:
    """Build an OpenAPI 3.1 scaffold aligned with the project's API contract convention."""
    frd_id      = common["frd_id"]
    module_name = common["module_name"]
    today       = common["today"]
    base_path   = f"/{module_name.lower().replace(' ', '-')}"
    resource    = to_pascal_case(module_name)

    fa = frd.get("functional_requirements", {}).get("functional_areas", [])
    paths = _build_openapi_paths(base_path, resource, fa)

    return {
        "openapi": "3.1.0",
        "info": {
            "title": f"{module_name} API",
            "description": (
                frd.get("overview", {}).get("summary", "")
                or f"{MARKER_DRAFT_REVIEW} Describe the {module_name} API purpose and scope."
            ),
            "version": DRAFT_VERSION,
            "contact": {
                "name":  common["author"] or f"{MARKER_DRAFT_REVIEW} Owning team name",
                "email": f"{MARKER_DRAFT_REVIEW} team@example.com",
            },
        },
        "servers": [
            {"url": f"{MARKER_DRAFT_REVIEW} https://api.example.com/v1",          "description": "Production"},
            {"url": f"{MARKER_DRAFT_REVIEW} https://api-staging.example.com/v1",  "description": "Staging"},
        ],
        "security": [{"BearerAuth": []}],
        "tags": [
            {
                "name":        module_name,
                "description": f"{module_name} operations",
                "externalDocs": {
                    "description": f"Source FRD: {frd_id}",
                    "url":         f"{MARKER_DRAFT_REVIEW} Link to FRD artifact",
                },
            }
        ],
        "paths": paths,
        "components": {
            "schemas": {
                resource: {
                    "type":        "object",
                    "description": f"{MARKER_DRAFT_REVIEW} Define the {module_name} resource schema",
                    "properties": {
                        "id":                       {"type": "string", "format": "uuid", "readOnly": True, "example": "550e8400-e29b-41d4-a716-446655440000"},
                        f"{MARKER_DRAFT_REVIEW} field": {"type": "string", "description": f"{MARKER_DRAFT_REVIEW} Field description"},
                    },
                    "required": ["id"],
                },
                "ErrorResponse": {
                    "$ref": "./_shared_schemas.yaml#/components/schemas/ErrorResponse",
                },
            },
            "securitySchemes": {
                "BearerAuth": {
                    "type":         "http",
                    "scheme":       "bearer",
                    "bearerFormat": "JWT",
                    "description":  "OAuth 2.0 JWT Bearer token.",
                }
            },
            "parameters": {
                "CorrelationIdHeader": {
                    "$ref": "./_shared_schemas.yaml#/components/parameters/CorrelationIdHeader",
                },
                "PageParam": {
                    "$ref": "./_shared_schemas.yaml#/components/parameters/PageParam",
                },
                "PageSizeParam": {
                    "$ref": "./_shared_schemas.yaml#/components/parameters/PageSizeParam",
                },
            },
        },
        # OpenAPI extension fields — traceability back to source FRD
        "x-source-frd":    frd_id,
        "x-generated-date": today,
    }


def _build_openapi_paths(base_path: str, resource: str, functional_areas: list) -> dict:
    """
    Build an OpenAPI paths dict.

    If functional_areas exist, derive one collection path per area (up to 3)
    plus a generic {id} path.  If empty, fall back to a standard CRUD pair.
    """
    paths: dict = {}
    schema_ref  = f"#/components/schemas/{resource}"
    error_ref   = "#/components/schemas/ErrorResponse"
    common_params = [
        {"$ref": "./_shared_schemas.yaml#/components/parameters/CorrelationIdHeader"},
    ]

    # Collection path (GET list + POST create)
    collection_path = f"{base_path}/{resource.lower()}"
    paths[collection_path] = _openapi_collection_ops(resource, schema_ref, error_ref, common_params)

    # Item path (GET / PUT / DELETE by ID)
    item_path = f"{base_path}/{resource.lower()}/{{id}}"
    paths[item_path] = _openapi_item_ops(resource, schema_ref, error_ref, common_params)

    # Extra paths from functional areas (first 2 non-trivial ones)
    added = 0
    for area in functional_areas:
        if added >= 2:
            break
        area_name = area.get("area_name", "")
        if not area_name or MARKER_DRAFT_REVIEW in area_name:
            continue
        sub_resource = to_pascal_case(area_name)
        sub_path     = f"{base_path}/{sub_resource.lower()}"
        if sub_path in paths:
            continue
        paths[sub_path] = _openapi_collection_ops(sub_resource, schema_ref, error_ref, common_params)
        added += 1

    return paths


def _openapi_collection_ops(resource: str, schema_ref: str, error_ref: str, common_params: list) -> dict:
    return {
        "get": {
            "summary":     f"List {resource} items",
            "operationId": f"list{resource}",
            "tags":        [],
            "parameters":  common_params + [
                {"$ref": "./_shared_schemas.yaml#/components/parameters/PageParam"},
                {"$ref": "./_shared_schemas.yaml#/components/parameters/PageSizeParam"},
            ],
            "responses": {
                "200": {
                    "description": f"Paginated list of {resource} items",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type":  "array",
                                        "items": {"$ref": schema_ref},
                                    },
                                    "meta": {"$ref": "./_shared_schemas.yaml#/components/schemas/PaginationMeta"},
                                },
                            }
                        }
                    },
                },
                "400": {"description": "Bad Request",          "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "401": {"description": "Unauthorized"},
                "500": {"description": "Internal Server Error", "content": {"application/json": {"schema": {"$ref": error_ref}}}},
            },
        },
        "post": {
            "summary":     f"Create a {resource}",
            "operationId": f"create{resource}",
            "tags":        [],
            "parameters":  common_params,
            "requestBody": {
                "required": True,
                "content":  {"application/json": {"schema": {"$ref": schema_ref}}},
            },
            "responses": {
                "201": {"description": f"{resource} created successfully",  "content": {"application/json": {"schema": {"$ref": schema_ref}}}},
                "400": {"description": "Bad Request",                       "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "401": {"description": "Unauthorized"},
                "422": {"description": "Unprocessable Entity",              "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "500": {"description": "Internal Server Error",             "content": {"application/json": {"schema": {"$ref": error_ref}}}},
            },
        },
    }


def _openapi_item_ops(resource: str, schema_ref: str, error_ref: str, common_params: list) -> dict:
    id_param = {
        "name":        "id",
        "in":          "path",
        "required":    True,
        "schema":      {"type": "string", "format": "uuid"},
        "description": f"Unique identifier of the {resource}",
    }
    return {
        "get": {
            "summary":     f"Get {resource} by ID",
            "operationId": f"get{resource}ById",
            "tags":        [],
            "parameters":  [id_param] + common_params,
            "responses": {
                "200": {"description": f"{resource} found",     "content": {"application/json": {"schema": {"$ref": schema_ref}}}},
                "401": {"description": "Unauthorized"},
                "404": {"description": f"{resource} not found", "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "500": {"description": "Internal Server Error",  "content": {"application/json": {"schema": {"$ref": error_ref}}}},
            },
        },
        "put": {
            "summary":     f"Update {resource}",
            "operationId": f"update{resource}",
            "tags":        [],
            "parameters":  [id_param] + common_params,
            "requestBody": {
                "required": True,
                "content":  {"application/json": {"schema": {"$ref": schema_ref}}},
            },
            "responses": {
                "200": {"description": f"{resource} updated",  "content": {"application/json": {"schema": {"$ref": schema_ref}}}},
                "400": {"description": "Bad Request",          "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "401": {"description": "Unauthorized"},
                "404": {"description": "Not found",            "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "422": {"description": "Unprocessable Entity", "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "500": {"description": "Internal Server Error", "content": {"application/json": {"schema": {"$ref": error_ref}}}},
            },
        },
        "delete": {
            "summary":     f"Delete {resource}",
            "operationId": f"delete{resource}",
            "tags":        [],
            "parameters":  [id_param] + common_params,
            "responses": {
                "204": {"description": "Deleted successfully"},
                "401": {"description": "Unauthorized"},
                "404": {"description": "Not found",            "content": {"application/json": {"schema": {"$ref": error_ref}}}},
                "500": {"description": "Internal Server Error", "content": {"application/json": {"schema": {"$ref": error_ref}}}},
            },
        },
    }
