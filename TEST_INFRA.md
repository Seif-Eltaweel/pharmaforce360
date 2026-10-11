# 🧪 PharmaForce 360° Navigation & Canvas Layer Test Infrastructure

> **Document**: `TEST_INFRA.md`  
> **Target**: Microsoft Power BI PBIP Project (`powerbi/PharmaForce360.Report`)  
> **Specification Reference**: `docs/navigation_bar_specification.md` & `.agents/teamwork/ORIGINAL_REQUEST.md`  
> **Status**: Test Suite Complete & Baseline Executed  
> **Author**: E2E Test Writer Agent (`teamwork_preview_test_writer`)  

---

## 1. Overview & Purpose

The **PharmaForce 360° E2E Navigation & Canvas Layer Test Suite** provides an authoritative, opaque-box verification harness designed to validate all requirements, geometry constraints, and acceptance criteria defined in `docs/navigation_bar_specification.md` and `ORIGINAL_REQUEST.md`.

The test harness evaluates:
1. **Global Theme Hardening & Transparency Enforcement (R1)**: Verifies explicit overrides for `actionButton`, `shape`, and `image` (`transparency: 100`, `border: [{"show": false}]`) in root and registered theme JSON files, preventing white box regressions.
2. **Eight-Domain Navigation Rail & Action Button Architecture (R2)**: Validates that all 8 analytical domains exist in `report.json` with calibrated SVG sidebars (`0, 0, 240, 720`) and 64 functional `actionButton` visuals (`X=12, W=216, H=40`, calibrated Y offsets, `pageNavigation` action bindings, `drillFilterOtherVisuals: true`).
3. **Canvas Grid Alignment & Collision Elimination (R3)**: Validates strict horizontal clearance ($X \ge 252$ px) across all analytical slicers, cards, and charts, vertical band compliance, and collision elimination.
4. **Schema & Integrity Verification (R4)**: Validates BOM-free UTF-8 encoding, PBIP JSON schema syntax, and produces a complete coordinate compliance audit matrix.

---

## 2. Directory Layout & File Inventory

```
D:\portfolio2026\02_PharmaForce360\
├── tests/
│   ├── __init__.py                         # Test package initializer
│   ├── helpers.py                          # Core data models, PBIP parsers, geometry constants & audit utils
│   ├── conftest.py                         # Pytest session fixtures (ReportModel, ThemeModel, SVG lists)
│   ├── test_r1_theme_hardening.py          # Pytest suite for Requirement R1
│   ├── test_r2_navigation_architecture.py  # Pytest suite for Requirement R2
│   ├── test_r3_canvas_grid_alignment.py    # Pytest suite for Requirement R3
│   ├── test_r4_schema_and_integrity.py     # Pytest suite for Requirement R4
│   └── verify_navigation_and_layout.py     # Standalone CLI test runner (zero external dependencies)
├── TEST_INFRA.md                           # Test infrastructure architecture & reference guide (this document)
└── TEST_READY.md                           # Verification readiness and baseline sign-off publication
```

---

## 3. Test Runner Architecture

### 3.1. Zero-Dependency Standalone Runner (`verify_navigation_and_layout.py`)
To enable execution in diverse CI/CD, containerized, and local developer environments without mandatory virtual environment setup or third-party packages, `tests/verify_navigation_and_layout.py` relies exclusively on the Python standard library (`json`, `pathlib`, `sys`, `dataclasses`, `typing`).

**Key capabilities**:
- Performs direct byte-level BOM detection (`\xef\xbb\xbf`, `\xff\xfe`, `\xfe\xff`).
- Decodes embedded PBIP JSON strings (`report.json["config"]`, section configs, visual container configs).
- Evaluates geometry tolerances ($X \pm 1.0$ px, $Y \pm 2.0$ px, $W \pm 2.0$ px, $H \pm 2.0$ px).
- Computes 2D Axis-Aligned Bounding Box (AABB) intersection algorithms to detect visual collisions.
- Outputs structured Markdown tables documenting visual coordinates, Z-order, and navigation targets.
- Returns standard process exit codes:
  - `0`: All requirements and acceptance criteria passed.
  - `1`: Any requirement or acceptance criterion failed.

### 3.2. Pytest Integration Suite (`tests/test_r*.py`)
The suite is also fully integrated with `pytest`, providing modular test discovery, parameterized checks per section, and detailed assert introspection.

