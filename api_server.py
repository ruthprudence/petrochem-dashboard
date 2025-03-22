from flask import Flask, jsonify, request
import pandas as pd
import socket
import logging
from datetime import datetime
from data_fetcher import fetch_eia_data
from data_processor import process_eia_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask app for API endpoints
app = Flask(__name__)

# Global data cache
global_data = None

def load_data():
    """Load and process data for API endpoints"""
    global global_data
    try:
        df = fetch_eia_data()
        global_data = process_eia_data(df)
        logger.info(f"API server: Data loaded with shape {global_data.shape}")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")

@app.route('/api/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called")
    # Include network info for debugging
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return jsonify({
        "status": "ok", 
        "timestamp": datetime.now().isoformat(),
        "hostname": host_name,
        "ip": host_ip
    })

@app.route('/api/data', methods=['GET'])
def get_data():
    logger.info("Data endpoint called")
    if global_data is None:
        load_data()
        
    if global_data is None:
        return jsonify({"error": "No data available"}), 404
    
    # Convert DataFrame to dict for JSON serialization
    data_dict = {
        "columns": list(global_data.columns),
        "data": global_data.reset_index().to_dict(orient='records')
    }
    return jsonify(data_dict)

@app.route('/api/date-range', methods=['GET'])
def get_date_range():
    logger.info("Date range endpoint called")
    if global_data is None:
        load_data()
        
    if global_data is None:
        return jsonify({"error": "No data available"}), 404
    
    min_date = global_data.index.min().isoformat()
    max_date = global_data.index.max().isoformat()
    
    return jsonify({
        "min_date": min_date,
        "max_date": max_date
    })

if __name__ == "__main__":
    logger.info("Starting Flask API server on 0.0.0.0:8080")
    # Load data when server starts
    load_data()
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)
