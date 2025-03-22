# Create a script file
cat > /home/opc/run_streamlit.sh << 'EOL'
#!/bin/bash
source /home/opc/petroenv/bin/activate
cd /home/opc
streamlit run /home/opc/app.py
EOL

# Make it executable
chmod +x /home/opc/run_streamlit.sh
