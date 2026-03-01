"""ID generation and file naming helpers following SDLC document conventions."""
import re


def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase: 'Data Ingestion' → 'DataIngestion'."""
    words = re.split(r'[\s_\-]+', text.strip())
    return "".join(word.capitalize() for word in words if word)


def generate_pc_id(project_code: str, sequence: int = 1) -> str:
    """Generate PC document ID: PC-[PROJECT]-[NNNN]."""
    return f"PC-{project_code.upper()}-{sequence:04d}"


def generate_frd_id(project_code: str, sequence: int = 1) -> str:
    """Generate FRD document ID: FRD-[PROJECT]-[NNNN]."""
    return f"FRD-{project_code.upper()}-{sequence:04d}"


def generate_psd_id(sequence: int) -> str:
    """Generate PSD document ID: PSD-[NNNN] (global sequential)."""
    return f"PSD-{sequence:04d}"


def generate_aec_id(sequence: int) -> str:
    """Generate AEC document ID: AEC-[NNNN]."""
    return f"AEC-{sequence:04d}"


def generate_dc_id(sequence: int) -> str:
    """Generate DC document ID: DC-[NNNN]."""
    return f"DC-{sequence:04d}"


def generate_dbc_id(sequence: int) -> str:
    """Generate DBC document ID: DBC-[NNNN]."""
    return f"DBC-{sequence:04d}"


def generate_mdc_id(sequence: int) -> str:
    """Generate MDC document ID: MDC-[NNNN]."""
    return f"MDC-{sequence:04d}"


def generate_dd_id(sequence: int) -> str:
    """Generate DD document ID: DD-[NNNN]."""
    return f"DD-{sequence:04d}"


def generate_dd_filename(sequence: int, system_name: str, version: str, ext: str) -> str:
    """
    Generate DD filename per policy.
    Format: DD-[NNNN]_[SystemName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(system_name)[:50]
    return f"{generate_dd_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_mdc_filename(sequence: int, source_name: str, version: str, ext: str) -> str:
    """
    Generate MDC filename per policy.
    Format: MDC-[NNNN]_[SourceName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(source_name)[:50]
    return f"{generate_mdc_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_ut_id(sequence: int) -> str:
    """Generate UT document ID: UT-[NNNN]."""
    return f"UT-{sequence:04d}"


def generate_ut_tc_id(ut_sequence: int, tc_sequence: int) -> str:
    """Generate UT test case ID: UT-[NNNN]-TC[NN]."""
    return f"UT-{ut_sequence:04d}-TC{tc_sequence:02d}"


def generate_fr_id(sequence: int) -> str:
    """Generate functional requirement ID: FR-[NNN]."""
    return f"FR-{sequence:03d}"


def generate_fr_sub_id(fr_sequence: int, sub_sequence: int) -> str:
    """Generate sub-requirement ID: FR-[NNN].[N]."""
    return f"FR-{fr_sequence:03d}.{sub_sequence}"


def generate_ac_fr_id(fr_id: str, sequence: int) -> str:
    """Generate acceptance criterion ID: AC-FR-[NNN]-[NN]."""
    return f"AC-{fr_id}-{sequence:02d}"


def generate_fa_id(sequence: int) -> str:
    """Generate functional area ID: FA-[N]."""
    return f"FA-{sequence}"


def generate_frd_filename(
    project_code: str, sequence: int,
    short_title: str, version: str, ext: str
) -> str:
    """
    Generate FRD filename per policy.
    Format: FRD-[PROJECT]-[NNNN]_[ShortTitle]_v[Major.Minor].[ext]
    """
    pascal_title = to_pascal_case(short_title)[:40]
    doc_id = generate_frd_id(project_code, sequence)
    return f"{doc_id}_{pascal_title}_v{version}.{ext}"


def generate_psd_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """
    Generate PSD filename per policy.
    Format: PSD-[NNNN]_[ShortTitle]_v[X.Y].[ext]
    """
    pascal_title = to_pascal_case(short_title)[:50]
    doc_id = generate_psd_id(sequence)
    return f"{doc_id}_{pascal_title}_v{version}.{ext}"


def generate_ut_filename(sequence: int, function_name: str, version: str, ext: str) -> str:
    """
    Generate UT filename per policy.
    Format: UT-[NNNN]_[FunctionName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(function_name)[:40]
    doc_id = generate_ut_id(sequence)
    return f"{doc_id}_{pascal_name}_v{version}.{ext}"


def generate_aec_filename(sequence: int, event_name: str, version: str, ext: str) -> str:
    """
    Generate AEC filename per policy.
    Format: AEC-[NNNN]_[EventName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(event_name)[:50]
    return f"{generate_aec_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_dc_filename(sequence: int, entity_name: str, version: str, ext: str) -> str:
    """
    Generate DC filename per policy.
    Format: DC-[NNNN]_[EntityName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(entity_name)[:50]
    return f"{generate_dc_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_dbc_filename(sequence: int, service_name: str, version: str, ext: str) -> str:
    """
    Generate DBC filename per policy.
    Format: DBC-[NNNN]_[ServiceName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(service_name)[:50]
    return f"{generate_dbc_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_api_filename(frd_id: str, domain_name: str) -> str:
    """
    Generate API contract filename per policy.
    Format: [FRD-ID]_[domain]_api_contract.yaml
    """
    safe_domain = domain_name.lower().replace(" ", "-").replace("_", "-")
    return f"{frd_id}_{safe_domain}_api_contract.yaml"


def generate_hld_id(sequence: int) -> str:
    """Generate HLD document ID: HLD-[NNNN]."""
    return f"HLD-{sequence:04d}"


def generate_hld_filename(sequence: int, system_name: str, version: str, ext: str) -> str:
    """Generate HLD filename: HLD-[NNNN]_[SystemName]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(system_name)[:50]
    return f"{generate_hld_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_cicd_id(sequence: int) -> str:
    """Generate CICD document ID: CICD-[NNNN]."""
    return f"CICD-{sequence:04d}"


def generate_cicd_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """Generate CICD filename: CICD-[NNNN]_[ShortTitle]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(short_title)[:50]
    return f"{generate_cicd_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_dbad_id(sequence: int) -> str:
    """Generate DBAD document ID: DBAD-[NNNN]."""
    return f"DBAD-{sequence:04d}"


def generate_dbad_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """Generate DBAD filename: DBAD-[NNNN]_[ShortTitle]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(short_title)[:50]
    return f"{generate_dbad_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_tsi_id(sequence: int) -> str:
    """Generate TSI document ID: TSI-[NNNN]."""
    return f"TSI-{sequence:04d}"


def generate_tsi_filename(sequence: int, system_name: str, version: str, ext: str) -> str:
    """Generate TSI filename: TSI-[NNNN]_[SystemName]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(system_name)[:50]
    return f"{generate_tsi_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_nfts_id(sequence: int) -> str:
    """Generate NFTS document ID: NFTS-[NNNN]."""
    return f"NFTS-{sequence:04d}"


def generate_nfts_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """Generate NFTS filename: NFTS-[NNNN]_[ShortTitle]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(short_title)[:50]
    return f"{generate_nfts_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_dg_id(sequence: int) -> str:
    """Generate DG document ID: DG-[NNNN]."""
    return f"DG-{sequence:04d}"


def generate_dg_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """Generate DG filename: DG-[NNNN]_[ShortTitle]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(short_title)[:50]
    return f"{generate_dg_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_nfrar_id(sequence: int) -> str:
    """Generate NFRAR document ID: NFRAR-[NNNN]."""
    return f"NFRAR-{sequence:04d}"


def generate_nfrar_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """Generate NFRAR filename: NFRAR-[NNNN]_[ShortTitle]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(short_title)[:50]
    return f"{generate_nfrar_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_mvp_id(sequence: int) -> str:
    """Generate MVP document ID: MVP-[NNNN]."""
    return f"MVP-{sequence:04d}"


def generate_mvp_filename(sequence: int, short_title: str, version: str, ext: str) -> str:
    """Generate MVP filename: MVP-[NNNN]_[ShortTitle]_v[X.Y].[ext]"""
    pascal_name = to_pascal_case(short_title)[:50]
    return f"{generate_mvp_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_rtm_id(sequence: int) -> str:
    """Generate RTM document ID: RTM-[NNNN] (global sequential)."""
    return f"RTM-{sequence:04d}"


def generate_rtm_filename(sequence: int, system_name: str, version: str, ext: str) -> str:
    """
    Generate RTM filename per policy.
    Format: RTM-[NNNN]_[SystemName]_v[X.Y].[ext]
    """
    pascal_name = to_pascal_case(system_name)[:50]
    return f"{generate_rtm_id(sequence)}_{pascal_name}_v{version}.{ext}"


def generate_trace_filename(project_code: str, sequence: int, version: str) -> str:
    """Generate master traceability matrix filename."""
    return f"TRACE-{project_code.upper()}-{sequence:04d}_MasterTraceability_v{version}.yaml"


def extract_project_code(doc_id: str) -> str:
    """Extract project code from a document ID like PC-NPH-0001 or FRD-NPH-ING-0001."""
    parts = doc_id.split("-")
    if len(parts) >= 3:
        return parts[1]
    return ""


def extract_module_code(_frd_id: str) -> str:
    """Extract module code from FRD metadata (legacy). FRD IDs no longer contain module codes."""
    return ""


def parse_doc_id_type(doc_id: str) -> str:
    """Extract document type prefix from ID: 'FRD-NPH-ING-0001' → 'FRD'."""
    return doc_id.split("-")[0] if doc_id else ""
