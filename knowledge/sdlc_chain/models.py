"""Data model classes used throughout the SDLC chain system.

Defines dataclasses for PC documents, requirement-to-module mappings,
and document lifecycle tracking.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# PC models
# ---------------------------------------------------------------------------


@dataclass
class PcObjective:
    id: str
    statement: str
    success_measure: str


@dataclass
class PcAcceptanceCriterion:
    id: str
    statement: str


@dataclass
class PcSubRequirement:
    id: str
    statement: str


@dataclass
class PcFunctionalRequirement:
    id: str
    type: str
    statement: str
    priority: str
    traces_to: List[str] = field(default_factory=list)
    acceptance: List[PcAcceptanceCriterion] = field(default_factory=list)
    sub_requirements: List[PcSubRequirement] = field(default_factory=list)


@dataclass
class PcNonFunctionalRequirement:
    id: str
    type: str
    category: str
    statement: str
    priority: str
    target_metric: str
    acceptance: List[PcAcceptanceCriterion] = field(default_factory=list)


@dataclass
class PcConstraint:
    id: str
    type: str
    statement: str
    priority: str


@dataclass
class PcGlossaryItem:
    term: str
    definition: str


@dataclass
class PcDocument:
    id: str
    title: str
    version: str
    status: str
    classification: str
    created_date: str
    last_updated: str
    owners: Dict[str, str] = field(default_factory=dict)
    related_documents: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    executive_summary: str = ""
    objectives: List[PcObjective] = field(default_factory=list)
    problem_statement: str = ""
    scope_in: List[str] = field(default_factory=list)
    scope_out: List[str] = field(default_factory=list)
    scope_domain_definitions: List[str] = field(default_factory=list)
    stakeholders: List[Dict[str, str]] = field(default_factory=list)
    current_state: List[str] = field(default_factory=list)
    future_state_vision: str = ""
    future_state_outcomes: List[str] = field(default_factory=list)
    functional_requirements: List[PcFunctionalRequirement] = field(default_factory=list)
    nonfunctional_requirements: List[PcNonFunctionalRequirement] = field(default_factory=list)
    constraints: List[PcConstraint] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    constraint_statements: List[str] = field(default_factory=list)
    risks: List[Dict[str, str]] = field(default_factory=list)
    success_metrics: List[Dict[str, str]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    glossary: List[PcGlossaryItem] = field(default_factory=list)
    traceability_matrix: List[Dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Mapping models
# ---------------------------------------------------------------------------


@dataclass
class FunctionMapping:
    function_name: str
    archetype: str
    requirements: List[str] = field(default_factory=list)


@dataclass
class ModuleMapping:
    module_code: str
    module_name: str
    requirements: List[str] = field(default_factory=list)
    functions: List[FunctionMapping] = field(default_factory=list)


@dataclass
class MappingConfig:
    pc_id: str
    project_code: str
    modules: List[ModuleMapping] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Tracker models
# ---------------------------------------------------------------------------


@dataclass
class ProposedDocument:
    id: str
    doc_type: str
    parent_doc: str
    source_requirement: str
    proposed_date: str
    resolution: Optional[str] = None
    rationale: Optional[str] = None
    resolved_date: Optional[str] = None
    resolved_by: Optional[str] = None


@dataclass
class DeprecatedReference:
    doc_id: str
    removed_requirement: str
    flagged_date: str
    resolution: Optional[str] = None


@dataclass
class ContentMarker:
    doc_id: str
    field_path: str
    marker_type: str
    marker_text: str


@dataclass
class TrackerState:
    generated: str
    pc_id: str
    proposed_documents: List[ProposedDocument] = field(default_factory=list)
    deprecated_references: List[DeprecatedReference] = field(default_factory=list)
