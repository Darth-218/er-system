"""
Patient CRUD Queries
"""

from db.connection import get_connection, DatabaseError


def get_patient_by_id(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.patient_number, p.ssn, p.address, p.phone,
                   p.birthdate, p.sex, p.medical_history,
                   p.blood_pressure, p.heart_rate, p.temperature, p.spo2,
                   p.admission_date, p.latitude, p.longitude,
                   u.name, u.email
            FROM patient p
            JOIN user u ON p.user_id = u.id
            WHERE u.id = %s
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            row['medical_status'] = {
                'bp': row.get('blood_pressure'),
                'heart_rate': row.get('heart_rate'),
                'temperature': row.get('temperature'),
                'spo2': row.get('spo2'),
            }
        return row
    except Exception as e:
        raise DatabaseError(f"Failed to fetch patient: {e}")
    finally:
        conn.close()


def search_patients(query):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.patient_number, u.name, p.ssn, p.birthdate, p.sex
            FROM patient p
            JOIN user u ON p.user_id = u.id
            WHERE u.name LIKE %s OR p.patient_number LIKE %s
            ORDER BY u.name
            LIMIT 20
        """, (f"%{query}%", f"%{query}%"))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to search patients: {e}")
    finally:
        conn.close()
