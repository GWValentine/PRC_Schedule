"""
Page to display a selected JSON file
Author: Grant Valentine
AI use: streamlit select box, user choosing file to display
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="PRC JSON Files",
    page_icon="🛫",
    layout="wide",
)

# Path where JSON data is stored
DATA_DIR = "./src/data"

st.title("Raw JSON Viewer")

# Get available JSON files
json_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".json")])

# Dropdown to select a JSON file
selected_file = st.selectbox("Select a JSON file to view:", json_files)

if selected_file:
    file_path = os.path.join(DATA_DIR, selected_file)

    try:
        with open(file_path, "r") as file:
            json_data = json.load(file)

        # Display the raw JSON
        st.json(json_data, expanded=False)

    except json.JSONDecodeError:
        st.error("Error: Invalid JSON file format.")
