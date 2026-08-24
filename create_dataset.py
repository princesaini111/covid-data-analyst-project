import pandas as pd
import numpy as np

countries = {
    "India": ("Asia", 1380004385),
    "United States": ("North America", 331002647),
    "United Kingdom": ("Europe", 67886004),
    "Brazil": ("South America", 212559409),
    "France": ("Europe", 67839115),
    "Germany": ("Europe", 83783945),
    "Italy": ("Europe", 60461828),
    "Canada": ("North America", 37742157),
    "Australia": ("Oceania", 25499881),
    "Japan": ("Asia", 126476458)
}

dates = pd.date_range("2020-02-01", "2022-01-31")
rng = np.random.default_rng(42)

rows = []

for country, (continent, population) in countries.items():

    t = np.arange(len(dates))

    wave1 = np.exp(-((t - 160) / 70) ** 2)
    wave2 = np.exp(-((t - 330) / 85) ** 2)
    wave3 = np.exp(-((t - 590) / 90) ** 2)

    scale = population / 100_000_000

    new_cases = (
        (wave1 + 0.9 * wave2 + 1.2 * wave3)
        * (2500 + 4500 * scale)
        + rng.normal(0, 350, len(t))
    )

    new_cases = np.maximum(new_cases, 0)

    new_cases[:25] *= np.linspace(0.05, 1, 25)

    total_cases = np.cumsum(new_cases)

    new_deaths = new_cases * 0.012 + rng.normal(0, 8, len(t))
    new_deaths = np.maximum(new_deaths, 0)

    total_deaths = np.cumsum(new_deaths)

    vaccination_start = 325

    x = np.maximum(t - vaccination_start, 0)

    total_vaccinations = (
        population * 0.78
        / (1 + np.exp(-(x - 150) / 70))
    )

    total_vaccinations[t < vaccination_start] = 0

    new_vaccinations = np.diff(
        np.r_[0, total_vaccinations]
    )

    for i, date in enumerate(dates):

        rows.append({
            "location": country,
            "continent": continent,
            "date": date,
            "population": population,
            "new_cases": round(new_cases[i], 2),
            "total_cases": round(total_cases[i], 2),
            "new_deaths": round(new_deaths[i], 2),
            "total_deaths": round(total_deaths[i], 2),
            "new_vaccinations": round(new_vaccinations[i], 2),
            "total_vaccinations": round(total_vaccinations[i], 2)
        })

df = pd.DataFrame(rows)

df.to_csv("owid-covid-data.csv", index=False)

print("========================================")
print("COVID DATASET CREATED SUCCESSFULLY")
print("========================================")
print(f"Rows: {len(df):,}")
print(f"Countries: {df['location'].nunique()}")
print(f"Start date: {df['date'].min().date()}")
print(f"End date: {df['date'].max().date()}")
print()
print("File created:")
print("owid-covid-data.csv")