---

## 4. Requirement-to-Test Mapping

| Req ID | Requirement Description | Test File | Key Test Methods | Authoritative Source |
|---|---|---|---|---|
| **R1** | Theme Hardening & Transparency | `tests/test_r1_theme_hardening.py` | `test_root_theme_action_button_override`<br/>`test_root_theme_shape_override`<br/>`test_root_theme_image_override`<br/>`test_registered_theme_action_button_override`<br/>`test_registered_theme_shape_override`<br/>`test_registered_theme_image_override`<br/>`test_sidebar_visuals_no_opaque_white_or_card_border` | `ORIGINAL_REQUEST.md` § R1<br/>`navigation_bar_specification.md` § 3 |
| **R2** | Eight-Domain Navigation Architecture | `tests/test_r2_navigation_architecture.py` | `test_eight_domain_sections_exist_in_report`<br/>`test_section_display_names`<br/>`test_static_svg_resources_registered`<br/>`test_static_svg_assets_exist_on_disk`<br/>`test_sidebar_backdrop_visual_per_page`<br/>`test_action_button_count_per_page`<br/>`test_action_buttons_geometry_and_navigation` | `ORIGINAL_REQUEST.md` § R2<br/>`navigation_bar_specification.md` § 2, 4.1, 5 |
| **R3** | Canvas Grid Alignment & Collision Elimination | `tests/test_r3_canvas_grid_alignment.py` | `test_analytical_visuals_horizontal_clearance`<br/>`test_visuals_within_canvas_boundary`<br/>`test_slicers_and_kpi_cards_no_vertical_overlap`<br/>`test_executive_overview_specific_band_alignment` | `ORIGINAL_REQUEST.md` § R3<br/>`navigation_bar_specification.md` § 4 |
| **R4** | Schema & Integrity Verification | `tests/test_r4_schema_and_integrity.py` | `test_theme_root_is_bom_free_utf8`<br/>`test_theme_registered_is_bom_free_utf8`<br/>`test_report_json_is_bom_free_utf8`<br/>`test_theme_root_valid_json`<br/>`test_theme_registered_valid_json`<br/>`test_report_json_pbip_structure`<br/>`test_coordinate_compliance_audit_matrix_generation` | `ORIGINAL_REQUEST.md` § R4 |

---

## 5. Execution Commands

### 5.1. Running via Standalone Test Runner
```bash
# From repository root (D:\portfolio2026\02_PharmaForce360)
python tests/verify_navigation_and_layout.py
```

### 5.2. Running via Pytest
```bash
# Execute full suite with verbose reporting
pytest tests/ -v

# Execute specific requirement suite
pytest tests/test_r1_theme_hardening.py -v
pytest tests/test_r2_navigation_architecture.py -v
pytest tests/test_r3_canvas_grid_alignment.py -v
pytest tests/test_r4_schema_and_integrity.py -v
```

---

## 6. Pre-Implementation Baseline Test Execution Results

Prior to implementing Milestones M1 through M5, the test suite was executed against the existing repository to establish the baseline failure state.

