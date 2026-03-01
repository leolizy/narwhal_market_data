"""Module/function mapping file: load, generate, and validate."""
from typing import List, Optional
from pathlib import Path

from .models import (
    FunctionMapping, ModuleMapping, MappingConfig,
    PcDocument, PcFunctionalRequirement,
)
from .yaml_utils import load_yaml, dump_yaml
from .config import VALID_ARCHETYPES


def load_mapping(path: str) -> MappingConfig:
    """Load and parse a module mapping YAML file into MappingConfig."""
    data = load_yaml(path)

    modules = []
    for mod in data.get("modules", []):
        functions = []
        for func in mod.get("functions", []):
            functions.append(FunctionMapping(
                function_name=func.get("function_name", ""),
                archetype=func.get("archetype", ""),
                requirements=func.get("requirements", []),
            ))
        modules.append(ModuleMapping(
            module_code=mod.get("module_code", ""),
            module_name=mod.get("module_name", ""),
            requirements=mod.get("requirements", []),
            functions=functions,
        ))

    return MappingConfig(
        pc_id=data.get("pc_id", ""),
        project_code=data.get("project_code", ""),
        modules=modules,
    )


def generate_mapping_template(pc: PcDocument, project_code: str) -> dict:
    """
    Generate a mapping template YAML structure from a parsed PC.

    Extracts all functional requirement IDs and places them in a single
    UNASSIGNED module for the user to reorganize.
    """
    req_ids = [
        req.id for req in pc.functional_requirements
        if req.id and req.id.strip()
    ]

    return {
        "pc_id": pc.id,
        "project_code": project_code.upper(),
        "modules": [
            {
                "module_code": "MOD01",
                "module_name": "UNASSIGNED - Rename and split into modules",
                "requirements": req_ids,
                "functions": [
                    {
                        "function_name": "UNASSIGNED - Define functions and assign requirements",
                        "archetype": "PROCESS_FLOW",
                        "requirements": req_ids,
                    }
                ],
            }
        ],
    }


def validate_mapping(mapping: MappingConfig, pc: PcDocument) -> List[str]:
    """
    Validate mapping against PC.

    Returns list of error/warning strings. Empty list means valid.
    """
    errors = []

    # Check PC ID matches
    if mapping.pc_id and pc.id and mapping.pc_id != pc.id:
        errors.append(
            f"Mapping pc_id '{mapping.pc_id}' does not match PC id '{pc.id}'"
        )

    # Check project code
    if not mapping.project_code:
        errors.append("Mapping project_code is empty")
    elif not mapping.project_code.isalnum() or not mapping.project_code.isupper():
        errors.append(
            f"project_code '{mapping.project_code}' must be 2-5 uppercase alphanumeric"
        )
    elif len(mapping.project_code) < 2 or len(mapping.project_code) > 5:
        errors.append(
            f"project_code '{mapping.project_code}' must be 2-5 characters"
        )

    # Collect all PC functional requirement IDs
    pc_req_ids = {req.id for req in pc.functional_requirements if req.id}

    # Track requirement assignments
    assigned_reqs = {}  # req_id → module_code
    all_module_codes = set()

    for module in mapping.modules:
        # Validate module_code
        mc = module.module_code
        if not mc:
            errors.append("Module has empty module_code")
        elif not mc.isalnum() or not mc.isupper():
            errors.append(f"module_code '{mc}' must be uppercase alphanumeric")
        elif len(mc) < 2 or len(mc) > 5:
            errors.append(f"module_code '{mc}' must be 2-5 characters")

        if mc in all_module_codes:
            errors.append(f"Duplicate module_code '{mc}'")
        all_module_codes.add(mc)

        # Validate module requirements
        for req_id in module.requirements:
            if req_id not in pc_req_ids:
                errors.append(
                    f"Module '{mc}': requirement '{req_id}' not found in PC"
                )
            if req_id in assigned_reqs:
                errors.append(
                    f"Requirement '{req_id}' assigned to both "
                    f"'{assigned_reqs[req_id]}' and '{mc}'"
                )
            assigned_reqs[req_id] = mc

        # Validate functions
        func_req_ids = set()
        for func in module.functions:
            if not func.function_name:
                errors.append(f"Module '{mc}': function has empty function_name")
            if func.archetype and func.archetype not in VALID_ARCHETYPES:
                errors.append(
                    f"Module '{mc}', function '{func.function_name}': "
                    f"invalid archetype '{func.archetype}'. "
                    f"Must be one of: {', '.join(sorted(VALID_ARCHETYPES))}"
                )
            for req_id in func.requirements:
                if req_id not in module.requirements:
                    errors.append(
                        f"Module '{mc}', function '{func.function_name}': "
                        f"requirement '{req_id}' not in module's requirements list"
                    )
                func_req_ids.add(req_id)

        # Check all module reqs are assigned to at least one function
        unassigned = set(module.requirements) - func_req_ids
        if unassigned:
            errors.append(
                f"Module '{mc}': requirements {sorted(unassigned)} "
                f"not assigned to any function"
            )

    # Check for PC requirements not assigned to any module
    unassigned_pc = pc_req_ids - set(assigned_reqs.keys())
    if unassigned_pc:
        errors.append(
            f"PC requirements not assigned to any module: {sorted(unassigned_pc)}"
        )

    return errors
