# Phase 3: Emergency Department Workflows & Geo-Location

## Overview
Phase 3 specialized the system for the high-pressure environment of an Emergency Department (ED). This phase implemented critical "real-time" features including triage, bed management, and spatial logistics.

## The ER Workflow Implementation

### Triage System
The triage process is the heart of the ED. Implemented in `queries/emergency_queries.py`, the system manages:
- **ESI Leveling:** Patients are assigned an Emergency Severity Index (ESI) level from 1 (Immediate/Resuscitation) to 5 (Non-urgent).
- **Arrival Tracking:** Precise timestamps for arrival and triage completion.
- **Prioritized Queue:** The waiting room logic automatically sorts patients by ESI level and then by arrival time to ensure the sickest patients are seen first.

### ER Bed Management
Efficient bed utilization is critical for ED throughput.
- **State tracking:** Beds are tracked as `available`, `occupied`, or `cleaning`.
- **Assignment Logic:** Nurses can assign patients to available beds and release them upon discharge or admission to a general ward.
- **Audit Trail:** The system maintains a history of bed assignments for medical and administrative review.

### Geo-Location Integration
To assist patients in finding the facility, the system leverages MySQL Spatial extensions.
- **Spatial Data:** Latitude and longitude are stored for the hospital and patient locations.
- **Nearest-Facility Queries:** Using `ST_Distance_Sphere`, the system can calculate the real-world distance (in meters) between a patient's location and the facility.

## Deliverables
- [x] Triage record CRUD and ESI prioritization logic.
- [x] Bed status management and assignment workflow.
- [x] Real-time waiting room queue tracking.
- [x] Geospatial distance calculations via SQL.
- [x] Nurse Dashboard (`30_Nurse.py`) implementing these workflows.
