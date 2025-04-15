"""
    Streamlit front-end display departures over multiple days
    Author: Grant Valentine
    AI Use: Counter and dataframe, pandas, datetime and pytz
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from collections import Counter
from data import load_data, reload_data

st.set_page_config(
    page_title="PRC Departure Graph",
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
    return local_time.strftime("%Y-%m-%d")  # Format output as date only


st.title("PRC Departure Graph")
utc_time = st.sidebar.toggle("Display time in UTC", value=False)
st.sidebar.button("Update Data", type="primary", on_click=reload_data)

# Load multiple JSON files
schedules = load_data()
table_data = []
departure_dates = []

for schedule in schedules:
    flight_info = schedule["flight"]

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

    if departure_timestamp != "Unknown":
        departure_dates.append(format_local_time(departure_timestamp, utc_time))

# Count the number of departures per day
date_counts = Counter(departure_dates)

# Convert to DataFrame for plotting
df = pd.DataFrame(list(date_counts.items()), columns=["Departure Date", "Flights"])
df = df.sort_values(by="Departure Date")  # Sort dates in ascending order

st.line_chart(df, x="Departure Date", y="Flights", use_container_width=True)
