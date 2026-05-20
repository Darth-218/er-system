"""
Doctor Dashboard — Schedule, Patients, Prescriptions, Room Reservations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.auth import require_role
from queries.doctor_queries import (
    get_doctor_by_id, get_doctor_schedule, get_doctor_appointments,
    get_doctor_prescriptions, get_doctor_treatment_hours
)
from queries.appointment_queries import list_available_doctors, cancel_appointment
from queries.prescription_queries import write_prescription, get_patient_prescriptions
from queries.emergency_queries import list_er_beds, assign_bed, release_bed
from db.connection import DatabaseError

st.set_page_config(
    page_title="Doctor Dashboard - Hospital Information System",
    page_icon="👨‍⚕️",
    layout="wide"
)

# Authentication guard
require_role("doctor")

# Get doctor data
doctor = get_doctor_by_id(st.session_state.user_id)

if not doctor:
    st.error("Doctor record not found")
    st.stop()

st.title("👨‍⚕️ Doctor Dashboard")
st.markdown(f"### Welcome, Dr. {st.session_state.name}")
st.write(f"**Department:** {doctor.get('department_name', 'Not assigned')} | **Specialty:** {doctor.get('major_scientific_area', 'Not specified')}")

# =============================================================
# SIDEBAR: Quick Stats & Navigation
# =============================================================
with st.sidebar:
    st.header("Quick Stats")
    
    # Get today's date
    today = date.today()
    
    try:
        # Get today's appointments
        today_appointments = get_doctor_schedule(st.session_state.user_id, str(today))
        today_count = len(today_appointments)
        
        # Get upcoming appointments (next 7 days)
        next_week = str(today + timedelta(days=7))
        week_appointments = get_doctor_appointments(st.session_state.user_id, str(today), next_week)
        week_count = len(week_appointments)
        
        # Get treatment hours stats
        treatment_hours = get_doctor_treatment_hours(st.session_state.user_id, 
                                                    str(today - timedelta(days=30)), 
                                                    str(today))
        
        st.metric("Today's Appointments", today_count)
        st.metric("Next 7 Days", week_count)
        st.metric("This Month", len(treatment_hours))
        
    except DatabaseError:
        st.metric("Today's Appointments", "Error")
        st.metric("Next 7 Days", "Error")
        st.metric("This Month", "Error")

# =============================================================
# MAIN LAYOUT: Tabs
# =============================================================
tab_schedule, tab_patients, tab_prescriptions, tab_rooms, tab_reports = st.tabs([
    "📅 Schedule", "👥 Patients", "💊 Prescriptions", "🏥 Rooms", "📊 Reports"
])

# =============================================================
# TAB 1: SCHEDULE
# =============================================================
with tab_schedule:
    st.subheader("Daily Schedule")
    
    # Date selector
    selected_date = st.date_input("Select Date", value=date.today())
    
    try:
        schedule = get_doctor_schedule(st.session_state.user_id, str(selected_date))
        
        if schedule:
            df = pd.DataFrame(schedule)
            df['appointment_datetime'] = pd.to_datetime(df['appointment_datetime'])
            df['time'] = df['appointment_datetime'].dt.strftime('%I:%M %p')
            
            st.dataframe(df[['time', 'patient_number', 'patient_name', 'status', 'notes']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No appointments scheduled for this date.")
            
    except DatabaseError as e:
        st.error(f"Failed to load schedule: {e}")

# =============================================================
# TAB 2: PATIENTS
# =============================================================
with tab_patients:
    st.subheader("Patient Management")
    
    # Date range for appointments
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    try:
        appointments = get_doctor_appointments(st.session_state.user_id, 
                                           str(start_date), str(end_date))
        
        if appointments:
            df = pd.DataFrame(appointments)
            df['appointment_datetime'] = pd.to_datetime(df['appointment_datetime'])
            df['date'] = df['appointment_datetime'].dt.strftime('%Y-%m-%d')
            df['time'] = df['appointment_datetime'].dt.strftime('%I:%M %p')
            
            st.dataframe(df[['date', 'time', 'patient_number', 'patient_name', 'status', 'payment_amount']], 
                        use_container_width=True, hide_index=True)
            
            # Appointment actions
            st.subheader("Appointment Actions")
            selected_appointment = st.selectbox(
                "Select appointment to manage",
                options=[f"{a['date']} {a['time']} - {a['patient_name']}" for a in appointments],
                key="appointment_select"
            )
            
            if st.button("Cancel Selected Appointment"):
                appointment_id = appointments[st.session_state.appointment_select.split(' - ')[0].split(' ')[0]]['id']
                try:
                    cancel_appointment(appointment_id)
                    st.success("Appointment cancelled successfully!")
                    st.rerun()
                except DatabaseError as e:
                    st.error(f"Failed to cancel appointment: {e}")
        else:
            st.info("No appointments found for the selected date range.")
            
    except DatabaseError as e:
        st.error(f"Failed to load appointments: {e}")

# =============================================================
# TAB 3: PRESCRIPTIONS
# =============================================================
with tab_prescriptions:
    st.subheader("Prescription Management")
    
    # Get all prescriptions
    try:
        prescriptions = get_doctor_prescriptions(st.session_state.user_id)
        
        if prescriptions:
            df = pd.DataFrame(prescriptions)
            df['prescribed_date'] = pd.to_datetime(df['prescribed_date'])
            df['date'] = df['prescribed_date'].dt.strftime('%Y-%m-%d')
            
            st.dataframe(df[['date', 'patient_number', 'patient_name', 'medication_name', 
                           'dosage', 'frequency', 'refills_remaining']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No prescriptions found.")
            
    except DatabaseError as e:
        st.error(f"Failed to load prescriptions: {e}")
    
    # Add new prescription form
    st.subheader("Add New Prescription")
    with st.form("prescription_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.number_input("Patient ID", min_value=1)
            medication_name = st.text_input("Medication Name")
        with col2:
            dosage = st.text_input("Dosage")
            frequency = st.text_input("Frequency (e.g., 'twice daily')")
        
        duration = st.text_input("Duration (e.g., '7 days')")
        instructions = st.text_area("Instructions")
        refills = st.number_input("Refills Remaining", min_value=0, value=0)
        
        submitted = st.form_submit_button("Add Prescription")
        
        if submitted:
            try:
                write_prescription(
                    patient_id=patient_id,
                    doctor_id=st.session_state.user_id,
                    medication=medication_name,
                    dose=dosage,
                    frequency=frequency,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=int(duration.split()[0]) if duration.split()[0].isdigit() else 7),
                    directions=instructions
                )
                st.success("Prescription added successfully!")
                st.rerun()
            except DatabaseError as e:
                st.error(f"Failed to add prescription: {e}")

# =============================================================
# TAB 4: ROOMS
# =============================================================
with tab_rooms:
    st.subheader("ER Room Management")
    
    try:
        er_beds = list_er_beds()
        
        if er_beds:
            df = pd.DataFrame(er_beds)
            st.dataframe(df[['bed_number', 'status', 'current_patient_id', 'last_updated']], 
                        use_container_width=True, hide_index=True)
            
            # Room management actions
            st.subheader("Room Management Actions")
            bed_id = st.number_input("Bed ID", min_value=1)
            action = st.selectbox("Action", ["Assign Patient", "Release Bed"])
            
            if action == "Assign Patient":
                patient_id = st.number_input("Patient ID", min_value=1)
                if st.button("Assign Patient to Bed"):
                    try:
                        assign_bed(bed_id, patient_id)
                        st.success("Patient assigned to bed successfully!")
                        st.rerun()
                    except DatabaseError as e:
                        st.error(f"Failed to assign patient: {e}")
                        
            elif action == "Release Bed":
                if st.button("Release Bed"):
                    try:
                        release_bed(bed_id)
                        st.success("Bed released successfully!")
                        st.rerun()
                    except DatabaseError as e:
                        st.error(f"Failed to release bed: {e}")
        else:
            st.info("No ER beds found.")
            
    except DatabaseError as e:
        st.error(f"Failed to load ER beds: {e}")

# =============================================================
# TAB 5: REPORTS
# =============================================================
with tab_reports:
    st.subheader("Treatment Hours Report")
    
    # Date range for report
    col1, col2 = st.columns(2)
    with col1:
        report_start = st.date_input("Report Start Date", value=date.today() - timedelta(days=30))
    with col2:
        report_end = st.date_input("Report End Date", value=date.today())
    
    try:
        treatment_data = get_doctor_treatment_hours(st.session_state.user_id, 
                                                str(report_start), str(report_end))
        
        if treatment_data:
            df = pd.DataFrame(treatment_data)
            df['treatment_date'] = pd.to_datetime(df['treatment_date'])
            
            st.dataframe(df[['treatment_date', 'appointment_count', 'total_minutes', 
                           'completed_count', 'cancelled_count']], 
                        use_container_width=True, hide_index=True)
            
            # Summary statistics
            st.subheader("Summary Statistics")
            total_appointments = df['appointment_count'].sum()
            total_minutes = df['total_minutes'].sum()
            completed_rate = (df['completed_count'].sum() / total_appointments * 100) if total_appointments > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Appointments", total_appointments)
            col2.metric("Total Treatment Minutes", total_minutes)
            col3.metric("Completion Rate", f"{completed_rate:.1f}%")
        else:
            st.info("No treatment data found for the selected period.")
            
    except DatabaseError as e:
        st.error(f"Failed to load treatment report: {e}")
