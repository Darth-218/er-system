"""
Public home page - No authentication required
"""

import streamlit as st
from datetime import datetime
from queries.contact_queries import add_contact_inquiry

st.set_page_config(
    page_title="Hospital Information System - Emergency Department",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Information System")
st.markdown("### Emergency Department")

# Hero section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🏥 Welcome to City General Hospital</h3>
        <p>Providing quality emergency care 24/7 with cutting-edge technology and compassionate staff.</p>
        <p><strong>📍 Location:</strong> 123 Medical Center Drive, Healthcare City</p>
        <p><strong>📞 Emergency Hotline:</strong> 911 or (555) 123-4567</p>
        <p><strong>⏰ ER Hours:</strong> Open 24/7/365</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="emergency-badge" style="text-align:center;">
        <h2>🚨</h2>
        <h3>EMERGENCY</h3>
        <p>Call 911 Immediately</p>
    </div>
    """, unsafe_allow_html=True)

# Quick stats
st.markdown("### 📊 Quick Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👥 Current Patients", "42", "+12 today")
with col2:
    st.metric("⏳ Avg. Wait Time", "15 min", "-5 min")
with col3:
    st.metric("🛏️ Available Beds", "8", "🚨 Critical")
with col4:
    st.metric("👨‍⚕️ On-Duty Doctors", "12", "4 specialists")

# Services
st.markdown("### 🏥 Our Emergency Services")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🚑 Trauma Care
    - Level 1 Trauma Center
    - 24/7 Surgical Team
    - Advanced Life Support
    """)
    
with col2:
    st.markdown("""
    #### 🫀 Cardiac Emergency
    - Heart Attack Treatment
    - Cardiac Cath Lab
    - Telecardiology
    """)
    
with col3:
    st.markdown("""
    #### 🧠 Neurological Care
    - Stroke Unit
    - Neurological ICU
    - Emergency Neurology
    """)

# Contact form for visitors
st.markdown("---")
st.markdown("### 📧 Contact Us")

with st.form("contact_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
    with col2:
        phone = st.text_input("Phone Number")
        subject = st.selectbox("Subject", ["General Inquiry", "Appointment", "Medical Records", "Feedback", "Emergency (Non-Urgent)"])
    
    message = st.text_area("Message*", height=100)
    
    submitted = st.form_submit_button("Send Message", use_container_width=True)
    
    if submitted:
        if name and email and message:
            with st.spinner("Sending message..."):
                success = add_contact_inquiry(name, email, phone, subject, message)
                if success:
                    st.success("✅ Your message has been sent. We'll get back to you within 24 hours.")
                    st.balloons()
                else:
                    st.error("❌ Failed to send message. Please try again later.")
        else:
            st.warning("Please fill in all required fields (*).")

# Footer
st.markdown("---")
st.caption("© 2024 City General Hospital - Emergency Department Management System")