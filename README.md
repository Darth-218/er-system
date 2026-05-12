# Hospital Information System (HIS) — Emergency Department

## Overview

A web application simulating a Hospital Information System for the **Emergency Department**. The system manages patients, doctors, appointments, prescriptions, triage workflows, room allocation, and administrative reporting — all accessed by different user roles with secure authentication.

---

## Tech Stack

| Layer        | Technology                                                  |
| ------------ | ----------------------------------------------------------- |
| Frontend     | **Streamlit** (pure Python — no HTML/CSS/JS needed)         |
| Backend      | Python + Streamlit (unified logic)                          |
| Database     | **MySQL** (local server)                                    |
| Geo-location | MySQL spatial queries (`ST_Distance`, `ST_Distance_Sphere`) |
| DB Driver    | `mysql-connector-python` or `pymysql`                       |
| Auth         | Custom session-based via `st.session_state`                 |
| File Storage | Local `uploads/` directory                                  |
| Query Layer  | Raw SQL executed via Python DB driver                       |

**Why this stack?** One language (Python) for everything. Streamlit removes the frontend/backend split — write a single `app.py` with pages for each role. MySQL provides a real relational database with spatial geo support for nearest-hospital queries, proper concurrency, and ACID transactions. Raw SQL keeps the focus on writing queries, not ORMs. Run the whole project with `streamlit run app.py`.

---

## Project Architecture

### Directory Layout

```
project/
├── app.py                    # Entry point — shared sidebar, role routing
├── pages/
│   ├── 01_Home.py            # Public/visitor home page
│   ├── 02_Login.py           # Login page
│   ├── 10_Patient.py         # Patient dashboard
│   ├── 20_Doctor.py          # Doctor dashboard
│   ├── 30_Nurse.py           # Nurse dashboard (triage, beds)
│   └── 40_Admin.py           # Admin dashboard (reports, users)
├── db/
│   ├── schema.sql            # DDL — all CREATE TABLE statements
│   ├── seed.sql              # Sample/seed data
│   ├── setup_db.py           # Create database + run schema/seed
│   └── connection.py         # MySQL connection helper (config via env vars)
├── queries/
│   ├── auth_queries.py       # Login, registration, roles
│   ├── patient_queries.py    # CRUD + queries for patients
│   ├── doctor_queries.py     # CRUD + queries for doctors
│   ├── appointment_queries.py
│   ├── prescription_queries.py
│   ├── emergency_queries.py  # Triage, ER beds, waiting room
│   ├── contact_queries.py    # Contact form submissions
│   └── report_queries.py     # Aggregation/reporting queries
├── utils/
│   ├── auth.py               # st.session_state login/session mgmt
│   └── file_handler.py       # Upload/download helpers
├── uploads/                  # Patient scans, medical images (gitignored)
└── requirements.txt          # Dependencies
```

**Streamlit `pages/` convention:** Files prefixed with numbers control sidebar ordering. Each page file maps to one role's view.

### Data Flow

```
User (Browser)  ──>  Streamlit page  ──>  queries/*.py  ──>  MySQL DB
                                        ⬑  utils/auth.py
```

1. User opens `app.py` — sidebar shows available pages based on role
2. Each page calls the appropriate query function from `queries/`
3. Query functions execute raw SQL via `mysql.connector` (or `pymysql`) and return results
4. Page renders results with Streamlit components (tables, charts, forms)
5. File uploads go through `utils/file_handler.py` — saved to disk, path stored in DB

### Auth Flow

```
Login form  ──>  auth_queries.py (verify credentials)
            ──>  auth.py (store role + user_id in st.session_state)
            ──>  Redirect to role-appropriate page
```

- Session state is per-browser-tab (Streamlit reset on rerun)
- Every page checks `st.session_state.role` before rendering
- No external auth dependency — pure Python session management

### File Upload Flow

```
st.file_uploader  ──>  utils/file_handler.py
                          ├── saves to uploads/{patient_id}/{filename}
                          └── inserts path + metadata into DB
```

- Original files stored on disk; database stores only the relative path
- Files served only through Streamlit pages that verify user authentication and permission
- Access control is enforced per-request (user must be logged in with the right role)
- This keeps the database small and fast while allowing access control at the app level

### Query Modules (Split by Domain)

| Module                    | Responsibility                                            |
| ------------------------- | --------------------------------------------------------- |
| `auth_queries.py`         | User registration, login, role lookup                     |
| `patient_queries.py`      | Patient CRUD, medical history, medical status             |
| `doctor_queries.py`       | Doctor CRUD, department assignment, hours tracking        |
| `appointment_queries.py`  | Schedule, pay, cancel, refund, availability checks        |
| `prescription_queries.py` | Write prescriptions, medication directions, date tracking |
| `emergency_queries.py`    | Triage records, ER bed allocation, waiting room queue     |
| `contact_queries.py`      | Contact form submissions, inquiry management, status      |
| `report_queries.py`       | Aggregations, date-range reports, room utilization        |

Each team member owns one or more query modules + the corresponding Streamlit page(s).

---

## Database Schema (ER & Relational)

### Core Entities

