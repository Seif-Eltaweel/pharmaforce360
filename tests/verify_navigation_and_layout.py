#!/usr/bin/env python3
"""
PharmaForce 360° E2E Navigation & Canvas Layer Test Runner.

Executes comprehensive validation of Requirements R1 through R4:
  - R1: Global Theme Hardening & Transparency Enforcement
  - R2: Eight-Domain Navigation Rail & Action Button Architecture
  - R3: Canvas Grid Alignment & Collision Elimination
  - R4: Schema & Integrity Verification and Coordinate Compliance Audit

Zero external dependencies required (runs via standard library python).
Exit code 0 on all tests passed; exit code 1 on any test failure.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Ensure repository root is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.helpers import (
    DOMAIN_MAPPING,
    ACTION_BUTTON_SPECS,
    BUTTON_GEOMETRY,
    SIDEBAR_IMAGE_GEOMETRY,
    CANVAS_DIMENSIONS,
    SIDEBAR_WIDTH_PX,
    ANALYTICAL_MIN_X_PX,
    PATH_REPORT_JSON,
    PATH_THEME_ROOT,
    PATH_THEME_REGISTERED,
    DIR_REGISTERED_RESOURCES,
    check_bom_free_utf8,
    load_report_model,
    load_theme_model,
    check_bounding_box_overlap,
    audit_section_coordinates,
    format_audit_table_markdown,
    ReportModel,
    ThemeModel,
    VisualContainer,
)


# ==============================================================================
# Test Result Data Structures
# ==============================================================================

@dataclass
class TestResult:
    req_id: str
    name: str
    passed: bool
    message: str
    details: Optional[List[str]] = None


class TestRunner:
    def __init__(self, repo_root: Path = REPO_ROOT) -> None:
        self.repo_root = repo_root
        self.results: List[TestResult] = []
        self.report_model: Optional[ReportModel] = None
        self.root_theme: Optional[ThemeModel] = None
        self.registered_theme: Optional[ThemeModel] = None

    def log(self, msg: str) -> None:
        print(msg)

    def record(
        self,
        req_id: str,
        name: str,
        passed: bool,
        message: str,
        details: Optional[List[str]] = None,
    ) -> None:
        self.results.append(
            TestResult(
                req_id=req_id,
                name=name,
                passed=passed,
                message=message,
                details=details,
            )
        )

    # --------------------------------------------------------------------------
    # R1: Theme Hardening Checks
    # --------------------------------------------------------------------------
    def verify_r1_theme_hardening(self) -> None:
        self.log("\n[R1] Executing Theme Hardening & Transparency Checks...")

        # Helper to test theme visual override
        def check_theme_override(theme: ThemeModel, vtype: str, label: str) -> Tuple[bool, str]:
            if not theme or not theme.visual_styles:
                return False, f"{label}: visualStyles not loaded"
            if vtype not in theme.visual_styles:
                return False, f"{label}: missing '{vtype}' in visualStyles"
            star = theme.visual_styles[vtype].get("*", {})
            bg = star.get("background", [])
            trans = bg[0].get("transparency") if bg and isinstance(bg, list) else None
            border = star.get("border", [])
            b_show = border[0].get("show") if border and isinstance(border, list) else None

            if trans != 100:
                return False, f"{label}: '{vtype}' background transparency is {trans} (expected 100)"
            if b_show is not False:
                return False, f"{label}: '{vtype}' border show is {b_show} (expected False)"
            return True, f"{label}: '{vtype}' transparency:100, border.show:false"

        for vtype in ("actionButton", "shape", "image"):
            # Check root theme
            if self.root_theme:
                passed, msg = check_theme_override(self.root_theme, vtype, "powerbi/theme.json")
                self.record("R1", f"Root Theme Override ({vtype})", passed, msg)
            else:
                self.record("R1", f"Root Theme Override ({vtype})", False, "Failed to load powerbi/theme.json")

            # Check registered theme
            if self.registered_theme:
                passed, msg = check_theme_override(
                    self.registered_theme, vtype, "PharmaForce360Theme.json"
                )
                self.record("R1", f"Registered Theme Override ({vtype})", passed, msg)
            else:
                self.record("R1", f"Registered Theme Override ({vtype})", False, "Failed to load PharmaForce360Theme.json")

        # Check sidebar visual containers for white boxes in report.json
        if self.report_model:
            violations = []
            for sec_name, sec in self.report_model.sections.items():
                for v in sec.visuals:
                    if v.x < SIDEBAR_WIDTH_PX:
                        if v.bg_color and v.bg_color.upper() == "#FFFFFF" and (v.bg_transparency == 0 or v.bg_transparency is None):
                            violations.append(f"{sec_name} -> {v.name} has opaque white background")
                        if v.border_show is True:
                            violations.append(f"{sec_name} -> {v.name} has visible border")

            passed = len(violations) == 0
            msg = "Zero white box or card border styling regressions in sidebar" if passed else f"{len(violations)} sidebar visual styling regression(s)"
            self.record("R1", "Sidebar Visual Transparency Enforcement", passed, msg, violations)

    # --------------------------------------------------------------------------
    # R2: Navigation Rail & Action Buttons
    # --------------------------------------------------------------------------
    def verify_r2_navigation_rail(self) -> None:
        self.log("\n[R2] Executing Eight-Domain Navigation Rail & Action Button Checks...")

        if not self.report_model:
            self.record("R2", "Eight-Domain Architecture", False, "report.json not loaded")
            return

        # 1. 8 Domain Sections Exist
        missing_sections = []
        for sec_id in DOMAIN_MAPPING.keys():
            if sec_id not in self.report_model.sections:
                missing_sections.append(sec_id)
        passed = len(missing_sections) == 0
        msg = "All 8 analytical domain sections exist in report.json" if passed else f"Missing section(s): {missing_sections}"
        self.record("R2", "Eight Domain Sections Exist", passed, msg, missing_sections)

        # 2. Section Display Names
        display_mismatches = []
        for sec_id, meta in DOMAIN_MAPPING.items():
            if sec_id in self.report_model.sections:
                actual = self.report_model.sections[sec_id].display_name
                expected = meta["display_name"]
                if actual != expected:
                    display_mismatches.append(f"{sec_id}: expected '{expected}', got '{actual}'")
        passed = len(display_mismatches) == 0
        msg = "All 8 domain display names match specification" if passed else f"{len(display_mismatches)} display name mismatch(es)"
        self.record("R2", "Section Display Names", passed, msg, display_mismatches)

        # 3. Static SVG Resource Registration in report.json
        reg_items = {item.get("name") for item in self.report_model.registered_resources}
        missing_svg_reg = [m["svg_asset"] for m in DOMAIN_MAPPING.values() if m["svg_asset"] not in reg_items]
        passed = len(missing_svg_reg) == 0
        msg = "All 8 SVG sidebars registered in RegisteredResources" if passed else f"Unregistered SVG asset(s): {missing_svg_reg}"
        self.record("R2", "SVG Resource Registration", passed, msg, missing_svg_reg)

        # 4. Static SVG files on disk
        missing_disk = []
        for m in DOMAIN_MAPPING.values():
            if not (DIR_REGISTERED_RESOURCES / m["svg_asset"]).is_file():
                missing_disk.append(m["svg_asset"])
        passed = len(missing_disk) == 0
        msg = "All 8 SVG asset files exist on disk" if passed else f"Missing on disk: {missing_disk}"
        self.record("R2", "SVG Assets On Disk", passed, msg, missing_disk)

        # 5. Sidebar SVG Backdrop on each of the 8 pages
        backdrop_fails = []
        for sec_id, meta in DOMAIN_MAPPING.items():
            if sec_id not in self.report_model.sections:
                backdrop_fails.append(f"{sec_id}: section does not exist")
                continue
            sec = self.report_model.sections[sec_id]
            backdrop = sec.sidebar_backdrop
            if not backdrop:
                backdrop_fails.append(f"{sec_id}: missing SVG backdrop image at (0, 0, 240, 720)")
            else:
                expected_svg = meta["svg_asset"]
                if backdrop.image_resource_name and expected_svg not in backdrop.image_resource_name:
                    backdrop_fails.append(f"{sec_id}: backdrop binds to '{backdrop.image_resource_name}', expected '{expected_svg}'")

        passed = len(backdrop_fails) == 0
        msg = "All 8 pages contain calibrated SVG backdrop image" if passed else f"{len(backdrop_fails)} page(s) missing/invalid backdrop"
        self.record("R2", "Sidebar SVG Backdrop per Page", passed, msg, backdrop_fails)

        # 6. 8 Distinct Action Buttons per page (Total 64)
        button_fails = []
        total_buttons_found = 0
        for sec_id in DOMAIN_MAPPING.keys():
            if sec_id not in self.report_model.sections:
                button_fails.append(f"{sec_id}: section does not exist")
                continue
            sec = self.report_model.sections[sec_id]
            buttons = sorted(sec.action_buttons, key=lambda b: b.y)
            total_buttons_found += len(buttons)

            if len(buttons) != 8:
                button_fails.append(f"{sec_id}: expected 8 action buttons, found {len(buttons)}")
                continue

            for i, spec in enumerate(ACTION_BUTTON_SPECS):
                btn = buttons[i]
                slot = spec["slot"]
                expected_y = spec["y"]
                expected_target = spec["target"]

                if abs(btn.x - BUTTON_GEOMETRY["x"]) > 1.0 or abs(btn.width - BUTTON_GEOMETRY["width"]) > 2.0 or abs(btn.height - BUTTON_GEOMETRY["height"]) > 2.0:
                    button_fails.append(f"{sec_id} Slot {slot}: invalid geometry (X={btn.x}, W={btn.width}, H={btn.height})")
                if abs(btn.y - expected_y) > 2.0:
                    button_fails.append(f"{sec_id} Slot {slot}: Y={btn.y} != expected {expected_y}")
                if not btn.drill_filter_other_visuals:
                    button_fails.append(f"{sec_id} Slot {slot}: drillFilterOtherVisuals is not True")
                if btn.action_type != "pageNavigation":
                    button_fails.append(f"{sec_id} Slot {slot}: action type is '{btn.action_type}', expected 'pageNavigation'")
                if btn.action_target != expected_target:
                    button_fails.append(f"{sec_id} Slot {slot}: target '{btn.action_target}', expected '{expected_target}'")

        passed = len(button_fails) == 0
        msg = f"All 64 action buttons calibrated with native pageNavigation (found {total_buttons_found}/64)" if passed else f"{len(button_fails)} button calibration defect(s)"
        self.record("R2", "Action Buttons Architecture (64 Total)", passed, msg, button_fails)

    # --------------------------------------------------------------------------
    # R3: Canvas Grid Alignment & Collision Elimination
    # --------------------------------------------------------------------------
    def verify_r3_canvas_layout(self) -> None:
        self.log("\n[R3] Executing Canvas Grid Alignment & Collision Checks...")

        if not self.report_model:
            self.record("R3", "Canvas Grid Alignment", False, "report.json not loaded")
            return

        # 1. Horizontal Clearance (X >= 252 px)
        clearance_fails = []
        for sec_id in DOMAIN_MAPPING.keys():
            if sec_id not in self.report_model.sections:
                continue
            sec = self.report_model.sections[sec_id]
            for v in sec.analytical_visuals:
                if v.x < ANALYTICAL_MIN_X_PX:
                    clearance_fails.append(f"{sec_id} -> {v.name} ({v.visual_type}) at X={v.x:.1f} < {ANALYTICAL_MIN_X_PX}")

        passed = len(clearance_fails) == 0
        msg = f"All analytical visuals observe X >= {ANALYTICAL_MIN_X_PX} px clearance" if passed else f"{len(clearance_fails)} visual clearance violation(s)"
        self.record("R3", "Analytical Visuals Horizontal Clearance (X >= 252)", passed, msg, clearance_fails)

        # 2. Canvas Boundaries (1280 x 720)
        bound_fails = []
        for sec_id in DOMAIN_MAPPING.keys():
            if sec_id not in self.report_model.sections:
                continue
            sec = self.report_model.sections[sec_id]
            for v in sec.visuals:
                if v.x < 0 or v.y < 0 or (v.x + v.width) > (CANVAS_DIMENSIONS["width"] + 1.0) or (v.y + v.height) > (CANVAS_DIMENSIONS["height"] + 1.0):
                    bound_fails.append(f"{sec_id} -> {v.name} outside 1280x720 (X={v.x}, Y={v.y}, W={v.width}, H={v.height})")

        passed = len(bound_fails) == 0
        msg = "All visuals fit cleanly within 1280 x 720 canvas bounds" if passed else f"{len(bound_fails)} boundary violation(s)"
        self.record("R3", "Canvas 1280x720 Boundary Compliance", passed, msg, bound_fails)

        # 3. Top Slicer and KPI Summary Card Collision Check
        collision_fails = []
        for sec_id in DOMAIN_MAPPING.keys():
            if sec_id not in self.report_model.sections:
                continue
            sec = self.report_model.sections[sec_id]
            slicers = [v for v in sec.analytical_visuals if v.visual_type == "slicer"]
            kpis = [v for v in sec.analytical_visuals if v.visual_type == "card"]
            for s in slicers:
                for k in kpis:
                    if check_bounding_box_overlap(s, k, tolerance_px=1.0):
                        collision_fails.append(f"{sec_id} -> Slicer '{s.name}' collides with KPI '{k.name}'")

        passed = len(collision_fails) == 0
        msg = "Zero vertical overlap between top slicers (Y: 16-62) and KPI cards (Y: 72-160)" if passed else f"{len(collision_fails)} slicer/KPI collision(s)"
        self.record("R3", "Zero Slicer / KPI Card Overlap", passed, msg, collision_fails)

    # --------------------------------------------------------------------------
    # R4: Schema & Integrity Verification
    # --------------------------------------------------------------------------
    def verify_r4_schema_integrity(self) -> None:
        self.log("\n[R4] Executing Schema, Encoding & Audit Matrix Verification...")

        # 1. BOM-free UTF-8 checks
        for p, label in [
            (PATH_THEME_ROOT, "powerbi/theme.json"),
            (PATH_THEME_REGISTERED, "PharmaForce360Theme.json"),
            (PATH_REPORT_JSON, "powerbi/PharmaForce360.Report/report.json"),
        ]:
            passed, msg = check_bom_free_utf8(p)
            self.record("R4", f"BOM-Free UTF-8 ({label})", passed, msg)

        # 2. JSON syntax checks
        for p, label in [
            (PATH_THEME_ROOT, "powerbi/theme.json"),
            (PATH_THEME_REGISTERED, "PharmaForce360Theme.json"),
            (PATH_REPORT_JSON, "report.json"),
        ]:
            if p.is_file():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.record("R4", f"Valid JSON Syntax ({label})", True, f"Clean JSON parse ({len(data)} root keys)")
                except Exception as e:
                    self.record("R4", f"Valid JSON Syntax ({label})", False, f"JSON decode error: {e}")
            else:
                self.record("R4", f"Valid JSON Syntax ({label})", False, f"File not found: {p}")

        # 3. PBIP Embedded Config Integrity
        if self.report_model:
            config_errors = []
            for sec_name, sec in self.report_model.sections.items():
                for v in sec.visuals:
                    if not v.raw_config:
                        config_errors.append(f"{sec_name} -> visual config invalid")
            passed = len(config_errors) == 0
            msg = "All embedded visual configurations parse cleanly as JSON" if passed else f"{len(config_errors)} invalid configs"
            self.record("R4", "PBIP Embedded Config Integrity", passed, msg, config_errors)

    # --------------------------------------------------------------------------
    # Main Execution Flow
    # --------------------------------------------------------------------------
    def run_all(self) -> int:
        self.log("=" * 80)
        self.log("  PHARMAFORCE 360° E2E VERIFICATION TEST RUNNER")
        self.log("  Target: Navigation Bar & Canvas Layer Architecture")
        self.log(f"  Working Directory: {self.repo_root}")
        self.log("=" * 80)

        # Pre-load models
        try:
            self.report_model = load_report_model(PATH_REPORT_JSON)
        except Exception as e:
            self.log(f"[WARN] Failed to parse report.json: {e}")

        try:
            self.root_theme = load_theme_model(PATH_THEME_ROOT)
        except Exception as e:
            self.log(f"[WARN] Failed to parse root theme: {e}")

        try:
            self.registered_theme = load_theme_model(PATH_THEME_REGISTERED)
        except Exception as e:
            self.log(f"[WARN] Failed to parse registered theme: {e}")

        # Run Requirements
        self.verify_r4_schema_integrity()
        self.verify_r1_theme_hardening()
        self.verify_r2_navigation_rail()
        self.verify_r3_canvas_layout()

        # Print Test Results Summary
        self.log("\n" + "=" * 80)
        self.log("  TEST EXECUTION RESULTS SUMMARY")
        self.log("=" * 80)

        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = sum(1 for r in self.results if not r.passed)
        total_count = len(self.results)

        for r in self.results:
            icon = "✓ PASS" if r.passed else "✗ FAIL"
            self.log(f"[{r.req_id}] {icon:<7} | {r.name:<45} | {r.message}")
            if not r.passed and r.details:
                for d in r.details[:5]:
                    self.log(f"       -> {d}")
                if len(r.details) > 5:
                    self.log(f"       -> ... and {len(r.details) - 5} more defect(s)")

        # Coordinate Compliance Audit Table
        self.log("\n" + "=" * 80)
        self.log("  COORDINATE COMPLIANCE AUDIT MATRIX")
        self.log("=" * 80)

        all_audit_entries = []
        if self.report_model:
            for sec_name, sec in self.report_model.sections.items():
                if sec_name in DOMAIN_MAPPING:
                    all_audit_entries.extend(audit_section_coordinates(sec))

        if all_audit_entries:
            table_md = format_audit_table_markdown(all_audit_entries)
            self.log(table_md)
        else:
            self.log("No analytical visual entries available for coordinate audit.")

        self.log("\n" + "=" * 80)
        self.log(f"TOTAL TESTS: {total_count} | PASSED: {passed_count} | FAILED: {failed_count}")
        status_banner = "ALL REQUIREMENTS PASSED" if failed_count == 0 else "BASELINE VERIFICATION FAILED (EXPECTED PRE-IMPLEMENTATION)"
        self.log(f"STATUS: {status_banner}")
        self.log("=" * 80 + "\n")

        return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    runner = TestRunner()
    sys.exit(runner.run_all())
