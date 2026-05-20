# Phase 4: Admin Dashboard & System Reporting

## Overview
Phase 4 focused on the "big picture" functionality—providing hospital administrators with the tools necessary to monitor system performance, analyze ED throughput, and manage long-term medical records.

## Reporting & Analytics Implementation
The reporting engine is powered by complex aggregation queries defined in `queries/report_queries.py`.

### Quantitative Reports
- **Doctor Productivity:** Reports aggregating the number of appointments and total revenue generated per doctor over specific timeframes.
- **Bed Utilization:** A real-time snapshot of ER bed status, calculating the percentage of occupied vs. available beds.
- **ESI Statistics:** Analysis of patient acuity levels to determine the distribution of emergency vs. non-urgent cases.
- **Admission Summaries:** A high-level view of all recent patient admissions and their medical histories.

### Administrative Control
The Admin dashboard provides a centralized command center for the system:
- **System Health:** High-level counts of total patients, doctors, and pending appointments.
- **Data Export:** Capability to view data in tabular formats that can be easily exported for external analysis.
- **Contact Management:** An interface to review public inquiries and assign them to specific administrators for resolution.

## File & Metadata Management
To handle large medical files (scans, images) without bloating the database:
- **Hybrid Storage:** Original files are stored in the local `uploads/` directory.
- **Metadata Tracking:** The `file_metadata` table stores the filename, type, size, and a link to the patient, allowing for fast indexing and retrieval without reading the actual file.

## Deliverables
- [x] Complex aggregation queries for professional reporting.
- [x] Dashboard statistics for system monitoring.
- [x] File upload and retrieval system with metadata tracking.
- [x] Admin Dashboard (`40_Admin.py`) for system-wide oversight.
