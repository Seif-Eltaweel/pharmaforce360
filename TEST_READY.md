# 🚀 TEST_READY — PharmaForce 360° E2E Navigation & Layout Verification Suite

> **Published by**: E2E Test Writer (`teamwork_preview_test_writer`)  
> **Date**: 2026-10-11  
> **Status**: Verified Ready for TDD & Milestone Verification  
> **Scope**: Requirements R1, R2, R3, R4 per `docs/navigation_bar_specification.md` and `ORIGINAL_REQUEST.md`  

---

## 1. Readiness Confirmation

The E2E test harness and verification test runner for the PharmaForce 360° Power BI PBIP navigation overhaul are **complete, validated, and ready for use**.

The test suite strictly satisfies the **Progressive Testability** and **Test Integrity** protocols:
- **Zero Facade Tests**: All tests directly inspect physical PBIP files (`report.json`, `theme.json`, SVG assets) and execute mathematical geometry calculations.
- **Authoritative Derivation**: All expected coordinates, dimensions, internal section IDs, display titles, and action properties are derived verbatim from `docs/navigation_bar_specification.md` and `ORIGINAL_REQUEST.md`.
- **Baseline Validated**: Executed on the pre-implementation codebase. Fails accurately on all 14 expected defect areas (theme overrides missing, 7 domain sections missing, 0/64 action buttons configured, slicers and cards violating $X \ge 252$ px clearance). Passes on schema validity, BOM-free encoding, and physical SVG disk presence.

---

## 2. Test Execution Command

Implementers and orchestrators can execute the test suite at any point using the standalone test runner:

```bash
# Standalone CLI test runner (zero external dependencies)
python tests/verify_navigation_and_layout.py
```

Alternatively, if pytest is available:
```bash
pytest tests/ -v
```

---

## 3. Test Suite Inventory

| File Path | Requirement Scope | Test Count | Description |
|---|---|---|---|
| `tests/helpers.py` | Core Models & Parsers | - | PBIP models, coordinate extractors, AABB collision detection, and markdown audit matrix formatter |
| `tests/conftest.py` | Pytest Fixtures | - | Session fixtures for report, theme, and static assets |
| `tests/test_r1_theme_hardening.py` | Requirement R1 | 7 tests | Validates explicit transparency: 100 and border: false overrides for `actionButton`, `shape`, `image` in both themes |
| `tests/test_r2_navigation_architecture.py` | Requirement R2 | 7 tests | Validates 8 domain sections, display names, SVG registration, SVG backdrops, and 64 native action buttons |
| `tests/test_r3_canvas_grid_alignment.py` | Requirement R3 | 4 tests | Validates $X \ge 252$ px horizontal clearance, 1280x720 canvas bounds, and vertical band separation |
| `tests/test_r4_schema_and_integrity.py` | Requirement R4 | 7 tests | Validates BOM-free UTF-8 encoding, JSON syntax, PBIP structure, and generates coordinate audit matrix |
| `tests/verify_navigation_and_layout.py` | Comprehensive Runner | 23 checks | Standalone executable script generating summary report, coordinate audit table, and standard exit codes |

---

## 4. Quality Gate Criteria for Milestone Sign-Off

| Milestone | Gate Criteria | Verification Command |
|---|---|---|
| **M1: Theme Hardening & Asset Registration** | `powerbi/theme.json` and `PharmaForce360Theme.json` contain overrides for `actionButton`, `shape`, `image`. All 8 SVGs registered in `resourcePackages`. | `python tests/verify_navigation_and_layout.py` (R1 checks must pass 100%) |
| **M2: Executive Overview Modernization** | `Section_Executive_Overview` has `nav_sidebar_overview.svg` at (0, 0, 240, 720), 8 actionButtons configured, analytical visuals shifted to $X \ge 252$ px. | `python tests/verify_navigation_and_layout.py` (Executive Overview checks must pass) |
| **M3: Domains 02–05 Modernization** | Sections 02–05 exist, have SVG sidebars, 32 action buttons, and $X \ge 252$ px clearance. | `python tests/verify_navigation_and_layout.py` (Domains 02–05 pass) |
| **M4: Domains 06–08 Modernization** | Sections 06–08 exist, have SVG sidebars, 24 action buttons, and $X \ge 252$ px clearance. | `python tests/verify_navigation_and_layout.py` (Domains 06–08 pass) |
| **M5: Final Verification & Audit Matrix** | Full suite passes (23/23 checks pass, exit code 0). Coordinate audit matrix shows 0 violations across all 8 pages. | `python tests/verify_navigation_and_layout.py` (Exit code 0) |
