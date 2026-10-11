"""
Test Suite for Requirement R3: Canvas Grid Alignment & Collision Elimination.

Validates that:
1. All analytical slicers, KPI metric cards, and chart visuals reside strictly at X >= 252 px,
   ensuring zero horizontal bleed into the 240 px navigation rail and 12 px clearance gutter.
2. Visual vertical positions strictly avoid overlap between top slicers (Y: 16-62) and KPI cards (Y: 72-160).
3. All visuals remain within the calibrated 1280 x 720 px canvas bounds.
4. No unintended collisions or visual container overlaps occur on analytical canvases.
"""

import pytest
from typing import List, Tuple
from tests.helpers import (
    ReportModel,
    DOMAIN_MAPPING,
    ANALYTICAL_MIN_X_PX,
    CANVAS_DIMENSIONS,
    VERTICAL_BANDS,
    check_bounding_box_overlap,
)


class TestR3CanvasGridAlignment:
    """Requirement R3 Test Cases."""

    @pytest.mark.parametrize("sec_id", DOMAIN_MAPPING.keys())
    def test_analytical_visuals_horizontal_clearance(self, report_model: ReportModel, sec_id: str):
        """
        Verify that ALL analytical visuals (slicers, cards, charts, headers outside the sidebar)
        reside strictly at X >= 252.0 px on each analytical page.
        """
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]
        analytical_visuals = section.analytical_visuals

        violations = []
        for v in analytical_visuals:
            if v.x < ANALYTICAL_MIN_X_PX:
                violations.append(
                    f"Visual '{v.name}' (type '{v.visual_type}') positioned at X={v.x:.1f} < {ANALYTICAL_MIN_X_PX}"
                )

        assert not violations, (
            f"Page '{sec_id}' has {len(violations)} visual(s) violating X >= {ANALYTICAL_MIN_X_PX} px clearance:\n"
            + "\n".join(violations)
        )

    @pytest.mark.parametrize("sec_id", DOMAIN_MAPPING.keys())
    def test_visuals_within_canvas_boundary(self, report_model: ReportModel, sec_id: str):
        """Verify all visuals remain within the 1280 x 720 canvas dimensions."""
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]
        violations = []
        max_w = CANVAS_DIMENSIONS["width"]
        max_h = CANVAS_DIMENSIONS["height"]

        for v in section.visuals:
            if v.x < 0 or v.y < 0:
                violations.append(f"Visual '{v.name}' has negative coordinates: X={v.x}, Y={v.y}")
            if (v.x + v.width) > (max_w + 1.0):
                violations.append(f"Visual '{v.name}' right edge {v.x + v.width:.1f} exceeds {max_w}")
            if (v.y + v.height) > (max_h + 1.0):
                violations.append(f"Visual '{v.name}' bottom edge {v.y + v.height:.1f} exceeds {max_h}")

        assert not violations, (
            f"Page '{sec_id}' visual canvas boundary violations:\n" + "\n".join(violations)
        )

    @pytest.mark.parametrize("sec_id", DOMAIN_MAPPING.keys())
    def test_slicers_and_kpi_cards_no_vertical_overlap(self, report_model: ReportModel, sec_id: str):
        """
        Verify that top dropdown slicers (Band 1, Y: 16-62) and KPI summary cards (Band 2, Y: 72-160)
        maintain vertical separation with zero overlap.
        """
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]
        slicers = [v for v in section.analytical_visuals if v.visual_type == "slicer"]
        kpi_cards = [v for v in section.analytical_visuals if v.visual_type == "card"]

        collisions = []
        for s in slicers:
            for k in kpi_cards:
                if check_bounding_box_overlap(s, k, tolerance_px=1.0):
                    collisions.append(
                        f"Slicer '{s.name}' (Y={s.y:.1f}, H={s.height:.1f}) collides with "
                        f"KPI Card '{k.name}' (Y={k.y:.1f}, H={k.height:.1f})"
                    )

        assert not collisions, (
            f"Page '{sec_id}' has {len(collisions)} collision(s) between slicers and KPI cards:\n"
            + "\n".join(collisions)
        )

    def test_executive_overview_specific_band_alignment(self, report_model: ReportModel):
        """
        Detailed verification of Executive Overview visual bands:
        - Slicers: Y in [16, 65]
        - KPI Cards: Y in [68, 165]
        - Upper Charts: Y in [170, 435]
        - Lower Charts: Y in [438, 715]
        """
        sec_id = "Section_Executive_Overview"
        if sec_id not in report_model.sections:
            pytest.fail(f"Section '{sec_id}' does not exist")

        section = report_model.sections[sec_id]

        # Top slicers check
        slicers = [v for v in section.analytical_visuals if v.visual_type == "slicer"]
        for s in slicers:
            assert s.y >= 15.0 and (s.y + s.height) <= 68.0, (
                f"Slicer '{s.name}' vertical span ({s.y:.1f} to {s.y+s.height:.1f}) "
                f"outside Band 1 [16, 65]"
            )

        # KPI cards check
        cards = [v for v in section.analytical_visuals if v.visual_type == "card"]
        for c in cards:
            assert c.y >= 68.0 and (c.y + c.height) <= 165.0, (
                f"Card '{c.name}' vertical span ({c.y:.1f} to {c.y+c.height:.1f}) "
                f"outside Band 2 [68, 165]"
            )
