# 🏥 PharmaForce 360° — Commercial Intelligence & Field Operations Suite
## Implementation & Architecture Plan (Full Egyptian Field Force Realism Edition)

---

## 🎯 Goal Description
Create an end-to-end pharmaceutical commercial intelligence project and Kaggle dataset tailored specifically to the **Greater Cairo Pharmaceutical Market** ($0.00 cost architecture):
1. **Dynamic Market Shocks & Rep Turnover**:
   - **Rep Turnover & Territory S-Curve Handover**: ~5 reps resign over 24 months. When a replacement rep takes over, territory performance initially **drops 5% to 10% below baseline** due to broken doctor rapport, followed by a **classic mathematical S-Curve (Sigmoid trust ramp-up)** over 90–120 days to fully return to territory potential.
   - **Supply Shortages & Competitor Windfall**: A 6-week import shortage on one company product, and a 6-week competitor stock-out windfall driving a +50% surge in our alternative brand.
2. **Egyptian Calendar & Seasonal Dynamics**:
   - **Work Week**: Saturday through Thursday (Friday strictly off).
   - **Ramadan Effect (2025 & 2026)**: Shifts hours to Post-Iftar (`20:30 – 23:30`), drops call completion by ~25%, and appropriately reduces monthly rep quotas.
   - **Cairo Winter Rainstorms**: Sporadic days across Dec–Feb causing traffic gridlock, resulting in a 12–18% dip in completed calls.
   - **Egyptian Public Holidays**: Eid El-Fitr, Eid El-Adha, 6th of October, Sham El-Nessim, and Coptic Christmas flagged with `Is_Public_Holiday = True` and zero scheduled calls.
3. **Territory-Weighted Marketing Budgets**: Promotional expense allowances in `fact_dr_expense` scale with brick importance and Tier A doctor concentration (Dokki/Mohandessin gets 180k–250k EGP/quarter; Shorouk gets 20k–35k EGP).
4. **Doctor Compliance Personas**: Models the real-world "Free Rider" problem (35% Loyal Champions, 35% Partial Converters, 20% Non-Compliant Free Riders who take the expense and write zero extra Rx, 10% Delayed Converters).
5. **Weekly Call Plan & Submission Delinquency (`fact_rep_weekly_plan`)**: Captures weekly visit plans with authentic field discipline (~60% on-time Saturday morning, ~20% late mid-week Mon/Tue, ~20% delinquent/no plan submitted).
6. **Product-Level Quotas (`fact_rep_targets`)**: Quotas broken down per drug (`Product_ID`) to enforce balanced product selling.
7. **Automated AM Institutional Accounts Pipeline (`src/extract_am_accounts.py`)**: Zero-cost OpenStreetMap Overpass extraction of Greater Cairo Hospitals, Bank HQs, and Corporate/Petroleum complexes, with spatial join to Greater Cairo bricks and rep allocation (2–3 AM accounts per rep).
8. **Doctor Tier Catchment Dispersion**: Tier A consultants radiate prescriptions broadly across Cairo (50% local / 32% neighborhood / 18% distal), while Tier C neighborhood clinics are hyper-local (88% filled within <300m).
9. **Supply Chain Socioeconomic Sensitivity**: Central bricks rely 90%+ on Big 5 distributors (*Ibn Sina, UCP, Soficopharm*), while peripheral bricks rely up to 45% on **Local Private Warehouses (المخازن)** (`DIST-06`).
10. **Pivoted Doctor Timetable Schedule (`dim_doctor_schedule`)**: Columns `Monday` through `Sunday` with explicit time ranges (`17:00 - 21:00`, `09:30 - 13:30`, or `Off`), strictly non-overlapping.
11. **The "Brick Effect" & Closed-Loop Detailing Verification**: Statistical correlation linking rep detailing and sample drops in Greater Cairo bricks to nearby pharmacy sell-out, verified in `fact_pharmacy_visits` linking back to `fact_rep_visits.Visit_ID`.
12. **Machine Learning Pipeline (`src/ml_pipeline.py`)**: Prescriber Churn Risk & Next-Best-Action visit prioritizer in `fact_doctor_predictions.csv`.
13. **Kaggle Dataset Package (10.0 Usability Score)**: Clean CSVs, metadata, data dictionary, and domain documentation.
14. **Power BI Project (`.pbip`) Architecture**: 5-page persona-driven report suite styled in Modern Clinical & Corporate Clean aesthetic (`#0A2540`, `#00A3E0`, `#F8FAFC`).

