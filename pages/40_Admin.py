"""
Admin Dashboard
PLACEHOLDER — Member 5 will implement.
Contains: reports, user management, contact inbox, statistics.
"""

import streamlit as st
import pandas as pd
from datetime import date

from utils.auth import require_role
from queries.report_queries import (
    get_appointment_report,
    get_bed_utilization_report,
    get_esi_statistics,
    get_patient_admission_summary,
    get_dashboard_stats
)

st.set_page_config(page_title="Admin Dashboard", layout="wide")
require_role("admin")

st.title("Admin Dashboard")
st.subheader("Doctor Appointment Report")

stats = get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", stats["patients"])
col2.metric("Total Doctors", stats["doctors"])
col3.metric("Appointments", stats["appointments"])
col4.metric("Available Beds", stats["available_beds"])

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start date", date(2025, 5, 1))

with col2:
    end_date = st.date_input("End date", date(2025, 5, 31))

if st.button("Generate Report"):
    try:
        report = get_appointment_report(start_date, end_date)

        if report:
            df = pd.DataFrame(report)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)

            st.download_button(
                label="Download Report as CSV",
                data=csv,
                file_name="appointment_report.csv",
                mime="text/csv"
            )
            st.bar_chart(df.set_index("doctor_name")["total_appointments"])

            st.success("Report generated successfully.")
        else:
            st.warning("No appointments found in this date range.")

    except Exception as e:
        st.error(f"Error generating report: {e}")


st.subheader("ER Bed Utilization Report")

if st.button("Show Bed Utilization"):

    try:
        bed_report = get_bed_utilization_report()

        if bed_report:
            bed_df = pd.DataFrame(bed_report)

            st.dataframe(bed_df, use_container_width=True)
            csv = bed_df.to_csv(index=False)

            st.download_button(
                label="Download Bed Report",
                data=csv,
                file_name="bed_utilization_report.csv",
                mime="text/csv"
            )
            st.bar_chart(
                bed_df.set_index("status")["total_beds"]
            )

        else:
            st.warning("No bed data found.")

    except Exception as e:
        st.error(f"Error loading bed report: {e}")


st.subheader("Emergency Severity Index (ESI) Statistics")

if st.button("Show ESI Statistics"):

    try:
        esi_report = get_esi_statistics()

        if esi_report:
            esi_df = pd.DataFrame(esi_report)

            st.dataframe(esi_df, use_container_width=True)
            csv = esi_df.to_csv(index=False)

            st.download_button(
                label="Download ESI Report",
                data=csv,
                file_name="esi_statistics.csv",
                mime="text/csv"
            )
            st.bar_chart(
                esi_df.set_index("esi_level")["total_patients"]
            )

        else:
            st.warning("No triage statistics found.")

    except Exception as e:
        st.error(f"Error loading ESI statistics: {e}")


st.subheader("Patient Admission Summary")

if st.button("Show Patient Admissions"):

    try:
        patient_report = get_patient_admission_summary()

        if patient_report:
            patient_df = pd.DataFrame(patient_report)

            st.dataframe(patient_df, use_container_width=True)
            csv = patient_df.to_csv(index=False)

            st.download_button(
                label="Download Patient Admissions",
                data=csv,
                file_name="patient_admissions.csv",
                mime="text/csv"
            )
        else:
            st.warning("No patient data found.")

    except Exception as e:
        st.error(f"Error loading patient summary: {e}")