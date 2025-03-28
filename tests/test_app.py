"""
Test the PRC Departure Streamlit App
Author: Grant Valentine
"""
from unittest import TestCase
from streamlit.testing.v1 import AppTest



class Test(TestCase):    
    """
    Test Cases for App
    """
    def test_ui_title(self) -> None:
        """
        Tests UI Title
        """
        at = AppTest.from_file("./src/PRC_Schedule.py")
        at.run()
        assert at.title[0].value.startswith("PRC Departure Schedule")
        assert not at.exception

    def test_display_time_toggle(self) -> None:
        """
        Test the toggle functionality for UTC and local time display
        """
        at = AppTest.from_file("./src/PRC_Schedule.py")
        at.run()
        toggle = at.toggle[0]
        assert toggle.value == 0

        # Set toggle to UTC (True)
        toggle.set_value(True)
        at.run()
        assert toggle.value == 1