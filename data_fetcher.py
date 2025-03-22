import os
import json
import pandas as pd

DATA_DIR = "fetch/data"

def get_latest_data_file():
    """Find the latest JSON file in the data directory."""
    files = [f for f in os.listdir(DATA_DIR) if f.startswith("eia_data_") and f.endswith(".json")]
    if not files:
        return None
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(DATA_DIR, f)))
    return os.path.join(DATA_DIR, latest_file)

def fetch_eia_data():
    """Load the latest stored EIA data from JSON."""
    latest_file = get_latest_data_file()
    if not latest_file:
        print("No data file found.")
        return pd.DataFrame()  # Return empty DataFrame if no data

    with open(latest_file, "r") as f:
        data = json.load(f)

    if "response" in data:
        records = data["response"]["data"]
    else:
        records = data  # Handle direct list of records

    return pd.DataFrame(records)
