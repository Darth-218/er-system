"""
Nurse Dashboard — Emergency Department
Triage intake, ER bed management, waiting room queue.
"""

import streamlit as st
from datetime import datetime

from utils.auth import require_role
from queries.emergency_queries import (
    add_triage_record, list_triage_queue, get_triage_records,
    list_er_beds, list_available_beds, assign_bed, release_bed,
    complete_cleaning, get_bed_history, get_bed_stats,
    get_waiting_queue, count_waiting_patients, remove_from_waiting,
    search_patients_by_name,
)
from db.connection import DatabaseError

st.set_page_config(page_title="Nurse Dashboard — ER", layout="wide")
require_role("nurse")

st.title("🏥 Emergency Department — Nurse Dashboard")
st.markdown(f"**Nurse:** {st.session_state.get('name', 'Unknown')}")

# =============================================================
# SIDEBAR: Quick Stats
# =============================================================
try:
    stats = get_bed_stats()
    waiting_count = count_waiting_patients()
except DatabaseError:
    stats = {"available": 0, "occupied": 0, "cleaning": 0}
    waiting_count = 0

with st.sidebar:
    st.header("ER Status")
    col1, col2 = st.columns(2)
    col1.metric("Available Beds", stats.get("available", 0))
    col2.metric("Occupied", stats.get("occupied", 0))
    col1.metric("Cleaning", stats.get("cleaning", 0))
    col2.metric("Waiting", waiting_count)

# =============================================================
# MAIN LAYOUT: Tabs
# =============================================================
tab_triage, tab_beds, tab_queue = st.tabs([
    "🩺 Triage Intake", "🛏️ ER Beds", "📋 Waiting Room"
])

# =============================================================
# TAB 1 — TRIAGE INTAKE
# =============================================================
with tab_triage:
    st.header("Triage Intake")

    with st.expander("➕ New Triage Record", expanded=True):
        with st.form("triage_form"):
            patient_search = st.text_input(
                "Search Patient (name or patient number)",
                placeholder="Type at least 3 characters..."
            )

            patients = []
            if len(patient_search.strip()) >= 3:
                try:
                    patients = search_patients_by_name(patient_search.strip())
                except DatabaseError as e:
                    st.error(f"Search failed: {e}")

            if patients:
                patient_options = {
                    f"{p['name']} ({p['patient_number']})": p["id"]
                    for p in patients
                }
                selected_patient = st.selectbox(
                    "Select Patient", list(patient_options.keys())
                )
                patient_id = patient_options[selected_patient]
            else:
                if patient_search:
                    st.info("No matching patients found.")
                patient_id = None

            col1, col2 = st.columns(2)
            with col1:
                esi_level = st.selectbox(
                    "ESI Level (1=most urgent)", [1, 2, 3, 4, 5], index=2
                )
                blood_pressure = st.text_input(
                    "Blood Pressure", placeholder="e.g. 120/80"
                )
                heart_rate = st.number_input(
                    "Heart Rate (bpm)", min_value=0, max_value=300, value=80
                )
            with col2:
                temperature = st.number_input(
                    "Temperature (°C)", min_value=32.0, max_value=44.0,
                    value=37.0, format="%.1f"
                )
                chief_complaint = st.text_area(
                    "Chief Complaint", placeholder="Describe the reason for visit..."
                )

            submitted = st.form_submit_button("Submit Triage", disabled=not patient_id)
            if submitted and patient_id:
                nurse_id = st.session_state.get("user_id")
                try:
                    triage_id = add_triage_record(
                        patient_id=patient_id,
                        nurse_id=nurse_id,
                        esi_level=esi_level,
                        chief_complaint=chief_complaint,
                        blood_pressure=blood_pressure or None,
                        heart_rate=heart_rate,
                        temperature=temperature,
                    )
                    st.success(f"Triage record created (ID: {triage_id}). Patient added to waiting room.")
                    st.rerun()
                except DatabaseError as e:
                    st.error(f"Failed to create triage record: {e}")

    st.subheader("Active Triage Queue")
    try:
        triage_queue = list_triage_queue()
        if triage_queue:
            display = []
            for t in triage_queue:
                display.append({
                    "ESI": t["esi_level"],
                    "Patient": t["patient_name"],
                    "Complaint": t["chief_complaint"][:50] if t["chief_complaint"] else "",
                    "BP": t["blood_pressure"] or "-",
                    "HR": t["heart_rate"],
                    "Temp": t["temperature"],
                    "Arrived": t["arrival_time"].strftime("%H:%M") if t["arrival_time"] else "",
                })
            st.dataframe(display, use_container_width=True, hide_index=True)
        else:
            st.info("No patients in triage queue.")
    except DatabaseError as e:
        st.error(f"Failed to load triage queue: {e}")

