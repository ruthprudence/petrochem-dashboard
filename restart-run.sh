#!/bin/bash

# Path to your virtual environment and app
VENV_PATH="/home/opc/petrochem-dashboard/petroenv"
APP_DIR="/home/opc/petrochem-dashboard"
APP_FILE="app.py"

# Change to app directory
cd $APP_DIR

# Infinite loop to restart the process if it fails
while true; do
    echo "[$(date)] Starting Streamlit app..."
    
    # Activate virtual environment and run streamlit
    source $VENV_PATH/bin/activate
    streamlit run $APP_FILE
    
    # Capture exit code
    EXIT_CODE=$?
    
    # Deactivate virtual environment
    deactivate
    
    echo "[$(date)] Process exited with code $EXIT_CODE. Restarting in 5 seconds..."
    sleep 5
done
