"""
Emergency Department Query Module — Member 3 / Phase 3

Triage, ER Bed Management, Waiting Room Queue, Geo-Location.
All queries use parameterized %s placeholders and return dicts.
"""

from db.connection import get_connection, DatabaseError


# =============================================================
# TRIAGE SYSTEM
# =============================================================

def add_triage_record(patient_id, nurse_id, esi_level, chief_complaint=None,
                      blood_pressure=None, heart_rate=None, temperature=None):
    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            INSERT INTO triage_record
                (patient_id, nurse_id, esi_level, chief_complaint,
                 blood_pressure, heart_rate, temperature)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (patient_id, nurse_id, esi_level, chief_complaint,
              blood_pressure, heart_rate, temperature))
        triage_id = cursor.lastrowid

        cursor.execute("""
            SELECT COALESCE(MAX(queue_position), 0) + 1 AS next_pos
            FROM waiting_room
            WHERE status = 'waiting'
        """)
        next_pos = cursor.fetchone()["next_pos"]

        est_wait = _estimate_wait(esi_level)

        cursor.execute("""
            INSERT INTO waiting_room
                (patient_id, triage_id, queue_position, estimated_wait_minutes)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, triage_id, next_pos, est_wait))

        conn.commit()
        return triage_id
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to add triage record: {e}")
    finally:
        conn.close()


def _estimate_wait(esi_level):
    mapping = {1: 0, 2: 5, 3: 15, 4: 30, 5: 60}
    return mapping.get(esi_level, 30)


def get_triage_records(patient_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, u.name AS nurse_name
            FROM triage_record t
            JOIN user u ON t.nurse_id = u.id
            WHERE t.patient_id = %s
            ORDER BY t.created_at DESC
        """, (patient_id,))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch triage records: {e}")
    finally:
        conn.close()


def list_triage_queue():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id, t.patient_id, p.patient_number, u.name AS patient_name,
                   t.esi_level, t.arrival_time, t.chief_complaint,
                   t.blood_pressure, t.heart_rate, t.temperature
            FROM triage_record t
            JOIN patient p ON t.patient_id = p.id
            JOIN user u ON p.user_id = u.id
            WHERE t.id NOT IN (
                SELECT wr.triage_id FROM waiting_room wr WHERE wr.status = 'left'
            )
            ORDER BY t.esi_level ASC, t.arrival_time ASC
        """)
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to list triage queue: {e}")
    finally:
        conn.close()


# =============================================================
# ER BED MANAGEMENT
# =============================================================

def add_er_bed(department_id, bed_number):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO er_bed (department_id, bed_number)
            VALUES (%s, %s)
        """, (department_id, bed_number))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to add ER bed: {e}")
    finally:
        conn.close()


