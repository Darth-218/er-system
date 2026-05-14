"""
Authentication utilities for session management and role-based access control
"""

import streamlit as st

def login(user_id, role, name):
    """
    Set session state for authenticated user
    
    Args:
        user_id (int): User's primary key
        role (str): User's role (patient/doctor/nurse/admin)
        name (str): Display name
    """
    st.session_state.logged_in = True
    st.session_state.user_id = user_id
    st.session_state.role = role
    st.session_state.name = name

def logout():
    """
    Clear all session authentication keys
    """
    keys_to_clear = ['logged_in', 'user_id', 'role', 'name']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def require_role(required_role):
    """
    Check if user has required role, stop page if not
    
    Args:
        required_role (str): Minimum role required (visitor/patient/nurse/doctor/admin)
    """
    if not st.session_state.get('logged_in', False):
        st.warning("Please login to access this page")
        st.switch_page("pages/02_Login.py")
        st.stop()
    
    # Role hierarchy
    role_hierarchy = {
        'visitor': 0,
        'patient': 1,
        'nurse': 2,
        'doctor': 3,
        'admin': 4
    }
    
    current_level = role_hierarchy.get(st.session_state.role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    if current_level < required_level:
        st.error(f"Access denied. This page requires {required_role} role or higher.")
        st.stop()

def is_authenticated():
    """
    Check if user is authenticated
    
    Returns:
        bool: True if logged in, False otherwise
    """
    return st.session_state.get('logged_in', False)