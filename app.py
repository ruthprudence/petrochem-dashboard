#!/usr/bin/env python
import streamlit as st
from data_fetcher import fetch_eia_data
from data_processor import process_eia_data
from visualization import plot_price_trends
import socket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("streamlit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Streamlit application")
    st.title("🛢️ Petrochemical Market Dashboard")
    st.write("Tracking oil prices & industry trends using stored EIA data.")
    
    try:
        df = fetch_eia_data()
        processed_df = process_eia_data(df)
        
        # Log data shape for debugging
        logger.info(f"Data loaded with shape: {processed_df.shape}")
        
        if not processed_df.empty:
            st.sidebar.header("🔧 Controls")
            min_date, max_date = processed_df.index.min(), processed_df.index.max()
            date_range = st.sidebar.slider(
                "Select Date Range",
                min_value=min_date.to_pydatetime(),
                max_value=max_date.to_pydatetime(),
                value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
                format="YYYY-MM-DD"
            )

            chart_type = st.sidebar.selectbox(
                "Select Chart Type",
                ["Line Chart", "Bar Chart", "Rolling Average"]
            )

            rolling_window = None
            if chart_type == 'Rolling Average':
                rolling_window = st.sidebar.slider("Rolling Window (Days)", 3, 30, 7)

            plot_price_trends(processed_df, chart_type, date_range, rolling_window)
            
            # Display network information for troubleshooting
            host_name = socket.gethostname()
            try:
                host_ip = socket.gethostbyname(host_name)
            except:
                host_ip = "Could not determine IP"
            
            st.sidebar.header("ℹ️ Network Info")
            st.sidebar.markdown(f"""
            ### Server Info:
            - Hostname: `{host_name}`
            - IP Address: `{host_ip}`
            - Dashboard Port: 8501
            
            ### API Server
            The API server can be started separately with:
            ```
            python api_server.py
            ```
            """)
        else:
            st.error("No data available to display.")
            logger.error("No data available to display")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.exception("An error occurred in the Streamlit application")

if __name__ == "__main__":
    main()
