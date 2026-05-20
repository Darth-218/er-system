# Phase 1: Foundation — Database Design & Core Models

## Overview
Phase 1 focused on establishing the structural foundation of the Hospital Information System (HIS). The primary goal was to translate the Hospital's conceptual requirements into a robust relational database schema and implement the core authentication and profile models.

## Database Architecture
The system is built on a **MySQL** relational database. The design emphasizes data integrity through the use of primary keys, foreign key constraints, and unique indexes.

### Core Entities Implemented
- **User Table:** The central hub for authentication. It implements role-based access control (RBAC) with roles: `visitor`, `patient`, `nurse`, `doctor`, and `admin`.
- **Patient Table:** Stores comprehensive medical data, including sensitive identifiers (SSN, patient number) and real-time vitals (BP, heart rate, temperature, SpO2).
- **Doctor Table:** Tracks professional credentials, scientific areas of expertise, and department affiliation.
- **Department Table:** Manages organizational structure, including department codes and chairman assignments.
- **Contact Inquiry Table:** A public-facing entity to capture and track patient/visitor inquiries.

## Technical Implementation
- **Schema Definition:** All tables were defined in `db/schema.sql` using standard DDL.
- **Data Seeding:** `db/seed.sql` provides a baseline of departments and sample users to facilitate development and testing.
- **Connection Layer:** `db/connection.py` provides a singleton-style connection helper to ensure efficient resource usage across the application.

## Deliverables
- [x] ER Diagram mapping to relational schema.
- [x] Full DDL script with constraints.
- [x] Role-based authentication query logic in `queries/auth_queries.py`.
- [x] Base CRUD operations for Patients and Doctors.
