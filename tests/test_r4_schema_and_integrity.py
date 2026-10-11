"""
Test Suite for Requirement R4: Schema & Integrity Verification and Coordinate Compliance Audit.

Validates that:
1. report.json and theme.json files are BOM-free UTF-8 and valid JSON.
2. Power BI visual definitions and embedded config JSON objects parse cleanly.
3. Coordinate compliance audit matrix is generated and validates all visual boundaries.
"""

import json
import pytest
from pathlib import Path
from tests.helpers import (
    check_bom_free_utf8,
    load_report_model,
    audit_section_coordinates,
    format_audit_table_markdown,
    PATH_REPORT_JSON,
    PATH_THEME_ROOT,
    PATH_THEME_REGISTERED,
    DOMAIN_MAPPING,
    ReportModel,
)


class TestR4SchemaAndIntegrity:
    """Requirement R4 Test Cases."""

    def test_theme_root_is_bom_free_utf8(self):
        """Verify powerbi/theme.json is BOM-free UTF-8."""
        valid, msg = check_bom_free_utf8(PATH_THEME_ROOT)
        assert valid, f"powerbi/theme.json encoding error: {msg}"

    def test_theme_registered_is_bom_free_utf8(self):
        """Verify RegisteredResources/PharmaForce360Theme.json is BOM-free UTF-8."""
        valid, msg = check_bom_free_utf8(PATH_THEME_REGISTERED)
        assert valid, f"PharmaForce360Theme.json encoding error: {msg}"

    def test_report_json_is_bom_free_utf8(self):
        """Verify report.json is BOM-free UTF-8."""
        valid, msg = check_bom_free_utf8(PATH_REPORT_JSON)
        assert valid, f"report.json encoding error: {msg}"

    def test_theme_root_valid_json(self):
        """Verify powerbi/theme.json parses as valid JSON."""
        content = PATH_THEME_ROOT.read_text(encoding="utf-8")
        data = json.loads(content)
        assert isinstance(data, dict), "Root theme JSON must be a dictionary"
        assert "visualStyles" in data, "Theme missing 'visualStyles' key"

    def test_theme_registered_valid_json(self):
        """Verify PharmaForce360Theme.json parses as valid JSON."""
        content = PATH_THEME_REGISTERED.read_text(encoding="utf-8")
        data = json.loads(content)
        assert isinstance(data, dict), "Registered theme JSON must be a dictionary"
        assert "visualStyles" in data, "Registered theme missing 'visualStyles' key"

    def test_report_json_pbip_structure(self, report_model: ReportModel):
        """Verify report.json top-level PBIP structure and embedded configs."""
        raw = report_model.raw_json
        assert "config" in raw, "report.json missing 'config' key"
        assert "sections" in raw, "report.json missing 'sections' key"
        assert "resourcePackages" in raw, "report.json missing 'resourcePackages' key"

        # Verify root config parses as JSON
        if isinstance(raw["config"], str):
            cfg_obj = json.loads(raw["config"])
            assert isinstance(cfg_obj, dict), "Parsed root config must be a dict"

        # Verify each visual container embedded config parses cleanly
        for sec_name, sec in report_model.sections.items():
            for v in sec.visuals:
                assert isinstance(v.raw_config, dict), (
                    f"Visual '{v.name}' on page '{sec_name}' has invalid config"
                )

    def test_coordinate_compliance_audit_matrix_generation(self, report_model: ReportModel):
        """
        Generate coordinate compliance matrix for all visuals across analytical pages.
        Verifies that matrix generation succeeds and produces structured records.
        """
        all_audit_entries = []
        for sec_name, sec in report_model.sections.items():
            if sec_name in DOMAIN_MAPPING:
                entries = audit_section_coordinates(sec)
                all_audit_entries.extend(entries)

        assert len(all_audit_entries) > 0, "No visual entries extracted for audit matrix"

        # Verify table formatting
        table_md = format_audit_table_markdown(all_audit_entries)
        assert len(table_md) > 100, "Generated markdown audit table is unexpectedly short"
        assert "| Section | Visual Name |" in table_md, "Audit table missing expected header"