---

## ⚠️ User Review Required

> [!IMPORTANT]
> **New-Hire S-Curve Transition**:
> * When a new rep takes over a territory, performance initially dips **5% to 10% below the historical baseline** (due to relationship friction with doctors).
> * Performance then follows a mathematical **Sigmoid S-Curve**:
>   $$M(t) = 0.90 + \frac{0.15}{1 + e^{-0.08(t - 45)}}$$
>   Reaching full steady-state recovery by Day 90–120.

---

## 🏗️ Complete Master Tables (15 Tables)

1. `dim_date`: Calendar master (2025–2026, 24 months, Sat-Thu work week, Friday off, Ramadan flags, Egyptian holidays, weather events).
2. `dim_brick_territory`: 28 Greater Cairo bricks with centroid GPS and Socioeconomic Tiers (1 to 3).
3. `dim_account`: Master AM Accounts (Hospitals, Banks, Corporate Clinics) with allocated Rep IDs.
4. `dim_distributor`: Big 5 Egyptian Distributors (Ibn Sina, UCP, Soficopharm, PharmaOverseas, Ramco) + `DIST-06: Local Private Warehouses (المخازن)`.
5. `dim_product`: 2 Lines, 4 drugs each, 1 shared (`VascuPro`), plus competitor prices in EGP.
6. `dim_competitor_product`: Rival drugs, manufacturers, and benchmark prices in EGP.
7. `dim_medical_rep`: 32 Reps (tracking replacement flags, predecessor IDs, and hire dates).
8. `dim_doctor`: ~700 Doctors across 5 specialties, tiering (20% A, 40% B, 40% C), practice pattern (Daily vs Alternate).
9. `dim_doctor_schedule`: Pivoted timetable grid (`Monday`..`Sunday`) with time ranges and coordinates.
10. `dim_pharmacy`: ~550 Panel Pharmacies with coordinates and primary distributor preference.
11. `fact_rep_weekly_plan`: Weekly planned doctor visits with `Submission_Status` (*On-Time*, *Late Mid-Week*, *Missing*).
12. `fact_rep_visits`: ~45,000 Field Detailing Calls to Doctors (AM Hospital & PM Private Clinic), linked to `Plan_ID` with `Is_Planned_Visit` flag, influenced by Ramadan and weather.
13. `fact_pharmacy_visits`: ~15,000 Pharmacy Audits with **`Related_Doctor_Visit_ID`**, pharmacist sell-out feedback, stock-out observations, and transfer orders to Ibn Sina / UCP / المخازن.
14. `fact_pharmacy_sales`: Monthly pharmacy dispensing per drug in EGP, modeling the Brick Effect, stock-outs, and distributor fulfillment channel.
15. `fact_rep_targets`: Monthly sales quotas in EGP broken down **per drug** (`Product_ID`) and field activity targets.
16. `fact_dr_expense`: Promotional investments with `Expense_Kind`, `Amount_Of_Money` in EGP, and Doctor Compliance Personas (including "Free Riders").
17. `fact_ims_market_audit`: Audited monthly market share and Evolution Index (EI) per brick.
18. `fact_doctor_predictions`: ML Churn Risk & Next-Best-Action visit prioritizer.

---

## 🧪 Verification Plan
* Validate new-hire S-Curve: Assert a 5–10% drop below baseline in month 1 of replacement rep, followed by Sigmoidal recovery by month 3–4.
* Validate rep vacancy: Confirm 3–4 week visit drops in affected territories during handover windows.
* Validate shortage dynamics: Confirm 0 sales during shortage window and surge during competitor windfall.
* Verify 100% foreign key integrity across all tables and complete Kaggle 10.0 documentation checklist.
