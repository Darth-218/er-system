"""
Home Page — Visitor / Public access
PLACEHOLDER — Member 2 will implement full content.
"""

import streamlit as st

st.set_page_config(page_title="HIS — Home", layout="wide")

st.title("Hospital Information System")
st.markdown("### Emergency Department")

st.markdown("""
Welcome to the City General Hospital Emergency Department information system.

**For visitors:** Use the navigation sidebar to log in or explore.
- **Patients:** View appointments, prescriptions, and medical records
- **Doctors:** Manage schedules, patients, and prescriptions
- **Nurses:** Triage intake, bed management, waiting room
- **Admin:** Reports, user management, statistics

---

*This page will be fully implemented by Member 2 (Phase 5).*
""")

st.page_link("pages/02_Login.py", label="→ Login", use_container_width=True)
