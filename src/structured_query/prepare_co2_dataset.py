from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw/datasets/owid_co2_data.csv")
PROCESSED_DATA_PATH = Path("data/processed/co2_emissions_clean.csv")

COLUMNS_TO_KEEP = [
    "country",
    "year",
    "iso_code",
    "population",
    "gdp",
    "co2",
    "co2_per_capita",
    "consumption_co2",
    "consumption_co2_per_capita",
    "coal_co2",
    "oil_co2",
    "gas_co2",
    "cement_co2",
    "flaring_co2",
    "methane",
    "nitrous_oxide",
    "total_ghg",
]


def prepare_co2_dataset() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_PATH)

    available_columns = [col for col in COLUMNS_TO_KEEP if col in df.columns]
    df = df[available_columns].copy() #κρατάω μόνο αυτές τις στήλες

    df = df.dropna(subset=["country", "year"])

    df["year"] = df["year"].astype(int)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    return df


if __name__ == "__main__":
    clean_df = prepare_co2_dataset()

    print("Processed CO2 dataset saved successfully!")
    print(f"Rows: {len(clean_df)}")
    print(f"Columns: {list(clean_df.columns)}")
    print(clean_df.head())