def list_er_beds(department_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        if department_id:
            cursor.execute("""
                SELECT b.*, u.name AS patient_name
                FROM er_bed b
                LEFT JOIN patient p ON b.patient_id = p.id
                LEFT JOIN user u ON p.user_id = u.id
                WHERE b.department_id = %s
                ORDER BY b.bed_number
            """, (department_id,))
        else:
            cursor.execute("""
                SELECT b.*, u.name AS patient_name, d.name AS department_name
                FROM er_bed b
                LEFT JOIN patient p ON b.patient_id = p.id
                LEFT JOIN user u ON p.user_id = u.id
                LEFT JOIN department d ON b.department_id = d.id
                ORDER BY b.department_id, b.bed_number
            """)
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to list ER beds: {e}")
    finally:
        conn.close()


def list_available_beds(department_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        if department_id:
            cursor.execute("""
                SELECT * FROM er_bed
                WHERE status = 'available' AND department_id = %s
                ORDER BY bed_number
            """, (department_id,))
        else:
            cursor.execute("""
                SELECT * FROM er_bed
                WHERE status = 'available'
                ORDER BY department_id, bed_number
            """)
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to list available beds: {e}")
    finally:
        conn.close()


def assign_bed(bed_id, patient_id):
    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            UPDATE er_bed
            SET status = 'occupied', patient_id = %s, assigned_at = NOW()
            WHERE bed_id = %s AND status = 'available'
        """, (patient_id, bed_id))
        if cursor.rowcount == 0:
            conn.rollback()
            return False

        cursor.execute("""
            INSERT INTO er_bed_history (bed_id, patient_id, assigned_at)
            VALUES (%s, %s, NOW())
        """, (bed_id, patient_id))

        cursor.execute("""
            UPDATE waiting_room
            SET status = 'in-progress'
            WHERE patient_id = %s AND status = 'waiting'
        """, (patient_id,))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to assign bed: {e}")
    finally:
        conn.close()


def release_bed(bed_id):
    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT patient_id FROM er_bed WHERE bed_id = %s", (bed_id,))
        bed = cursor.fetchone()
        if not bed or not bed["patient_id"]:
            conn.rollback()
            return False

        patient_id = bed["patient_id"]

        cursor.execute("""
            UPDATE er_bed
            SET status = 'cleaning', patient_id = NULL, assigned_at = NULL
            WHERE bed_id = %s
        """, (bed_id,))

        cursor.execute("""
            UPDATE er_bed_history
            SET released_at = NOW()
            WHERE bed_id = %s AND released_at IS NULL
        """, (bed_id,))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to release bed: {e}")
    finally:
        conn.close()


def complete_cleaning(bed_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE er_bed SET status = 'available' WHERE bed_id = %s AND status = 'cleaning'
        """, (bed_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to complete cleaning: {e}")
    finally:
        conn.close()


def get_bed_history(bed_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT h.*, u.name AS patient_name
            FROM er_bed_history h
            LEFT JOIN patient p ON h.patient_id = p.id
            LEFT JOIN user u ON p.user_id = u.id
            WHERE h.bed_id = %s
            ORDER BY h.assigned_at DESC
        """, (bed_id,))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch bed history: {e}")
    finally:
        conn.close()


def get_bed_stats(department_id=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        if department_id:
            cursor.execute("""
                SELECT status, COUNT(*) AS count
                FROM er_bed
                WHERE department_id = %s
                GROUP BY status
            """, (department_id,))
        else:
            cursor.execute("""
                SELECT status, COUNT(*) AS count
                FROM er_bed
                GROUP BY status
            """)
        rows = cursor.fetchall()
        stats = {"available": 0, "occupied": 0, "cleaning": 0}
        for row in rows:
            stats[row["status"]] = row["count"]
        return stats
    except Exception as e:
        raise DatabaseError(f"Failed to get bed stats: {e}")
    finally:
        conn.close()


# =============================================================
# WAITING ROOM QUEUE
# =============================================================

def get_waiting_queue():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT wr.id, wr.patient_id, wr.triage_id,
                   wr.queue_position, wr.estimated_wait_minutes,
                   wr.entered_at, wr.status,
                   p.patient_number, u.name AS patient_name,
                   t.esi_level, t.chief_complaint,
                   t.blood_pressure, t.heart_rate, t.temperature
            FROM waiting_room wr
            JOIN patient p ON wr.patient_id = p.id
            JOIN user u ON p.user_id = u.id
            JOIN triage_record t ON wr.triage_id = t.id
            WHERE wr.status = 'waiting'
            ORDER BY t.esi_level ASC, wr.entered_at ASC
        """)
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to fetch waiting queue: {e}")
    finally:
        conn.close()


def count_waiting_patients():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(*) AS count FROM waiting_room WHERE status = 'waiting'
        """)
        return cursor.fetchone()["count"]
    except Exception as e:
        raise DatabaseError(f"Failed to count waiting patients: {e}")
    finally:
        conn.close()


def remove_from_waiting(patient_id, new_status="left"):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE waiting_room
            SET status = %s
            WHERE patient_id = %s AND status = 'waiting'
        """, (new_status, patient_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to update waiting room status: {e}")
    finally:
        conn.close()


# =============================================================
# GEO-LOCATION / SPATIAL QUERIES
# =============================================================

def find_nearest_hospitals(latitude, longitude, radius_meters=5000):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, address, latitude, longitude,
                   ST_Distance_Sphere(
                       POINT(%s, %s),
                       POINT(longitude, latitude)
                   ) AS distance_meters
            FROM hospital_location
            HAVING distance_meters <= %s
            ORDER BY distance_meters ASC
        """, (longitude, latitude, radius_meters))
        return cursor.fetchall()
    except Exception as e:
        raise DatabaseError(f"Failed to find nearest hospitals: {e}")
    finally:
        conn.close()


def update_patient_location(patient_id, latitude, longitude):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE patient SET latitude = %s, longitude = %s WHERE id = %s
        """, (latitude, longitude, patient_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Failed to update patient location: {e}")
    finally:
        conn.close()


def search_patients_by_name(query):
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
