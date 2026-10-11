"""
Test Suite for Requirement R2: Eight-Domain Navigation Rail & Action Button Architecture.

Validates that:
1. All 8 analytical domains exist in report.json with matching internal names and display names.
2. Static SVG sidebar assets are properly registered in resourcePackages and exist on disk.
3. Each of the 8 pages contains the corresponding nav_sidebar_<page>.svg visual at (0, 0, 240, 720).
4. Each of the 8 pages contains 8 distinct actionButton visuals at X=12, W=216, H=40,
   at calibrated vertical coordinates (Y: 134, 188, 242, 296, 350, 404, 458, 512)
   with drillFilterOtherVisuals: true and active pageNavigation actions.
"""

import pytest
from typing import List, Dict, Any
from tests.helpers import (
    ReportModel,
    DOMAIN_MAPPING,
    ACTION_BUTTON_SPECS,
    BUTTON_GEOMETRY,
    SIDEBAR_IMAGE_GEOMETRY,
    DIR_REGISTERED_RESOURCES,
)


class TestR2NavigationArchitecture:
    """Requirement R2 Test Cases."""

    def test_eight_domain_sections_exist_in_report(self, report_model: ReportModel):
        """Verify all 8 analytical domains exist with exact internal section IDs."""
        missing_sections = []
        for sec_id in DOMAIN_MAPPING.keys():
            if sec_id not in report_model.sections:
                missing_sections.append(sec_id)

        assert not missing_sections, (
            f"Missing required analytical domain section(s) in report.json: {missing_sections}. "
            f"Present sections: {list(report_model.sections.keys())}"
        )

    @pytest.mark.parametrize("sec_id,expected_meta", DOMAIN_MAPPING.items())
    def test_section_display_names(self, report_model: ReportModel, sec_id: str, expected_meta: Dict[str, Any]):
        """Verify each analytical domain has the specified display name."""
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' is missing in report.json")

        section = report_model.sections[sec_id]
        expected_title = expected_meta["display_name"]
        assert section.display_name == expected_title, (
            f"Section '{sec_id}' display name mismatch: "
            f"expected '{expected_title}', got '{section.display_name}'"
        )

    def test_static_svg_resources_registered(self, report_model: ReportModel):
        """Verify all 8 nav_sidebar_*.svg assets are registered in report.json resourcePackages."""
        registered_item_names = {item.get("name") for item in report_model.registered_resources}
        missing_registered = []

        for meta in DOMAIN_MAPPING.values():
            svg_asset = meta["svg_asset"]
            if svg_asset not in registered_item_names:
                missing_registered.append(svg_asset)

        assert not missing_registered, (
            f"Missing SVG asset registration in RegisteredResources: {missing_registered}. "
            f"Currently registered: {sorted(list(registered_item_names))}"
        )

    def test_static_svg_assets_exist_on_disk(self):
        """Verify all 8 nav_sidebar_*.svg files exist in RegisteredResources directory."""
        missing_files = []
        for meta in DOMAIN_MAPPING.values():
            svg_path = DIR_REGISTERED_RESOURCES / meta["svg_asset"]
            if not svg_path.is_file():
                missing_files.append(meta["svg_asset"])

        assert not missing_files, (
            f"Missing SVG file(s) in {DIR_REGISTERED_RESOURCES}: {missing_files}"
        )

    @pytest.mark.parametrize("sec_id,meta", DOMAIN_MAPPING.items())
    def test_sidebar_backdrop_visual_per_page(self, report_model: ReportModel, sec_id: str, meta: Dict[str, Any]):
        """
        Verify each of the 8 pages contains the corresponding nav_sidebar_<page>.svg
        background visual at geometry (X=0, Y=0, W=240, H=720).
        """
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]
        backdrop = section.sidebar_backdrop
        assert backdrop is not None, (
            f"Page '{sec_id}' is missing sidebar SVG backdrop visual at (0, 0, 240, 720). "
            f"Visual types present: {[v.visual_type for v in section.visuals]}"
        )

        assert backdrop.visual_type == "image", (
            f"Page '{sec_id}' backdrop visualType must be 'image', got: {backdrop.visual_type}"
        )
        assert abs(backdrop.x - SIDEBAR_IMAGE_GEOMETRY["x"]) < 0.5, f"Backdrop X != 0: {backdrop.x}"
        assert abs(backdrop.y - SIDEBAR_IMAGE_GEOMETRY["y"]) < 0.5, f"Backdrop Y != 0: {backdrop.y}"
        assert abs(backdrop.width - SIDEBAR_IMAGE_GEOMETRY["width"]) < 1.0, f"Backdrop W != 240: {backdrop.width}"
        assert abs(backdrop.height - SIDEBAR_IMAGE_GEOMETRY["height"]) < 1.0, f"Backdrop H != 720: {backdrop.height}"

        expected_svg = meta["svg_asset"]
        if backdrop.image_resource_name:
            assert expected_svg in backdrop.image_resource_name, (
                f"Page '{sec_id}' backdrop image binding mismatch: "
                f"expected '{expected_svg}', got '{backdrop.image_resource_name}'"
            )

    @pytest.mark.parametrize("sec_id", DOMAIN_MAPPING.keys())
    def test_action_button_count_per_page(self, report_model: ReportModel, sec_id: str):
        """Verify each analytical page contains exactly 8 distinct actionButton visuals."""
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]
        buttons = section.action_buttons
        assert len(buttons) == 8, (
            f"Page '{sec_id}' must have exactly 8 actionButton visuals, found {len(buttons)}."
        )

    @pytest.mark.parametrize("sec_id", DOMAIN_MAPPING.keys())
    def test_action_buttons_geometry_and_navigation(self, report_model: ReportModel, sec_id: str):
        """
        Verify the 8 actionButton visuals on each page match the calibrated coordinates,
        drillFilterOtherVisuals: true, and target pageNavigation bindings.
        """
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]
        buttons = sorted(section.action_buttons, key=lambda b: b.y)

        assert len(buttons) == 8, f"Page '{sec_id}' does not have 8 action buttons."

        for i, expected_spec in enumerate(ACTION_BUTTON_SPECS):
            btn = buttons[i]
            slot = expected_spec["slot"]
            expected_y = expected_spec["y"]
            expected_target = expected_spec["target"]

            # Geometry check
            assert abs(btn.x - BUTTON_GEOMETRY["x"]) <= 1.0, (
                f"Page '{sec_id}', Button slot {slot}: expected X={BUTTON_GEOMETRY['x']}, got {btn.x}"
            )
            assert abs(btn.width - BUTTON_GEOMETRY["width"]) <= 2.0, (
                f"Page '{sec_id}', Button slot {slot}: expected Width={BUTTON_GEOMETRY['width']}, got {btn.width}"
            )
            assert abs(btn.height - BUTTON_GEOMETRY["height"]) <= 2.0, (
                f"Page '{sec_id}', Button slot {slot}: expected Height={BUTTON_GEOMETRY['height']}, got {btn.height}"
            )
            assert abs(btn.y - expected_y) <= 2.0, (
                f"Page '{sec_id}', Button slot {slot}: expected Y={expected_y}, got {btn.y}"
            )

            # DrillFilterOtherVisuals check
            assert btn.drill_filter_other_visuals is True, (
                f"Page '{sec_id}', Button slot {slot}: drillFilterOtherVisuals must be True"
            )

            # Navigation action check
            assert btn.action_type == "pageNavigation", (
                f"Page '{sec_id}', Button slot {slot}: action type must be 'pageNavigation', got '{btn.action_type}'"
            )
            assert btn.action_target == expected_target, (
                f"Page '{sec_id}', Button slot {slot}: navigation target must be '{expected_target}', "
                f"got '{btn.action_target}'"
            )
