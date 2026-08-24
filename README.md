# COVID-19 Public Health Data Analysis & Dashboard

**Tools:** Python (Pandas, NumPy, Matplotlib, Seaborn) · Power BI · Public Health Data

## Project Overview
End-to-end data analysis project on global COVID-19 case, death, and vaccination
data. Covers data cleaning, exploratory data analysis (EDA), and an interactive
Power BI dashboard tracking pandemic trends across countries and time.

## Files in this project
| File | Purpose |
|---|---|
| `analysis.py` | Main pipeline: cleans data, runs EDA, generates charts, exports Power BI-ready tables |
| `generate_demo_data.py` | Creates a small demo dataset so you can test-run the pipeline immediately |
| `covid_sample_data.csv` | Demo/test dataset (synthetic, for pipeline testing only) |
| `charts/` | 5 EDA visualizations (PNG) |
| `exports_for_powerbi/` | 4 clean CSVs, ready to import into Power BI |

## Step 1 — Get the REAL dataset (important)
The demo dataset included here is synthetic and only meant to let you test
that the code runs. **For your actual resume-worthy project, use real data:**

1. Go to: https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv
2. Click **"Download raw file"**
3. Save it in this same folder as `owid-covid-data.csv`
4. Re-run `python3 analysis.py` — it automatically detects and uses the real file

This is Our World in Data's dataset — the same source used by most public COVID
dashboards and news outlets, updated with full historical data across ~200 countries.

## Step 2 — Run the analysis
```bash
pip install pandas numpy matplotlib seaborn
python3 analysis.py
```
This produces:
- 5 PNG charts in `/charts` (global trend, top countries, fatality rate, vaccination progress, per-capita comparison)
- 4 clean CSVs in `/exports_for_powerbi`, ready to load into Power BI

## Step 3 — Build the Power BI dashboard
Power BI Desktop only runs on Windows, so build this part locally:

1. Open **Power BI Desktop** → Get Data → Text/CSV → import all 4 files from `/exports_for_powerbi`
2. Go to **Model view** and relate the tables on `location` (country name) where relevant
3. Build these visuals (mirrors what a real analyst dashboard looks like):
   - **Card visuals**: Total Cases, Total Deaths, Total Vaccinations (from `country_summary_latest.csv`, summed)
   - **Line chart**: `global_daily_trend.csv` → date (x-axis) vs. `cases_7day_avg` and `deaths_7day_avg`
   - **Bar chart**: `country_summary_latest.csv` → top 10 countries by `total_cases`
   - **Map visual**: `country_summary_latest.csv` → `location` field, bubble size = `total_cases`
   - **Bar chart**: `case_fatality_rate_%` by country
   - **Stacked bar**: `continent_summary.csv` → cases/deaths by continent
4. Add a **date slicer** so the dashboard is interactive
5. Save as `covid_dashboard.pbix`

## Key Insights to Write Up (based on demo run — verify against real data)
- Global daily cases followed a multi-wave pattern, with the largest wave in mid-2021
- Vaccination rollout began ramping in early-to-mid 2021, coinciding with the decline after the final wave
- Case fatality rate varied noticeably by country, reflecting differences in healthcare capacity and testing coverage
- Larger, more densely tested countries dominate raw case counts, but per-capita (cases-per-million) rankings tell a different story — worth highlighting both views

## Resume Bullet (once you've run it on real data)
> Built an end-to-end COVID-19 data analysis project using Python (Pandas, NumPy) to clean and analyze a public health dataset spanning 200+ countries and 2+ years; developed an interactive Power BI dashboard tracking case trends, fatality rates, and vaccination progress across regions.
