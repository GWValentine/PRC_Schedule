"""
Generate JSON files from Flight API and load scheduling data
Author: Grant Valentine
AI Use: ChatGPT: Help with DataFrames, removing duplicate flights from schedule.
    Help with datetime and JSON try/except errors
    Help with Github API Keys
"""

import streamlit as st
import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

# JSON Data Path
DATA_DIR = "./src/data"
API_KEY = st.secrets["API_KEY"]
BASE_URL = f"https://api.flightapi.io/schedule/{API_KEY}?mode=departures&iata=PRC&day="

# Verify data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


@st.cache_data(show_spinner="Fetching data from API...", ttl=60 * 10)
def load_data() -> list:
    """Load PRC departure data for today and the past 4 days, checking if the date's file exists first."""
    combined_departures = []

    # API Days (1 is today, -1 is yesterday)
    API_days = [1, -1, -2, -3, -4]

    for i in range(5):
        # Calculate date of JSON to load
        date_str = (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d")
        file_path = f"{DATA_DIR}/PRC_depart_data_{date_str}.json"

        # Check if file exists, if not, fetch from API
        if not os.path.exists(file_path):
            fetch_and_save_data(API_days[i], file_path)

        # Load the data from JSON file
        if os.path.exists(file_path):  # Ensure it exists after fetching
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                    departures = (
                        data.get("airport", {})
                        .get("pluginData", {})
                        .get("schedule", {})
                        .get("departures", {})
                        .get("data", [])
                    )
                    combined_departures.extend(departures)  # Append to the full list
                except json.JSONDecodeError:
                    st.error(f"Error reading {file_path}. File may be corrupted.")

    # Convert list to DataFrame for duplicate removal
    if combined_departures:
        df = pd.DataFrame(combined_departures)

        # Choose valid columns for filtering duplicates
        valid_columns = [
            col for col in [
                "flight",
                "time",
                "destination",
                "icao",
                "iata",
                "scheduledTime"] if col in df.columns]

        if valid_columns:
            df = df.drop_duplicates(subset=valid_columns, keep="first")

        # Convert back to list of dictionaries
        combined_departures = df.to_dict(orient="records")

    return combined_departures  # Return merged and cleaned list of departures


def fetch_and_save_data(day: int, file_path: str) -> None:
    """Fetch departure data from API and save to JSON file."""
    url = BASE_URL + str(day)  # API uses 1 for today, -1 for yesterday
    try:
        response = requests.get(url)
        data = response.json()
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)  # Save formatted JSON
    except IOError as e:
        st.error(f"Failed to fetch data from API for {file_path}. HTTP {response.status_code}.\nError: {e}")
    except json.JSONDecodeError:
        st.error(f"Invalid JSON received from API for {file_path}.")


def reload_data() -> None:
    """Clear the cached data, forcing a fresh load next request."""
    load_data.clear()
