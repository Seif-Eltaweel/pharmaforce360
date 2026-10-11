"""
Test Suite for Requirement R1: Global Theme Hardening & Transparency Enforcement.

Validates that:
1. Both powerbi/theme.json and PharmaForce360Theme.json contain explicit overrides
   for actionButton, shape, and image with transparency: 100 and border: [{"show": false}].
2. No visual within sidebar coordinates (X <= 240) inherits or declares an opaque white
   background or visible border card style.
"""

import pytest
from typing import Any, Dict
from tests.helpers import (
    ThemeModel,
    ReportModel,
    SIDEBAR_WIDTH_PX,
)


def _assert_theme_override(theme: ThemeModel, visual_type: str, theme_label: str) -> None:
    """Helper asserting that a theme contains the required transparency & border override."""
    styles = theme.visual_styles
    assert visual_type in styles, (
        f"[{theme_label}] Missing visualStyles override for visualType '{visual_type}'. "
        f"Available styles: {list(styles.keys())}"
    )

    type_styles = styles[visual_type]
    assert "*" in type_styles, (
        f"[{theme_label}] visualStyles['{visual_type}'] must contain wildcard selector '*'."
    )
    star_rules = type_styles["*"]

    # 1. Background transparency: 100
    assert "background" in star_rules, (
        f"[{theme_label}] visualStyles['{visual_type}']['*'] missing 'background' rule."
    )
    bg_rule = star_rules["background"]
    assert isinstance(bg_rule, list) and len(bg_rule) > 0, (
        f"[{theme_label}] 'background' must be a non-empty list."
    )
    bg_transparency = bg_rule[0].get("transparency")
    assert bg_transparency == 100, (
        f"[{theme_label}] visualStyles['{visual_type}'] background transparency must be 100, "
        f"got: {bg_transparency}"
    )

    # 2. Border show: false
    assert "border" in star_rules, (
        f"[{theme_label}] visualStyles['{visual_type}']['*'] missing 'border' rule."
    )
    border_rule = star_rules["border"]
    assert isinstance(border_rule, list) and len(border_rule) > 0, (
        f"[{theme_label}] 'border' must be a non-empty list."
    )
    border_show = border_rule[0].get("show")
    assert border_show is False, (
        f"[{theme_label}] visualStyles['{visual_type}'] border show must be False, "
        f"got: {border_show}"
    )


class TestR1ThemeHardening:
    """Requirement R1 Test Cases."""

    def test_root_theme_action_button_override(self, root_theme: ThemeModel):
        """Verify powerbi/theme.json overrides actionButton with 100% transparency and border disabled."""
        _assert_theme_override(root_theme, "actionButton", "powerbi/theme.json")

    def test_root_theme_shape_override(self, root_theme: ThemeModel):
        """Verify powerbi/theme.json overrides shape with 100% transparency and border disabled."""
        _assert_theme_override(root_theme, "shape", "powerbi/theme.json")

    def test_root_theme_image_override(self, root_theme: ThemeModel):
        """Verify powerbi/theme.json overrides image with 100% transparency and border disabled."""
        _assert_theme_override(root_theme, "image", "powerbi/theme.json")

    def test_registered_theme_action_button_override(self, registered_theme: ThemeModel):
        """Verify PharmaForce360Theme.json overrides actionButton with 100% transparency and border disabled."""
        _assert_theme_override(registered_theme, "actionButton", "PharmaForce360Theme.json")

    def test_registered_theme_shape_override(self, registered_theme: ThemeModel):
        """Verify PharmaForce360Theme.json overrides shape with 100% transparency and border disabled."""
        _assert_theme_override(registered_theme, "shape", "PharmaForce360Theme.json")

    def test_registered_theme_image_override(self, registered_theme: ThemeModel):
        """Verify PharmaForce360Theme.json overrides image with 100% transparency and border disabled."""
        _assert_theme_override(registered_theme, "image", "PharmaForce360Theme.json")

    def test_sidebar_visuals_no_opaque_white_or_card_border(self, report_model: ReportModel):
        """
        Verify no visual located in the sidebar coordinates (X <= 240) defines an opaque white
        background (#FFFFFF with transparency 0) or visible card border.
        """
        violations = []
        for sec_name, sec in report_model.sections.items():
            for v in sec.visuals:
                if v.x < SIDEBAR_WIDTH_PX:
                    # Check background opacity
                    is_opaque_white = (
                        v.bg_color is not None
                        and v.bg_color.upper() == "#FFFFFF"
                        and (v.bg_transparency == 0 or v.bg_transparency is None)
                    )
                    # Check border visibility
                    is_border_visible = v.border_show is True

                    if is_opaque_white:
                        violations.append(
                            f"Page '{sec_name}', visual '{v.name}' (type {v.visual_type}, X={v.x:.1f}) "
                            f"has opaque white background (#FFFFFF, transparency={v.bg_transparency})"
                        )
                    if is_border_visible:
                        violations.append(
                            f"Page '{sec_name}', visual '{v.name}' (type {v.visual_type}, X={v.x:.1f}) "
                            f"has visible card border (border.show=true)"
                        )

        assert not violations, (
            f"Found {len(violations)} sidebar visual styling regression(s):\n"
            + "\n".join(violations)
        )
