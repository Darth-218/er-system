-- ============================================================
-- Hospital Information System — Database Schema
-- Department: Emergency
-- ============================================================
-- NOTE: Tables marked with -- PLACEHOLDER -- are owned by other
-- members and are stubbed here for dependency resolution.
-- ============================================================

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: User / Auth base table
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('visitor','patient','nurse','doctor','admin') NOT NULL DEFAULT 'visitor',
    name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Department
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS department (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    chairman_id INT,
    supervision_start_date DATE,
    FOREIGN KEY (chairman_id) REFERENCES user(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Doctor profile
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    ssn VARCHAR(20) UNIQUE NOT NULL,
    sex ENUM('M','F','Other'),
    birthdate DATE,
    major_scientific_area VARCHAR(255),
    degree VARCHAR(100),
    join_date DATE,
    department_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (department_id) REFERENCES department(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Patient
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    patient_number VARCHAR(50) UNIQUE NOT NULL,
    ssn VARCHAR(20) UNIQUE NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    birthdate DATE,
    sex ENUM('M','F','Other'),
    medical_history TEXT,
    blood_pressure VARCHAR(20),
    heart_rate INT,
    temperature DECIMAL(4,1),
    spo2 TINYINT,
    admission_date DATETIME,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Room (non-ER)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    room_type VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Contact Inquiry
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS contact_inquiry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('open','resolved') DEFAULT 'open',
    assigned_admin_id INT,
    FOREIGN KEY (assigned_admin_id) REFERENCES user(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 2: Appointment
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS appointment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_datetime DATETIME NOT NULL,
    status ENUM('scheduled','cancelled','completed') DEFAULT 'scheduled',
    payment_amount DECIMAL(10,2),
    payment_status ENUM('unpaid','paid','refunded') DEFAULT 'unpaid',
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 2: Prescription
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS prescription (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    prescription_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    medication VARCHAR(255) NOT NULL,
    dose VARCHAR(100),
    frequency VARCHAR(100),
    start_date DATE,
    end_date DATE,
    directions TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 2: Treatment / Doctor-Patient hours
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS treatment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    hours_per_week DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 1: Room reservation
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS room_reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

-- ============================================================
-- PHASE 3 — Emergency Department Tables  (Member 3)
-- ============================================================

-- -------------------------------------------------------
-- TriageRecord: ESI level, vitals, chief complaint
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS triage_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    nurse_id INT NOT NULL,
    esi_level TINYINT NOT NULL CHECK(esi_level BETWEEN 1 AND 5),
    arrival_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    chief_complaint TEXT,
    blood_pressure VARCHAR(20),
    heart_rate INT,
    temperature DECIMAL(4,1),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (nurse_id) REFERENCES user(id),
    INDEX idx_triage_esi (esi_level, arrival_time)
);

-- -------------------------------------------------------
-- ERBed: Bed management in the emergency room
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS er_bed (
    bed_id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    bed_number VARCHAR(10) NOT NULL,
    status ENUM('available','occupied','cleaning') DEFAULT 'available',
    patient_id INT,
    assigned_at DATETIME,
    notes TEXT,
    FOREIGN KEY (department_id) REFERENCES department(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    INDEX idx_bed_status (status, department_id)
);

-- -------------------------------------------------------
-- ERBedHistory: Audit trail of bed assignments
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS er_bed_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bed_id INT NOT NULL,
    patient_id INT NOT NULL,
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    released_at DATETIME,
    FOREIGN KEY (bed_id) REFERENCES er_bed(bed_id),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    INDEX idx_bed_history (bed_id, released_at)
);

-- -------------------------------------------------------
-- WaitingRoom: Queue management
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS waiting_room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    triage_id INT NOT NULL,
    queue_position INT,
    estimated_wait_minutes INT,
    entered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('waiting','in-progress','left') DEFAULT 'waiting',
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (triage_id) REFERENCES triage_record(id),
    INDEX idx_waiting_status (status, queue_position)
);

-- -------------------------------------------------------
-- HospitalLocation: Geo-coordinates for spatial queries
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS hospital_location (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES department(id)
);

-- Spatial index for ST_Distance_Sphere queries
-- (MySQL requires a SRID-defined column for spatial indexes)
ALTER TABLE hospital_location ADD COLUMN coords POINT SRID 4326
    GENERATED ALWAYS AS (ST_SRID(POINT(longitude, latitude), 4326)) STORED;
CREATE SPATIAL INDEX idx_hospital_coords ON hospital_location(coords);

-- -------------------------------------------------------
-- PLACEHOLDER — Member 5: File metadata
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS file_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    stored_path VARCHAR(500) NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_type VARCHAR(50),
    file_size BIGINT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);
