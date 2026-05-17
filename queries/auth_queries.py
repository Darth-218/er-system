"""
Authentication Queries
"""

import bcrypt
from db.connection import get_connection, DatabaseError


def authenticate_user(email, password):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, email, password_hash, role, name FROM user WHERE email = %s
        """, (email,))
        user = cursor.fetchone()
        if not user:
            return None
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return {
                'user_id': user['id'],
                'role': user['role'],
                'name': user['name'],
            }
        return None
    except Exception as e:
        raise DatabaseError(f"Authentication failed: {e}")
    finally:
        conn.close()


def register_user(name, email, password, role, profile_data=None):
    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("""
            INSERT INTO user (email, password_hash, role, name)
            VALUES (%s, %s, %s, %s)
        """, (email, hashed.decode('utf-8'), role, name))
        user_id = cursor.lastrowid

        if role == 'patient' and profile_data:
            cursor.execute("""
                INSERT INTO patient (user_id, patient_number, ssn, address, phone, birthdate, sex, medical_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                profile_data.get('patient_number'),
                profile_data.get('ssn'),
                profile_data.get('address'),
                profile_data.get('phone'),
                profile_data.get('birthdate'),
                profile_data.get('sex'),
                profile_data.get('medical_history'),
            ))

        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        raise DatabaseError(f"Registration failed: {e}")
    finally:
        conn.close()
