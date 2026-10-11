# 📋 HANDOFF DOCUMENT: PharmaForce 360° Commercial Intelligence Suite

> **Target Session Purpose**: Starting the complete implementation in a fresh conversation.
> **Execution Engine**: **Google Colab Notebook (`notebooks/PharmaForce360_Data_Generator.ipynb`)** where **EACH CELL GENERATES A SINGLE TABLE**, followed by automated ZIP creation and 1-click browser download (Option A).
> **Workspace**: `d:\portfolio2026\`
> **Detailed Plan Reference**: [pharma_powerbi_kaggle_plan.md](file:///C:/Users/20106/.gemini/antigravity/brain/d5f2dd4f-76f4-4d45-a52d-2e7354d739ee/pharma_powerbi_kaggle_plan.md)

---

## 🎯 1. Executive Summary & Google Colab Strategy
Build an industry-standard, end-to-end synthetic pharmaceutical commercial intelligence dataset and Power BI platform for the **Greater Cairo Pharmaceutical Market (Egypt)** with all financial metrics in **Egyptian Pounds (EGP)**.

To maximize execution speed and transparency, the data will be generated in Google Colab via a **modular notebook** structured with **one dedicated cell per table**. Each cell prints `.head(2)` for visual inspection. The final cell bundles all 15 CSVs into a zip file and triggers an automatic browser download directly to your computer!

---

## 📓 2. Google Colab Notebook Cell Architecture (`PharmaForce360_Data_Generator.ipynb`)

| Cell # | Cell Responsibility & Output | Details & Realism Enforced |
|---|---|---|
| **Cell 1** | **Setup, Dependencies & Constants** | `!pip install faker pandas numpy scikit-learn lightgbm shap -q`, set `seed=42`, import libraries. |
| **Cell 2** | `dim_date.csv` | 24 Months (2025–2026), Sat–Thu work week (Friday off), Ramadan flags, Egyptian holidays (0 calls), winter rain events. |
| **Cell 3** | `dim_brick_territory.csv` | 36 Greater Cairo Bricks across Cairo, Giza, and southern Qalyubia (6 Zones) with centroid GPS coordinates and Socioeconomic Tiers (1 to 3). |
| **Cell 4** | `dim_account.csv` | Master AM Institutional Accounts (113 authentic Hospitals, Medical Centers & Specialized Institutes, 2–4 per brick). |
| **Cell 5** | `dim_distributor.csv` | Big 5 Distributors (*Ibn Sina, UCP, Soficopharm, PharmaOverseas, Ramco*) + *المخازن* (`DIST-06`). |
| **Cell 6** | `dim_product.csv` | 2 Lines, 4 drugs each, `VascuPro 50mg` shared (7 unique drugs), prices in EGP. |
| **Cell 7** | `dim_competitor_product.csv` | Rival drugs (*Concor, Crestor, Jardiance, Vastarel, Symbicort, Cipralex, Singulair*) with prices in EGP. |
| **Cell 8** | `dim_medical_rep.csv` | 32 Reps (16 Cardio, 16 Respiratory/Neuro), tracking predecessor IDs and replacement handover flags. |
| **Cell 9** | `dim_doctor.csv` | ~700 Doctors across 5 specialties (20% A / 40% B / 40% C), Daily vs Alternate-Day (Sat/Mon/Wed vs Sun/Tue/Thu) patterns. |
| **Cell 10** | `dim_doctor_schedule.csv` | **Pivoted Timetable Grid** (Columns: `Monday`..`Sunday` with time ranges like `"17:00 - 21:00"` or `"Off"`), with non-overlapping clinic validation. |
| **Cell 11** | `dim_pharmacy.csv` | ~550 Panel Pharmacies with coordinates, footfall, and primary distributor preference. |
| **Cell 12** | `fact_rep_weekly_plan.csv` | Weekly call plans (Sat–Thu cycle) capturing ~40% delinquency (~20% missing, ~20% late mid-week). |
| **Cell 13** | `fact_rep_visits.csv` | ~45,000 Field Detailing Calls (AM Hospital vs PM Private Clinic), Ramadan hours (`20:30–23:30`), rain traffic delays, and replacement rep S-curve dip. |
| **Cell 14** | `fact_pharmacy_visits.csv` | ~15,000 Pharmacy Audits with **`Related_Doctor_Visit_ID`** closed-loop verification, stock-outs, and transfer orders to Ibn Sina / UCP / المخازن. |
| **Cell 15** | `fact_pharmacy_sales.csv` | Monthly pharmacy dispensing in EGP, modeling the Brick Effect, Tier-weighted catchment radii, and supply shocks. |
| **Cell 16** | `fact_rep_targets.csv` | Monthly quotas broken down **per drug (`Product_ID`)** in EGP, calibrated to the Territory Potential Index. |
| **Cell 17** | `fact_dr_expense.csv` | Promotional investments in EGP (`Amount_Of_Money`), territory budget ceilings, and Doctor Compliance Personas (including 20% Free Riders). |
| **Cell 18** | `fact_ims_market_audit.csv` | Audited IQVIA monthly market share and Evolution Index (EI) per brick. |
| **Cell 19** | `fact_doctor_predictions.csv` | Python ML pipeline: Prescriber Churn Risk & Next-Best-Action visit prioritizer. |
| **Cell 20** | **Automated Integrity & Sanity Verification** | Runs automated assertions: zero overlapping doctor schedules, foreign key validation, S-curve dip verification. |
| **Cell 21** | 📦 **Option A: Auto-Zip & Download** | Zips all 15 CSVs and triggers `files.download('pharmaforce360_cairo_dataset.zip')` to your local computer! |

---

## 🛠️ 3. Suggested Skills for Next Agent
* `python-development` (for Jupyter notebook construction and data generation)
* `executing-plans` (to follow the cell-by-cell execution plan)
* `database-design` (for Star Schema integrity)
* `tdd-workflow` (for validation assertions)
* `data-storytelling` (for Kaggle 10.0 and Power BI assets)

---

## 🚀 4. Exact Action for Fresh Conversation
Open a new chat and simply type:
> *"Please read [d:/portfolio2026/HANDOFF.md](file:///d:/portfolio2026/HANDOFF.md) and build the Google Colab notebook `notebooks/PharmaForce360_Data_Generator.ipynb` following the cell-by-cell architecture and Option A auto-download."*
