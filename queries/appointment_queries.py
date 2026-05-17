"""
Appointment CRUD Queries
"""

from db.connection import get_connection, DatabaseError


def get_patient_appointments(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.id AS appointment_id, a.appointment_datetime, a.status,
                   a.payment_amount, a.payment_status, a.symptoms,
                   u.name AS doctor_name
            FROM appointment a
            JOIN doctor d ON a.doctor_id = d.id
            JOIN user u ON d.user_id = u.id
            JOIN patient p ON a.patient_id = p.id
            WHERE p.user_id = %s
            ORDER BY a.appointment_datetime DESC
        """, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch appointments: {e}")
    finally:
        conn.close()


def add_appointment(patient_id, doctor_id, appointment_datetime, symptoms=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM patient WHERE user_id = %s", (patient_id,))
        patient = cursor.fetchone()
        if not patient:
            raise DatabaseError("Patient record not found")
        pid = patient['id']

        cursor.execute("""
            INSERT INTO appointment (patient_id, doctor_id, appointment_datetime, symptoms)
            VALUES (%s, %s, %s, %s)
        """, (pid, doctor_id, appointment_datetime, symptoms))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to schedule appointment: {e}")
    finally:
        conn.close()


def list_available_doctors(department):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.id AS doctor_id, u.name, d.major_scientific_area AS specialty
            FROM doctor d
            JOIN user u ON d.user_id = u.id
            JOIN department dept ON d.department_id = dept.id
            WHERE dept.name = %s
            ORDER BY u.name
        """, (department,))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to list doctors: {e}")
    finally:
        conn.close()


def schedule_appointment(patient_id, doctor_id, appointment_datetime):
    return add_appointment(patient_id, doctor_id, appointment_datetime)


def cancel_appointment(appointment_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE appointment SET status = 'cancelled' WHERE id = %s AND status = 'scheduled'
        """, (appointment_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to cancel appointment: {e}")
    finally:
        conn.close()
