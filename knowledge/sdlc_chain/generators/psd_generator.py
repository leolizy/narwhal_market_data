"""PSD generation: transforms FRD functional areas into PSD YAML structure."""


def _build_integration_points(frd: dict) -> dict:
    """
    Generate the integration_points section for a PSD from its parent FRD.

    Source material (from FRD):
      - frd["module_interface"]["apis_provided"]   — interfaces this module exposes
      - frd["module_interface"]["events_published"] — events this module emits
      - frd["cross_module_interactions"]["items"]   — what this module consumes

    Each item in the returned integrations list maps to a PSD INT-NNN entry:
      integration_id  : "INT-001"
      system_name     : module or external system name
      direction       : Inbound | Outbound | Bidirectional
      protocol        : REST | gRPC | Message Queue | Database | File
      data_exchanged  : brief description of payload or entity
      error_handling  : fallback / retry behaviour
      sla             : latency / availability target

    Contract references to add once downstream docs exist:
      api_spec_reference  → DBC-NNNN (from module_interface.apis_provided)
      schema_reference    → AEC-NNNN (from module_interface.events_published)

    TODO: implement when the PSD generator is built.
    """
    raise NotImplementedError("psd_generator._build_integration_points not yet implemented")
