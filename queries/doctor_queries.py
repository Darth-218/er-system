"""
Doctor CRUD Queries
"""

from db.connection import get_connection, DatabaseError


def get_doctor_by_id(doctor_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.id, d.user_id, d.ssn, d.sex, d.birthdate, 
                   d.major_scientific_area, d.degree, d.join_date, d.department_id,
                   u.name, u.email, u.role, u.created_at
            FROM doctor d
            JOIN user u ON d.user_id = u.id
            WHERE d.id = %s
        """, (doctor_id,))
        return cursor.fetchone()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctor: {e}")
    finally:
        conn.close()


def list_doctors(department_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT d.id, d.user_id, d.ssn, d.sex, d.birthdate, 
                   d.major_scientific_area, d.degree, d.join_date, d.department_id,
                   u.name, u.email, u.role, u.created_at,
                   dep.name AS department_name
            FROM doctor d
            JOIN user u ON d.user_id = u.id
            LEFT JOIN department dep ON d.department_id = dep.id
        """
        params = []
        
        if department_id:
            query += " WHERE d.department_id = %s"
            params.append(department_id)
            
        query += " ORDER BY u.name"
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctors: {e}")
    finally:
        conn.close()


def create_doctor(user_id, ssn, sex, birthdate, major_scientific_area, degree, join_date, department_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO doctor (user_id, ssn, sex, birthdate, major_scientific_area, degree, join_date, department_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, ssn, sex, birthdate, major_scientific_area, degree, join_date, department_id))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to create doctor: {e}")
    finally:
        conn.close()


def update_doctor(doctor_id, ssn=None, sex=None, birthdate=None, major_scientific_area=None, degree=None, join_date=None, department_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if ssn is not None:
            updates.append("ssn = %s")
            params.append(ssn)
        if sex is not None:
            updates.append("sex = %s")
            params.append(sex)
        if birthdate is not None:
            updates.append("birthdate = %s")
            params.append(birthdate)
        if major_scientific_area is not None:
            updates.append("major_scientific_area = %s")
            params.append(major_scientific_area)
        if degree is not None:
            updates.append("degree = %s")
            params.append(degree)
        if join_date is not None:
            updates.append("join_date = %s")
            params.append(join_date)
        if department_id is not None:
            updates.append("department_id = %s")
            params.append(department_id)
        
        if not updates:
            return False
            
        query = f"UPDATE doctor SET {', '.join(updates)} WHERE id = %s"
        params.append(doctor_id)
        
        cursor.execute(query, tuple(params))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to update doctor: {e}")
    finally:
        conn.close()


def delete_doctor(doctor_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctor WHERE id = %s", (doctor_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to delete doctor: {e}")
    finally:
        conn.close()


def get_doctor_by_user_id(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.id, d.user_id, d.ssn, d.sex, d.birthdate, 
                   d.major_scientific_area, d.degree, d.join_date, d.department_id,
                   u.name, u.email, u.role, u.created_at
            FROM doctor d
            JOIN user u ON d.user_id = u.id
            WHERE d.user_id = %s
        """, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctor by user ID: {e}")
    finally:
        conn.close()


def get_doctor_appointments(doctor_id, start_date=None, end_date=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT a.id, a.patient_id, a.doctor_id, a.appointment_datetime,
                   a.duration_minutes, a.status, a.payment_amount, a.notes,
                   p.patient_number, u.name AS patient_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN user u ON p.user_id = u.id
            WHERE a.doctor_id = %s
        """
        params = [doctor_id]
        
        if start_date and end_date:
            query += " AND DATE(a.appointment_datetime) BETWEEN %s AND %s"
            params.extend([start_date, end_date])
        elif start_date:
            query += " AND DATE(a.appointment_datetime) >= %s"
            params.append(start_date)
        elif end_date:
            query += " AND DATE(a.appointment_datetime) <= %s"
            params.append(end_date)
            
        query += " ORDER BY a.appointment_datetime"
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctor appointments: {e}")
    finally:
        conn.close()


def get_doctor_schedule(doctor_id, date=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT a.id, a.patient_id, a.appointment_datetime, a.duration_minutes,
                   a.status, a.notes, p.patient_number, u.name AS patient_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN user u ON p.user_id = u.id
            WHERE a.doctor_id = %s
        """
        params = [doctor_id]
        
        if date:
            query += " AND DATE(a.appointment_datetime) = %s"
            params.append(date)
            
        query += " ORDER BY a.appointment_datetime"
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctor schedule: {e}")
    finally:
        conn.close()


def get_doctor_treatment_hours(doctor_id, start_date=None, end_date=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                DATE(a.appointment_datetime) AS treatment_date,
                COUNT(*) AS appointment_count,
                SUM(a.duration_minutes) AS total_minutes,
                SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
                SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count
            FROM appointment a
            WHERE a.doctor_id = %s
        """
        params = [doctor_id]
        
        if start_date and end_date:
            query += " AND DATE(a.appointment_datetime) BETWEEN %s AND %s"
            params.extend([start_date, end_date])
        elif start_date:
            query += " AND DATE(a.appointment_datetime) >= %s"
            params.append(start_date)
        elif end_date:
            query += " AND DATE(a.appointment_datetime) <= %s"
            params.append(end_date)
            
        query += " GROUP BY DATE(a.appointment_datetime) ORDER BY treatment_date DESC"
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctor treatment hours: {e}")
    finally:
        conn.close()


def get_doctor_prescriptions(doctor_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.patient_id, p.doctor_id, p.medication_name,
                   p.dosage, p.frequency, p.duration, p.instructions,
                   p.prescribed_date, p.refills_remaining,
                   pat.patient_number, u.name AS patient_name
            FROM prescription p
            JOIN patient pat ON p.patient_id = pat.id
            JOIN user u ON pat.user_id = u.id
            WHERE p.doctor_id = %s
            ORDER BY p.prescribed_date DESC
        """, (doctor_id,))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch doctor prescriptions: {e}")
    finally:
        conn.close()
