# Phase 5: Frontend Implementation & User Experience

## Overview
Phase 5 transformed the backend query logic and database schema into a fully interactive web application. Using **Streamlit**, we implemented a role-based access system that ensures users only see the tools and data relevant to their professional role.

## Interface Architecture
The project uses a modular page structure where each file in the `pages/` directory represents a distinct user view.

### Role-Based Access Control (RBAC)
- **Authentication Guard:** Every authenticated page uses the `require_role()` utility. If a user attempts to access a page (e.g., the Doctor Dashboard) without the required role, the application blocks access.
- **Session State:** Using `st.session_state`, the application remembers the user's identity and role across page navigations, eliminating the need for repeated logins.

### User-Specific Dashboards
- **Patient Portal (`10_Patient.py`):** Focused on self-service. Patients can view their upcoming appointments, track their active prescriptions, and browse their uploaded medical scans.
- **Doctor Console (`20_Doctor.py`):** A productivity-focused view. It emphasizes a daily schedule, a patient treatment list, and a fast-entry form for writing prescriptions.
- **Nurse Station (`30_Nurse.py`):** An operational cockpit. It provides an immediate view of the ER queue, the status of every bed in the facility, and the triage intake form.
- **Admin Command Center (`40_Admin.py`):** A data-driven view. It utilizes Plotly and Pandas to render statistical reports and manage the overall health of the system.

## UX & Design Patterns
- **Tabbed Interfaces:** To prevent "information overload," complex pages are divided into tabs (e.g., the Doctor dashboard is split into Schedule, Patients, and Prescriptions).
- **Real-time Feedback:** The use of `st.spinner`, `st.success`, and `st.error` gives the user immediate feedback on database operations.
- **Responsive Navigation:** A shared sidebar provides consistent movement between the home page and role-specific dashboards.

## Deliverables
- [x] Full implementation of 6 Streamlit pages.
- [x] Role-based routing and session management.
- [x] Integrated data visualization for the Admin dashboard.
- [x] End-to-end workflow from public home page $\rightarrow$ login $\rightarrow$ role-specific dashboard.
