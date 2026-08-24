"""
generate_demo_data.py
----------------------
Creates a DEMO dataset (covid_sample_data.csv) that mirrors the real
Our World in Data (OWID) COVID-19 dataset structure and general trend shape,
so you can test-run analysis.py immediately.

IMPORTANT: This is synthetic/illustrative data for testing the pipeline only.
For your actual portfolio project, download the REAL dataset from:
https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv
(click "Download raw file"), save it as owid-covid-data.csv in this folder,
and run analysis.py on that instead. The script works identically on both.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

countries = {
    "United States": {"continent": "North America", "population": 331_000_000, "peak_scale": 1.0},
    "India": {"continent": "Asia", "population": 1_380_000_000, "peak_scale": 0.9},
    "Brazil": {"continent": "South America", "population": 213_000_000, "peak_scale": 0.95},
    "United Kingdom": {"continent": "Europe", "population": 67_000_000, "peak_scale": 1.1},
    "Germany": {"continent": "Europe", "population": 83_000_000, "peak_scale": 0.8},
    "France": {"continent": "Europe", "population": 65_000_000, "peak_scale": 0.85},
    "Italy": {"continent": "Europe", "population": 60_000_000, "peak_scale": 0.9},
    "Japan": {"continent": "Asia", "population": 125_000_000, "peak_scale": 0.4},
    "South Africa": {"continent": "Africa", "population": 59_000_000, "peak_scale": 0.7},
    "Australia": {"continent": "Oceania", "population": 25_000_000, "peak_scale": 0.3},
}

dates = pd.date_range("2020-02-01", "2022-01-31", freq="D")

rows = []
for country, meta in countries.items():
    base = meta["peak_scale"]
    pop = meta["population"]
    cum_cases, cum_deaths, cum_vax = 0, 0, 0
    for i, d in enumerate(dates):
        t = i / len(dates)
        # three rough "waves" using layered gaussians, scaled by country factor
        wave = (
            np.exp(-((t - 0.18) ** 2) / (2 * 0.015)) * 1.0 +
            np.exp(-((t - 0.45) ** 2) / (2 * 0.02)) * 1.4 +
            np.exp(-((t - 0.75) ** 2) / (2 * 0.02)) * 1.8
        )
        noise = np.random.normal(1, 0.15)
        new_cases = max(0, wave * base * (pop / 5_000_000) * noise)
        new_deaths = max(0, new_cases * np.random.uniform(0.008, 0.02))

        # vaccination ramps up from mid-2021
        if d >= pd.Timestamp("2021-01-15"):
            days_since = (d - pd.Timestamp("2021-01-15")).days
            new_vax = max(0, pop * 0.0016 * base * (1 / (1 + np.exp(-(days_since - 120) / 40))) * np.random.uniform(0.85, 1.15))
        else:
            new_vax = 0

        cum_cases += new_cases
        cum_deaths += new_deaths
        cum_vax += new_vax

        rows.append({
            "location": country,
            "continent": meta["continent"],
            "date": d.strftime("%Y-%m-%d"),
            "population": pop,
            "new_cases": round(new_cases),
            "total_cases": round(cum_cases),
            "new_deaths": round(new_deaths),
            "total_deaths": round(cum_deaths),
            "new_vaccinations": round(new_vax),
            "total_vaccinations": round(cum_vax),
        })

df = pd.DataFrame(rows)
df.to_csv("covid_sample_data.csv", index=False)
print(f"Demo dataset created: covid_sample_data.csv  ({len(df):,} rows, {df['location'].nunique()} countries)")
