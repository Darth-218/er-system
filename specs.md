# Software Requirements Specification (SRS)
## Hospital Information System – Emergency Department

### 1. Introduction

#### 1.1 Purpose
This document defines the functional and non‑functional requirements for an **Emergency Department (ED)** module of a Hospital Information System (HIS). The system supports daily operations, patient management, doctor workflows, appointment handling, file uploads, and administrative analytics.

#### 1.2 Scope
The system focuses exclusively on the **Emergency Department**. It provides:
- Visitor home page and user authentication (doctors, patients, nurses, employees, administrators).
- User profiles with role‑specific dashboards.
- Secure file serving and upload of patient scans.
- Appointment scheduling, online payment, cancellation, and refunds.
- Prescription management and medical history tracking.
- Room reservation by doctors for patient treatment.
- Geolocation services to find the nearest emergency department location.
- Administrative dashboard with statistical reports.
- Contact forms for inquiries.

#### 1.3 Definitions & Acronyms
- **HIS** – Hospital Information System
- **ED** – Emergency Department
- **Patient‑number** – unique internal identifier for each patient
- **SSN** – Social Security Number (unique)
- **Department code** – unique identifier of a department
- **Medical status** – blood pressure, heart rate, temperature

---

### 2. User Roles

| Role          | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| Visitor       | Unauthenticated user; can view home page and contact form.                  |
| Patient       | Registered user; books/cancels appointments, uploads scans, views own record.|
| Doctor        | Manages patient examinations, writes prescriptions, reserves rooms, views schedule. |
| Nurse         | Assists in recording vital signs, updating medical status.                  |
| Employee      | Administrative staff; manages contact requests, assists with appointments.   |
| Administrator | Full access to statistical dashboard, user management, system reports.      |

---

### 3. Functional Requirements

#### 3.1 Home Page (Visitor)
- Public landing page describing the Emergency Department.
- Links to: login, registration, contact form.

#### 3.2 Authentication & Registration
- User registration with role selection (patient, doctor, nurse, employee).
- Login with email/username and password; role‑based access control.
- Password recovery and secure session management.

#### 3.3 User Profiles
- **Patient profile**: name, patient‑number, SSN, address, phone, birthdate, sex, medical history, medical status (BP, heart rate, temperature), admission date to ED, uploaded scans.
- **Doctor profile**: name, sex, birthdate, SSN, major scientific area, degree, department affiliation (Emergency), join date.
- **Nurse/Employee profile**: personal details, role, contact info.
- **Admin profile**: same as employee plus system privileges.

#### 3.4 File Management
- Static file serving (e.g., previous scans, reports).
- Secure upload of patient scans (X‑ray, CT, MRI) with timestamp and uploader identity.
- Files linked to the patient’s record.

#### 3.5 Appointments Model (Doctor–Patient)
- Patients can book, reschedule, or cancel appointments with ED doctors.
- Appointment attributes: date, time, doctor, patient, reason, status (scheduled, completed, cancelled).
- **Payment & Refund**:
  - Patient registers for an appointment and pays online.
  - Cancellation before a threshold (e.g., 2 hours) triggers automatic refund.
  - Refund status tracked (pending, completed, rejected).
- Appointment reminders (email/SMS).

#### 3.6 Prescriptions Management
- Doctor writes a prescription for a patient.
- Each prescription records: prescription date, doctor, patient.
- For each medication: directions (times/day, dose), start date, end date.
- Multiple medications per prescription; many prescriptions per patient.
- Many doctors can write many prescriptions for the same patient.

#### 3.7 Medical Records
- Store patient personal and medical data (as in 3.3).
- Admission date to ED automatically recorded.
- Track medical status over time (history of BP, heart rate, temperature).
- Nurses can update vital signs at any time.

#### 3.8 Department & Locations (Emergency)
- Emergency Department attributes:
  - Name (unique)
  - Department code (unique)
  - Chairman (a doctor) + date supervision started
  - Several physical locations (e.g., “Main Hospital”, “East Wing”)
- Each location has address, GPS coordinates (for geo‑queries).

#### 3.9 Doctor–Patient Relationship
- A doctor examines one or more patients on a regular basis.
- Many doctors can investigate the same patient concurrently.
- Track **hours per week** each doctor spends on each patient.

