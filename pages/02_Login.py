"""
Login page - Handles authentication
Redirects authenticated users to their dashboard
"""

import streamlit as st
from queries.auth_queries import authenticate_user
from utils.auth import login
import time

st.set_page_config(
    page_title="Login - Hospital Information System",
    page_icon="🔐",
    layout="centered"
)

# Redirect if already logged in
if st.session_state.get('logged_in', False):
    st.warning(f"You are already logged in as {st.session_state.get('name', '')}")
    st.info("Please use the sidebar to navigate to your dashboard")
    st.stop()

st.title("🔐 Hospital Information System Login")
st.markdown("### Emergency Department Access")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>👤 Patient Access</h4>
        <p>View your appointments, prescriptions, and medical records</p>
        <p><strong>Demo Credentials:</strong><br>
        Email: patient@example.com<br>
        Password: patient123</p>
    </div>
    
    <div class="info-card">
        <h4>👨‍⚕️ Doctor Access</h4>
        <p>Manage patient appointments and write prescriptions</p>
        <p><strong>Demo Credentials:</strong><br>
        Email: doctor@example.com<br>
        Password: doctor123</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>👩‍⚕️ Nurse Access</h4>
        <p>Handle triage, bed management, and waiting room</p>
        <p><strong>Demo Credentials:</strong><br>
        Email: nurse@example.com<br>
        Password: nurse123</p>
    </div>
    
    <div class="info-card">
        <h4>📊 Admin Access</h4>
        <p>System administration, reports, and user management</p>
        <p><strong>Demo Credentials:</strong><br>
        Email: admin@example.com<br>
        Password: admin123</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Login form
with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    login_button = st.form_submit_button("🔓 Login", use_container_width=True)
    
    if login_button:
        if email and password:
            with st.spinner("Authenticating..."):
                time.sleep(0.5)  # Simulate processing
                user_data = authenticate_user(email, password)
                
                if user_data:
                    # Set session state using login function
                    login(user_data['user_id'], user_data['role'], user_data['name'])
                    st.success(f"✅ Welcome back, {user_data['name']}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        else:
            st.warning("Please enter both email and password.")

# Registration link
st.markdown("---")
st.markdown("📝 [New Patient? Register Here](#) | 🔒 [Forgot Password?](#)")