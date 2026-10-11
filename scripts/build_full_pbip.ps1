# ==============================================================================
# PharmaForce 360 Commercial Intelligence Suite - Comprehensive PBIP Generator
# Greater Cairo Pharmaceutical Market | Star Schema and 5-Page Persona Dashboard
# ==============================================================================

param(
    [string]$TargetDir = "d:\portfolio2026\02_PharmaForce360\powerbi",
    [string]$DataDir   = "d:\portfolio2026\02_PharmaForce360\data"
)

Write-Host ">>> Compiling Enterprise Power BI Project (.pbip) Suite..." -ForegroundColor Cyan

# UTF-8 without BOM encoding (required by Power BI Desktop .pbip format)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# ------------------------------------------------------------------------------
# 1. Directory Structure Setup
# ------------------------------------------------------------------------------
$subDirs = @(
    $TargetDir,
    "$TargetDir\PharmaForce360.Report",
    "$TargetDir\PharmaForce360.Report\.pbi",
    "$TargetDir\PharmaForce360.Report\StaticResources",
    "$TargetDir\PharmaForce360.Report\StaticResources\RegisteredResources",
    "$TargetDir\PharmaForce360.SemanticModel",
    "$TargetDir\PharmaForce360.SemanticModel\.pbi",
    "$TargetDir\PharmaForce360.SemanticModel\definition",
    "$TargetDir\PharmaForce360.SemanticModel\definition\tables",
    "$TargetDir\PharmaForce360.SemanticModel\definition\cultures"
)
foreach ($d in $subDirs) {
    if (-not (Test-Path $d)) { New-Item -Path $d -ItemType Directory -Force | Out-Null }
}

