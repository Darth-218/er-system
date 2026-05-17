"""
Prescription CRUD Queries
"""

from db.connection import get_connection, DatabaseError


def get_patient_prescriptions(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT pr.id AS prescription_id,
                   pr.medication, pr.dose, pr.frequency,
                   pr.start_date, pr.end_date, pr.directions,
                   pr.prescription_date AS date_prescribed,
                   u.name AS doctor_name,
                   CASE
                       WHEN pr.end_date IS NULL OR pr.end_date >= CURDATE() THEN 'active'
                       ELSE 'inactive'
                   END AS status
            FROM prescription pr
            JOIN doctor d ON pr.doctor_id = d.id
            JOIN user u ON d.user_id = u.id
            JOIN patient p ON pr.patient_id = p.id
            WHERE p.user_id = %s
            ORDER BY pr.prescription_date DESC
        """, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch prescriptions: {e}")
    finally:
        conn.close()


def write_prescription(patient_id, doctor_id, medication, dose, frequency, start_date, end_date, directions):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM patient WHERE user_id = %s", (patient_id,))
        patient = cursor.fetchone()
        if not patient:
            raise DatabaseError("Patient record not found")
        pid = patient['id']

        cursor.execute("""
            INSERT INTO prescription (patient_id, doctor_id, medication, dose, frequency, start_date, end_date, directions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (pid, doctor_id, medication, dose, frequency, start_date, end_date, directions))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to write prescription: {e}")
    finally:
        conn.close()