# =============================================================
# TAB 2 — ER BEDS
# =============================================================
with tab_beds:
    st.header("ER Bed Management")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Bed Status Board")
        try:
            beds = list_er_beds()
        except DatabaseError as e:
            st.error(f"Failed to load beds: {e}")
            beds = []

        if beds:
            for i in range(0, len(beds), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(beds):
                        bed = beds[i + j]
                        status = bed["status"]
                        emoji = {"available": "🟢", "occupied": "🔴", "cleaning": "🟡"}
                        color = {
                            "available": "green",
                            "occupied": "red",
                            "cleaning": "#cccc00",
                        }
                        with cols[j]:
                            st.markdown(
                                f"**{bed['bed_number']}**  \n"
                                f"<span style='color:{color[status]}'>{emoji[status]} {status.upper()}</span>",
                                unsafe_allow_html=True,
                            )
                            if bed["patient_name"]:
                                st.caption(f"Patient: {bed['patient_name']}")
                            else:
                                st.caption("—")
        else:
            st.info("No ER beds found.")

    with col_right:
        st.subheader("Actions")

        with st.form("assign_bed_form"):
            st.write("**Assign Patient to Bed**")
            avail_beds = []
            try:
                avail_beds = list_available_beds()
            except DatabaseError:
                st.error("Could not load available beds.")

            bed_options = {}
            if avail_beds:
                bed_options = {
                    f"{b['bed_number']} (Dept {b['department_id']})": b["bed_id"]
                    for b in avail_beds
                }
                bed_choice = st.selectbox(
                    "Select Bed", list(bed_options.keys())
                )
            else:
                st.info("No available beds.")
                bed_choice = None

            search_assign = st.text_input(
                "Patient name or number",
                placeholder="Search patient to assign...",
                key="assign_search"
            )
            assign_patients = []
            if len(search_assign.strip()) >= 3:
                try:
                    assign_patients = search_patients_by_name(search_assign.strip())
                except DatabaseError:
                    pass

            assign_patient_id = None
            if assign_patients:
                assign_opts = {
                    f"{p['name']} ({p['patient_number']})": p["id"]
                    for p in assign_patients
                }
                assign_sel = st.selectbox(
                    "Select patient", list(assign_opts.keys()),
                    key="assign_select"
                )
                assign_patient_id = assign_opts[assign_sel]

            assign_btn = st.form_submit_button(
                "Assign Bed", disabled=not (bed_choice and assign_patient_id)
            )
            if assign_btn and bed_choice and assign_patient_id:
                try:
                    bed_id = bed_options[bed_choice]
                    success = assign_bed(bed_id, assign_patient_id)
                    if success:
                        st.success("Patient assigned to bed!")
                        st.rerun()
                    else:
                        st.error("Bed is no longer available.")
                except DatabaseError as e:
                    st.error(f"Assignment failed: {e}")

        with st.form("release_bed_form"):
            st.write("**Release / Clean Bed**")
            try:
                occupied_beds = list_er_beds()
                occ_opts = {
                    f"{b['bed_number']} ({b.get('patient_name', 'empty')})": b["bed_id"]
                    for b in occupied_beds if b["status"] == "occupied"
                }
                clean_opts = {
                    f"{b['bed_number']} (cleaning)": b["bed_id"]
                    for b in occupied_beds if b["status"] == "cleaning"
                }
            except DatabaseError:
                occ_opts = {}
                clean_opts = {}

            if occ_opts:
                release_choice = st.selectbox(
                    "Occupied beds", list(occ_opts.keys())
                )
                if st.form_submit_button("Release Bed"):
                    try:
                        release_bed(occ_opts[release_choice])
                        st.success("Bed released and marked for cleaning.")
                        st.rerun()
                    except DatabaseError as e:
                        st.error(f"Failed to release bed: {e}")
            else:
                st.info("No occupied beds.")

            if clean_opts:
                clean_choice = st.selectbox(
                    "Cleaning beds", list(clean_opts.keys())
                )
                if st.form_submit_button("Mark Cleaned"):
                    try:
                        complete_cleaning(clean_opts[clean_choice])
                        st.success("Bed marked as available.")
                        st.rerun()
                    except DatabaseError as e:
                        st.error(f"Failed to complete cleaning: {e}")

    st.divider()
    st.subheader("Bed History")
    try:
        beds_for_history = list_er_beds()
        if beds_for_history:
            hist_opts = {b["bed_number"]: b["bed_id"] for b in beds_for_history}
            hist_choice = st.selectbox(
                "Select bed to view history", list(hist_opts.keys())
            )
            if hist_choice:
                history = get_bed_history(hist_opts[hist_choice])
                if history:
                    display_hist = []
                    for h in history:
                        display_hist.append({
                            "Patient": h["patient_name"],
                            "Assigned": h["assigned_at"].strftime("%Y-%m-%d %H:%M") if h["assigned_at"] else "-",
                            "Released": h["released_at"].strftime("%Y-%m-%d %H:%M") if h["released_at"] else "Still occupied",
                        })
                    st.dataframe(display_hist, use_container_width=True, hide_index=True)
                else:
                    st.info("No history for this bed.")
    except DatabaseError as e:
        st.error(f"Failed to load history: {e}")

# =============================================================
# TAB 3 — WAITING ROOM QUEUE
# =============================================================
with tab_queue:
    st.header("Waiting Room Queue")

    col_q, col_action = st.columns([3, 1])

    with col_q:
        try:
            queue = get_waiting_queue()
            if queue:
                display_q = []
                for q in queue:
                    display_q.append({
                        "Pos": q["queue_position"],
                        "Patient": q["patient_name"],
                        "ESI": q["esi_level"],
                        "Complaint": q["chief_complaint"][:50] if q["chief_complaint"] else "",
                        "Wait (min)": q["estimated_wait_minutes"],
                        "Arrived": q["entered_at"].strftime("%H:%M") if q["entered_at"] else "",
                    })
                st.dataframe(display_q, use_container_width=True, hide_index=True)
            else:
                st.info("Waiting room is empty.")
        except DatabaseError as e:
            st.error(f"Failed to load waiting queue: {e}")

    with col_action:
        st.subheader("Actions")
        try:
            queue = get_waiting_queue()
        except DatabaseError:
            queue = []

        if queue:
            with st.form("remove_from_queue"):
                remove_opts = {
                    f"{q['patient_name']} (ESI {q['esi_level']})": q["patient_id"]
                    for q in queue
                }
                remove_choice = st.selectbox(
                    "Remove patient", list(remove_opts.keys())
                )
                reason = st.radio("Reason", ["Admitted to bed", "Left without treatment"])
                if st.form_submit_button("Remove from Queue"):
                    try:
                        pid = remove_opts[remove_choice]
                        status = "in-progress" if reason == "Admitted to bed" else "left"
                        remove_from_waiting(pid, status)
                        st.success(f"Patient {reason.lower()}.")
                        st.rerun()
                    except DatabaseError as e:
                        st.error(f"Failed to update queue: {e}")
