import requests
import sqlite3
import time
import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Key constant
EIA_API_KEY = os.getenv("EIA_API_KEY")

# API Endpoint
EIA_URL = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

# Maximum rows per API request
LIMIT = 5000

# SQLite database file
DB_FILE = "eia_data.db"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def create_database():
    """Create the SQLite database and table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS petroleum_data (
            period TEXT,
            duoarea TEXT,
            area_name TEXT,
            product TEXT,
            product_name TEXT,
            process TEXT,
            process_name TEXT,
            series TEXT PRIMARY KEY,
            series_description TEXT,
            value REAL,
            units TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_data(offset=0):
    """Fetch paginated data from the EIA API."""
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "daily",
        "data[0]": "value",
        "offset": offset,
        "length": LIMIT
    }
    
    response = requests.get(EIA_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if "response" in data and "data" in data["response"]:
            return data["response"]["data"], int(data["response"]["total"])
    
    print(f"Error fetching data: {response.status_code} - {response.text}")
    return [], 0

def store_data(data):
    """Store new data in SQLite, avoiding duplicates."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for entry in data:
        try:
            cursor.execute('''
                INSERT INTO petroleum_data (period, duoarea, area_name, product, product_name, process, 
                process_name, series, series_description, value, units) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry.get("period"),
                entry.get("duoarea"),
                entry.get("area-name"),
                entry.get("product"),
                entry.get("product-name"),
                entry.get("process"),
                entry.get("process-name"),
                entry.get("series"),
                entry.get("series-description"),
                float(entry.get("value", 0)),
                entry.get("units")
            ))
        except sqlite3.IntegrityError:
            # Skip duplicate entries (already in DB)
            pass 

    conn.commit()
    conn.close()

def get_existing_series():
    """Retrieve existing series IDs from the database to avoid re-inserting data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT series FROM petroleum_data")
    existing_series = {row[0] for row in cursor.fetchall()}
    conn.close()
    return existing_series

def get_all_data():
    """Fetch all available data using pagination and store only new entries."""
    create_database()
    existing_series = get_existing_series()

    all_data = []
    offset = 0
    total_rows = 1  # Placeholder, will update after first call

    while offset < total_rows:
        batch, total_rows = fetch_data(offset)

        # Filter out already stored series
        new_entries = [entry for entry in batch if entry["series"] not in existing_series]
        if new_entries:
            store_data(new_entries)

        all_data.extend(new_entries)
        offset += LIMIT
        time.sleep(1)  # Avoid hitting API rate limits

    return all_data

def save_data_json(data):
    """Save fetched data to a timestamped JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"data/eia_data_{timestamp}.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    print("Fetching new data from EIA API...")
    new_data = get_all_data()

    if new_data:
        print(f"Fetched and stored {len(new_data)} new records.")
        save_data_json(new_data)
    else:
        print("No new data to store.")

if __name__ == "__main__":
    main()
