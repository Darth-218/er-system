"""
Patient Dashboard
PLACEHOLDER — Member 2 will implement.
"""

import streamlit as st
from utils.auth import require_role

st.set_page_config(page_title="Patient Dashboard", layout="wide")
require_role("patient")

st.title("Patient Dashboard")
st.info("This page will be implemented by Member 2 (Phase 5).")
