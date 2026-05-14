"""
Admin Dashboard
PLACEHOLDER — Member 5 will implement.
Contains: reports, user management, contact inbox, statistics.
"""

import streamlit as st
from utils.auth import require_role

st.set_page_config(page_title="Admin Dashboard", layout="wide")
require_role("admin")

st.title("Admin Dashboard")
st.info("This page will be implemented by Member 5 (Phase 4).")
