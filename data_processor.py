import pandas as pd

def process_eia_data(df):
    """Clean and process EIA data for visualization."""
    if df.empty:
        return df

    # Convert period column to datetime
    df["period"] = pd.to_datetime(df["period"])

    # Set period as index
    df.set_index("period", inplace=True)

    # Convert value column to numeric type
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    return df.sort_index()
