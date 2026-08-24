"""
analysis.py
------------
COVID-19 Public Health Data Analysis
Data Analyst Portfolio Project | Python (Pandas, NumPy, Matplotlib, Seaborn)

Pipeline:
1. Load raw data (real OWID dataset or the demo dataset)
2. Clean & preprocess
3. Exploratory Data Analysis (EDA)
4. Generate charts (saved to /charts)
5. Export summary tables (for Power BI dashboard import)

Usage:
    python3 analysis.py

To use REAL data instead of the demo dataset:
    1. Download https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv
       ("Download raw file" button)
    2. Save it in this folder as owid-covid-data.csv
    3. Re-run this script — it auto-detects the real file if present.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("charts", exist_ok=True)
os.makedirs("exports_for_powerbi", exist_ok=True)

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
REAL_FILE = "owid-covid-data.csv"
DEMO_FILE = "covid_sample_data.csv"

if os.path.exists(REAL_FILE):
    print(f"Loading REAL dataset: {REAL_FILE}")
    df = pd.read_csv(REAL_FILE)
    using_real_data = True
else:
    print(f"'{REAL_FILE}' not found — using demo dataset: {DEMO_FILE}")
    print("(Download the real OWID dataset for your actual submission — see script docstring.)")
    df = pd.read_csv(DEMO_FILE)
    using_real_data = False

df["date"] = pd.to_datetime(df["date"])

# ---------------------------------------------------------
# 2. CLEAN & PREPROCESS
# ---------------------------------------------------------
key_cols = ["location", "continent", "date", "population",
            "new_cases", "total_cases", "new_deaths", "total_deaths",
            "new_vaccinations", "total_vaccinations"]
key_cols = [c for c in key_cols if c in df.columns]
df = df[key_cols].copy()

# Drop aggregate rows OWID includes for continents/world/income groups
if "continent" in df.columns:
    df = df[df["continent"].notna()]

numeric_cols = [c for c in key_cols if c not in ("location", "continent", "date")]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(0)
    df[col] = df[col].clip(lower=0)  # remove negative data-correction artifacts for daily figures

df = df.sort_values(["location", "date"]).reset_index(drop=True)

print(f"\nCleaned dataset: {len(df):,} rows | {df['location'].nunique()} countries | "
      f"{df['date'].min().date()} to {df['date'].max().date()}")

# ---------------------------------------------------------
# 3. EXPLORATORY DATA ANALYSIS
# ---------------------------------------------------------

# --- Global daily trend ---
global_trend = df.groupby("date")[["new_cases", "new_deaths"]].sum().reset_index()
global_trend["cases_7day_avg"] = global_trend["new_cases"].rolling(7).mean()
global_trend["deaths_7day_avg"] = global_trend["new_deaths"].rolling(7).mean()

plt.figure(figsize=(11, 5))
plt.plot(global_trend["date"], global_trend["cases_7day_avg"], color="#1F3864", linewidth=2)
plt.title("Global Daily New Cases — 7-Day Rolling Average", fontsize=13, fontweight="bold")
plt.xlabel("Date"); plt.ylabel("New Cases (7-day avg)")
plt.tight_layout()
plt.savefig("charts/01_global_daily_cases_trend.png", dpi=150)
plt.close()

# --- Top 10 countries by total cases (latest snapshot) ---
latest = df.sort_values("date").groupby("location").tail(1)
top10_cases = latest.nlargest(10, "total_cases")[["location", "total_cases"]]

plt.figure(figsize=(9, 5))
sns.barplot(data=top10_cases, y="location", x="total_cases", hue="location",
            palette="Blues_r", legend=False)
plt.title("Top 10 Countries by Total Confirmed Cases", fontsize=13, fontweight="bold")
plt.xlabel("Total Cases"); plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/02_top10_countries_cases.png", dpi=150)
plt.close()

# --- Case Fatality Rate by country (top 10 by total cases) ---
latest = latest.copy()
latest["case_fatality_rate_%"] = np.where(
    latest["total_cases"] > 0,
    (latest["total_deaths"] / latest["total_cases"]) * 100,
    0
)
cfr_top10 = latest.nlargest(10, "total_cases")[["location", "case_fatality_rate_%"]]

plt.figure(figsize=(9, 5))
sns.barplot(data=cfr_top10, y="location", x="case_fatality_rate_%", hue="location",
            palette="Reds_r", legend=False)
plt.title("Case Fatality Rate (%) — Top 10 Countries by Case Volume", fontsize=13, fontweight="bold")
plt.xlabel("Case Fatality Rate (%)"); plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/03_case_fatality_rate.png", dpi=150)
plt.close()

# --- Vaccination progress over time (top 5 countries by population) ---
if "total_vaccinations" in df.columns:
    top5_pop = latest.nlargest(5, "population")["location"].tolist()
    vax_trend = df[df["location"].isin(top5_pop)]

    plt.figure(figsize=(11, 5))
    for country in top5_pop:
        sub = vax_trend[vax_trend["location"] == country]
        plt.plot(sub["date"], sub["total_vaccinations"], label=country, linewidth=2)
    plt.title("Cumulative Vaccinations Over Time — 5 Largest Countries by Population",
               fontsize=13, fontweight="bold")
    plt.xlabel("Date"); plt.ylabel("Total Vaccinations")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("charts/04_vaccination_progress.png", dpi=150)
    plt.close()

# --- Cases per million (normalized comparison) ---
latest["cases_per_million"] = (latest["total_cases"] / latest["population"]) * 1_000_000
top10_per_capita = latest.nlargest(10, "cases_per_million")[["location", "cases_per_million"]]

plt.figure(figsize=(9, 5))
sns.barplot(data=top10_per_capita, y="location", x="cases_per_million", hue="location",
            palette="Purples_r", legend=False)
plt.title("Top 10 Countries by Cases per Million (Population-Adjusted)",
           fontsize=13, fontweight="bold")
plt.xlabel("Cases per Million"); plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/05_cases_per_million.png", dpi=150)
plt.close()

print("\n5 charts saved to /charts")

# ---------------------------------------------------------
# 4. EXPORT CLEAN SUMMARY TABLES FOR POWER BI
# ---------------------------------------------------------
# Power BI works best off tidy, pre-aggregated tables rather than raw daily
# data for every visual — export both a full clean table and key summaries.

df.to_csv("exports_for_powerbi/clean_full_data.csv", index=False)

latest_summary = latest[[
    "location", "continent", "population", "total_cases", "total_deaths",
    "total_vaccinations", "case_fatality_rate_%", "cases_per_million"
]].sort_values("total_cases", ascending=False)
latest_summary.to_csv("exports_for_powerbi/country_summary_latest.csv", index=False)

global_trend.to_csv("exports_for_powerbi/global_daily_trend.csv", index=False)

continent_summary = df.groupby("continent")[["new_cases", "new_deaths"]].sum().reset_index()
continent_summary.to_csv("exports_for_powerbi/continent_summary.csv", index=False)

print("Export files saved to /exports_for_powerbi:")
print("  - clean_full_data.csv         (full cleaned dataset)")
print("  - country_summary_latest.csv  (latest snapshot per country, KPIs)")
print("  - global_daily_trend.csv      (daily global trend, 7-day avg)")
print("  - continent_summary.csv       (totals by continent)")

if not using_real_data:
    print("\nNOTE: This run used DEMO data. Replace with the real OWID dataset")
    print("before treating these charts/exports as your final project output.")