#### 3.10 Room Reservation by Doctors
- Doctors can reserve different rooms for patient treatment (e.g., trauma room, observation room, ultrasound room).
- Room attributes: room number, type, capacity, equipment, availability.
- Reservation period: start time, end time, patient, doctor.

#### 3.11 Contact Forms
- Unauthenticated visitors and users can submit inquiries/requests.
- Form fields: name, email, subject, message.
- Admin/employee can reply and mark as resolved.

#### 3.12 Admin Dashboard – Statistical Analysis
- Daily/weekly/monthly patient visits to ED.
- Average wait time for appointments.
- Most prescribed medications.
- Room utilisation rate.
- Revenue from appointments vs. refunds.
- Uploaded scans count per doctor/patient.
- Filtering by date, doctor, or patient group.

#### 3.13 Geolocation
- For a given user location (address or coordinates), find the nearest Emergency Department location.
- Display distance and directions.
- Used during emergency contact or appointment location selection.

#### 3.14 Report Generation
- **Doctor appointment report**: list of all appointments per doctor, with patient details and status.
- **Room allocation report**: which rooms were reserved, by whom, for which patient, duration.
- Export as PDF/CSV.

---

### 4. Data Requirements (Entity–Attribute Summary)

#### 4.1 Patient
| Attribute           | Type         | Constraints / Notes                          |
|---------------------|--------------|----------------------------------------------|
| patient‑number      | Integer      | **Unique**, primary key                      |
| SSN                 | String(11)   | **Unique**                                   |
| name                | String       |                                              |
| address             | String       |                                              |
| phone               | String       |                                              |
| birthdate           | Date         |                                              |
| sex                 | Enum(M/F/O)  |                                              |
| medical history     | Text         |                                              |
| blood pressure      | String       | e.g., “120/80”                               |
| heart rate          | Integer      | bpm                                          |
| temperature         | Decimal      | Celsius                                      |
| admission date      | DateTime     | To ED                                        |

#### 4.2 Doctor
| Attribute             | Type         | Constraints                 |
|-----------------------|--------------|-----------------------------|
| social security number| String(11)   | **Unique**                  |
| name                  | String       |                             |
| sex                   | Enum(M/F/O)  |                             |
| birthdate             | Date         |                             |
| major scientific area | String       | e.g., Cardiology, Trauma    |
| degree                | String       | e.g., MD, PhD               |
| join date (to dept)   | Date         |                             |

#### 4.3 Emergency Department
| Attribute           | Type         | Constraints            |
|---------------------|--------------|------------------------|
| department code     | String       | **Unique**, PK         |
| name                | String       | **Unique**             |
| chairman (doctor)   | Foreign Key  | References doctor      |
| supervision start   | Date         |                        |

#### 4.4 Department Location
| Attribute     | Type         | Constraints                    |
|---------------|--------------|--------------------------------|
| location ID   | Integer      | PK                             |
| department code| FK          | References department          |
| address       | String       |                                |
| GPS coordinates| Point       | Used for nearest search        |

#### 4.5 Examines (relationship Doctor – Patient)
| Attribute            | Type      | Constraints                             |
|----------------------|-----------|-----------------------------------------|
| doctor SSN           | FK        | Composite PK with patient‑number        |
| patient‑number       | FK        |                                         |
| hours per week       | Decimal   |                                         |

#### 4.6 Prescription
| Attribute         | Type      | Constraints                       |
|-------------------|-----------|-----------------------------------|
| prescription ID   | Integer   | PK                                |
| prescription date | Date      |                                   |
| doctor SSN        | FK        |                                   |
| patient‑number    | FK        |                                   |

#### 4.7 Prescribed Medication (line item)
| Attribute         | Type      | Constraints                       |
|-------------------|-----------|-----------------------------------|
| medication name   | String    |                                   |
| times per day     | Integer   |                                   |
| dose              | String    | e.g., “500 mg”                    |
| start date        | Date      |                                   |
| end date          | Date      |                                   |
| prescription ID   | FK        |                                   |

