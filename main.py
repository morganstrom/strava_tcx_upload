from io import BytesIO

import requests
import streamlit as st

from models import TrainingCenterDatabase
from adapters import upload_activity, get_token
from credentials import CLIENT_ID

AUTHENTICATE_URL = "https://www.strava.com/oauth/authorize"
SPORT_TYPES = [
    "AlpineSki", "BackcountrySki", "Badminton", "Canoeing", "Crossfit", "EBikeRide", "Elliptical", "EMountainBikeRide",
    "Golf", "GravelRide", "Handcycle", "HighIntensityIntervalTraining", "Hike", "IceSkate", "InlineSkate", "Kayaking",
    "Kitesurf", "MountainBikeRide", "NordicSki", "Pickleball", "Pilates", "Racquetball", "Ride", "RockClimbing",
    "RollerSki", "Rowing", "Run", "Sail", "Skateboard", "Snowboard", "Snowshoe", "Soccer", "Squash", "StairStepper",
    "StandUpPaddling", "Surfing", "Swim", "TableTennis", "Tennis", "TrailRun", "Velomobile", "VirtualRide",
    "VirtualRow", "VirtualRun", "Walk", "WeightTraining", "Wheelchair", "Windsurf", "Workout", "Yoga"]


def get_authentication_link():
    return (f"{AUTHENTICATE_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8501" +
            "&approval_prompt=force&scope=activity:write")


def format_file(file: BytesIO):
    xml = file.read()
    database = TrainingCenterDatabase.from_xml(xml)
    return database.collapse_activities()


if __name__ == '__main__':
    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    params = st.experimental_get_query_params()
    if st.session_state.access_token is None and "code" not in params:
        st.link_button("Authenticate with Strava", get_authentication_link())
    elif st.session_state.access_token is None and "code" in params:
        try:
            st.session_state.access_token = get_token(params["code"][0])
        except requests.exceptions.HTTPError as e:
            st.warning(e)
        st.success("Authenticated!")
    elif st.session_state.access_token is not None:
        st.success("Authenticated!")

    files = st.file_uploader("Upload file", accept_multiple_files=True)
    name = st.text_input("Activity name", "StrongLifts 5x5")
    sport_type = st.selectbox("Activity type", SPORT_TYPES, SPORT_TYPES.index("WeightTraining"))
    upload_button = st.button("Upload to Strava")
    if upload_button:
        for file in files:
            st.write(f"Processing {file.name}")
            db = format_file(file)
            path = f"output/{file.name}"
            db.to_file(path)
            try:
                response = upload_activity(st.session_state.access_token, path, name, sport_type)
                st.write(response["status"])
            except requests.exceptions.HTTPError as e:
                st.warning(e)
        st.success("Done!")