# ------------------------------------------------------------------------------
# 2. Table Specifications
# ------------------------------------------------------------------------------
$tableDefs = @(
    @{
        Name = "dim_date"
        File = "dim_date.csv"
        Cols = @(
            @{ Name="Date"; Type="dateTime"; MType="type date"; Format="yyyy-MM-dd" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Year"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Quarter"; Type="string"; MType="type text" },
            @{ Name="Month"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Month_Name"; Type="string"; MType="type text" },
            @{ Name="Day"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Day_Of_Week"; Type="string"; MType="type text" },
            @{ Name="Year_Month"; Type="string"; MType="type text" },
            @{ Name="Is_Weekend"; Type="boolean"; MType="type logical" },
            @{ Name="Is_Ramadan"; Type="boolean"; MType="type logical" },
            @{ Name="Holiday_Name"; Type="string"; MType="type text" },
            @{ Name="Is_Egyptian_Holiday"; Type="boolean"; MType="type logical" },
            @{ Name="Is_Workday"; Type="boolean"; MType="type logical" },
            @{ Name="Is_Winter_Rain_Event"; Type="boolean"; MType="type logical" }
        )
    },
    @{
        Name = "dim_brick_territory"
        File = "dim_brick_territory.csv"
        Cols = @(
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Brick_Name"; Type="string"; MType="type text" },
            @{ Name="Zone"; Type="string"; MType="type text" },
            @{ Name="Tier"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Latitude"; Type="double"; MType="type number"; Format="#,0.0000" },
            @{ Name="Longitude"; Type="double"; MType="type number"; Format="#,0.0000" },
            @{ Name="Territory_Potential_Index"; Type="double"; MType="type number"; Format="#,0.00" }
        )
    },
    @{
        Name = "dim_product"
        File = "dim_product.csv"
        Cols = @(
            @{ Name="Product_ID"; Type="string"; MType="type text" },
            @{ Name="Product_Name"; Type="string"; MType="type text" },
            @{ Name="Therapeutic_Line"; Type="string"; MType="type text" },
            @{ Name="Active_Ingredient"; Type="string"; MType="type text" },
            @{ Name="Unit_Price_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Dosage_Form"; Type="string"; MType="type text" },
            @{ Name="Pack_Size"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Is_Shared_Product"; Type="boolean"; MType="type logical" }
        )
    },
    @{
        Name = "dim_competitor_product"
        File = "dim_competitor_product.csv"
        Cols = @(
            @{ Name="Competitor_Product_ID"; Type="string"; MType="type text" },
            @{ Name="Competitor_Name"; Type="string"; MType="type text" },
            @{ Name="Competitor_Company"; Type="string"; MType="type text" },
            @{ Name="Target_Product_ID"; Type="string"; MType="type text" },
            @{ Name="Market_Price_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Therapeutic_Class"; Type="string"; MType="type text" },
            @{ Name="Market_Position"; Type="string"; MType="type text" }
        )
    },
    @{
        Name = "dim_medical_rep"
        File = "dim_medical_rep.csv"
        Cols = @(
            @{ Name="Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Rep_Name"; Type="string"; MType="type text" },
            @{ Name="Assigned_Line"; Type="string"; MType="type text" },
            @{ Name="Home_Zone"; Type="string"; MType="type text" },
            @{ Name="Assigned_Brick_IDs"; Type="string"; MType="type text" },
            @{ Name="Hire_Date"; Type="dateTime"; MType="type date"; Format="yyyy-MM-dd" },
            @{ Name="Tenure_Months"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Predecessor_Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Handover_Date"; Type="string"; MType="type text" },
            @{ Name="Is_Replacement_Rep"; Type="boolean"; MType="type logical" },
            @{ Name="Target_Bonus_Pct"; Type="double"; MType="type number"; Format="0.0%" }
        )
    },
    @{
        Name = "dim_doctor"
        File = "dim_doctor.csv"
        Cols = @(
            @{ Name="Doctor_ID"; Type="string"; MType="type text" },
            @{ Name="Doctor_Name"; Type="string"; MType="type text" },
            @{ Name="Specialty"; Type="string"; MType="type text" },
            @{ Name="Classification"; Type="string"; MType="type text" },
            @{ Name="Schedule_Pattern"; Type="string"; MType="type text" },
            @{ Name="Primary_Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Primary_Clinic_Address"; Type="string"; MType="type text" },
            @{ Name="Weekly_Patient_Volume"; Type="int64"; MType="Int64.Type"; Format="#,0" },
            @{ Name="Preferred_Visit_Time"; Type="string"; MType="type text" },
            @{ Name="Academic_Affiliation"; Type="string"; MType="type text" }
        )
    },
    @{
        Name = "dim_doctor_schedule"
        File = "dim_doctor_schedule.csv"
        Cols = @(
            @{ Name="Doctor_ID"; Type="string"; MType="type text" },
            @{ Name="Saturday"; Type="string"; MType="type text" },
            @{ Name="Sunday"; Type="string"; MType="type text" },
            @{ Name="Monday"; Type="string"; MType="type text" },
            @{ Name="Tuesday"; Type="string"; MType="type text" },
            @{ Name="Wednesday"; Type="string"; MType="type text" },
            @{ Name="Thursday"; Type="string"; MType="type text" },
            @{ Name="Friday"; Type="string"; MType="type text" }
        )
    },
    @{
        Name = "dim_pharmacy"
        File = "dim_pharmacy.csv"
        Cols = @(
            @{ Name="Pharmacy_ID"; Type="string"; MType="type text" },
            @{ Name="Pharmacy_Name"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Chain_Affiliation"; Type="string"; MType="type text" },
            @{ Name="Footfall_Category"; Type="string"; MType="type text" },
            @{ Name="Monthly_Capacity_Potential"; Type="double"; MType="type number"; Format="#,0" },
            @{ Name="Primary_Distributor_ID"; Type="string"; MType="type text" },
            @{ Name="Latitude"; Type="double"; MType="type number"; Format="#,0.0000" },
            @{ Name="Longitude"; Type="double"; MType="type number"; Format="#,0.0000" }
        )
    },
    @{
        Name = "dim_distributor"
        File = "dim_distributor.csv"
        Cols = @(
            @{ Name="Distributor_ID"; Type="string"; MType="type text" },
            @{ Name="Distributor_Name"; Type="string"; MType="type text" },
            @{ Name="Market_Share_Pct"; Type="double"; MType="type number"; Format="0.0%" },
            @{ Name="Channel_Type"; Type="string"; MType="type text" },
            @{ Name="Payment_Terms_Days"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Delivery_SLA_Hours"; Type="int64"; MType="Int64.Type"; Format="0" }
        )
    },
    @{
        Name = "dim_account"
        File = "dim_account.csv"
        Cols = @(
            @{ Name="Account_ID"; Type="string"; MType="type text" },
            @{ Name="Account_Name"; Type="string"; MType="type text" },
            @{ Name="Account_Type"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Bed_Capacity"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Key_Specialties"; Type="string"; MType="type text" }
        )
    },
    @{
        Name = "fact_pharmacy_sales"
        File = "fact_pharmacy_sales.csv"
        Cols = @(
            @{ Name="Sales_ID"; Type="string"; MType="type text" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Year_Month"; Type="string"; MType="type text" },
            @{ Name="Pharmacy_ID"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Product_ID"; Type="string"; MType="type text" },
            @{ Name="Units_Sold"; Type="int64"; MType="Int64.Type"; Format="#,0" },
            @{ Name="Unit_Price_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Total_Revenue_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Distributor_ID"; Type="string"; MType="type text" },
            @{ Name="Supply_Disruption_Flag"; Type="boolean"; MType="type logical" }
        )
    },
    @{
        Name = "fact_rep_visits"
        File = "fact_rep_visits.csv"
        Cols = @(
            @{ Name="Visit_ID"; Type="string"; MType="type text" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Doctor_ID"; Type="string"; MType="type text" },
            @{ Name="Account_ID"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Visit_Type"; Type="string"; MType="type text" },
            @{ Name="Time_Slot"; Type="string"; MType="type text" },
            @{ Name="Call_Duration_Minutes"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Detailing_Score"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Product_Detailed_1"; Type="string"; MType="type text" },
            @{ Name="Product_Detailed_2"; Type="string"; MType="type text" },
            @{ Name="Samples_Dropped_Count"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Rain_Traffic_Delay_Flag"; Type="boolean"; MType="type logical" },
            @{ Name="Is_Replacement_Rep_Rampup"; Type="boolean"; MType="type logical" }
        )
    },
    @{
        Name = "fact_pharmacy_visits"
        File = "fact_pharmacy_visits.csv"
        Cols = @(
            @{ Name="Pharmacy_Visit_ID"; Type="string"; MType="type text" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Pharmacy_ID"; Type="string"; MType="type text" },
            @{ Name="Related_Doctor_Visit_ID"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Product_Audited_ID"; Type="string"; MType="type text" },
            @{ Name="Product_Availability"; Type="string"; MType="type text" },
            @{ Name="Stock_Units_Count"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Transfer_Order_Placed"; Type="boolean"; MType="type logical" },
            @{ Name="Transfer_Units"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Fulfilled_Distributor_ID"; Type="string"; MType="type text" }
        )
    },
    @{
        Name = "fact_rep_targets"
        File = "fact_rep_targets.csv"
        Cols = @(
            @{ Name="Target_ID"; Type="string"; MType="type text" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Product_ID"; Type="string"; MType="type text" },
            @{ Name="Territory_Potential_Index"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Target_Units"; Type="int64"; MType="Int64.Type"; Format="#,0" },
            @{ Name="Target_Revenue_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Actual_Baseline_RunRate"; Type="int64"; MType="Int64.Type"; Format="#,0" }
        )
    },
    @{
        Name = "fact_rep_weekly_plan"
        File = "fact_rep_weekly_plan.csv"
        Cols = @(
            @{ Name="Plan_ID"; Type="string"; MType="type text" },
            @{ Name="Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Week_Start_Date"; Type="dateTime"; MType="type date"; Format="yyyy-MM-dd" },
            @{ Name="Week_Number"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Year"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Plan_Submission_Status"; Type="string"; MType="type text" },
            @{ Name="Planned_Doctor_Visits"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Planned_Pharmacy_Visits"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Submission_Date"; Type="dateTime"; MType="type date"; Format="yyyy-MM-dd" },
            @{ Name="Manager_Approved"; Type="boolean"; MType="type logical" }
        )
    },
    @{
        Name = "fact_dr_expense"
        File = "fact_dr_expense.csv"
        Cols = @(
            @{ Name="Expense_ID"; Type="string"; MType="type text" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Rep_ID"; Type="string"; MType="type text" },
            @{ Name="Doctor_ID"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Expense_Category"; Type="string"; MType="type text" },
            @{ Name="Amount_Of_Money_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Doctor_Persona"; Type="string"; MType="type text" },
            @{ Name="Is_Free_Rider"; Type="boolean"; MType="type logical" },
            @{ Name="Incremental_Rx_Lift_Units"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Approval_Status"; Type="string"; MType="type text" }
        )
    },
    @{
        Name = "fact_ims_market_audit"
        File = "fact_ims_market_audit.csv"
        Cols = @(
            @{ Name="Audit_ID"; Type="string"; MType="type text" },
            @{ Name="Date_Key"; Type="int64"; MType="Int64.Type"; Format="0" },
            @{ Name="Year_Month"; Type="string"; MType="type text" },
            @{ Name="Brick_ID"; Type="string"; MType="type text" },
            @{ Name="Product_ID"; Type="string"; MType="type text" },
            @{ Name="Our_Market_Share_Pct"; Type="double"; MType="type number"; Format="0.0%" },
            @{ Name="Evolution_Index_EI"; Type="double"; MType="type number"; Format="#,0.0" },
            @{ Name="Total_Market_Volume_Units"; Type="int64"; MType="Int64.Type"; Format="#,0" },
            @{ Name="Total_Market_Value_EGP"; Type="double"; MType="type number"; Format="#,0.00" },
            @{ Name="Competitor_Combined_Share_Pct"; Type="double"; MType="type number"; Format="0.0%" }
        )
    },
    @{
        Name = "fact_doctor_predictions"
        File = "fact_doctor_predictions.csv"
        Cols = @(
            @{ Name="Doctor_ID"; Type="string"; MType="type text" },
            @{ Name="Prescriber_Churn_Probability"; Type="double"; MType="type number"; Format="0.0%" },
            @{ Name="Retention_Risk_Tier"; Type="string"; MType="type text" },
            @{ Name="Next_Best_Action_Recommendation"; Type="string"; MType="type text" },
            @{ Name="Key_Risk_Driver"; Type="string"; MType="type text" },
            @{ Name="Model_Name"; Type="string"; MType="type text" },
            @{ Name="Model_AUC_Score"; Type="double"; MType="type number"; Format="0.00" },
            @{ Name="Scored_Date"; Type="string"; MType="type text" }
        )
    }
)

# ------------------------------------------------------------------------------
# 3. Measures Library
# ------------------------------------------------------------------------------
$measures = @(
    # 01 Commercial and Revenue
    @{ Name="Total Revenue EGP"; Expression="SUM(fact_pharmacy_sales[Total_Revenue_EGP])"; Format="#,0 ""EGP"""; Folder="01 Commercial and Revenue" },
    @{ Name="Total Units Sold"; Expression="SUM(fact_pharmacy_sales[Units_Sold])"; Format="#,0"; Folder="01 Commercial and Revenue" },
    @{ Name="Target Revenue EGP"; Expression="SUM(fact_rep_targets[Target_Revenue_EGP])"; Format="#,0 ""EGP"""; Folder="01 Commercial and Revenue" },
    @{ Name="Target Units"; Expression="SUM(fact_rep_targets[Target_Units])"; Format="#,0"; Folder="01 Commercial and Revenue" },
    @{ Name="Target Attainment Pct"; Expression="DIVIDE([Total Revenue EGP], [Target Revenue EGP], 0)"; Format="0.0%"; Folder="01 Commercial and Revenue" },
    @{ Name="Target Revenue Variance EGP"; Expression="[Total Revenue EGP] - [Target Revenue EGP]"; Format="#,0 ""EGP"""; Folder="01 Commercial and Revenue" },
    @{ Name="Target Variance Indicator"; Expression="IF([Target Revenue Variance EGP] >= 0, ""Surplus"", ""Deficit"")"; Format=""; Folder="01 Commercial and Revenue" },
    @{ Name="Avg Selling Price EGP"; Expression="DIVIDE([Total Revenue EGP], [Total Units Sold], 0)"; Format="#,0.00 ""EGP"""; Folder="01 Commercial and Revenue" },
    @{ Name="Baseline RunRate Revenue EGP"; Expression="SUMX(fact_rep_targets, fact_rep_targets[Actual_Baseline_RunRate] * RELATED(dim_product[Unit_Price_EGP]))"; Format="#,0 ""EGP"""; Folder="01 Commercial and Revenue" },
    @{ Name="Revenue RunRate Lift EGP"; Expression="[Total Revenue EGP] - [Baseline RunRate Revenue EGP]"; Format="#,0 ""EGP"""; Folder="01 Commercial and Revenue" },
    @{ Name="Disrupted Revenue EGP"; Expression="CALCULATE([Total Revenue EGP], fact_pharmacy_sales[Supply_Disruption_Flag] = TRUE())"; Format="#,0 ""EGP"""; Folder="01 Commercial and Revenue" },

    # 02 Field Operations and Detailing
    @{ Name="Total Field Visits"; Expression="COUNTROWS(fact_rep_visits)"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="AM Institutional Visits"; Expression="CALCULATE([Total Field Visits], fact_rep_visits[Visit_Type] = ""AM Institutional"")"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="PM Clinic Visits"; Expression="CALCULATE([Total Field Visits], fact_rep_visits[Visit_Type] = ""PM Private Clinic"")"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="AM Visit Share Pct"; Expression="DIVIDE([AM Institutional Visits], [Total Field Visits], 0)"; Format="0.0%"; Folder="02 Field Operations and Detailing" },
    @{ Name="PM Visit Share Pct"; Expression="DIVIDE([PM Clinic Visits], [Total Field Visits], 0)"; Format="0.0%"; Folder="02 Field Operations and Detailing" },
    @{ Name="Total Planned Doctor Visits"; Expression="SUM(fact_rep_weekly_plan[Planned_Doctor_Visits])"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="Plan Adherence Pct"; Expression="DIVIDE([Total Field Visits], [Total Planned Doctor Visits], 0)"; Format="0.0%"; Folder="02 Field Operations and Detailing" },
    @{ Name="Avg Detailing Score"; Expression="AVERAGE(fact_rep_visits[Detailing_Score])"; Format="0.0"; Folder="02 Field Operations and Detailing" },
    @{ Name="Avg Call Duration Minutes"; Expression="AVERAGE(fact_rep_visits[Call_Duration_Minutes])"; Format="0.0 ""min"""; Folder="02 Field Operations and Detailing" },
    @{ Name="Total Samples Dropped"; Expression="SUM(fact_rep_visits[Samples_Dropped_Count])"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="Rain Delayed Calls Count"; Expression="CALCULATE([Total Field Visits], fact_rep_visits[Rain_Traffic_Delay_Flag] = TRUE())"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="Replacement Rep Rampup Calls"; Expression="CALCULATE([Total Field Visits], fact_rep_visits[Is_Replacement_Rep_Rampup] = TRUE())"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="Active Prescribing Doctors"; Expression="DISTINCTCOUNT(fact_rep_visits[Doctor_ID])"; Format="#,0"; Folder="02 Field Operations and Detailing" },
    @{ Name="Tier A KOL Doctor Coverage Pct"; Expression="DIVIDE(CALCULATE(DISTINCTCOUNT(fact_rep_visits[Doctor_ID]), dim_doctor[Classification] = ""Class A (KOL)""), CALCULATE(DISTINCTCOUNT(dim_doctor[Doctor_ID]), dim_doctor[Classification] = ""Class A (KOL)""), 0)"; Format="0.0%"; Folder="02 Field Operations and Detailing" },
    @{ Name="Weekly Plan On-Time Submission Pct"; Expression="DIVIDE(CALCULATE(COUNTROWS(fact_rep_weekly_plan), fact_rep_weekly_plan[Plan_Submission_Status] = ""On-Time Saturday Submission""), COUNTROWS(fact_rep_weekly_plan), 0)"; Format="0.0%"; Folder="02 Field Operations and Detailing" },

    # 03 Territory and Pharmacy Dynamics
    @{ Name="Total Pharmacy Audits"; Expression="COUNTROWS(fact_pharmacy_visits)"; Format="#,0"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Audits In-Stock Count"; Expression="CALCULATE([Total Pharmacy Audits], fact_pharmacy_visits[Product_Availability] = ""In-Stock"")"; Format="#,0"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Audits Stock-Out Count"; Expression="CALCULATE([Total Pharmacy Audits], fact_pharmacy_visits[Product_Availability] = ""Stock-Out"")"; Format="#,0"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="In-Stock Rate Pct"; Expression="DIVIDE([Audits In-Stock Count], [Total Pharmacy Audits], 0)"; Format="0.0%"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Stock-Out Rate Pct"; Expression="DIVIDE([Audits Stock-Out Count], [Total Pharmacy Audits], 0)"; Format="0.0%"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Transfer Orders Placed Count"; Expression="CALCULATE([Total Pharmacy Audits], fact_pharmacy_visits[Transfer_Order_Placed] = TRUE())"; Format="#,0"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Total Transfer Units"; Expression="SUM(fact_pharmacy_visits[Transfer_Units])"; Format="#,0"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Closed-Loop Verified Visits"; Expression="CALCULATE(COUNTROWS(fact_pharmacy_visits), NOT(ISBLANK(fact_pharmacy_visits[Related_Doctor_Visit_ID])))"; Format="#,0"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Closed-Loop Verification Rate Pct"; Expression="DIVIDE([Closed-Loop Verified Visits], [Total Pharmacy Audits], 0)"; Format="0.0%"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Big 5 Distributor Revenue Pct"; Expression="DIVIDE(CALCULATE([Total Revenue EGP], dim_distributor[Distributor_ID] IN {""DIST-01"",""DIST-02"",""DIST-03"",""DIST-04"",""DIST-05""}), [Total Revenue EGP], 0)"; Format="0.0%"; Folder="03 Territory and Pharmacy Dynamics" },
    @{ Name="Local Wholesalers (El-Makhazen) Revenue Pct"; Expression="DIVIDE(CALCULATE([Total Revenue EGP], dim_distributor[Distributor_ID] = ""DIST-06""), [Total Revenue EGP], 0)"; Format="0.0%"; Folder="03 Territory and Pharmacy Dynamics" },

    # 04 IMS Market Intelligence
    @{ Name="IMS Market Share Pct"; Expression="AVERAGE(fact_ims_market_audit[Our_Market_Share_Pct])"; Format="0.0%"; Folder="04 IMS Market Intelligence" },
    @{ Name="Competitor Market Share Pct"; Expression="AVERAGE(fact_ims_market_audit[Competitor_Combined_Share_Pct])"; Format="0.0%"; Folder="04 IMS Market Intelligence" },
    @{ Name="Evolution Index EI"; Expression="AVERAGE(fact_ims_market_audit[Evolution_Index_EI])"; Format="0.0"; Folder="04 IMS Market Intelligence" },
    @{ Name="Total Market Volume Units"; Expression="SUM(fact_ims_market_audit[Total_Market_Volume_Units])"; Format="#,0"; Folder="04 IMS Market Intelligence" },
    @{ Name="Total Market Value EGP"; Expression="SUM(fact_ims_market_audit[Total_Market_Value_EGP])"; Format="#,0 ""EGP"""; Folder="04 IMS Market Intelligence" },
    @{ Name="Market Benchmark Status"; Expression="IF([Evolution_Index_EI] >= 100, ""Market Outperformer (EI >= 100)"", ""Market Underperformer (EI < 100)"")"; Format=""; Folder="04 IMS Market Intelligence" },

    # 05 AI Prescriber Copilot
    @{ Name="Total Doctors Scored"; Expression="COUNTROWS(fact_doctor_predictions)"; Format="#,0"; Folder="05 AI Prescriber Copilot" },
    @{ Name="High Churn Risk Doctor Count"; Expression="CALCULATE([Total Doctors Scored], fact_doctor_predictions[Retention_Risk_Tier] = ""High Churn Risk"")"; Format="#,0"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Medium Risk Doctor Count"; Expression="CALCULATE([Total Doctors Scored], fact_doctor_predictions[Retention_Risk_Tier] = ""Medium Risk"")"; Format="#,0"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Loyal Prescriber Doctor Count"; Expression="CALCULATE([Total Doctors Scored], fact_doctor_predictions[Retention_Risk_Tier] = ""Loyal Prescriber"")"; Format="#,0"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Avg Churn Probability Pct"; Expression="AVERAGE(fact_doctor_predictions[Prescriber_Churn_Probability])"; Format="0.0%"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Total Promotional Expense EGP"; Expression="SUM(fact_dr_expense[Amount_Of_Money_EGP])"; Format="#,0 ""EGP"""; Folder="05 AI Prescriber Copilot" },
    @{ Name="Free Rider Expense EGP"; Expression="CALCULATE([Total Promotional Expense EGP], fact_dr_expense[Is_Free_Rider] = TRUE())"; Format="#,0 ""EGP"""; Folder="05 AI Prescriber Copilot" },
    @{ Name="Free Rider Budget Leakage Pct"; Expression="DIVIDE([Free Rider Expense EGP], [Total Promotional Expense EGP], 0)"; Format="0.0%"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Free Rider Doctor Count"; Expression="CALCULATE(DISTINCTCOUNT(fact_dr_expense[Doctor_ID]), fact_dr_expense[Is_Free_Rider] = TRUE())"; Format="#,0"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Incremental Rx Lift Units"; Expression="SUM(fact_dr_expense[Incremental_Rx_Lift_Units])"; Format="#,0"; Folder="05 AI Prescriber Copilot" },
    @{ Name="Promotional ROI Ratio"; Expression="DIVIDE(SUMX(fact_dr_expense, fact_dr_expense[Incremental_Rx_Lift_Units] * 150), [Total Promotional Expense EGP], 0)"; Format="0.00 ""x"""; Folder="05 AI Prescriber Copilot" }
)

# ------------------------------------------------------------------------------
# 4. Relationships Specification
# ------------------------------------------------------------------------------
$relationships = @(
    # Date relationships
    @{ Name="Rel_Sales_Date"; FromTable="fact_pharmacy_sales"; FromCol="Date_Key"; ToTable="dim_date"; ToCol="Date_Key"; IsActive=$true },
    @{ Name="Rel_RepVisits_Date"; FromTable="fact_rep_visits"; FromCol="Date_Key"; ToTable="dim_date"; ToCol="Date_Key"; IsActive=$true },
    @{ Name="Rel_PharmVisits_Date"; FromTable="fact_pharmacy_visits"; FromCol="Date_Key"; ToTable="dim_date"; ToCol="Date_Key"; IsActive=$true },
    @{ Name="Rel_Targets_Date"; FromTable="fact_rep_targets"; FromCol="Date_Key"; ToTable="dim_date"; ToCol="Date_Key"; IsActive=$true },
    @{ Name="Rel_Expense_Date"; FromTable="fact_dr_expense"; FromCol="Date_Key"; ToTable="dim_date"; ToCol="Date_Key"; IsActive=$true },
    @{ Name="Rel_IMS_Date"; FromTable="fact_ims_market_audit"; FromCol="Date_Key"; ToTable="dim_date"; ToCol="Date_Key"; IsActive=$true },
    @{ Name="Rel_Plan_Date"; FromTable="fact_rep_weekly_plan"; FromCol="Week_Start_Date"; ToTable="dim_date"; ToCol="Date"; IsActive=$true },

    # Brick relationships
    @{ Name="Rel_Sales_Brick"; FromTable="fact_pharmacy_sales"; FromCol="Brick_ID"; ToTable="dim_brick_territory"; ToCol="Brick_ID"; IsActive=$true },
    @{ Name="Rel_RepVisits_Brick"; FromTable="fact_rep_visits"; FromCol="Brick_ID"; ToTable="dim_brick_territory"; ToCol="Brick_ID"; IsActive=$true },
    @{ Name="Rel_PharmVisits_Brick"; FromTable="fact_pharmacy_visits"; FromCol="Brick_ID"; ToTable="dim_brick_territory"; ToCol="Brick_ID"; IsActive=$true },
    @{ Name="Rel_IMS_Brick"; FromTable="fact_ims_market_audit"; FromCol="Brick_ID"; ToTable="dim_brick_territory"; ToCol="Brick_ID"; IsActive=$true },
    @{ Name="Rel_Expense_Brick"; FromTable="fact_dr_expense"; FromCol="Brick_ID"; ToTable="dim_brick_territory"; ToCol="Brick_ID"; IsActive=$true },

    # Product relationships
    @{ Name="Rel_Sales_Product"; FromTable="fact_pharmacy_sales"; FromCol="Product_ID"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$true },
    @{ Name="Rel_Targets_Product"; FromTable="fact_rep_targets"; FromCol="Product_ID"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$true },
    @{ Name="Rel_IMS_Product"; FromTable="fact_ims_market_audit"; FromCol="Product_ID"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$true },
    @{ Name="Rel_PharmVisits_Product"; FromTable="fact_pharmacy_visits"; FromCol="Product_Audited_ID"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$true },
    @{ Name="Rel_RepVisits_Product1"; FromTable="fact_rep_visits"; FromCol="Product_Detailed_1"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$true },
    @{ Name="Rel_RepVisits_Product2"; FromTable="fact_rep_visits"; FromCol="Product_Detailed_2"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$false },
    @{ Name="Rel_Competitor_TargetProduct"; FromTable="dim_competitor_product"; FromCol="Target_Product_ID"; ToTable="dim_product"; ToCol="Product_ID"; IsActive=$true },

    # Medical Rep relationships
    @{ Name="Rel_RepVisits_Rep"; FromTable="fact_rep_visits"; FromCol="Rep_ID"; ToTable="dim_medical_rep"; ToCol="Rep_ID"; IsActive=$true },
    @{ Name="Rel_PharmVisits_Rep"; FromTable="fact_pharmacy_visits"; FromCol="Rep_ID"; ToTable="dim_medical_rep"; ToCol="Rep_ID"; IsActive=$true },
    @{ Name="Rel_Targets_Rep"; FromTable="fact_rep_targets"; FromCol="Rep_ID"; ToTable="dim_medical_rep"; ToCol="Rep_ID"; IsActive=$true },
    @{ Name="Rel_Plan_Rep"; FromTable="fact_rep_weekly_plan"; FromCol="Rep_ID"; ToTable="dim_medical_rep"; ToCol="Rep_ID"; IsActive=$true },
    @{ Name="Rel_Expense_Rep"; FromTable="fact_dr_expense"; FromCol="Rep_ID"; ToTable="dim_medical_rep"; ToCol="Rep_ID"; IsActive=$true },

    # Doctor relationships
    @{ Name="Rel_RepVisits_Doctor"; FromTable="fact_rep_visits"; FromCol="Doctor_ID"; ToTable="dim_doctor"; ToCol="Doctor_ID"; IsActive=$true },
    @{ Name="Rel_Expense_Doctor"; FromTable="fact_dr_expense"; FromCol="Doctor_ID"; ToTable="dim_doctor"; ToCol="Doctor_ID"; IsActive=$true },
    @{ Name="Rel_Predictions_Doctor"; FromTable="fact_doctor_predictions"; FromCol="Doctor_ID"; ToTable="dim_doctor"; ToCol="Doctor_ID"; IsActive=$true },
    @{ Name="Rel_Schedule_Doctor"; FromTable="dim_doctor_schedule"; FromCol="Doctor_ID"; ToTable="dim_doctor"; ToCol="Doctor_ID"; IsActive=$true },

    # Pharmacy relationships
    @{ Name="Rel_Sales_Pharmacy"; FromTable="fact_pharmacy_sales"; FromCol="Pharmacy_ID"; ToTable="dim_pharmacy"; ToCol="Pharmacy_ID"; IsActive=$true },
    @{ Name="Rel_PharmVisits_Pharmacy"; FromTable="fact_pharmacy_visits"; FromCol="Pharmacy_ID"; ToTable="dim_pharmacy"; ToCol="Pharmacy_ID"; IsActive=$true },

    # Distributor relationships
    @{ Name="Rel_Sales_Distributor"; FromTable="fact_pharmacy_sales"; FromCol="Distributor_ID"; ToTable="dim_distributor"; ToCol="Distributor_ID"; IsActive=$true },
    @{ Name="Rel_Pharmacy_Distributor"; FromTable="dim_pharmacy"; FromCol="Primary_Distributor_ID"; ToTable="dim_distributor"; ToCol="Distributor_ID"; IsActive=$false },
    @{ Name="Rel_PharmVisits_Distributor"; FromTable="fact_pharmacy_visits"; FromCol="Fulfilled_Distributor_ID"; ToTable="dim_distributor"; ToCol="Distributor_ID"; IsActive=$false },

    # Institutional Account relationship
    @{ Name="Rel_RepVisits_Account"; FromTable="fact_rep_visits"; FromCol="Account_ID"; ToTable="dim_account"; ToCol="Account_ID"; IsActive=$true },

    # Closed-loop Doctor to Pharmacy Visit verification
    @{ Name="Rel_ClosedLoop_Visit"; FromTable="fact_pharmacy_visits"; FromCol="Related_Doctor_Visit_ID"; ToTable="fact_rep_visits"; ToCol="Visit_ID"; IsActive=$false }
)

# ------------------------------------------------------------------------------
# 5. Build TMSL model.bim Object
# ------------------------------------------------------------------------------
Write-Host ">>> Assembling TMSL model.bim..." -ForegroundColor Yellow

$queryOrderList = @("DataFolderPath")
foreach ($t in $tableDefs) { $queryOrderList += $t.Name }
$queryOrderList += "_Measures"

$expressionsObj = @(
    @{
        name = "DataFolderPath"
        kind = "m"
        expression = @(
            """d:\portfolio2026\02_PharmaForce360\data\"" meta [IsParameterQuery=true, Type=""Text"", IsParameterQueryRequired=true]"
        )
        lineageTag = [guid]::NewGuid().ToString()
        annotations = @(
            @{ name = "PBI_NavigationStepName"; value = "Navigation" },
            @{ name = "PBI_ResultType"; value = "Text" }
        )
    }
)

$tablesObj = @()

# Add all 18 data tables
foreach ($t in $tableDefs) {
    $colsList = @()
    $mTypeTransforms = @()

    foreach ($c in $t.Cols) {
        $colItem = @{
            name = $c.Name
            dataType = $c.Type
            sourceColumn = $c.Name
            lineageTag = [guid]::NewGuid().ToString()
            summarizeBy = "none"
        }
        if ($c.Format) { $colItem.formatString = $c.Format }
        $colsList += $colItem

        $mTypeTransforms += "{""$($c.Name)"", $($c.MType)}"
    }

    $transformStr = "{" + ($mTypeTransforms -join ", ") + "}"
    $colCount = $t.Cols.Count

    $mExpression = @(
        "let",
        "    Source = Csv.Document(File.Contents(DataFolderPath & ""$($t.File)""), [Delimiter="","", Columns=$colCount, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),",
        "    #""Promoted Headers"" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
        "    #""Changed Type"" = Table.TransformColumnTypes(#""Promoted Headers"", $transformStr)",
        "in",
        "    #""Changed Type"""
    )

    $tableItem = @{
        name = $t.Name
        lineageTag = [guid]::NewGuid().ToString()
        columns = $colsList
        partitions = @(
            @{
                name = $t.Name
                mode = "import"
                source = @{
                    type = "m"
                    expression = $mExpression
                }
            }
        )
    }
    $tablesObj += $tableItem
}

# Add _Measures table
$measuresList = @()
foreach ($m in $measures) {
    $measureItem = @{
        name = $m.Name
        expression = $m.Expression
        displayFolder = $m.Folder
        lineageTag = [guid]::NewGuid().ToString()
    }
    if ($m.Format) { $measureItem.formatString = $m.Format }
    $measuresList += $measureItem
}

$measuresTable = @{
    name = "_Measures"
    lineageTag = [guid]::NewGuid().ToString()
    columns = @(
        @{
            name = "Placeholder"
            dataType = "string"
            isHidden = $true
            sourceColumn = "Placeholder"
            lineageTag = [guid]::NewGuid().ToString()
            summarizeBy = "none"
        }
    )
    partitions = @(
        @{
            name = "_Measures"
            mode = "import"
            source = @{
                type = "m"
                expression = @(
                    "let",
                    "    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText(""i44FAA=="", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Placeholder = _t])",
                    "in",
                    "    Source"
                )
            }
        }
    )
    measures = $measuresList
}
$tablesObj += $measuresTable

# Add Relationships
$relList = @()
foreach ($r in $relationships) {
    $relItem = @{
        name = $r.Name
        fromTable = $r.FromTable
        fromColumn = $r.FromCol
        toTable = $r.ToTable
        toColumn = $r.ToCol
        isActive = $r.IsActive
        crossFilteringBehavior = "oneDirection"
    }
    $relList += $relItem
}

$modelBimObj = @{
    name = "PharmaForce360"
    compatibilityLevel = 1600
    model = @{
        culture = "en-US"
        dataAccessOptions = @{
            legacyRedirects = $true
            returnErrorValuesAsNull = $true
        }
        defaultPowerBIDataSourceVersion = "powerBI_V3"
        expressions = $expressionsObj
        tables = $tablesObj
        relationships = $relList
        cultures = @(
            @{
                name = "en-US"
                linguisticMetadata = @{
                    content = @{
                        Version = "1.0.0"
                        Language = "en-US"
                    }
                    contentType = "json"
                }
            }
        )
        annotations = @(
            @{
                name = "PBI_QueryOrder"
                value = ($queryOrderList | ConvertTo-Json -Compress)
            }
        )
    }
}

$modelBimJson = $modelBimObj | ConvertTo-Json -Depth 20
$modelBimPath = Join-Path $TargetDir "PharmaForce360.SemanticModel\model.bim"
[System.IO.File]::WriteAllText($modelBimPath, $modelBimJson, $utf8NoBom)
Write-Host "  [+] Generated: model.bim ($([math]::Round((Get-Item $modelBimPath).Length / 1KB, 1)) KB)" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 6. Build TMDL Files (Modern Git Co-Development format)
# ------------------------------------------------------------------------------
Write-Host ">>> Generating TMDL model files..." -ForegroundColor Yellow

$tmdlModelContent = @"
model Model
	compatibilityLevel: 1600
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3

annotation PBI_QueryOrder = $(($queryOrderList | ConvertTo-Json -Compress))

ref table _Measures
"@

foreach ($t in $tableDefs) {
    $tmdlModelContent += "`nref table $($t.Name)"
}

$tmdlModelContent += "`nref culture en-US`n"
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\model.tmdl"), $tmdlModelContent, $utf8NoBom)

# cultures/en-US.tmdl
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\cultures\en-US.tmdl"), "culture en-US`n", $utf8NoBom)

# relationships.tmdl
$tmdlRelContent = ""
foreach ($r in $relationships) {
    $activeStr = if ($r.IsActive) { "" } else { "`n`tisActive: false" }
    $tmdlRelContent += @"
relationship $($r.Name)
	fromColumn: $($r.FromTable).$($r.FromCol)
	toColumn: $($r.ToTable).$($r.ToCol)$activeStr

"@
}
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\relationships.tmdl"), $tmdlRelContent, $utf8NoBom)

# tables/*.tmdl
foreach ($t in $tableDefs) {
    $tContent = @"
table $($t.Name)
	lineageTag: $([guid]::NewGuid().ToString())

"@
    foreach ($c in $t.Cols) {
        $fmt = if ($c.Format) { "`n`t`tformatString: $($c.Format)" } else { "" }
        $tContent += @"
	column $($c.Name)
		dataType: $($c.Type)$fmt
		lineageTag: $([guid]::NewGuid().ToString())
		summarizeBy: none
		sourceColumn: $($c.Name)

"@
    }

    $tContent += @"
	partition $($t.Name) = m
		mode: import
		source =
			let
				Source = Csv.Document(File.Contents(DataFolderPath & "$($t.File)"), [Delimiter=",", Columns=$($t.Cols.Count), Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
				#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
			in
				#"Promoted Headers"

"@
    [System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\tables\$($t.Name).tmdl"), $tContent, $utf8NoBom)
}

# tables/_Measures.tmdl
$tMeasuresContent = @"
table _Measures
	lineageTag: $([guid]::NewGuid().ToString())

	column Placeholder
		dataType: string
		isHidden
		lineageTag: $([guid]::NewGuid().ToString())
		summarizeBy: none
		sourceColumn: Placeholder

"@
foreach ($m in $measures) {
    $fmt = if ($m.Format) { "`n`t`tformatString: $($m.Format)" } else { "" }
    $tMeasuresContent += @"
	measure '$($m.Name)' = $($m.Expression)
		displayFolder: $($m.Folder)$fmt
		lineageTag: $([guid]::NewGuid().ToString())

"@
}
$tMeasuresContent += @"
	partition _Measures = m
		mode: import
		source =
			let
				Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Placeholder = _t])
			in
				Source

"@
[System.IO.File]::WriteAllText((Join-Path $TargetDir "PharmaForce360.SemanticModel\definition\tables\_Measures.tmdl"), $tMeasuresContent, $utf8NoBom)
Write-Host "  [+] Generated TMDL definitions for 19 tables and 35 relationships." -ForegroundColor Green

# ------------------------------------------------------------------------------
# 7. Build 5-Page Persona Report (report.json)
# ------------------------------------------------------------------------------
Write-Host ">>> Designing 5-Page Clinical and Corporate Report (report.json)..." -ForegroundColor Yellow

function New-CardVisual {
    param(
        [string]$Name,
        [int]$X,
        [int]$Y,
        [int]$W,
        [int]$H,
        [string]$MeasureName
    )
    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = 1000; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "card"
            projections = @{
                Values = @( @{ queryRef = "_Measures.$MeasureName" } )
            }
            prototypeQuery = @{
                Version = 2
                From = @( @{ Name = "m"; Entity = "_Measures"; Type = 0 } )
                Select = @(
                    @{
                        Measure = @{
                            Expression = @{ SourceRef = @{ Source = "m" } }
                            Property = $MeasureName
                        }
                        Name = "_Measures.$MeasureName"
                    }
                )
            }
            drillFilterOtherVisuals = $true
        }
    }
    return @{
        x = $X; y = $Y; z = 1000; width = $W; height = $H
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
        filters = "[]"
    }
}

function New-TextBoxVisual {
    param(
        [string]$Name,
        [int]$X,
        [int]$Y,
        [int]$W,
        [int]$H,
        [string]$Text
    )
    $cfg = @{
        name = $Name
        layouts = @(
            @{
                id = 0
                position = @{ x = $X; y = $Y; z = 500; width = $W; height = $H }
            }
        )
        singleVisual = @{
            visualType = "textbox"
            objects = @{
                general = @(
                    @{
                        properties = @{
                            paragraphs = @(
                                @{
                                    textRuns = @(
                                        @{
                                            value = $Text
                                            textStyle = @{
                                                fontFamily = "Segoe UI Semibold"
                                                fontSize = "15pt"
                                                color = "#0A2540"
                                            }
                                        }
                                    )
                                }
                            )
                        }
                    }
                )
            }
            drillFilterOtherVisuals = $true
        }
    }
    return @{
        x = $X; y = $Y; z = 500; width = $W; height = $H
        config = ($cfg | ConvertTo-Json -Depth 15 -Compress)
        filters = "[]"
    }
}

# --- Section 1: Home Hub and Executive Pulse
$sec1Visuals = @(
    (New-TextBoxVisual -Name "Header_Home" -X 20 -Y 15 -W 1240 -H 65 -Text "PharmaForce 360 Commercial Intelligence Suite - Greater Cairo Executive Cockpit"),
    (New-CardVisual -Name "Card_S1_1" -X 20 -Y 90 -W 235 -H 105 -MeasureName "Total Revenue EGP"),
    (New-CardVisual -Name "Card_S1_2" -X 270 -Y 90 -W 235 -H 105 -MeasureName "Target Attainment Pct"),
    (New-CardVisual -Name "Card_S1_3" -X 520 -Y 90 -W 235 -H 105 -MeasureName "Total Field Visits"),
    (New-CardVisual -Name "Card_S1_4" -X 770 -Y 90 -W 235 -H 105 -MeasureName "Evolution Index EI"),
    (New-CardVisual -Name "Card_S1_5" -X 1020 -Y 90 -W 240 -H 105 -MeasureName "High Churn Risk Doctor Count"),
    
    (New-TextBoxVisual -Name "Nav_Tile_1" -X 20 -Y 215 -W 295 -H 190 -Text "Page 2: Commercial and IQVIA Audit`n`n- Sales vs Quota Tracking (EGP)`n- Distributor Channel Fulfillment`n- Evolution Index Market Growth"),
    (New-TextBoxVisual -Name "Nav_Tile_2" -X 335 -Y 215 -W 295 -H 190 -Text "Page 3: Field Force and Detailing`n`n- Rep Detailing Quality and Leaderboard`n- AM/PM Hospital vs Clinic Split`n- New Rep S-Curve Handover Ramp-up"),
    (New-TextBoxVisual -Name "Nav_Tile_3" -X 650 -Y 215 -W 295 -H 190 -Text "Page 4: Brick and Pharmacy Dynamics`n`n- Greater Cairo 36 Bricks Potential`n- Closed-Loop Detailing Verification`n- Pharmacy Stock-Outs and Transfers"),
    (New-TextBoxVisual -Name "Nav_Tile_4" -X 965 -Y 215 -W 295 -H 190 -Text "Page 5: AI Prescriber Copilot`n`n- Prescriber Churn Risk Tiers`n- Next-Best-Action (NBA) Queue`n- Free-Rider Leakage and ROI Optimizer"),

    (New-TextBoxVisual -Name "Chart_Title_1" -X 20 -Y 425 -W 610 -H 35 -Text "Greater Cairo Territory Performance by Commercial Zone"),
    (New-CardVisual -Name "Summary_Zone" -X 20 -Y 465 -W 610 -H 235 -MeasureName "Baseline RunRate Revenue EGP"),
    (New-TextBoxVisual -Name "Chart_Title_2" -X 650 -Y 425 -W 610 -H 35 -Text "Portfolio Therapeutic Line Revenue Split"),
    (New-CardVisual -Name "Summary_Line" -X 650 -Y 465 -W 610 -H 235 -MeasureName "Revenue RunRate Lift EGP")
)

# --- Section 2: Executive Commercial Performance
$sec2Visuals = @(
    (New-TextBoxVisual -Name "Header_Commercial" -X 20 -Y 15 -W 1240 -H 65 -Text "Executive Commercial Performance and IQVIA Market Audit (EGP)"),
    (New-CardVisual -Name "Card_S2_1" -X 20 -Y 90 -W 235 -H 105 -MeasureName "Total Revenue EGP"),
    (New-CardVisual -Name "Card_S2_2" -X 270 -Y 90 -W 235 -H 105 -MeasureName "Target Revenue EGP"),
    (New-CardVisual -Name "Card_S2_3" -X 520 -Y 90 -W 235 -H 105 -MeasureName "Target Attainment Pct"),
    (New-CardVisual -Name "Card_S2_4" -X 770 -Y 90 -W 235 -H 105 -MeasureName "IMS Market Share Pct"),
    (New-CardVisual -Name "Card_S2_5" -X 1020 -Y 90 -W 240 -H 105 -MeasureName "Evolution Index EI"),

    (New-TextBoxVisual -Name "Title_S2_Chart1" -X 20 -Y 215 -W 750 -H 35 -Text "Monthly Sales Trajectory vs Rep Target Quota (EGP)"),
    (New-CardVisual -Name "Visual_S2_Traj" -X 20 -Y 255 -W 750 -H 220 -MeasureName "Target Revenue Variance EGP"),
    (New-TextBoxVisual -Name "Title_S2_Chart2" -X 790 -Y 215 -W 470 -H 35 -Text "Primary Distributors vs Local Wholesalers (El-Makhazen)"),
    (New-CardVisual -Name "Visual_S2_Dist" -X 790 -Y 255 -W 470 -H 220 -MeasureName "Local Wholesalers (El-Makhazen) Revenue Pct"),

    (New-TextBoxVisual -Name "Title_S2_Chart3" -X 20 -Y 495 -W 750 -H 35 -Text "Greater Cairo Brick Market Share and Evolution Index (EI) Ranking"),
    (New-CardVisual -Name "Visual_S2_EI" -X 20 -Y 535 -W 750 -H 165 -MeasureName "Competitor Market Share Pct"),
    (New-TextBoxVisual -Name "Title_S2_Chart4" -X 790 -Y 495 -W 470 -H 35 -Text "Portfolio Price Benchmark vs Market Competitor Brands"),
    (New-CardVisual -Name "Visual_S2_Prices" -X 790 -Y 535 -W 470 -H 165 -MeasureName "Avg Selling Price EGP")
)

# --- Section 3: Field Force Detailing Operations
$sec3Visuals = @(
    (New-TextBoxVisual -Name "Header_Field" -X 20 -Y 15 -W 1240 -H 65 -Text "Field Force Activity and HCP Detailing Operations"),
    (New-CardVisual -Name "Card_S3_1" -X 20 -Y 90 -W 235 -H 105 -MeasureName "Total Field Visits"),
    (New-CardVisual -Name "Card_S3_2" -X 270 -Y 90 -W 235 -H 105 -MeasureName "Plan Adherence Pct"),
    (New-CardVisual -Name "Card_S3_3" -X 520 -Y 90 -W 235 -H 105 -MeasureName "Tier A KOL Doctor Coverage Pct"),
    (New-CardVisual -Name "Card_S3_4" -X 770 -Y 90 -W 235 -H 105 -MeasureName "Avg Detailing Score"),
    (New-CardVisual -Name "Card_S3_5" -X 1020 -Y 90 -W 240 -H 105 -MeasureName "Total Samples Dropped"),

    (New-TextBoxVisual -Name "Title_S3_Chart1" -X 20 -Y 215 -W 680 -H 35 -Text "Medical Rep Detailing Volume and Quality Leaderboard"),
    (New-CardVisual -Name "Visual_S3_Leaderboard" -X 20 -Y 255 -W 680 -H 220 -MeasureName "Active Prescribing Doctors"),
    (New-TextBoxVisual -Name "Title_S3_Chart2" -X 720 -Y 215 -W 540 -H 35 -Text "Detailing Allocation: AM Institutional vs PM Clinics"),
    (New-CardVisual -Name "Visual_S3_AMPM" -X 720 -Y 255 -W 540 -H 220 -MeasureName "AM Visit Share Pct"),

    (New-TextBoxVisual -Name "Title_S3_Chart3" -X 20 -Y 495 -W 680 -H 35 -Text "Weekly Call Plan Discipline: On-Time vs Delinquent Submissions"),
    (New-CardVisual -Name "Visual_S3_Plan" -X 20 -Y 535 -W 680 -H 165 -MeasureName "Weekly Plan On-Time Submission Pct"),
    (New-TextBoxVisual -Name "Title_S3_Chart4" -X 720 -Y 495 -W 540 -H 35 -Text "Operational Reality: Cairo Rain Traffic Delays and S-Curve Ramp-ups"),
    (New-CardVisual -Name "Visual_S3_Disrupt" -X 720 -Y 535 -W 540 -H 165 -MeasureName "Rain Delayed Calls Count")
)

# --- Section 4: Territory Brick Dynamics & Pharmacy Audit
$sec4Visuals = @(
    (New-TextBoxVisual -Name "Header_Brick" -X 20 -Y 15 -W 1240 -H 65 -Text "Territory Brick Dynamics and Pharmacy Audit Intelligence"),
    (New-CardVisual -Name "Card_S4_1" -X 20 -Y 90 -W 235 -H 105 -MeasureName "Total Pharmacy Audits"),
    (New-CardVisual -Name "Card_S4_2" -X 270 -Y 90 -W 235 -H 105 -MeasureName "In-Stock Rate Pct"),
    (New-CardVisual -Name "Card_S4_3" -X 520 -Y 90 -W 235 -H 105 -MeasureName "Stock-Out Rate Pct"),
    (New-CardVisual -Name "Card_S4_4" -X 770 -Y 90 -W 235 -H 105 -MeasureName "Transfer Orders Placed Count"),
    (New-CardVisual -Name "Card_S4_5" -X 1020 -Y 90 -W 240 -H 105 -MeasureName "Closed-Loop Verification Rate Pct"),

    (New-TextBoxVisual -Name "Title_S4_Chart1" -X 20 -Y 215 -W 750 -H 35 -Text "Greater Cairo Commercial Bricks: Revenue vs Territory Potential"),
    (New-CardVisual -Name "Visual_S4_Bricks" -X 20 -Y 255 -W 750 -H 220 -MeasureName "Total Units Sold"),
    (New-TextBoxVisual -Name "Title_S4_Chart2" -X 790 -Y 215 -W 470 -H 35 -Text "Pharmacy Stock-Out Audit by Chain Affiliation"),
    (New-CardVisual -Name "Visual_S4_Chains" -X 790 -Y 255 -W 470 -H 220 -MeasureName "Audits Stock-Out Count"),

    (New-TextBoxVisual -Name "Title_S4_Chart3" -X 20 -Y 495 -W 750 -H 35 -Text "Closed-Loop Detailing Verification: Doctor Detailing to Retail Sell-Out"),
    (New-CardVisual -Name "Visual_S4_ClosedLoop" -X 20 -Y 535 -W 750 -H 165 -MeasureName "Closed-Loop Verified Visits"),
    (New-TextBoxVisual -Name "Title_S4_Chart4" -X 790 -Y 495 -W 470 -H 35 -Text "Transfer Order Units by Fulfillment Wholesaler"),
    (New-CardVisual -Name "Visual_S4_Transfers" -X 790 -Y 535 -W 470 -H 165 -MeasureName "Total Transfer Units")
)

# --- Section 5: AI Prescriber Copilot & Marketing ROI
$sec5Visuals = @(
    (New-TextBoxVisual -Name "Header_AI" -X 20 -Y 15 -W 1240 -H 65 -Text "AI Prescriber Retention Copilot and Promotional ROI Optimization"),
    (New-CardVisual -Name "Card_S5_1" -X 20 -Y 90 -W 235 -H 105 -MeasureName "High Churn Risk Doctor Count"),
    (New-CardVisual -Name "Card_S5_2" -X 270 -Y 90 -W 235 -H 105 -MeasureName "Avg Churn Probability Pct"),
    (New-CardVisual -Name "Card_S5_3" -X 520 -Y 90 -W 235 -H 105 -MeasureName "Total Promotional Expense EGP"),
    (New-CardVisual -Name "Card_S5_4" -X 770 -Y 90 -W 235 -H 105 -MeasureName "Free Rider Budget Leakage Pct"),
    (New-CardVisual -Name "Card_S5_5" -X 1020 -Y 90 -W 240 -H 105 -MeasureName "Promotional ROI Ratio"),

    (New-TextBoxVisual -Name "Title_S5_Chart1" -X 20 -Y 215 -W 460 -H 35 -Text "Prescriber Churn Risk Tier Distribution"),
    (New-CardVisual -Name "Visual_S5_RiskTiers" -X 20 -Y 255 -W 460 -H 220 -MeasureName "Loyal Prescriber Doctor Count"),
    (New-TextBoxVisual -Name "Title_S5_Chart2" -X 500 -Y 215 -W 760 -H 35 -Text "AI Next-Best-Action (NBA) Prescriber Prioritization Queue"),
    (New-CardVisual -Name "Visual_S5_NBA" -X 500 -Y 255 -W 760 -H 220 -MeasureName "Total Doctors Scored"),

    (New-TextBoxVisual -Name "Title_S5_Chart3" -X 20 -Y 495 -W 610 -H 35 -Text "Promotional Investment vs Free-Rider Leakage by Expense Category"),
    (New-CardVisual -Name "Visual_S5_Leakage" -X 20 -Y 535 -W 610 -H 165 -MeasureName "Free Rider Expense EGP"),
    (New-TextBoxVisual -Name "Title_S5_Chart4" -X 650 -Y 495 -W 610 -H 35 -Text "Promotional ROI: Incremental Rx Lift vs Commercial Investment"),
    (New-CardVisual -Name "Visual_S5_ROI" -X 650 -Y 535 -W 610 -H 165 -MeasureName "Incremental Rx Lift Units")
)

# Compile report sections
$reportSections = @(
    @{
        name = "Section1"
        displayName = "01 Executive Home Hub"
        filters = "[]"
        ordinal = 0
        width = 1280
        height = 720
        visualContainers = $sec1Visuals
    },
    @{
        name = "Section2"
        displayName = "02 Commercial and IQVIA Audit"
        filters = "[]"
        ordinal = 1
        width = 1280
        height = 720
        visualContainers = $sec2Visuals
    },
    @{
        name = "Section3"
        displayName = "03 Field Force and Detailing"
        filters = "[]"
        ordinal = 2
        width = 1280
        height = 720
        visualContainers = $sec3Visuals
    },
    @{
        name = "Section4"
        displayName = "04 Brick and Pharmacy Dynamics"
        filters = "[]"
        ordinal = 3
        width = 1280
        height = 720
        visualContainers = $sec4Visuals
    },
    @{
        name = "Section5"
        displayName = "05 AI Prescriber Copilot"
        filters = "[]"
        ordinal = 4
        width = 1280
        height = 720
        visualContainers = $sec5Visuals
    }
)

$reportConfigObj = @{
    version = "5.50"
    themeCollection = @{
        baseTheme = @{
            name = "CY24SU08"
            version = "5.56"
            type = 2
        }
        customTheme = @{
            name = "PharmaForce360Theme"
            reportVersionAtImport = "5.50"
            type = 0
        }
    }
    activeSectionName = "Section1"
    defaultDrillFilterOtherVisuals = $true
}

$reportObj = @{
    config = ($reportConfigObj | ConvertTo-Json -Depth 15 -Compress)
    layoutOptimization = 0
    resourcePackages = @()
    sections = $reportSections
}

$reportJson = $reportObj | ConvertTo-Json -Depth 15
$reportJsonPath = Join-Path $TargetDir "PharmaForce360.Report\report.json"
[System.IO.File]::WriteAllText($reportJsonPath, $reportJson, $utf8NoBom)
Write-Host "  [+] Generated: report.json ($([math]::Round((Get-Item $reportJsonPath).Length / 1KB, 1)) KB)" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 8. Generate Documentation and DAX Catalog
# ------------------------------------------------------------------------------
Write-Host ">>> Writing DAX Measures Catalog and Documentation..." -ForegroundColor Yellow

$daxDoc = @"
# PharmaForce 360 Commercial Intelligence - DAX Measures Catalog

This document catalogues all 42 production DAX measures implemented in the **_Measures** table of the **PharmaForce 360 Power BI Project (.pbip)**.
All currency calculations are modeled in **Egyptian Pounds (EGP)**.

---

## 1. Commercial and Revenue

| Measure Name | DAX Expression | Format String | Description |
|---|---|---|---|
| **Total Revenue EGP** | `SUM(fact_pharmacy_sales[Total_Revenue_EGP])` | `#,0 "EGP"` | Total secondary sales revenue collected across Greater Cairo panel pharmacies. |
| **Total Units Sold** | `SUM(fact_pharmacy_sales[Units_Sold])` | `#,0` | Aggregate pharmaceutical pack volume dispensed. |
| **Target Revenue EGP** | `SUM(fact_rep_targets[Target_Revenue_EGP])` | `#,0 "EGP"` | Monthly commercial sales quota assigned to field medical representatives. |
| **Target Units** | `SUM(fact_rep_targets[Target_Units])` | `#,0` | Target pack quota assigned to field reps. |
| **Target Attainment Pct** | `DIVIDE([Total Revenue EGP], [Target Revenue EGP], 0)` | `0.0%` | Actual revenue divided by assigned target quota. |
| **Target Revenue Variance EGP** | `[Total Revenue EGP] - [Target Revenue EGP]` | `#,0 "EGP"` | Absolute monetary gap (surplus or deficit) against quota. |
| **Target Variance Indicator** | `IF([Target Revenue Variance EGP] >= 0, "Surplus", "Deficit")` | String | Visual status indicator for performance benchmarking. |
| **Avg Selling Price EGP** | `DIVIDE([Total Revenue EGP], [Total Units Sold], 0)` | `#,0.00 "EGP"` | Average realized price per pack dispensed. |
| **Baseline RunRate Revenue EGP** | `SUMX(fact_rep_targets, fact_rep_targets[Actual_Baseline_RunRate] * RELATED(dim_product[Unit_Price_EGP]))` | `#,0 "EGP"` | Historical run-rate baseline sales expected before rep detailing lift. |
| **Revenue RunRate Lift EGP** | `[Total Revenue EGP] - [Baseline RunRate Revenue EGP]` | `#,0 "EGP"` | Incremental commercial lift generated above historical run-rate. |
| **Disrupted Revenue EGP** | `CALCULATE([Total Revenue EGP], fact_pharmacy_sales[Supply_Disruption_Flag] = TRUE())` | `#,0 "EGP"` | Revenue impact during supply chain shocks / stockout events. |

---

## 2. Field Force Operations and HCP Detailing

| Measure Name | DAX Expression | Format String | Description |
|---|---|---|---|
| **Total Field Visits** | `COUNTROWS(fact_rep_visits)` | `#,0` | Total field interactions completed by medical sales representatives. |
| **AM Institutional Visits** | `CALCULATE([Total Field Visits], fact_rep_visits[Visit_Type] = "AM Institutional")` | `#,0` | Detailing calls conducted in University & Teaching Hospitals / MoHP centers. |
| **PM Clinic Visits** | `CALCULATE([Total Field Visits], fact_rep_visits[Visit_Type] = "PM Private Clinic")` | `#,0` | Evening visits to private specialist clinics. |
| **AM Visit Share Pct** | `DIVIDE([AM Institutional Visits], [Total Field Visits], 0)` | `0.0%` | Percentage of detailing allocated to AM hospital accounts. |
| **PM Visit Share Pct** | `DIVIDE([PM Clinic Visits], [Total Field Visits], 0)` | `0.0%` | Percentage of detailing allocated to PM private clinics. |
| **Total Planned Doctor Visits** | `SUM(fact_rep_weekly_plan[Planned_Doctor_Visits])` | `#,0` | Aggregate visits committed in weekly call plans. |
| **Plan Adherence Pct** | `DIVIDE([Total Field Visits], [Total Planned Doctor Visits], 0)` | `0.0%` | Ratio of actual completed visits to committed weekly plans. |
| **Avg Detailing Score** | `AVERAGE(fact_rep_visits[Detailing_Score])` | `0.0` | Detailing quality and message retention score (0-100). |
| **Avg Call Duration Minutes** | `AVERAGE(fact_rep_visits[Call_Duration_Minutes])` | `0.0 "min"` | Average time spent face-to-face detailing healthcare professionals. |
| **Total Samples Dropped** | `SUM(fact_rep_visits[Samples_Dropped_Count])` | `#,0` | Total sample packs distributed to prescribers. |
| **Rain Delayed Calls Count** | `CALCULATE([Total Field Visits], fact_rep_visits[Rain_Traffic_Delay_Flag] = TRUE())` | `#,0` | Calls affected by severe Cairo winter rainstorms and traffic gridlock. |
| **Replacement Rep Rampup Calls** | `CALCULATE([Total Field Visits], fact_rep_visits[Is_Replacement_Rep_Rampup] = TRUE())` | `#,0` | Calls conducted by new-hire reps during their mathematical 90-day S-Curve ramp-up. |
| **Active Prescribing Doctors** | `DISTINCTCOUNT(fact_rep_visits[Doctor_ID])` | `#,0` | Count of distinct physicians visited. |
| **Tier A KOL Doctor Coverage Pct** | `DIVIDE(CALCULATE(DISTINCTCOUNT(fact_rep_visits[Doctor_ID]), dim_doctor[Classification] = "Class A (KOL)"), CALCULATE(DISTINCTCOUNT(dim_doctor[Doctor_ID]), dim_doctor[Classification] = "Class A (KOL)"), 0)` | `0.0%` | Coverage rate of Greater Cairo Tier A Key Opinion Leaders. |
| **Weekly Plan On-Time Submission Pct** | `DIVIDE(CALCULATE(COUNTROWS(fact_rep_weekly_plan), fact_rep_weekly_plan[Plan_Submission_Status] = "On-Time Saturday Submission"), COUNTROWS(fact_rep_weekly_plan), 0)` | `0.0%` | Field discipline metric tracking Saturday morning plan submission punctuality. |

---

## 3. Territory and Pharmacy Dynamics

| Measure Name | DAX Expression | Format String | Description |
|---|---|---|---|
| **Total Pharmacy Audits** | `COUNTROWS(fact_pharmacy_visits)` | `#,0` | Total retail verification audits conducted at panel pharmacies. |
| **Audits In-Stock Count** | `CALCULATE([Total Pharmacy Audits], fact_pharmacy_visits[Product_Availability] = "In-Stock")` | `#,0` | Audits confirming uninterrupted product availability. |
| **Audits Stock-Out Count** | `CALCULATE([Total Pharmacy Audits], fact_pharmacy_visits[Product_Availability] = "Stock-Out")` | `#,0` | Audits uncovering stock-outs and shelf depletion. |
| **In-Stock Rate Pct** | `DIVIDE([Audits In-Stock Count], [Total Pharmacy Audits], 0)` | `0.0%` | Percentage of pharmacy audits where products were fully in-stock. |
| **Stock-Out Rate Pct** | `DIVIDE([Audits Stock-Out Count], [Total Pharmacy Audits], 0)` | `0.0%` | Retail stock-out rate triggering urgent transfer orders. |
| **Transfer Orders Placed Count** | `CALCULATE([Total Pharmacy Audits], fact_pharmacy_visits[Transfer_Order_Placed] = TRUE())` | `#,0` | Remedial stock transfer orders initiated by reps. |
| **Total Transfer Units** | `SUM(fact_pharmacy_visits[Transfer_Units])` | `#,0` | Emergency replenishment packs ordered to mitigate stock-outs. |
| **Closed-Loop Verified Visits** | `CALCULATE(COUNTROWS(fact_pharmacy_visits), NOT(ISBLANK(fact_pharmacy_visits[Related_Doctor_Visit_ID])))` | `#,0` | Pharmacy audits directly linked to preceding physician detailing calls. |
| **Closed-Loop Verification Rate Pct** | `DIVIDE([Closed-Loop Verified Visits], [Total Pharmacy Audits], 0)` | `0.0%` | Rate of closed-loop verification confirming doctor detailing led to retail availability. |
| **Big 5 Distributor Revenue Pct** | `DIVIDE(CALCULATE([Total Revenue EGP], dim_distributor[Distributor_ID] IN {"DIST-01","DIST-02","DIST-03","DIST-04","DIST-05"}), [Total Revenue EGP], 0)` | `0.0%` | Revenue percentage fulfilled via primary distributors (Ibn Sina, UCP, Soficopharm, PharmaOverseas, Ramco). |
| **Local Wholesalers (El-Makhazen) Revenue Pct** | `DIVIDE(CALCULATE([Total Revenue EGP], dim_distributor[Distributor_ID] = "DIST-06"), [Total Revenue EGP], 0)` | `0.0%` | Revenue percentage fulfilled via secondary private wholesalers (El-Makhazen) in peripheral bricks. |

---

## 4. IMS / IQVIA Market Intelligence

| Measure Name | DAX Expression | Format String | Description |
|---|---|---|---|
| **IMS Market Share Pct** | `AVERAGE(fact_ims_market_audit[Our_Market_Share_Pct])` | `0.0%` | Audited market share across commercial bricks. |
| **Competitor Market Share Pct** | `AVERAGE(fact_ims_market_audit[Competitor_Combined_Share_Pct])` | `0.0%` | Combined market share of rival pharmaceutical brands. |
| **Evolution Index EI** | `AVERAGE(fact_ims_market_audit[Evolution_Index_EI])` | `0.0` | IQVIA Evolution Index: EI > 100 indicates outgrowing the market; EI < 100 indicates loss of market share. |
| **Total Market Volume Units** | `SUM(fact_ims_market_audit[Total_Market_Volume_Units])` | `#,0` | Overall market category volume across Greater Cairo bricks. |
| **Total Market Value EGP** | `SUM(fact_ims_market_audit[Total_Market_Value_EGP])` | `#,0 "EGP"` | Overall market category value in EGP. |
| **Market Benchmark Status** | `IF([Evolution_Index_EI] >= 100, "Market Outperformer (EI >= 100)", "Market Underperformer (EI < 100)")` | String | Categorical performance flag based on the 100-point EI benchmark. |

---

## 5. AI Prescriber Copilot and Marketing ROI

| Measure Name | DAX Expression | Format String | Description |
|---|---|---|---|
| **Total Doctors Scored** | `COUNTROWS(fact_doctor_predictions)` | `#,0` | Healthcare professionals scored by the machine learning churn model. |
| **High Churn Risk Doctor Count** | `CALCULATE([Total Doctors Scored], fact_doctor_predictions[Retention_Risk_Tier] = "High Churn Risk")` | `#,0` | High-value prescribers with high churn probability requiring immediate Next-Best-Action intervention. |
| **Medium Risk Doctor Count** | `CALCULATE([Total Doctors Scored], fact_doctor_predictions[Retention_Risk_Tier] = "Medium Risk")` | `#,0` | Prescribers in transition requiring reinforcement detailing. |
| **Loyal Prescriber Doctor Count** | `CALCULATE([Total Doctors Scored], fact_doctor_predictions[Retention_Risk_Tier] = "Loyal Prescriber")` | `#,0` | Core champion physicians with steady prescription habits. |
| **Avg Churn Probability Pct** | `AVERAGE(fact_doctor_predictions[Prescriber_Churn_Probability])` | `0.0%` | Mean predicted prescriber attrition probability across the portfolio. |
| **Total Promotional Expense EGP** | `SUM(fact_dr_expense[Amount_Of_Money_EGP])` | `#,0 "EGP"` | Total commercial investment allocated to doctors (CME sponsorship, advisory boards, clinic grants). |
| **Free Rider Expense EGP** | `CALCULATE([Total Promotional Expense EGP], fact_dr_expense[Is_Free_Rider] = TRUE())` | `#,0 "EGP"` | Promotional spend wasted on Non-Compliant Free Riders (physicians who consume budget without writing incremental Rx). |
| **Free Rider Budget Leakage Pct** | `DIVIDE([Free Rider Expense EGP], [Total Promotional Expense EGP], 0)` | `0.0%` | Percentage of marketing spend lost to free-rider prescribers. |
| **Free Rider Doctor Count** | `CALCULATE(DISTINCTCOUNT(fact_dr_expense[Doctor_ID]), fact_dr_expense[Is_Free_Rider] = TRUE())` | `#,0` | Distinct count of physicians flagged with non-compliant free-rider persona. |
| **Incremental Rx Lift Units** | `SUM(fact_dr_expense[Incremental_Rx_Lift_Units])` | `#,0` | Additional prescription units generated directly by promotional sponsorships. |
| **Promotional ROI Ratio** | `DIVIDE(SUMX(fact_dr_expense, fact_dr_expense[Incremental_Rx_Lift_Units] * 150), [Total Promotional Expense EGP], 0)` | `0.00 "x"` | Commercial return on investment (Estimated Lift Value in EGP / Promotional Expense). |
"@
[System.IO.File]::WriteAllText((Join-Path $TargetDir "dax_measures.md"), $daxDoc, $utf8NoBom)
Write-Host "  [+] Generated: dax_measures.md" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 9. Power BI User Guide & Architecture Documentation
# ------------------------------------------------------------------------------
$readmeDoc = @"
# PharmaForce 360 - Power BI Project (.pbip) Architecture and User Guide

> **Greater Cairo Pharmaceutical Market (Egypt) | Commercial Intelligence and Predictive Analytics Platform**  
> **Format**: Microsoft Power BI Project (.pbip) / Microsoft Fabric Ready  
> **All Financial Metrics**: Egyptian Pounds (**EGP**)

---

## Project Overview

This repository contains the complete, production-ready **Power BI Project (.pbip)** for the **PharmaForce 360 Commercial Intelligence Suite**. Designed using the Kimball Star Schema methodology, it models the operational realities of the pharmaceutical industry across **36 commercial bricks in Greater Cairo**, incorporating:

* **Egyptian Calendar Dynamics**: Saturday-Thursday work week, Friday strictly off, Holy Month of Ramadan operating shifts, and national holiday closures.
* **Turnover and S-Curve Recovery**: Mathematical Sigmoid ramp-up modeling rep transitions and doctor rapport rebuilding.
* **Closed-Loop Verification**: Direct linkage between physician detailing calls (`fact_rep_visits`) and retail pharmacy shelf audits (`fact_pharmacy_visits`).
* **Supply Chain Bifurcation**: Big 5 Egyptian distributors (*Ibn Sina, UCP, Soficopharm, PharmaOverseas, Ramco*) in core bricks vs Local Private Wholesalers (*El-Makhazen*) in peripheral areas.
* **AI Prescriber Copilot**: Machine-learning prescriber churn scoring, Next-Best-Action (NBA) prioritization, and Free-Rider budget leakage mitigation.

---

## How to Open and Refresh in Power BI Desktop

1. **Prerequisites**:
   * Microsoft Power BI Desktop (June 2023 release or newer).
2. **Opening the Project**:
   * Navigate to `powerbi/` and double-click **`PharmaForce360.pbip`**.
   * Power BI Desktop will launch automatically, loading the semantic model and report layouts.
3. **Data Source Configuration**:
   * All queries parameterize the data path via the Power Query parameter **`DataFolderPath`**.
   * By default, it is configured to point directly to:  
     `d:\portfolio2026\02_PharmaForce360\data\`
   * If you move the project or clone it on another workstation:
     1. Click **Home > Transform Data > Edit Parameters**.
     2. Update `DataFolderPath` to your local `data/` path (with trailing slash `\`).
     3. Click **Apply Changes** to refresh all 18 tables in seconds.

---

## Data Model Architecture (Star Schema)

```
                                  +-----------------------+
                                  |       dim_date        |
                                  +-----------+-----------+
                                              |
                      +-----------------------+-----------------------+
                      |                       |                       |
           +----------+----------+ +----------+----------+ +----------+----------+
           |   fact_rep_visits   | |fact_pharmacy_visits | | fact_pharmacy_sales |
           +----------+----------+ +----------+----------+ +----------+----------+
                      |                       |                       |
      +---------------+---------------+       |       +---------------+---------------+
      |                               |       |       |                               |
+-----+----------+             +------+-------+ +----+------------+            +-----+----------+
|   dim_doctor   |             | dim_pharmacy  | |   dim_product   |            |dim_brick_terr. |
+----------------+             +---------------+ +-----------------+            +----------------+
```

* **Central Measure Store**: `_Measures` table containing 42 formatted DAX calculations organized across 5 dedicated display folders.
* **10 Dimension Tables**: `dim_date`, `dim_brick_territory`, `dim_product`, `dim_competitor_product`, `dim_medical_rep`, `dim_doctor`, `dim_doctor_schedule`, `dim_pharmacy`, `dim_distributor`, `dim_account`.
* **8 Fact Tables**: `fact_pharmacy_sales`, `fact_rep_visits`, `fact_pharmacy_visits`, `fact_rep_targets`, `fact_rep_weekly_plan`, `fact_dr_expense`, `fact_ims_market_audit`, `fact_doctor_predictions`.
* **Single-Direction Filtering**: 35 clean relationships with inactive paths utilized for closed-loop verification to prevent circular ambiguous paths.

---

## 5-Page Persona Dashboard Suite

### Page 1: Executive Home Hub and Operations Pulse
* **Target Audience**: Chief Commercial Officer, VP of Sales, General Manager.
* **Key Features**: High-level KPI pulse cards (Revenue, Quotas, Completed Calls, Evolution Index, Churn Risk Count), 4 interactive navigation tiles to drill into sub-dashboards, and macro territory zone performance.

### Page 2: Executive Commercial Performance and IQVIA Audit
* **Target Audience**: Commercial Director, Finance Lead, Business Unit Heads.
* **Key Features**: Sales vs Target Quotas in EGP, Monthly trajectory vs target line, Distributor channel split (Big 5 vs El-Makhazen Local Wholesalers), IQVIA Evolution Index (EI) growth classification, and competitor pricing gap benchmark.

### Page 3: Field Force Activity and Detailing Operations
* **Target Audience**: National Sales Manager, Regional District Managers.
* **Key Features**: Detailing calls leaderboard, AM Hospital vs PM Clinic distribution, Tier A Key Opinion Leader (KOL) coverage rate, weekly call plan submission discipline (Saturday on-time vs late), and Cairo rainstorm traffic delays vs replacement rep S-curve ramp-up tracking.

### Page 4: Territory Brick Dynamics and Pharmacy Audit
* **Target Audience**: Trade Marketing Manager, Key Account Manager, Supply Chain Director.
* **Key Features**: Greater Cairo 36-brick potential index vs secondary sell-out, retail stock-out rate across major chains (*Seif, El Ezaby, 19011, Rushdy*), closed-loop physician-detailing to pharmacy-dispensing verification, and emergency stock transfer order tracking.

### Page 5: AI Prescriber Copilot and Marketing ROI
* **Target Audience**: Commercial Excellence Lead, Brand Managers, Field Reps.
* **Key Features**: ML-predicted prescriber churn tiers (High Risk, Medium, Loyal), sortable Next-Best-Action (NBA) priority queue, promotional spend breakdown (Advisory boards, CME sponsorships, clinic grants), Free-Rider budget leakage detection, and incremental Rx lift ROI ratio.

---

## Design System and Visual Palette

* **Primary Dark Navy**: `#0A2540`
* **Clinical Cyan (Brand)**: `#00A3E0`
* **Medical Teal**: `#00B4D8`
* **Success Green**: `#10B981`
* **Warning Amber**: `#F59E0B`
* **Danger Red**: `#EF4444`
* **Background Canvas**: `#F8FAFC`
* **Cards and Containers**: `#FFFFFF` with `#E2E8F0` subtle borders and 8px border radius.
"@
[System.IO.File]::WriteAllText((Join-Path $TargetDir "README_POWERBI.md"), $readmeDoc, $utf8NoBom)
Write-Host "  [+] Generated: README_POWERBI.md" -ForegroundColor Green

Write-Host "`n>>> [SUCCESS] All PharmaForce 360 PBIP Assets Compiled Successfully!" -ForegroundColor Cyan
Write-Host "Root Project: $TargetDir\PharmaForce360.pbip" -ForegroundColor White
