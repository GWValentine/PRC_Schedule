"""
Streamlit front-end for PRC Schedule (Multi-Day Selectable Table)
Author: Grant Valentine
AI Use: Datetime and pytz, parsing JSON data into usable list, sort table
"""

import streamlit as st
from datetime import datetime
import pytz
from data import load_data, reload_data

st.set_page_config(
    page_title="PRC Departure Schedule",
    page_icon="🛫",
    layout="wide",
)

# Define Arizona timezone (Prescott follows America/Phoenix)
arizona_tz = pytz.timezone("America/Phoenix")


def format_local_time(timestamp: int, utc: bool) -> str:
    "Function to convert UTC timestamp to a Date Format String, UTC or MST"
    local_time = datetime.fromtimestamp(timestamp, pytz.utc)  # Convert to UTC
    if not utc:
        local_time = local_time.astimezone(arizona_tz)  # If not UTC, convert to MST
    return local_time.strftime(f"%Y-%m-%d %I:%M:%S %p {local_time.tzname()}")  # Format output


st.title("PRC Departure Schedule")
utc_time = st.sidebar.toggle("Display time in UTC", value=False)
st.sidebar.button("Update Data", type="primary", on_click=reload_data)

# Load multiple JSON files
schedules = load_data()
table_data = []

for schedule in schedules:

    flight_info = schedule["flight"]
    Scheduled = False  # Determines which departure timestamp to get

    callsign = (
        flight_info.get("identification", {})
        .get("callsign", "Unknown")
    )
    aircraft = (
        flight_info.get("aircraft", {})
        .get("model", {})
        .get("text", "Unknown")
    )
    departure_timestamp = (
        flight_info.get("time", {})
        .get("real", {})
        .get("departure", "Unknown")
    )
    if not departure_timestamp:
        departure_timestamp = (
            flight_info.get("time", {})
            .get("scheduled", {})
            .get("departure", "Unknown")
        )
        Scheduled = True
    if departure_timestamp != "Unknown":
        departure_time = format_local_time(departure_timestamp, utc_time)
    else:
        departure_time = "Unknown"

    if Scheduled == True and departure_time != "Unknown":
        departure_time = "(Scheduled) " + departure_time
    destination = (
        flight_info.get("airport", {})
        .get("destination", {})
        .get("name", "Unknown")
    )

    table_data.append(
        {
            "Callsign": callsign,
            "Aircraft": aircraft,
            "Departure Time": departure_time,
            "Raw Timestamp": departure_timestamp,  # Store raw timestamp for sorting
            "Destination": destination,
        }
    )

# Sort the data by Raw Timestamp
table_data = sorted(table_data, key=lambda x: x["Raw Timestamp"] if isinstance(
    x["Raw Timestamp"], (int, float)) else int(0), reverse=True)

# Remove "Raw Timestamp" before displaying
for entry in table_data:
    entry.pop("Raw Timestamp")

all_cols = list(table_data[0].keys())
pre_cols = ["Callsign", "Departure Time"]
columns = st.sidebar.multiselect(
    "Select columns to be displayed:",
    all_cols,
    default=pre_cols,
    placeholder="Select Columns")

# Filter displayed columns
custom = [{k: v for k, v in p.items() if k in columns} for p in table_data]
st.table(custom)
