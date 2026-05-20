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

# Custom CSS for a professional Clinical Theme
st.markdown("""
    <style>
    /* Main backgrounds and fonts */
    .stApp {
        background-color: #fdfdfd;
    }
    
    /* Professional Header Style */
    .main-header {
        background-color: #1a365d;
        color: white;
        padding: 1.5rem;
        border-radius: 0px 0px 15px 15px;
        margin-bottom: 2rem;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Clinical Card Style */
    .clinical-card {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* Status Badges */
    .status-urgent {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-stable {
        background-color: #dcfce7;
        color: #166534;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
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
    st.sidebar.markdown("[🏠 Home](pages/01_Home.py)")
    st.sidebar.markdown("[🔐 Login](pages/02_Login.py)")
else:
    # Role-based navigation
    st.sidebar.success(f"👤 Welcome, {st.session_state.name}")
    st.sidebar.markdown(f"**Role:** {st.session_state.role}")
    st.sidebar.markdown("---")
    
    if st.session_state.role == "patient":
        st.sidebar.markdown("[📋 My Dashboard](pages/10_Patient.py)")
        st.sidebar.markdown("[📅 My Appointments](pages/10_Patient.py?page=appointments)")
        st.sidebar.markdown("[💊 My Prescriptions](pages/10_Patient.py?page=prescriptions)")
        st.sidebar.markdown("[📁 Medical Scans](pages/10_Patient.py?page=scans)")
        
    elif st.session_state.role == "doctor":
        st.sidebar.markdown("[👨‍⚕️ Doctor Dashboard](pages/20_Doctor.py)")
        st.sidebar.markdown("[📅 My Schedule](pages/20_Doctor.py?page=schedule)")
        st.sidebar.markdown("[👥 My Patients](pages/20_Doctor.py?page=patients)")
        st.sidebar.markdown("[💊 Write Prescription](pages/20_Doctor.py?page=prescriptions)")
        
    elif st.session_state.role == "nurse":
        st.sidebar.markdown("[👩‍⚕️ Nurse Dashboard](pages/30_Nurse.py)")
        st.sidebar.markdown("[🚑 Triage Intake](pages/30_Nurse.py?page=triage)")
        st.sidebar.markdown("[🛏️ Bed Management](pages/30_Nurse.py?page=beds)")
        st.sidebar.markdown("[⏳ Waiting Room](pages/30_Nurse.py?page=waiting)")
        
    elif st.session_state.role == "admin":
        st.sidebar.markdown("[📊 Admin Dashboard](pages/40_Admin.py)")
        st.sidebar.markdown("[📈 Reports](pages/40_Admin.py?page=reports)")
        st.sidebar.markdown("[👥 User Management](pages/40_Admin.py?page=users)")
        st.sidebar.markdown("[📧 Contact Inquiries](pages/40_Admin.py?page=inquiries)")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2024 Hospital Information System")
st.sidebar.caption("Emergency Department v1.0")