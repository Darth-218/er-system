"""
Hospital Information System — Emergency Department
Entry point. Routes users to role-appropriate pages.
"""

import streamlit as st

from utils.auth import require_role

st.set_page_config(
    page_title="HIS — Emergency Department",
    page_icon="🏥",
    layout="wide",
)

# Sidebar navigation
st.sidebar.title("HIS Emergency")

if st.session_state.get("logged_in", False):
    role = st.session_state.get("role", "visitor")
    name = st.session_state.get("name", "")
    st.sidebar.write(f"Logged in as: **{name}** ({role})")

    page_map = {
        "patient": "pages/10_Patient.py",
        "doctor": "pages/20_Doctor.py",
        "nurse": "pages/30_Nurse.py",
        "admin": "pages/40_Admin.py",
    }
    default_page = page_map.get(role, "pages/01_Home.py")
    st.switch_page(default_page)
else:
    st.sidebar.page_link("pages/01_Home.py", label="Home")
    st.sidebar.page_link("pages/02_Login.py", label="Login")

st.title("Hospital Information System")
st.markdown("### Emergency Department")
st.markdown(
    """
    Welcome to the Hospital Information System for the Emergency Department.
    Please log in to access your dashboard.
    """
)