#### 4.8 Room
| Attribute      | Type       | Constraints                      |
|----------------|------------|----------------------------------|
| room number    | String     | PK                               |
| type           | String     | e.g., Trauma, Observation        |
| capacity       | Integer    |                                  |
| equipment      | Text       |                                  |
| department code| FK         | Emergency Department             |

#### 4.9 Room Reservation
| Attribute      | Type       | Constraints                      |
|----------------|------------|----------------------------------|
| reservation ID | Integer    | PK                               |
| room number    | FK         |                                  |
| doctor SSN     | FK         |                                  |
| patient‑number | FK         |                                  |
| start time     | DateTime   |                                  |
| end time       | DateTime   |                                  |

#### 4.10 Appointment (with payment)
| Attribute          | Type       | Constraints                         |
|--------------------|------------|-------------------------------------|
| appointment ID     | Integer    | PK                                  |
| patient‑number     | FK         |                                     |
| doctor SSN         | FK         |                                     |
| date & time        | DateTime   |                                     |
| reason             | Text       |                                     |
| status             | Enum       | scheduled, completed, cancelled     |
| payment status     | Enum       | paid, refunded, pending             |
| refund amount      | Decimal    | if cancelled                        |

#### 4.11 File Upload (Patient Scan)
| Attribute      | Type       | Constraints                  |
|----------------|------------|------------------------------|
| file ID        | Integer    | PK                           |
| patient‑number | FK         |                              |
| file path      | String     | Static file reference        |
| upload timestamp| DateTime  |                              |
| uploaded by    | FK (user)  | doctor / nurse / employee    |

#### 4.12 Contact Form Request
| Attribute   | Type       | Constraints          |
|-------------|------------|----------------------|
| request ID  | Integer    | PK                   |
| name        | String     |                      |
| email       | String     |                      |
| subject     | String     |                      |
| message     | Text       |                      |
| resolved    | Boolean    | default false        |

---

### 5. Business Rules

1. **Unique values**: patient‑number, SSN (patient); department name, department code; doctor SSN.
2. Each doctor belongs to exactly **one** department (Emergency) with a specific join date.
3. A department may have **several locations** simultaneously.
4. Many doctors may investigate one patient – hours per week tracked per doctor‑patient pair.
5. A doctor can write many prescriptions; a prescription belongs to exactly one doctor and one patient.
6. For each medication in a prescription, start date and end date are mandatory.
7. A patient can be admitted only once but the admission date is recorded each time.
8. A doctor can reserve a room only for a patient they are currently treating.
9. A patient can only cancel an appointment and receive a refund if cancellation occurs before a defined cut‑off time (system parameter).
10. Only administrators can access the statistical dashboard and generate all reports.

---

### 6. Non‑Functional Requirements

- **Security**: All uploads are virus‑scanned; patient data encrypted at rest; HTTPS only.
- **Performance**: Geo‑location search returns results in <2 seconds; file uploads up to 50 MB.
- **Availability**: System operational 24/7 for emergency use.
- **Usability**: Mobile‑responsive design for field doctors and patients.
- **Compliance**: Follows medical data privacy regulations (e.g., HIPAA, GDPR).

---

### 7. Traceability to Original Requirements (PDF list)

| # | Requirement from PDF                                 | Included in Spec Section                           |
|--|------------------------------------------------------|----------------------------------------------------|
| 1 | Model patients, with complete info                  | 3.3, 4.1                                           |
| 2 | Model hospitals including regular rooms, etc.       | 3.10, 4.8, 4.9                                     |
| 3 | Model doctor info                                   | 3.3, 4.2                                           |
| 4 | Model work relationship doctor – hospital (dept)    | 3.8 (chairman), 4.3 (join date)                    |
| 5 | Model treatment relationship doctor – patient       | 3.9 (examines, hours/week)                         |
| 6 | Model geo locations (nearest place)                 | 3.13, 4.4                                          |
| 7 | Register/pay for doctor appointment                 | 3.5 (payment)                                      |
| 8 | Cancel / get refund for appointment                 | 3.5 (refund)                                       |
| 9 | Doctor reserve rooms for patient treatment          | 3.10, 4.9                                          |
| 10| Generate reports (appointments, room allocation)    | 3.14                                               |

---
