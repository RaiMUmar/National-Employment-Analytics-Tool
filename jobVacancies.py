#!/usr/bin/env python3

"""
Author: Rai Umar 

jobVacancies.py

This Python script demonstrates how to read and merge three separate datasets. 
Job vacancies, educational attainment, and income—across different Canadian provinces. 
It cleans each CSV (e.g., forward-filling blank rows and standardizing province names) and then produces:
1. Plots monthly job vacancies by province
2. Correlates the percentage of adults with tertiary education to average job vacancies in each province.
3. Compares the average income (25–34 age group) to that province’s tertiary‐education rate.


Menu of three questions:
1) Job Market Trends & Demand 
2) Education vs. Employment Vacancies       
3) Income vs. Education (by Age Group)  

Last Update Date: March 26 2025

To Run File:
Type in terminal: python3 jobVacancies.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# Helper: Standardize province names
def standardize_province_names(name):
    """
    Convert possible float/NaN to string, strip whitespace, fix known mismatches.
    """
    if not isinstance(name, str):
        name = str(name)

    name = name.strip()

    # Remove trailing " 10" if present
    if name.endswith(" 10"):
        name = name.replace(" 10", "")

    # Known name replacements (expand as needed)
    name_map = {
        "Québec": "Quebec",
        # e.g., "Canada10": "Canada",
    }
    if name in name_map:
        name = name_map[name]

    return name

# 1) JOB MARKET TRENDS (Line Chart)
def plot_job_market_trends(vacancy_csv="data.csv"):
    """
    "How have job openings changed in different provinces over a five-year period?"
    Reads job vacancy CSV, filters to "Job vacancies 4", then
    plots monthly columns by province as a line chart.
    Excludes "Canada" from the chart.
    """
    print("Generating Job Market Trends (Line Chart)...")
    try:
        df = pd.read_csv(
            vacancy_csv,
            skiprows=8,       
            header=0,
            skipfooter=25,    
            engine="python",
            on_bad_lines="skip"
        )

        # Forward-fill and standardize "Geography"
        df["Geography"] = df["Geography"].ffill()
        df["Geography"] = df["Geography"].apply(standardize_province_names)

        # Filter to "Job vacancies 4"
        df = df[df["Statistics"] == "Job vacancies 4"]
        if df.empty:
            print("No rows found for 'Job vacancies 4'. Check your CSV content.")
            return

        # Exclude "Canada"
        df = df[df["Geography"] != "Canada"]

        # Convert monthly columns to numeric
        for col in df.columns[2:]:
            df[col] = df[col].replace(",", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Example monthly columns
        month_cols = ["August 2024", "September 2024", "October 2024"]
        month_cols = [m for m in month_cols if m in df.columns]
        if not month_cols:
            print("No valid month columns found for plotting in job vacancy data.")
            return

        # Pivot: rows -> provinces, columns -> months
        plot_df = df.set_index("Geography")[month_cols]

        # Plot a line chart (transpose so months are on X-axis)
        plot_df.T.plot(figsize=(10, 6))
        plt.title("Job Vacancies by Province/Territory")
        plt.xlabel("Month")
        plt.ylabel("Number of Vacancies")
        plt.legend(title="Province/Territory", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[Error in plot_job_market_trends]: {e}")

# 2) EDUCATION vs. EMPLOYMENT VACANCIES
def plot_education_vs_vacancies(vacancy_csv="data.csv", education_csv="education.csv"):
    """
    "What is the relationship between education level and employment vacancy rates in Canada?"
    Excludes "Canada" from the charts.
    """
    print("Generating Education vs. Employment Vacancies chart...")
    try:
        # Vacancy Data
        df_vac = pd.read_csv(
            vacancy_csv,
            skiprows=8,
            header=0,
            skipfooter=25,
            engine="python",
            on_bad_lines="skip"
        )
        df_vac["Geography"] = df_vac["Geography"].ffill()
        df_vac["Geography"] = df_vac["Geography"].apply(standardize_province_names)
        df_vac = df_vac[df_vac["Statistics"] == "Job vacancies 4"]
        if df_vac.empty:
            print("No rows found for 'Job vacancies 4'.")
            return

        # Exclude "Canada"
        df_vac = df_vac[df_vac["Geography"] != "Canada"]

        for col in df_vac.columns[2:]:
            df_vac[col] = df_vac[col].replace(",", "", regex=True)
            df_vac[col] = pd.to_numeric(df_vac[col], errors="coerce")

        # Average vacancy across columns
        df_vac["AverageVacancies"] = df_vac[df_vac.columns[2:]].mean(axis=1)

        # Education Data
        df_edu = pd.read_csv(
            education_csv,
            skiprows=10,
            header=0,
            skipfooter=24,
            engine="python",
            on_bad_lines="skip"
        )
        # Forward-fill "Geography"
        df_edu["Geography"] = df_edu["Geography"].ffill()
        df_edu["Geography"] = df_edu["Geography"].apply(standardize_province_names)

        # If "Canada" appears here, optionally exclude it as well
        df_edu = df_edu[df_edu["Geography"] != "Canada"]

        df_tertiary = df_edu[df_edu["Educational attainment level 7"] == "Tertiary education"]
        df_tertiary = df_tertiary.rename(columns={"2023": "TertiaryEduPct"})
        df_tertiary["TertiaryEduPct"] = df_tertiary["TertiaryEduPct"].str.replace("[^0-9.]", "", regex=True)
        df_tertiary["TertiaryEduPct"] = pd.to_numeric(df_tertiary["TertiaryEduPct"], errors="coerce")

        merged_df = pd.merge(df_vac, df_tertiary, on="Geography", how="inner")
        if merged_df.empty:
            print("No matched provinces after merging. Check name standardization or skip logic.")
            return

        x = merged_df["TertiaryEduPct"]
        y = merged_df["AverageVacancies"]
        plt.figure(figsize=(8, 5))
        plt.scatter(x, y)
        plt.title("Tertiary Education (%) vs. Average Job Vacancies")
        plt.xlabel("Tertiary Education (%) (2023)")
        plt.ylabel("Average Vacancies")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[Error in plot_education_vs_vacancies]: {e}")

# 3) INCOME vs. EDUCATION
def plot_income_vs_education(income_csv="income.csv", education_csv="education.csv"):
    """
    "How does income vary based on age group and education level across Canada?"
    Excludes "Canada" from the charts.
    """
    print("Generating Income vs. Education chart...")
    try:
        # Income Data
        df_inc = pd.read_csv(
            income_csv,
            skiprows=0,
            header=0,
            engine="python",
            on_bad_lines="skip"
        )
        df_inc = df_inc[df_inc["Statistics"] == "Average income (excluding zeros)"]
        if df_inc.empty:
            print("No rows found for 'Average income (excluding zeros)'.")
            return

        df_inc["VALUE"] = pd.to_numeric(df_inc["VALUE"], errors="coerce")
        df_inc = df_inc[df_inc["Age group"] == "25 to 34 years"]
        if df_inc.empty:
            print("No rows found for '25 to 34 years'.")
            return

        df_inc["GEO"] = df_inc["GEO"].apply(standardize_province_names)

        # Exclude "Canada"
        df_inc = df_inc[df_inc["GEO"] != "Canada"]

        grouped_inc = df_inc.groupby("GEO")["VALUE"].mean().reset_index()
        grouped_inc = grouped_inc.rename(columns={
            "GEO": "Province",
            "VALUE": "AvgIncome_25to34"
        })

        # Education Data
        df_edu = pd.read_csv(
            education_csv,
            skiprows=10,
            header=0,
            skipfooter=24,
            engine="python",
            on_bad_lines="skip"
        )
        df_edu["Geography"] = df_edu["Geography"].ffill()
        df_edu["Geography"] = df_edu["Geography"].apply(standardize_province_names)
        # Exclude "Canada" if present
        df_edu = df_edu[df_edu["Geography"] != "Canada"]

        df_tertiary = df_edu[df_edu["Educational attainment level 7"] == "Tertiary education"]
        df_tertiary = df_tertiary.rename(columns={"2023": "TertiaryEduPct"})
        df_tertiary["TertiaryEduPct"] = df_tertiary["TertiaryEduPct"].str.replace("[^0-9.]", "", regex=True)
        df_tertiary["TertiaryEduPct"] = pd.to_numeric(df_tertiary["TertiaryEduPct"], errors="coerce")
        df_tertiary = df_tertiary.rename(columns={"Geography": "Province"})

        merged = pd.merge(grouped_inc, df_tertiary, on="Province", how="inner")
        if merged.empty:
            print("No matched provinces between income & education. Check name standardization.")
            return

        x = merged["TertiaryEduPct"]
        y = merged["AvgIncome_25to34"]

        plt.figure(figsize=(8, 5))
        plt.scatter(x, y)
        plt.title("Avg Income (25–34) vs. Tertiary Education (%) For Each Province")
        plt.xlabel("Tertiary Education (%) (2023)")
        plt.ylabel("Avg Income (excluding zeros), 25–34 yrs")
        plt.grid(True)

        for i, row in merged.iterrows():
            plt.annotate(row["Province"], (row["TertiaryEduPct"], row["AvgIncome_25to34"]))

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[Error in plot_income_vs_education]: {e}")

# MAIN MENU
def main():
    while True:
        print("\nSelect a graph to display (Excluding Canada):")
        print("1) Job Market Trends & Demand (Line Chart)")
        print("2) Education vs. Employment Vacancies")
        print("3) Income vs. Education (by Age Group)")
        print("4) Show ALL")
        print("Q) Quit")

        choice = input("Enter choice: ").strip().lower()
        if choice == "1":
            plot_job_market_trends("data.csv")
        elif choice == "2":
            plot_education_vs_vacancies("data.csv", "education.csv")
        elif choice == "3":
            plot_income_vs_education("income.csv", "education.csv")
        elif choice == "4":
            plot_job_market_trends("data.csv")
            plot_education_vs_vacancies("data.csv", "education.csv")
            plot_income_vs_education("income.csv", "education.csv")
        elif choice == "q":
            print("Exiting the script. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()