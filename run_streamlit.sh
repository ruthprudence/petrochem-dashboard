#!/bin/bash
# Redirect both stdout and stderr to a log file
exec > /home/opc/streamlit_output.log 2>&1

echo "Starting script at $(date)"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"

# Try to activate the virtual environment
echo "Attempting to activate virtual environment"
source /home/opc/petroenv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

echo "Python path: $(which python)"
echo "Streamlit path: $(which streamlit)"
echo "Python version: $(python --version)"

# Set the working directory
cd /home/opc
echo "Changed to directory: $(pwd)"

# Run the Streamlit app
echo "Starting Streamlit app"
/home/opc/petroenv/bin/streamlit run /home/opc/app.py
echo "Streamlit exited with code: $?"