- **Patient** — name, patient-number (unique), SSN (unique), address, phone, birthdate, sex, medical history, medical status (BP, heart rate, temperature), admission date
- **Department** — name (unique), department-code (unique), chairman (doctor), supervision start date, multiple locations
- **Doctor** — name, sex, birthdate, SSN, major scientific area, degree, join date, hours per week per patient
- **Prescription** — doctor, patient, date, medication, dose, frequency, start/end dates
- **Appointment** — patient, doctor, datetime, status (scheduled/cancelled/completed), payment
- **Room** — department, type, availability
- **User** — authentication base for Patient, Doctor, Nurse, Admin, Employee roles
- **ContactInquiry** — name, email, subject, message, submitted_at, status (open/resolved), assigned admin

### Emergency-Specific Extensions

- **TriageRecord** — ESI level (1-5), arrival time, chief complaint, vitals at triage
- **ERBed** — bed number, status (available/occupied/cleaning), assignment history
- **WaitingRoom** — queue position, estimated wait time

---

## Project Components & Phases

### Phase 1 — Foundation (Database + Core Models)

**Database Design**

- Draw ER diagram
- Map to relational schema
- Write DDL with constraints, primary/foreign keys, indices
- Seed data for departments, sample doctors, sample patients

**Core Models**

- Patient model (all required attributes)
- Doctor model (personal data, scientific area, degree)
- Department model (name, code, chairman, locations)
- User model with role-based inheritance (Doctor, Patient, Nurse, Admin, Employee)
- ContactInquiry model (name, email, subject, message, status, timestamps)

**Queries delivered:** Patient CRUD, Doctor CRUD, Department CRUD, ContactInquiry CRUD, user authentication queries, role-based data access queries

---

### Phase 2 — Appointments, Prescriptions & Treatments

**Appointments**

- Schedule appointment (patient selects doctor, date/time)
- Payment processing (register/pay)
- Cancellation and refund workflow
- Conflict detection (double-booking prevention)

**Prescriptions**

- Doctor writes prescription with medication, dose, frequency, directions
- Track start/end dates for each medication
- Multiple prescriptions per patient, multiple doctors per patient

**Treatment Relationship**

- Track which doctors treat which patients
- Record hours per week per doctor-patient pair
- Room reservation for patient treatment

**Queries delivered:** Appointment CRUD + status queries, prescription lookup queries, doctor-patient treatment queries, room availability/reservation queries

---

### Phase 3 — Emergency Department Workflows

**Triage System**

- Record triage data on patient arrival (ESI level, vitals, chief complaint)
- Auto-prioritize waiting queue based on ESI level and arrival time

**ER Bed Management**

- Assign patients to beds
- Track bed status (available, occupied, cleaning)
- Bed assignment history

**Waiting Room Queue**

- Real-time queue position tracking
- Estimated wait time calculation

**Geo-Location**

- Store hospital/patient addresses with geospatial coordinates
- Query nearest hospitals or facilities

**Queries delivered:** Triage record queries, ER bed allocation/release queries, waiting room queue queries, nearest-location spatial queries (`ST_Distance_Sphere`)

---

### Phase 4 — Admin Dashboard & Reporting

**Reports**

- Doctor appointment reports (daily/weekly/monthly per doctor)
- Room allocation reports (utilization rates)
- Patient admission/discharge summaries
- Emergency department throughput statistics

**Admin Dashboard**

- Statistical charts and graphs
- Filterable data tables
- Exportable reports

**File Management**

- Static file serving
- File uploads (patient scans, medical images, documents)
- File metadata tracking

**Queries delivered:** Aggregation queries for reports, join queries across entities, date-range filtering queries, file metadata queries, admin dashboard data queries

---

### Phase 5 — Frontend & User Experience

**Public Pages**

- Home page with hospital info
- Visitor information
- Contact forms for inquiries (submitted via `contact_queries.py`, viewable by admin)

**Authenticated Pages**

- Patient dashboard (view appointments, prescriptions, medical history, scans)
- Doctor dashboard (view schedule, patients, write prescriptions)
- Nurse dashboard (triage intake, bed management)
- Admin dashboard (statistics, user management, reports)

**User Experience**

- Responsive design
- Role-based navigation
- Form validation
- File upload interface for scans

**Queries delivered:** All frontend data-fetching queries across every page, user profile display queries

---

## Query Distribution (All Phases)

Every phase includes SQL queries as part of its deliverables. The types of queries across the project:

| Query Type  | Examples                                                      |
| ----------- | ------------------------------------------------------------- |
| CRUD        | INSERT/UPDATE/DELETE for all entities                         |
| Selection   | Filtered SELECTs by date, role, status                        |
| Aggregation | COUNT, AVG, SUM for reports/dashboards                        |
| Join        | Multi-table JOINs for prescriptions, appointments, treatments |
| Spatial     | MySQL `ST_Distance_Sphere` nearest-location queries           |
| Subquery    | Nested queries for complex reporting                          |
| Transaction | Payment + appointment creation, cancellation + refund         |

---

## Team Structure

| Component                              | Focus Area                                                                |
| -------------------------------------- | ------------------------------------------------------------------------- |
| Database Schema & DDL                  | ER diagram, relational mapping, DDL scripts, seed data                    |
| Backend — Auth & Profiles              | User system, roles, profiles, authentication                              |
| Backend — Appointments & Prescriptions | Scheduling, payments, prescriptions, room reservations                    |
| Backend — Emergency & Geo              | Triage, ER beds, waiting room, geo-location, reports                      |
| Frontend & UI                          | All pages, file uploads, dashboards, contact forms + `contact_queries.py` |
