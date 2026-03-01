"""Render FRD (and other doc type) YAML dicts into Markdown format."""
from typing import Dict, List, Optional


def render_frd_markdown(frd: dict) -> str:
    """Render an FRD dict (K8s envelope format) into Markdown."""
    lines = []

    # Metadata — read from top-level metadata key (K8s envelope)
    meta = frd.get("metadata", frd.get("document", {}))
    doc_id = meta.get("document_id", "")
    title = meta.get("title", "")

    lines.append(f"# {doc_id}: {title}" if doc_id else "# Functional Requirements Document (FRD)")
    lines.append("")
    lines.append(_metadata_table(meta))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1: Overview
    ov = frd.get("overview", {})
    lines.append("## 1. Overview")
    lines.append("")
    if ov.get("summary"):
        lines.append(f"**Summary:** {ov['summary']}")
        lines.append("")
    if ov.get("purpose"):
        lines.append(f"**Purpose:** {ov['purpose']}")
        lines.append("")
    if ov.get("audience"):
        lines.append(f"**Audience:** {ov['audience']}")
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 2: Scope
    scope = frd.get("scope", {})
    lines.append("## 2. Scope")
    lines.append("")
    lines.append("### In Scope")
    lines.append("")
    for i, item in enumerate(scope.get("in_scope", []), 1):
        lines.append(f"{i}. {item}")
    lines.append("")
    lines.append("### Out of Scope")
    lines.append("")
    for i, item in enumerate(scope.get("out_of_scope", []), 1):
        lines.append(f"{i}. {item}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 3: Definitions
    defs = frd.get("definitions", {})
    lines.append("## 3. Definitions")
    lines.append("")
    lines.append(_table(
        ["Term", "Definition"],
        [[d.get("term", ""), d.get("definition", "")] for d in defs.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 4: Business Context
    bc = frd.get("business_context", {})
    lines.append("## 4. Business Context")
    lines.append("")
    obj_ids = bc.get("parent_objectives", [])
    if obj_ids:
        lines.append(f"**Parent PC Objectives Supported:** {', '.join(f'`{o}`' for o in obj_ids)}")
        lines.append("")
    if bc.get("content"):
        lines.append(bc["content"])
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 5: Actors
    actors = frd.get("actors", {})
    lines.append("## 5. Actors")
    lines.append("")
    lines.append(_table(
        ["ID", "Actor", "Type", "Role"],
        [[a.get("id", ""), a.get("name", a.get("actor", "")), a.get("type", ""), a.get("role", "")]
         for a in actors.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 6: Functional Overview
    fo = frd.get("functional_overview", {})
    lines.append("## 6. Functional Overview")
    lines.append("")
    if fo.get("content"):
        lines.append(fo["content"])
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 7: Event Triggers
    et = frd.get("event_triggers", {})
    lines.append("## 7. Event Triggers")
    lines.append("")
    lines.append(_table(
        ["ID", "Trigger", "Type", "Initiates"],
        [[t.get("id", t.get("trigger_id", "")),
          t.get("trigger", t.get("event", "")),
          t.get("type", t.get("source", "")),
          t.get("initiates", ", ".join(t.get("triggered_requirements", [])))]
         for t in et.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 8: Functional Requirements
    fr = frd.get("functional_requirements", {})
    lines.append("## 8. Functional Requirements")
    lines.append("")
    for area in fr.get("functional_areas", []):
        area_label = area.get("area", f"{area.get('area_id', '')} {area.get('area_name', '')}".strip())
        lines.append(f"### {area_label}")
        lines.append("")
        rows = []
        for req in area.get("requirements", []):
            desc = req.get("description", req.get("statement", ""))
            traces = req.get("traces_to", req.get("traces_to_pc", []))
            ac_raw = req.get("acceptance_criteria", "")
            # acceptance_criteria may be a string or a list of dicts
            if isinstance(ac_raw, list):
                ac_str = "; ".join(
                    a.get("statement", a.get("criteria", str(a))) if isinstance(a, dict) else str(a)
                    for a in ac_raw
                )
            else:
                ac_str = str(ac_raw) if ac_raw else ""
            rows.append([
                req.get("id", ""),
                desc,
                req.get("priority", ""),
                ", ".join(traces) if isinstance(traces, list) else str(traces),
                ac_str,
            ])
        lines.append(_table(
            ["ID", "Requirement", "Priority", "Traces To", "Acceptance Criteria"],
            rows,
        ))
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 9: Business Rules
    br = frd.get("business_rules", {})
    lines.append("## 9. Business Rules")
    lines.append("")
    lines.append(_table(
        ["ID", "Rule", "Affects"],
        [[r.get("id", ""),
          r.get("rule", ""),
          ", ".join(r.get("affects", r.get("applies_to", [])))
          if isinstance(r.get("affects", r.get("applies_to", [])), list)
          else str(r.get("affects", r.get("applies_to", "")))]
         for r in br.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 10: Exception Scenarios
    ex = frd.get("exception_scenarios", {})
    lines.append("## 10. Exception Scenarios")
    lines.append("")
    lines.append(_table(
        ["ID", "Trigger Condition", "Expected Behaviour"],
        [[e.get("id", ""),
          e.get("trigger", e.get("trigger_condition", e.get("scenario", ""))),
          e.get("expected_behaviour", e.get("expected_behavior", e.get("user_outcome", "")))]
         for e in ex.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 11: Module Interface
    mi = frd.get("module_interface", {})
    lines.append("## 11. Module Interface")
    lines.append("")
    lines.append("### APIs Provided")
    lines.append("")
    lines.append(_table(
        ["API Name", "Operations", "Consumers"],
        [[a.get("name", a.get("interface_name", "")),
          ", ".join(a.get("operations", [])) if isinstance(a.get("operations"), list) else a.get("description", ""),
          ", ".join(a.get("consumers", []))]
         for a in mi.get("apis_provided", [])],
    ))
    lines.append("")
    lines.append("### Events Published")
    lines.append("")
    lines.append(_table(
        ["Event", "Trigger", "Consumers"],
        [[e.get("event", e.get("event_name", "")),
          e.get("trigger", ""),
          ", ".join(e.get("consumers", []))]
         for e in mi.get("events_published", [])],
    ))
    lines.append("")
    lines.append("### Data Owned")
    lines.append("")
    lines.append(_table(
        ["Entity", "Ownership", "Notes"],
        [[d.get("entity", ""), d.get("ownership", ""),
          d.get("notes", ", ".join(d.get("consumers", [])))]
         for d in mi.get("data_owned", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 12: Cross-Module Interactions
    cm = frd.get("cross_module_interactions", {})
    lines.append("## 12. Cross-Module Interactions")
    lines.append("")
    lines.append(_table(
        ["Dependency", "Type", "Purpose"],
        [[c.get("dependency", c.get("module", "")),
          c.get("type", c.get("interaction_type", "")),
          c.get("purpose", c.get("description", ""))]
         for c in cm.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 13: Data Requirements
    dr = frd.get("data_requirements", {})
    lines.append("## 13. Data Requirements")
    lines.append("")
    lines.append(_table(
        ["Entity", "Operations", "Sensitivity", "Notes"],
        [[e.get("name", e.get("entity_name", "")),
          ", ".join(e.get("operations", [])) if isinstance(e.get("operations"), list) else e.get("crud", ""),
          e.get("sensitivity", ""),
          e.get("notes", e.get("description", ""))]
         for e in dr.get("entities", [])],
    ))
    if dr.get("data_retention"):
        lines.append("")
        lines.append(f"**Data Retention:** {dr['data_retention']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 14: NFRs
    nfr = frd.get("nonfunctional_requirements", {})
    lines.append("## 14. Non-Functional Requirements")
    lines.append("")
    lines.append(_table(
        ["ID", "Requirement", "Source NFR"],
        [[n.get("id", ""),
          n.get("description", n.get("statement", "")),
          n.get("source_nfr", n.get("category", ""))]
         for n in nfr.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 15: Traceability Matrix
    tr = frd.get("traceability", {})
    lines.append("## 15. Traceability Matrix")
    lines.append("")
    lines.append(_table(
        ["PC Requirement", "FRD Requirements", "Downstream"],
        [[t.get("requirement_id", t.get("pc_requirement", "")),
          ", ".join(t.get("frd_requirements", [])),
          ", ".join(t.get("downstream", t.get("downstream_artifacts", [])))]
         for t in tr.get("matrix", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 16: Acceptance Criteria
    ac = frd.get("acceptance_criteria", {})
    lines.append("## 16. Acceptance Criteria")
    lines.append("")
    lines.append(_table(
        ["ID", "Criterion"],
        [[a.get("id", ""), a.get("criterion", a.get("criteria", a.get("statement", "")))]
         for a in ac.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 17: Assumptions & Constraints
    andc = frd.get("assumptions_and_constraints", {})
    lines.append("## 17. Assumptions & Constraints")
    lines.append("")
    lines.append("### Assumptions")
    lines.append("")
    lines.append(_table(
        ["ID", "Assumption"],
        [[a.get("id", ""), a.get("description", a.get("assumption", ""))]
         for a in andc.get("assumptions", [])],
    ))
    lines.append("")
    lines.append("### Constraints")
    lines.append("")
    lines.append(_table(
        ["ID", "Constraint"],
        [[c.get("id", ""), c.get("description", c.get("constraint", ""))]
         for c in andc.get("constraints", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 18: Dependencies
    dep = frd.get("dependencies", {})
    lines.append("## 18. Dependencies")
    lines.append("")
    lines.append(_table(
        ["ID", "Dependency"],
        [[d.get("id", ""), d.get("description", d.get("dependency", ""))]
         for d in dep.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 19: Open Issues
    oi = frd.get("open_issues", {})
    lines.append("## 19. Open Issues")
    lines.append("")
    oi_items = oi.get("items", [])
    if oi_items:
        lines.append(_table(
            ["ID", "Issue"],
            [[o.get("id", ""), o.get("issue", "")] for o in oi_items],
        ))
    else:
        lines.append("No open issues.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 20: Approvals
    ap = frd.get("approvals", {})
    lines.append("## 20. Approvals")
    lines.append("")
    lines.append(_table(
        ["Role", "Name", "Date", "Signature"],
        [[a.get("role", ""), a.get("name", ""), a.get("date", ""), a.get("signature", "")]
         for a in ap.get("items", [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Change Log
    cl = frd.get("change_log", {})
    lines.append("## Change Log")
    lines.append("")
    lines.append(_table(
        ["Version", "Date", "Author", "Description"],
        [[e.get("version", ""), e.get("date", ""), e.get("author", ""),
          e.get("description", e.get("summary", ""))]
         for e in cl.get("entries", [])],
    ))
    lines.append("")

    return "\n".join(lines)


def render_dd_markdown(dd: dict) -> str:
    """Render a DD (Data Dictionary) dict into Markdown matching 93-dd_template.md."""
    lines = []

    # Title
    lines.append("# Data Dictionary & Glossary")
    lines.append("")

    # Metadata table
    meta = dd.get("metadata", {})
    related = meta.get("related_documents", [])
    meta_rows = [
        ("Document ID",       meta.get("document_id", "")),
        ("Title",             meta.get("title", "")),
        ("Version",           meta.get("version", "")),
        ("Status",            meta.get("status", "")),
        ("Classification",    meta.get("classification", "")),
        ("Created Date",      meta.get("created_date", "")),
        ("Last Updated",      meta.get("last_updated", "")),
        ("Author",            meta.get("author", "")),
        ("Reviewer",          meta.get("reviewer", "")),
        ("Approver",          meta.get("approver", "")),
        ("System Name",       meta.get("system_name", "")),
        ("System Version",    meta.get("system_version", "")),
        ("Related Documents", ", ".join(related) if isinstance(related, list) else str(related)),
    ]
    hdr = ["| Field              | Value                                                        |",
           "|--------------------|--------------------------------------------------------------|"]
    for field, value in meta_rows:
        hdr.append(f"| {field:<18} | {str(value):<60} |")
    lines.append("\n".join(hdr))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1: Introduction
    intro = dd.get("introduction", {})
    lines.append("## 1. Introduction")
    lines.append("")
    if intro.get("purpose"):
        lines.append("### Purpose")
        lines.append("")
        lines.append(intro["purpose"])
        lines.append("")
    if intro.get("scope"):
        lines.append("### Scope")
        lines.append("")
        lines.append(intro["scope"])
        lines.append("")
    if intro.get("audience"):
        lines.append("### Audience")
        lines.append("")
        lines.append(intro["audience"])
        lines.append("")
    if intro.get("how_to_use"):
        lines.append("### How to Use")
        lines.append("")
        lines.append(intro["how_to_use"])
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 2: Data Domains
    domains = dd.get("data_domains", [])
    lines.append("## 2. Data Domains")
    lines.append("")
    lines.append(_table(
        ["Domain ID", "Domain Name", "Description", "Owner", "Related Modules"],
        [[d.get("domain_id", ""), d.get("domain_name", ""), d.get("description", ""),
          d.get("owner", ""), ", ".join(d.get("related_modules", []))]
         for d in (domains if isinstance(domains, list) else [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 3: Data Elements Catalog
    elements = dd.get("data_elements_catalog", [])
    lines.append("## 3. Data Elements Catalog")
    lines.append("")
    lines.append(_table(
        ["Element ID", "Element Name", "Display Name", "Domain", "Definition",
         "Data Type", "Nullable", "PK", "FK", "Sensitivity"],
        [[e.get("element_id", ""), e.get("element_name", ""), e.get("display_name", ""),
          e.get("domain", ""), e.get("definition", ""), e.get("data_type", ""),
          str(e.get("nullable", "")), str(e.get("primary_key", "")),
          str(e.get("foreign_key", "")), e.get("sensitivity", "")]
         for e in (elements if isinstance(elements, list) else [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 4: Entity Relationship Summary
    er = dd.get("entity_relationship_summary", [])
    lines.append("## 4. Entity Relationship Summary")
    lines.append("")
    if er:
        lines.append(_table(
            ["Relationship ID", "Parent Entity", "Child Entity", "Relationship Type",
             "On Delete", "On Update"],
            [[r.get("relationship_id", ""), r.get("parent_entity", ""),
              r.get("child_entity", ""), r.get("relationship_type", ""),
              r.get("on_delete", ""), r.get("on_update", "")]
             for r in er],
        ))
    else:
        lines.append("No entity relationships defined.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 5: Code Tables
    code_tables = dd.get("code_tables", [])
    lines.append("## 5. Code Tables & Reference Data")
    lines.append("")
    lines.append(_table(
        ["Code Table ID", "Code Table Name", "Description", "Owner"],
        [[ct.get("code_table_id", ""), ct.get("code_table_name", ""),
          ct.get("description", ""), ct.get("owner", "")]
         for ct in (code_tables if isinstance(code_tables, list) else [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 6: Data Glossary
    glossary = dd.get("data_glossary", [])
    lines.append("## 6. Data Glossary")
    lines.append("")
    lines.append(_table(
        ["Term ID", "Term", "Definition", "Context", "Synonyms", "Source", "Category"],
        [[t.get("term_id", ""), t.get("term", ""), t.get("definition", ""),
          t.get("context", ""), ", ".join(t.get("synonyms", [])),
          t.get("source", ""), t.get("category", "")]
         for t in (glossary if isinstance(glossary, list) else [])],
    ))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 7: Data Lineage
    lineage = dd.get("data_lineage", [])
    lines.append("## 7. Data Lineage & Mapping")
    lines.append("")
    if lineage:
        lines.append(_table(
            ["Mapping ID", "Source System", "Source Field", "Transformation",
             "Target System", "Target Field", "Frequency"],
            [[l.get("mapping_id", ""), l.get("source_system", ""), l.get("source_field", ""),
              l.get("transformation", ""), l.get("target_system", ""),
              l.get("target_field", ""), l.get("frequency", "")]
             for l in lineage],
        ))
    else:
        lines.append("No data lineage mappings defined.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 8: Data Quality Rules
    rules = dd.get("data_quality_rules", [])
    lines.append("## 8. Data Quality Rules")
    lines.append("")
    if rules:
        lines.append(_table(
            ["Rule ID", "Rule Name", "Description", "Rule Type", "Rule Expression",
             "Severity", "Action on Failure"],
            [[r.get("rule_id", ""), r.get("rule_name", ""), r.get("description", ""),
              r.get("rule_type", ""), r.get("rule_expression", ""),
              r.get("severity", ""), r.get("action_on_failure", "")]
             for r in rules],
        ))
    else:
        lines.append("No data quality rules defined.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 9: Attachments
    attachments = dd.get("attachments", [])
    lines.append("## 9. Attachments")
    lines.append("")
    if attachments:
        lines.append(_table(
            ["Attachment ID", "File Name", "Description", "File Type", "Version"],
            [[a.get("attachment_id", ""), a.get("file_name", ""),
              a.get("description", ""), a.get("file_type", ""), a.get("version", "")]
             for a in attachments],
        ))
    else:
        lines.append("No attachments.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Change Log
    change_log = dd.get("change_log", [])
    lines.append("## Change Log")
    lines.append("")
    lines.append(_table(
        ["Version", "Date", "Author", "Changes"],
        [[e.get("version", ""), e.get("date", ""), e.get("author", ""), e.get("changes", "")]
         for e in (change_log if isinstance(change_log, list) else [])],
    ))
    lines.append("")

    return "\n".join(lines)


def _metadata_table(doc: dict) -> str:
    """Render the FRD metadata table from a metadata dict."""
    related = doc.get("related_documents", [])
    rows = [
        ("Document ID",       doc.get("document_id", "")),
        ("Module Code",       doc.get("module_code", "")),
        ("Title",             doc.get("title", "")),
        ("Version",           doc.get("version", "")),
        ("Status",            doc.get("status", "")),
        ("Classification",    doc.get("classification", "")),
        ("Created Date",      doc.get("created_date", "")),
        ("Last Updated",      doc.get("last_updated", "")),
        ("Author",            doc.get("author", "")),
        ("Reviewer",          doc.get("reviewer", "")),
        ("Approver",          doc.get("approver", "")),
        ("Parent BRD",        doc.get("parent_brd", doc.get("parent_pc", ""))),
        ("Related Documents", ", ".join(related) if isinstance(related, list) else str(related)),
        ("Tags",              ", ".join(doc.get("tags", [])) if isinstance(doc.get("tags"), list) else ""),
        ("Supersedes",        str(doc.get("supersedes", "") or "")),
    ]
    lines = ["| Field              | Value                                                        |",
             "|--------------------|--------------------------------------------------------------|"]
    for field, value in rows:
        lines.append(f"| {field:<18} | {str(value):<60} |")
    return "\n".join(lines)


def _guidance(text: str) -> str:
    """Format a guidance blockquote."""
    if not text:
        return ""
    return f"> **Guidance:** {text}\n"


def _table(headers: List[str], rows: List[List[str]]) -> str:
    """Render a Markdown table."""
    if not headers:
        return ""
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "|" + "|".join("-" * (len(h) + 2) for h in headers) + "|"
    lines = [header_line, sep_line]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(str(c) for c in padded) + " |")
    return "\n".join(lines)
