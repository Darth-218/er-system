"""
Report / Aggregation Queries
PLACEHOLDER — Member 5 will implement.
"""

from db.connection import get_connection, DatabaseError


from db.connection import get_connection, DatabaseError


def get_appointment_report(start_date, end_date, doctor_id=None):
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                d.id AS doctor_id,
                u.name AS doctor_name,
                COUNT(a.id) AS total_appointments,
                SUM(a.payment_amount) AS total_revenue
            FROM appointment a
            JOIN doctor d ON a.doctor_id = d.id
            JOIN user u ON d.user_id = u.id
            WHERE DATE(a.appointment_datetime)
                  BETWEEN %s AND %s
        """

        params = [start_date, end_date]

        if doctor_id:
            query += " AND d.id = %s"
            params.append(doctor_id)

        query += """
            GROUP BY d.id, u.name
            ORDER BY total_appointments DESC
        """

        cursor.execute(query, tuple(params))

        return cursor.fetchall()

    except Exception as e:
        raise DatabaseError(f"Failed to fetch appointment report: {e}")

    finally:
        conn.close()


def get_bed_utilization_report():
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                status,
                COUNT(*) AS total_beds
            FROM er_bed
            GROUP BY status
        """)

        return cursor.fetchall()

    except Exception as e:
        raise DatabaseError(f"Failed to fetch bed utilization report: {e}")

    finally:
        conn.close()


def get_esi_statistics():
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                esi_level,
                COUNT(*) AS total_patients
            FROM triage_record
            GROUP BY esi_level
            ORDER BY esi_level
        """)

        return cursor.fetchall()

    except Exception as e:
        raise DatabaseError(f"Failed to fetch ESI statistics: {e}")

    finally:
        conn.close()



def get_patient_admission_summary():
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.patient_number,
                u.name AS patient_name,
                p.admission_date,
                p.medical_history
            FROM patient p
            JOIN user u ON p.user_id = u.id
            ORDER BY p.admission_date DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        raise DatabaseError(f"Failed to fetch patient summary: {e}")

    finally:
        conn.close()



def get_dashboard_stats():
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        stats = {}

        cursor.execute("SELECT COUNT(*) AS total FROM patient")
        stats["patients"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM doctor")
        stats["doctors"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM appointment")
        stats["appointments"] = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM er_bed
            WHERE status = 'available'
        """)
        stats["available_beds"] = cursor.fetchone()["total"]

        return stats

    except Exception as e:
        raise DatabaseError(f"Failed to fetch dashboard stats: {e}")

    finally:
        conn.close()


def get_file_metadata_report():
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                f.id,
                u.name AS patient_name,
                f.original_name,
                f.file_type,
                f.file_size,
                f.uploaded_at
            FROM file_metadata f
            JOIN patient p ON f.patient_id = p.id
            JOIN user u ON p.user_id = u.id
            ORDER BY f.uploaded_at DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        raise DatabaseError(f"Failed to fetch file metadata report: {e}")

    finally:
        conn.close()