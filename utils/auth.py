"""
PLACEHOLDER — Member 2: Authentication module.

This is a stub for dependency resolution. Member 2 will implement:
  - login(email, password)    -> bool, sets session_state
  - logout()                   -> clears session, reruns
  - require_role(role)         -> guards pages
  - register_patient(data)     -> self-registration
"""

import streamlit as st

ROLE_LEVELS = {
    "visitor": 0,
    "patient": 1,
    "nurse": 2,
    "doctor": 3,
    "admin": 4,
}


def require_role(min_role):
    if not st.session_state.get("logged_in", False):
        st.warning("You must be logged in to access this page.")
        st.stop()

    user_role = st.session_state.get("role", "visitor")
    if ROLE_LEVELS.get(user_role, 0) < ROLE_LEVELS.get(min_role, 0):
        st.warning("You do not have permission to access this page.")
        st.stop()


def login(email, password):
    # Placeholder — Member 2 will replace with real auth
    # For dev/testing: hardcoded nurse login
    if email == "nurse@test.com" and password == "nurse":
        st.session_state.logged_in = True
        st.session_state.user_id = 3
        st.session_state.role = "nurse"
        st.session_state.name = "Test Nurse"
        return True
    return False


def logout():
    for key in ["logged_in", "user_id", "role", "name"]:
        st.session_state.pop(key, None)
    st.rerun()
