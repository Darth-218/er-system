# Member 3 — Phase 3: Emergency Department Workflows

## Overview

Member 3 owns the complete **Emergency Department** backend and frontend:
- All emergency-specific database tables (triage, ER beds, waiting room, geo-location)
- Full query module: `queries/emergency_queries.py` (15 functions)
- Nurse dashboard: `pages/30_Nurse.py`
- Doctor page co-ownership: `pages/20_Doctor.py` (shared with Member 4)

---

## Files Created / Owned

| File | Role |
|---|---|
| `queries/emergency_queries.py` | All emergency + geo query functions |
| `pages/30_Nurse.py` | Full nurse dashboard (3 tabs) |
| `db/schema.sql` | Phase 3 tables (triage_record, er_bed, er_bed_history, waiting_room, hospital_location) + spatial index |
| `db/seed.sql` | Phase 3 seed data (10 ER beds, 2 triage records, waiting queue entries, 3 hospital locations) |

### Schema — Phase 3 Tables

```sql
triage_record      -- ESI level (1-5), vitals, chief complaint, FK → patient, user
er_bed             -- bed_number, status (available/occupied/cleaning), FK → patient, department
er_bed_history     -- audit trail: assigned_at / released_at per bed-patient pair
waiting_room       -- queue_position, estimated_wait_minutes, status, FK → triage_record
hospital_location  -- name, lat/lng, SPATIAL INDEX for ST_Distance_Sphere queries
```

### Emergency Queries (`emergency_queries.py`)

| Function | Type | Description |
|---|---|---|
| `add_triage_record()` | INSERT | Creates triage + auto-inserts into waiting room |
| `get_triage_records(patient_id)` | SELECT | Triage history for a patient |
| `list_triage_queue()` | SELECT | Active queue, ordered by ESI asc + arrival asc |
| `add_er_bed()` | INSERT | New bed for a department |
| `list_er_beds(department_id)` | SELECT | All beds with status + patient name |
| `list_available_beds(department_id)` | SELECT | Filtered available beds |
| `assign_bed(bed_id, patient_id)` | UPDATE+INSERT | Occupies bed + creates history record + updates waiting room |
| `release_bed(bed_id)` | UPDATE | Clears patient, sets status=cleaning, closes history |
| `complete_cleaning(bed_id)` | UPDATE | Sets status=available |
| `get_bed_history(bed_id)` | SELECT | Full assignment audit trail |
| `get_bed_stats(department_id)` | AGG | COUNT grouped by status |
| `get_waiting_queue()` | SELECT | Full queue with ESI-priority ordering |
| `count_waiting_patients()` | AGG | Queue length |
| `remove_from_waiting(patient_id)` | UPDATE | Mark as in-progress/left |
| `find_nearest_hospitals(lat, lng, radius)` | SPATIAL | `ST_Distance_Sphere` nearest-location query |
| `update_patient_location(patient_id, lat, lng)` | UPDATE | Store patient geo coords |
| `search_patients_by_name(query)` | SELECT | Fuzzy patient search (used by Nurse page) |

### Nurse Dashboard (`pages/30_Nurse.py`)

Three-tab layout:

| Tab | Content |
|---|---|
| 🩺 **Triage Intake** | Patient search, vitals form (BP/HR/temp), ESI level dropdown, chief complaint → submits triage + adds to waiting room |
| 🛏️ **ER Beds** | Color-coded bed grid (🟢available/🔴occupied/🟡cleaning), assign/release/mark-clean forms, bed history viewer |
| 📋 **Waiting Room** | Full queue sorted ESI asc + FIFO, metrics in sidebar, remove-from-queue actions |

---

## Dependencies (Placeholder Stubs)

These are files with `Placeholder` or `NotImplementedError` markers for other members:

| File | Owner | Wait status |
|---|---|---|
| `utils/auth.py` | Member 2 | **Needed for `require_role()`** — stub provides hardcoded nurse login for dev |
| `db/schema.sql` (base tables) | Member 1 | All base tables marked with `-- PLACEHOLDER --` |
| `db/seed.sql` (base data) | Member 1 | Users, departments, doctors, patients pre-seeded with IDs |
| `pages/10_Patient.py` | Member 2 | Placeholder |
| `pages/20_Doctor.py` | Member 3+4 | Placeholder — shared with Member 4 |
| `pages/40_Admin.py` | Member 5 | Placeholder |
| `queries/auth_queries.py` | Member 2 | Placeholder |
| `queries/patient_queries.py` | Member 1/2 | Placeholder (emergency queries use `search_patients_by_name` directly) |
| `queries/appointment_queries.py` | Member 2 | Placeholder |
| `queries/prescription_queries.py` | Member 2 | Placeholder |
| `queries/doctor_queries.py` | Member 1 | Placeholder |
| `queries/contact_queries.py` | Member 5 | Placeholder |
| `queries/report_queries.py` | Member 5 | Placeholder |
| `utils/file_handler.py` | Member 5 | Placeholder |

---

## Running the Project

```bash
# Enter dev shell (provides Python + streamlit + mysql-connector)
nix develop

# Initialize the database
python db/setup_db.py

# Set environment variables (or use defaults)
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=yourpassword
export MYSQL_DATABASE=his_emergency

# Start the app
streamlit run app.py
```

---

## Waiting Room Queue Logic

Patients in the waiting room are ordered by:
1. **ESI level ascending** (ESI 1 = most urgent, first)
2. **Arrival time ascending** (FIFO within same ESI level)

Estimated wait times are assigned based on ESI level:
| ESI | Wait (min) |
|---|---|
| 1 | 0 (immediate) |
| 2 | 5 |
| 3 | 15 |
| 4 | 30 |
| 5 | 60 |

---

## Geo-Location

Patient addresses store `latitude` / `longitude` columns on the `patient` table.
`hospital_location` table has a spatial index using `ST_SRID(POINT(longitude, latitude), 4326)`.

Query: `ST_Distance_Sphere` returns distances in meters, filtered by a configurable radius.
