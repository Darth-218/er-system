"""
Hospital Information System - Emergency Department
Main entry point with role-based routing
"""

import streamlit as st
from utils.auth import logout

st.set_page_config(
    page_title="Hospital Information System - Emergency Department",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        background-color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .emergency-badge {
        background-color: #e74c3c;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .info-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'name' not in st.session_state:
    st.session_state.name = None

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/150x50?text=HIS+Emergency", use_column_width=True)
st.sidebar.markdown("---")

if not st.session_state.logged_in:
    # Public navigation
    st.sidebar.page_link("pages/01_Home.py", label="🏠 Home")
    st.sidebar.page_link("pages/02_Login.py", label="🔐 Login")
else:
    # Role-based navigation
    st.sidebar.success(f"👤 Welcome, {st.session_state.name}")
    st.sidebar.markdown(f"**Role:** {st.session_state.role}")
    st.sidebar.markdown("---")
    
    if st.session_state.role == "patient":
        st.sidebar.page_link("pages/10_Patient.py", label="📋 My Dashboard")
        st.sidebar.page_link("pages/10_Patient.py?page=appointments", label="📅 My Appointments")
        st.sidebar.page_link("pages/10_Patient.py?page=prescriptions", label="💊 My Prescriptions")
        st.sidebar.page_link("pages/10_Patient.py?page=scans", label="📁 Medical Scans")
        
    elif st.session_state.role == "doctor":
        st.sidebar.page_link("pages/20_Doctor.py", label="👨‍⚕️ Doctor Dashboard")
        st.sidebar.page_link("pages/20_Doctor.py?page=schedule", label="📅 My Schedule")
        st.sidebar.page_link("pages/20_Doctor.py?page=patients", label="👥 My Patients")
        st.sidebar.page_link("pages/20_Doctor.py?page=prescriptions", label="💊 Write Prescription")
        
    elif st.session_state.role == "nurse":
        st.sidebar.page_link("pages/30_Nurse.py", label="👩‍⚕️ Nurse Dashboard")
        st.sidebar.page_link("pages/30_Nurse.py?page=triage", label="🚑 Triage Intake")
        st.sidebar.page_link("pages/30_Nurse.py?page=beds", label="🛏️ Bed Management")
        st.sidebar.page_link("pages/30_Nurse.py?page=waiting", label="⏳ Waiting Room")
        
    elif st.session_state.role == "admin":
        st.sidebar.page_link("pages/40_Admin.py", label="📊 Admin Dashboard")
        st.sidebar.page_link("pages/40_Admin.py?page=reports", label="📈 Reports")
        st.sidebar.page_link("pages/40_Admin.py?page=users", label="👥 User Management")
        st.sidebar.page_link("pages/40_Admin.py?page=inquiries", label="📧 Contact Inquiries")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2024 Hospital Information System")
st.sidebar.caption("Emergency Department v1.0")