from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/processed/co2_emissions_clean.csv")

def load_co2_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}. "
            "Run: python -m src.structured_query.prepare_co2_dataset"
        )

    return pd.read_csv(DATA_PATH)

def get_available_countries() -> list[str]:
    df = load_co2_data()
    countries = (
        df[df["iso_code"].notna() & (df["iso_code"].str.len() == 3)]["country"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return countries

def latest_year_with_co2() -> int:
    df = load_co2_data()
    df = df.dropna(subset=["co2"])
    return int(df["year"].max())

def top_emitters(year: int, n: int = 10) -> pd.DataFrame:
    df = load_co2_data()
    df_year = df[
        (df["year"] == year)
        & (df["co2"].notna())
        & (df["iso_code"].notna())
        & (df["iso_code"].str.len() == 3)
        ]
    result = (
        df_year[["country", "iso_code", "year", "co2", "co2_per_capita", "population"]]
        .sort_values("co2", ascending=False)
        .head(n)
    )

    return result

def country_emissions(country: str) -> pd.DataFrame:
    df = load_co2_data()

    result = df[
        (df["country"].str.lower() == country.lower())
        & (df["co2"].notna())
    ][["country", "year", "co2", "co2_per_capita", "total_ghg"]]

    return result.sort_values("year")

def compare_countries(countries: list[str], year: int) -> pd.DataFrame:
    df = load_co2_data()

    countries_lower = [c.lower() for c in countries]

    result = df[
        (df["year"] == year)
        & (df["country"].str.lower().isin(countries_lower))
    ][["country", "year", "co2", "co2_per_capita", "total_ghg"]]

    return result.sort_values("co2", ascending=False)

def compare_countries_over_time(countries: list[str]) -> pd.DataFrame:
    df = load_co2_data()

    countries_lower = [c.lower() for c in countries]

    result = df[
        (df["country"].str.lower().isin(countries_lower))
        & (df["co2"].notna())
    ][["country", "year", "co2"]]

    return result.sort_values(["country", "year"])


if __name__ == "__main__":
    latest_year = latest_year_with_co2()

    print(f"Latest year with CO2 data: {latest_year}")

    print("\nTop 10 emitters:")
    print(top_emitters(latest_year, 10))

    print("\nGreece emissions:")
    print(country_emissions("Greece").tail())

    print("\nCompare Greece, Germany, France:")
    print(compare_countries(["Greece", "Germany", "France"], latest_year))