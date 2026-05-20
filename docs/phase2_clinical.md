# Phase 2: Appointments, Prescriptions & Treatment Workflows

## Overview
Phase 2 implemented the core clinical workflows of the hospital, focusing on the lifecycle of a patient visit: from scheduling an appointment and receiving treatment to medication prescriptions.

## Key Feature Implementation

### Appointment Management
The system implements a flexible scheduling mechanism managed via `queries/appointment_queries.py`.
- **Scheduling:** Patients can browse available doctors within a specific department and request time slots.
- **Payment Integration:** The system tracks payment amounts and statuses (pending/paid) associated with each appointment.
- **Cancellations:** A workflow for cancelling appointments is implemented, ensuring the time slot is released.

### Prescription System
Clinicians can issue precise medical orders via `queries/prescription_queries.py`.
- **Detailed Orders:** Prescriptions include medication name, dosage, frequency, and specific clinician directions.
- **Temporal Tracking:** The system tracks both the date of prescription and the intended start/end dates for the treatment.
- **Patient History:** All prescriptions are linked to the patient's medical record, allowing for a longitudinal view of their medication history.

### Treatment & Room Reservation
To bridge the gap between appointments and the ER, the system manages the physical allocation of resources.
- **Doctor-Patient Relationship:** The database tracks which doctors are currently treating which patients.
- **Room Allocation:** Logic is implemented to reserve medical rooms for specific treatments, ensuring no resource conflicts.

## Deliverables
- [x] Appointment CRUD and status management logic.
- [x] Prescription writing and lookup functionality.
- [x] Room availability and reservation queries.
- [x] Integrated interfaces in the Patient and Doctor dashboards.
