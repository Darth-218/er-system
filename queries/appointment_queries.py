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
        
        # use a simple variable to store id
        pid = patient['id']

        # Check for double-booking (Conflict Prevention)
        cursor.execute("""
            SELECT id FROM appointment 
            WHERE doctor_id = %s 
            AND appointment_datetime = %s 
            AND status = 'scheduled'
        """, (doctor_id, appointment_datetime))
        
        if cursor.fetchone():
            raise DatabaseError("The doctor is already booked for this time slot. Please choose another time.")

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
        # Fetch appointment details to check cancellation window
        cursor.execute("""
            SELECT id, appointment_datetime, payment_amount, payment_status
            FROM appointment WHERE id = %s AND status = 'scheduled'
        """, (appointment_id,))
        apt = cursor.fetchone()
        if not apt:
            raise DatabaseError("Appointment not found or already cancelled/completed")

        # Calculate time difference in hours
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        apt_time = apt['appointment_datetime']
        if apt_time.tzinfo is None:
            from datetime import timedelta
            apt_time = apt_time.replace(tzinfo=timezone.utc)
        hours_until_appointment = (apt_time - now).total_seconds() / 3600

        # Refund window: cancellation must be at least 2 hours before appointment
        refund_threshold = 2  # hours
        eligible_for_refund = hours_until_appointment >= refund_threshold

        # Update status to cancelled
        cursor.execute("""
            UPDATE appointment SET status = 'cancelled' WHERE id = %s AND status = 'scheduled'
        """, (appointment_id,))
        conn.commit()

        if cursor.rowcount > 0 and eligible_for_refund and apt['payment_amount']:
            # Process refund
            cursor.execute("""
                UPDATE appointment SET 
                    payment_status = 'refunded',
                    refund_amount = payment_amount
                WHERE id = %s
            """, (appointment_id,))
            conn.commit()
            return {"cancelled": True, "refunded": True, "amount": apt['payment_amount']}

        return {"cancelled": cursor.rowcount > 0, "refunded": False, "amount": 0}
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to cancel appointment: {e}")
    finally:
        conn.close()