### 6.1. Baseline Summary Table
```
================================================================================
  TEST EXECUTION RESULTS SUMMARY (PRE-IMPLEMENTATION BASELINE)
================================================================================
[R4] ✓ PASS  | BOM-Free UTF-8 (powerbi/theme.json)           | Valid BOM-free UTF-8
[R4] ✓ PASS  | BOM-Free UTF-8 (PharmaForce360Theme.json)     | Valid BOM-free UTF-8
[R4] ✓ PASS  | BOM-Free UTF-8 (report.json)                  | Valid BOM-free UTF-8
[R4] ✓ PASS  | Valid JSON Syntax (powerbi/theme.json)        | Clean JSON parse (5 root keys)
[R4] ✓ PASS  | Valid JSON Syntax (PharmaForce360Theme.json)  | Clean JSON parse (5 root keys)
[R4] ✓ PASS  | Valid JSON Syntax (report.json)               | Clean JSON parse (3 root keys)
[R4] ✓ PASS  | PBIP Embedded Config Integrity                | All embedded visual configurations parse cleanly
[R1] ✗ FAIL  | Root Theme Override (actionButton)            | Missing 'actionButton' in visualStyles
[R1] ✗ FAIL  | Registered Theme Override (actionButton)      | Missing 'actionButton' in visualStyles
[R1] ✗ FAIL  | Root Theme Override (shape)                   | Missing 'shape' in visualStyles
[R1] ✗ FAIL  | Registered Theme Override (shape)             | Missing 'shape' in visualStyles
[R1] ✗ FAIL  | Root Theme Override (image)                   | Missing 'image' in visualStyles
[R1] ✗ FAIL  | Registered Theme Override (image)             | Missing 'image' in visualStyles
[R1] ✗ FAIL  | Sidebar Visual Transparency Enforcement       | Legacy sidebar textboxes & shapes inherit wildcard white style
[R2] ✗ FAIL  | Eight Domain Sections Exist                   | Missing 7 sections (Doctors, Reps, Bricks, Visits, Commercial, Stock, Expenses)
[R2] ✗ FAIL  | Section Display Names                         | Display names not aligned with 8-domain specification
[R2] ✗ FAIL  | SVG Resource Registration                     | 8 nav_sidebar_*.svg unregistered in resourcePackages
[R2] ✓ PASS  | SVG Assets On Disk                            | All 8 SVG files exist in RegisteredResources
[R2] ✗ FAIL  | Sidebar SVG Backdrop per Page                 | Missing SVG backdrop visual at (0, 0, 240, 720) across pages
[R2] ✗ FAIL  | Action Buttons Architecture (64 Total)        | 0/64 action buttons configured (legacy textboxes present)
[R3] ✗ FAIL  | Analytical Visuals Clearance (X >= 252)       | 16 visuals violate clearance (e.g. Slicer_Line X=226.4, Section2 X=20)
[R3] ✓ PASS  | Canvas 1280x720 Boundary Compliance           | All visuals fit within 1280 x 720 canvas
[R3] ✗ FAIL  | Zero Slicer / KPI Card Overlap                | Overlap detected on non-modernized sections
================================================================================
TOTAL CHECKS: 23 | PASSED: 9 | FAILED: 14
STATUS: BASELINE VERIFICATION FAILED (EXPECTED PRE-IMPLEMENTATION)
================================================================================
```

### 6.2. Baseline Defect Analysis
1. **Defect D1 (R1)**: Wildcard `"*"` rule in `theme.json` lacks explicit `actionButton`, `shape`, and `image` transparency overrides.
2. **Defect D2 (R2)**: Only 1 domain section (`Section_Executive_Overview`) exists with matching ID; remaining 7 analytical sections are named `Section2` through `Section5` or missing.
3. **Defect D3 (R2)**: Zero `actionButton` visuals are configured with `pageNavigation` (0 out of 64 present).
4. **Defect D4 (R2)**: Static SVGs are not registered in `report.json` `resourcePackages`.
5. **Defect D5 (R3)**: Analytical visual containers on Executive Overview begin at $X=226.4$ px and $X=215.0$ px instead of $X \ge 252.0$ px. Visuals on other sections begin at $X=20.0$ px.

---

## 7. Progressive Verification Plan by Milestone

| Milestone | Target Scope | Expected Passing Checks |
|---|---|---|
| **M1: Global Theme Hardening & Asset Registration** | `theme.json`, `PharmaForce360Theme.json`, `report.json.resourcePackages` | All R1 theme override checks pass (6/6). `SVG Resource Registration` passes. |
| **M2: Executive Overview Modernization & Grid Calibration** | `Section_Executive_Overview` | Backdrop at `(0,0,240,720)` passes for Overview. 8 actionButtons pass for Overview. Slicers, KPI cards, charts shift to $X \ge 252$. Band alignment passes. |
| **M3: Analytical Domains 02–05 Modernization** | `Section_Doctors_KOLs`, `Section_Medical_Reps`, `Section_Bricks_Territory`, `Section_Visits_Activity` | Sections 02–05 exist, display names pass, 32 action buttons pass, $X \ge 252$ passes for Domains 02–05. |
| **M4: Analytical Domains 06–08 Modernization** | `Section_Commercial_IQVIA`, `Section_Distributors_Stock`, `Section_Expenses_Budget` | Sections 06–08 exist, display names pass, 24 action buttons pass, $X \ge 252$ passes for Domains 06–08. (All 64 buttons pass). |
| **M5: Integrity Verification & Audit Matrix Sign-Off** | Full PBIP suite validation | 100% of checks pass (23/23). Coordinate compliance audit matrix verified. Exit code `0`. |
