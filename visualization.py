import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

def plot_price_trends(df, chart_type, date_range, rolling_window=None):
    """
    Plot price trends for oil prices.

    Args:
        df (pd.DataFrame): DataFrame containing oil price data.
        chart_type (str): Type of chart to plot (Line Chart, Bar Chart, Rolling Average).
        date_range (tuple): Tuple of start and end dates for the chart.
        rolling_window (int, optional): Number of days for the rolling average. Defaults to None.
    """

    fig, ax = plt.subplots(figsize=(10, 5))

    # Ensure the index is of datetime type
    df.index = pd.to_datetime(df.index)

    # Filter the DataFrame based on the date range
    filtered_df = df.loc[date_range[0]:date_range[1]].copy()  # Avoid SettingWithCopyWarning

    # Check for duplicate indices and reset if necessary
    if filtered_df.index.duplicated().any():
        filtered_df = filtered_df.reset_index(drop=True)

    # Drop duplicate rows
    filtered_df = filtered_df.drop_duplicates()

    if chart_type == 'Line Chart':
        sns.lineplot(x=filtered_df.index, y=filtered_df['value'], ax=ax, marker='o', label='Daily Price')
    elif chart_type == 'Bar Chart':
        sns.barplot(x=filtered_df.index, y=filtered_df['value'], ax=ax)
    elif chart_type == 'Rolling Average' and rolling_window:
        filtered_df["Rolling_Avg"] = filtered_df["value"].rolling(rolling_window).mean()
        sns.lineplot(x=filtered_df.index, y=filtered_df["Rolling_Avg"], ax=ax, label=f"{rolling_window}-Day Avg", color="red")

    ax.set_title(f"{chart_type} of Oil Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
