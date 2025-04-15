## KPRC Schedule

![Python Tests](https://github.com/GWValentine/PRC_Schedule/actions/workflows/python-test.yml/badge.svg)
![Docker Compose](https://github.com/GWValentine/PRC_Schedule/actions/workflows/docker-compose.yml/badge.svg)
![License](https://img.shields.io/github/license/GWValentine/PRC_Schedule)

Python [Streamlit](https://streamlit.io) app which fetches all flights on the schedule that day and the previous 4 days.

Deployed to the streamlit cloud here: https://kprc-schedule.streamlit.app/

The *tests* folder contains pytests, run with: `pytest`

Note: Due to limitations of the free service API, new data is only loaded on a new day, paid subscription to FlightAPI removes these issues and could expand time frame.
