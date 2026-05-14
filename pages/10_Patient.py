"""
Patient dashboard - Shows appointments, prescriptions, and medical records
Requires patient role
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import require_role
from queries.patient_queries import get_patient_by_id
from queries.appointment_queries import get_patient_appointments, add_appointment, list_available_doctors
from queries.prescription_queries import get_patient_prescriptions
from utils.file_handler import save_file, list_patient_files
import plotly.express as px

st.set_page_config(
    page_title="Patient Dashboard - Hospital Information System",
    page_icon="📋",
    layout="wide"
)

# Authentication guard
require_role("patient")

# Get patient data
patient = get_patient_by_id(st.session_state.user_id)

if not patient:
    st.error("Patient record not found")
    st.stop()

st.title("📋 Patient Dashboard")
st.markdown(f"### Welcome, {st.session_state.name}")

# Get query parameter for navigation
query_params = st.query_params
page = query_params.get("page", ["dashboard"])[0]

# Navigation tabs
tabs = st.tabs(["📊 Dashboard", "📅 Appointments", "💊 Prescriptions", "📁 Medical Records", "👤 Profile"])

# Tab 1: Dashboard
with tabs[0]:
    # Loading state
    with st.spinner("Loading dashboard data..."):
        appointments = get_patient_appointments(st.session_state.user_id)
        prescriptions = get_patient_prescriptions(st.session_state.user_id)
        files = list_patient_files(st.session_state.user_id)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        upcoming = len([a for a in appointments if a['status'] == 'scheduled'])
        st.metric("Upcoming Appointments", upcoming)
    with col2:
        active_rx = len([p for p in prescriptions if p.get('status') == 'active'])
        st.metric("Active Prescriptions", active_rx)
    with col3:
        st.metric("Medical Records", len(files))
    
    st.markdown("---")
    
    # Vital signs display
    st.markdown("### 🩺 Recent Vital Signs")
    if patient.get('medical_status'):
        vitals = patient['medical_status']
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Blood Pressure", vitals.get('bp', 'N/A'))
        with col2:
            st.metric("Heart Rate", f"{vitals.get('heart_rate', 'N/A')} bpm")
        with col3:
            st.metric("Temperature", f"{vitals.get('temperature', 'N/A')} °F")
        with col4:
            st.metric("Oxygen Saturation", f"{vitals.get('spo2', 'N/A')}%")
    else:
        st.info("No vital signs recorded")
    
    # Health tips
    st.markdown("---")
    st.markdown("### 💡 Health Tips")
    tips = [
        "Always take medications as prescribed",
        "Keep track of your symptoms",
        "Don't hesitate to visit ER for emergencies",
        "Maintain a healthy lifestyle"
    ]
    for tip in tips:
        st.info(f"📌 {tip}")

# Tab 2: Appointments
with tabs[1]:
    st.markdown("### 📅 Schedule New Appointment")
    
    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox("Department", ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "General Medicine"])
        doctors = list_available_doctors(department)
        
        if doctors:
            doctor_options = {f"{d['name']} - {d.get('specialty', 'General')}": d['doctor_id'] for d in doctors}
            selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))
            doctor_id = doctor_options[selected_doctor]
        else:
            st.warning("No doctors available in this department")
            doctor_id = None
    
    with col2:
        appointment_date = st.date_input("Preferred Date", min_value=datetime.now().date())
        appointment_time = st.time_input("Preferred Time")
        symptoms = st.text_area("Symptoms / Reason for visit", height=100)
    
    if st.button("Schedule Appointment", use_container_width=True):
        if doctor_id and symptoms:
            with st.spinner("Scheduling appointment..."):
                success = add_appointment(
                    patient_id=st.session_state.user_id,
                    doctor_id=doctor_id,
                    appointment_datetime=datetime.combine(appointment_date, appointment_time),
                    symptoms=symptoms
                )
                if success:
                    st.success("✅ Appointment scheduled successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to schedule appointment. Time slot may be taken.")
        else:
            st.warning("Please select a doctor and provide symptoms")
    
    st.markdown("---")
    st.markdown("### 📋 Your Appointments")
    
    # Loading state for appointments
    with st.spinner("Loading appointments..."):
        appointments = get_patient_appointments(st.session_state.user_id)
    
    if appointments:
        df = pd.DataFrame(appointments)
        df['datetime'] = pd.to_datetime(df['appointment_datetime'])
        df = df.sort_values('datetime', ascending=False)
        
        for _, apt in df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    st.markdown(f"**📅 {apt['datetime'].strftime('%Y-%m-%d %H:%M')}**")
                with col2:
                    st.markdown(f"**👨‍⚕️ Dr. {apt['doctor_name']}**")
                with col3:
                    status_color = "🟢" if apt['status'] == 'scheduled' else "🔴" if apt['status'] == 'cancelled' else "⚪"
                    st.markdown(f"{status_color} **{apt['status'].upper()}**")
                with col4:
                    if apt['status'] == 'scheduled':
                        if st.button("Cancel", key=f"cancel_{apt['appointment_id']}"):
                            # Cancel appointment logic would go here
                            st.warning("Cancellation feature coming soon")
    else:
        st.info("No appointments found. Schedule your first appointment above!")

# Tab 3: Prescriptions
with tabs[2]:
    st.markdown("### 💊 Active Prescriptions")
    
    with st.spinner("Loading prescriptions..."):
        prescriptions = get_patient_prescriptions(st.session_state.user_id)
    
    active_rx = [p for p in prescriptions if p.get('status') == 'active']
    
    if active_rx:
        for rx in active_rx:
            with st.expander(f"💊 {rx['medication']} - Dr. {rx.get('doctor_name', 'Unknown')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Dosage:** {rx.get('dose', 'N/A')}")
                    st.markdown(f"**Frequency:** {rx.get('frequency', 'N/A')}")
                with col2:
                    st.markdown(f"**Start Date:** {rx.get('start_date', 'N/A')}")
                    st.markdown(f"**End Date:** {rx.get('end_date', 'N/A')}")
                st.markdown(f"**Instructions:** {rx.get('directions', 'No instructions')}")
                st.progress(0.7, text="Treatment Progress")
    else:
        st.info("No active prescriptions")
    
    st.markdown("---")
    st.markdown("### 📜 Prescription History")
    old_rx = [p for p in prescriptions if p.get('status') != 'active']
    if old_rx:
        for rx in old_rx:
            st.caption(f"{rx.get('medication', 'Unknown')} - {rx.get('date_prescribed', 'Unknown date')} - Dr. {rx.get('doctor_name', 'Unknown')}")
    else:
        st.caption("No prescription history")

# Tab 4: Medical Records
with tabs[3]:
    st.markdown("### 📁 Upload Medical Document")
    
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'jpg', 'png', 'jpeg'])
    file_description = st.text_input("File Description")
    
    if uploaded_file and file_description:
        if st.button("Upload"):
            with st.spinner("Uploading file..."):
                success = save_file(
                    patient_id=st.session_state.user_id,
                    uploaded_file=uploaded_file,
                    description=file_description
                )
                if success:
                    st.success("File uploaded successfully!")
                    st.rerun()
                else:
                    st.error("Upload failed")
    
    st.markdown("---")
    st.markdown("### 📄 Your Medical Documents")
    
    with st.spinner("Loading documents..."):
        files = list_patient_files(st.session_state.user_id)
    
    if files:
        for file in files:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{file['file_name']}**")
                    st.caption(file.get('description', 'No description'))
                with col2:
                    st.caption(f"Uploaded: {file['uploaded_at']}")
                with col3:
                    if st.button("View", key=f"view_{file['file_id']}"):
                        st.info("File viewer would open here")
    else:
        st.info("No documents uploaded yet")

# Tab 5: Profile
with tabs[4]:
    st.markdown("### 👤 Personal Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Full Name", value=patient.get('name', ''), disabled=True)
        st.text_input("Patient Number", value=patient.get('patient_number', ''), disabled=True)
        st.text_input("Date of Birth", value=str(patient.get('birthdate', '')), disabled=True)
    with col2:
        st.text_input("Phone", value=patient.get('phone', ''), disabled=True)
        st.text_input("Email", value=patient.get('email', ''), disabled=True)
        st.text_input("Address", value=patient.get('address', ''), disabled=True)
    
    st.markdown("### 🏥 Medical History")
    st.text_area("Medical History", value=patient.get('medical_history', ''), height=150, disabled=True)
    
    if st.button("Request Information Update", use_container_width=True):
        st.info("Update request sent to admin. You'll be contacted within 48 hours.")