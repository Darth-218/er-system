-- ============================================================
-- Seed Data — Hospital Information System (Emergency Dept)
-- ============================================================

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Users
-- -------------------------------------------------------
INSERT IGNORE INTO user (id, email, password_hash, role, name) VALUES
(1, 'admin@his.com', '$2b$12$Z68Vv4.sqa0bDUgMMbYmMexewtNT/YfhZUcUOQsJdl2A0./PBKhHq', 'admin', 'Dr. Admin'),
(2, 'doctor@his.com', '$2b$12$MqbWsFFtGoSO/TvseO6qEuPUfe0ADyjEbSvtzUtZFfrKxFEAgzxYW', 'doctor', 'Dr. House'),
(3, 'nurse@his.com',  '$2b$12$ybdDf0/BHuoWqFxRq8vfae2RiOnQtmt0JRYbzgujezfnm/lD0pCUe',  'nurse',  'Nurse Joy'),
(4, 'patient@his.com', '$2b$12$qr7kj39YzXd0gjoK1T8NDeb8CeVCuh1KnYlMrLziz4E/lSCFLoqhG', 'patient', 'John Doe');

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Departments
-- -------------------------------------------------------
INSERT IGNORE INTO department (id, name, code, chairman_id, supervision_start_date) VALUES
(1, 'Emergency Department', 'ER', 2, '2024-01-01'),
(2, 'Cardiology', 'CARD', NULL, NULL),
(3, 'Radiology', 'RAD', NULL, NULL);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Doctors
-- -------------------------------------------------------
INSERT IGNORE INTO doctor (id, user_id, ssn, sex, birthdate, major_scientific_area, degree, join_date, department_id) VALUES
(1, 2, '111-22-3333', 'M', '1970-05-15', 'Emergency Medicine', 'MD', '2020-03-01', 1);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Patients
-- -------------------------------------------------------
INSERT IGNORE INTO patient (id, user_id, patient_number, ssn, address, phone, birthdate, sex, medical_history, blood_pressure, heart_rate, temperature, spo2, admission_date, latitude, longitude) VALUES
(1, 4, 'P-10001', '444-55-6666', '123 Main St, Cityville', '555-0101', '1985-08-20', 'M', 'Asthma', '120/80', 72, 37.0, 98, '2025-05-14 08:30:00', 40.7128, -74.0060),
(2, 4, 'P-10002', '444-55-7777', '456 Oak Ave, Townsburg', '555-0102', '1992-12-10', 'F', 'Diabetes Type 2', '130/85', 78, 36.8, 97, '2025-05-14 09:00:00', 40.7282, -73.7949);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Rooms
-- -------------------------------------------------------
INSERT IGNORE INTO room (id, department_id, room_number, room_type, is_available) VALUES
(1, 1, 'ER-101', 'Treatment', TRUE),
(2, 1, 'ER-102', 'Observation', TRUE),
(3, 2, 'CARD-201', 'Consultation', TRUE);

-- -------------------------------------------------------
-- PHASE 3: Emergency Department — Sample Data (Member 3)
-- -------------------------------------------------------

-- ER Beds
INSERT IGNORE INTO er_bed (bed_id, department_id, bed_number, status, patient_id, assigned_at, notes) VALUES
(1,  1, 'ER-BED-01', 'available', NULL, NULL, NULL),
(2,  1, 'ER-BED-02', 'available', NULL, NULL, NULL),
(3,  1, 'ER-BED-03', 'occupied',  1, '2025-05-14 08:35:00', 'Chest pain observation'),
(4,  1, 'ER-BED-04', 'available', NULL, NULL, NULL),
(5,  1, 'ER-BED-05', 'cleaning',  NULL, NULL, 'Spills, cleaning in progress'),
(6,  1, 'ER-BED-06', 'available', NULL, NULL, NULL),
(7,  1, 'ER-BED-07', 'occupied',  2, '2025-05-14 09:10:00', 'Diabetic episode monitoring'),
(8,  1, 'ER-BED-08', 'available', NULL, NULL, NULL),
(9,  1, 'ER-BED-09', 'available', NULL, NULL, NULL),
(10, 1, 'ER-BED-10', 'available', NULL, NULL, NULL);

-- Triage Records
INSERT IGNORE INTO triage_record (id, patient_id, nurse_id, esi_level, arrival_time, chief_complaint, blood_pressure, heart_rate, temperature) VALUES
(1, 1, 3, 2, '2025-05-14 08:30:00', 'Sharp chest pain radiating to left arm', '145/90', 102, 37.2),
(2, 2, 3, 3, '2025-05-14 09:00:00', 'Dizziness and blurred vision', '130/85', 78, 36.8);

-- Waiting Room
INSERT IGNORE INTO waiting_room (id, patient_id, triage_id, queue_position, estimated_wait_minutes, entered_at, status) VALUES
(1, 1, 1, 1, 5,  '2025-05-14 08:30:00', 'in-progress'),
(2, 2, 2, 2, 15, '2025-05-14 09:00:00', 'in-progress');

-- ER Bed History
INSERT IGNORE INTO er_bed_history (id, bed_id, patient_id, assigned_at, released_at) VALUES
(1, 3, 1, '2025-05-14 08:35:00', NULL),
(2, 7, 2, '2025-05-14 09:10:00', NULL);

-- Hospital Locations (for geo queries)
INSERT IGNORE INTO hospital_location (id, name, address, latitude, longitude, department_id) VALUES
(1, 'City General Hospital - Emergency', '100 Hospital Way, Cityville', 40.7128, -74.0060, 1),
(2, 'Downtown Medical Center', '200 Health Blvd, Townsburg', 40.7282, -73.7949, 2),
(3, 'Riverside Urgent Care', '50 River Rd, Lakewood', 40.6892, -74.0445, NULL);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 2: Appointments
-- -------------------------------------------------------
INSERT IGNORE INTO appointment (id, patient_id, doctor_id, appointment_datetime, status, payment_amount, payment_status) VALUES
(1, 1, 1, '2025-05-15 10:00:00', 'scheduled', 150.00, 'unpaid');

-- -------------------------------------------------------
-- PLACEHOLDER — Member 2: Prescriptions
-- -------------------------------------------------------
INSERT IGNORE INTO prescription (id, patient_id, doctor_id, medication, dose, frequency, start_date, end_date, directions) VALUES
(1, 1, 1, 'Aspirin', '81mg', 'Once daily', '2025-05-14', '2025-06-14', 'Take with food');
