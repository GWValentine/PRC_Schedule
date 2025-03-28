"""
Test the data module for PRC Departures
Author: Grant Valentine
"""
from unittest import TestCase
from src.data import load_data
from src.PRC_Schedule import format_local_time
from os.path import exists, join
from os import remove
from datetime import datetime, timezone

DATA_DIR = "./src/data"
API_KEY = "67e5a45ad107e1cb9de3c704"
BASE_URL = f"https://api.flightapi.io/schedule/{API_KEY}?mode=departures&iata=PRC&day="

class Test(TestCase):
    """
    Test for JSON data files
    """
    def test_data_acquisition(self) -> None:
        """
        Test Readability of JSON files
        IMPORTANT: Does not test for new JSON generations due to API 
        """
        # Uses old data file for testing
        path_to_data_file = join("app", "data", "Old", "OLD_PRC_depart_data.json")
        if exists(path_to_data_file):
            remove(path_to_data_file)
        assert False == exists(path_to_data_file)

        schedule = load_data()

        date_str = (datetime.now(timezone.utc)).strftime("%Y-%m-%d")
        file_path = f"{DATA_DIR}/PRC_depart_data_{date_str}.json"
        assert exists(file_path) #Checks that most current Date File is stored

        # Test without API restrictions could include deleting old JSON files
        # Refreshing the JSON files and checking for function

        flight_info = schedule[0]["flight"]
        assert flight_info
        assert flight_info["identification"]["callsign"]

    def test_datetime_conversions(self) -> None:
        """Testing fromat_local_time function for correction to UTC and MST"""
        utc_time = format_local_time(946684800, True) #Timestamp for new millennium
        print(utc_time)
        assert utc_time == "2000-01-01 12:00:00 AM UTC"
        mst_time = format_local_time(946684800, False)
        print(mst_time)
        assert mst_time == "1999-12-31 05:00:00 PM MST"