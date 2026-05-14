"""
Login Page
PLACEHOLDER — Member 2 will implement full authentication.
"""

import streamlit as st
from utils.auth import login, logout

st.set_page_config(page_title="Login", layout="centered")

if st.session_state.get("logged_in", False):
    st.success(f"Already logged in as {st.session_state.get('name', '')}")
    if st.button("Logout"):
        logout()
    st.page_link("pages/01_Home.py", label="← Back to Home")
    st.stop()

st.title("Login")

with st.form("login_form"):
    email = st.text_input("Email", placeholder="nurse@test.com")
    password = st.text_input("Password", type="password", placeholder="nurse")
    if st.form_submit_button("Login"):
        if login(email, password):
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials. Try nurse@test.com / nurse")

st.markdown("---")
st.page_link("pages/01_Home.py", label="← Back to Home")
