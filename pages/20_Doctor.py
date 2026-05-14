"""
Doctor Dashboard
PLACEHOLDER — Member 3+4 will implement.
Contains: schedule, patient list, prescriptions, room reservation, treatment hours.
"""

import streamlit as st
from utils.auth import require_role

st.set_page_config(page_title="Doctor Dashboard", layout="wide")
require_role("doctor")

st.title("Doctor Dashboard")
st.info("This page will be implemented by Member 3 + Member 4.")
