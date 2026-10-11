# Dispatch for E2E Test Writer 1

- **Role**: E2E Test Writer (teamwork_preview_test_writer)
- **Working Directory**: D:\portfolio2026\02_PharmaForce360\.agents\teamwork\test_writer_1
- **Project Directory**: D:\portfolio2026\02_PharmaForce360
- **Task**: Create E2E Test Infrastructure and Test Suite per ORIGINAL_REQUEST.md and PROJECT.md.

## 2026-10-11T05:24:01Z
You are the E2E Test Writer (teamwork_preview_test_writer).
Your working directory is: D:\portfolio2026\02_PharmaForce360\.agents\teamwork\test_writer_1
Your parent is: orchestrator_1 (Conversation ID: 177edf21-9ef8-4c4c-8bbf-cd906fdef733)

MANDATORY FIRST STEP: Read the user request at D:\portfolio2026\02_PharmaForce360\.agents\teamwork\ORIGINAL_REQUEST.md, the specification at D:\portfolio2026\02_PharmaForce360\docs\navigation_bar_specification.md, and the project scope at D:\portfolio2026\02_PharmaForce360\.agents\teamwork\orchestrator_1\PROJECT.md.

Scope & Mission (E2E Testing Track):
Design and implement a comprehensive opaque-box test suite and test runner that validates all requirements and acceptance criteria in ORIGINAL_REQUEST.md:
1. Requirement R1: Global Theme Hardening & Transparency Enforcement
   - Verify powerbi/theme.json and PharmaForce360Theme.json contain explicit overrides for actionButton, shape, and image with transparency: 100 and border: [{"show": false}].
   - Verify no visual within sidebar coordinates (X <= 240) inherits opaque white background or border.
2. Requirement R2: Eight-Domain Navigation Rail & Action Button Architecture
   - Verify all 8 analytical domains exist in report.json with matching internal names (Section_Executive_Overview, Section_Doctors_KOLs, Section_Medical_Reps, Section_Bricks_Territory, Section_Visits_Activity, Section_Commercial_IQVIA, Section_Distributors_Stock, Section_Expenses_Budget) and correct display names.
   - Verify each of the 8 pages contains the corresponding nav_sidebar_<page>.svg visual at (0, 0, 240, 720).
   - Verify each of the 8 pages contains 8 distinct actionButton visuals at X=12, W=216, H=40, positioned at Y=134, 188, 242, 296, 350, 404, 458, 512 with drillFilterOtherVisuals: true and active pageNavigation actions.
3. Requirement R3: Canvas Grid Alignment & Collision Elimination
   - Verify all analytical slicers, KPI metric cards, and charts reside strictly at X >= 252 px.
   - Verify zero overlap between top slicers (Y: 16-62) and KPI cards (Y: 72-160), and lower charts.
4. Requirement R4: Schema & Integrity Verification
   - Verify report.json and theme.json are BOM-free UTF-8 and valid JSON.
   - Generate and output a coordinate compliance audit table.

Deliverables:
- Create test runner script (e.g. tests/verify_navigation_and_layout.py or similar in tests/ directory).
- Execute the test runner to establish baseline test status (should fail on current pre-implementation state).
- Create D:\portfolio2026\02_PharmaForce360\TEST_INFRA.md and publish D:\portfolio2026\02_PharmaForce360\TEST_READY.md.
- Write handoff report to D:\portfolio2026\02_PharmaForce360\.agents\teamwork\test_writer_1\handoff.md with test execution command and initial baseline failure results.
- Send completion message to parent.
