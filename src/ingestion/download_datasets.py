from pathlib import Path
import requests


DATASETS_DIR = Path("data/raw/datasets")
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "owid_co2_data.csv": "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
    "owid_co2_codebook.csv": "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv",
}


def download_file(url: str, output_path: Path) -> None:
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output_path.write_bytes(response.content)
    print(f"Downloaded: {output_path}")

def download_all_datasets() -> None:
    for filename, url in DATASETS.items():
        output_path = DATASETS_DIR / filename
        download_file(url, output_path)


if __name__ == "__main__":
    download_all_datasets()