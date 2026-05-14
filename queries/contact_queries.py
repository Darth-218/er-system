"""
Contact inquiry management queries
Handles CRUD operations for contact form submissions
"""

import mysql.connector
from datetime import datetime
from db.connection import get_connection

class DatabaseError(Exception):
    """Custom exception for database errors"""
    pass

def add_contact_inquiry(name, email, phone, subject, message):
    """
    Insert a new contact inquiry
    
    Args:
        name (str): Contact person's name
        email (str): Email address
        phone (str): Phone number (optional)
        subject (str): Inquiry subject
        message (str): Inquiry message
    
    Returns:
        int: ID of the new inquiry, or None if failed
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        query = """
        INSERT INTO ContactInquiry (name, email, phone, subject, message, submitted_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'open')
        """
        cursor.execute(query, (name, email, phone, subject, message, datetime.now()))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error adding contact inquiry: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_contact_inquiries(status=None):
    """
    Get all contact inquiries, optionally filtered by status
    
    Args:
        status (str, optional): Filter by 'open' or 'resolved'
    
    Returns:
        list: List of inquiry dictionaries
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        if status:
            query = "SELECT * FROM ContactInquiry WHERE status = %s ORDER BY submitted_at DESC"
            cursor.execute(query, (status,))
        else:
            query = "SELECT * FROM ContactInquiry ORDER BY submitted_at DESC"
            cursor.execute(query)
        
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error fetching contact inquiries: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_inquiry_status(inquiry_id, status, admin_id):
    """
    Update inquiry status (open/resolved)
    
    Args:
        inquiry_id (int): Inquiry ID
        status (str): New status ('open' or 'resolved')
        admin_id (int): ID of admin making the change
    
    Returns:
        bool: True if successful, False otherwise
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        query = """
        UPDATE ContactInquiry 
        SET status = %s, resolved_by = %s, resolved_at = %s 
        WHERE inquiry_id = %s
        """
        cursor.execute(query, (status, admin_id, datetime.now(), inquiry_id))
        connection.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as e:
        print(f"Error updating inquiry status: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def count_inquiries_by_status():
    """
    Get count of inquiries grouped by status
    
    Returns:
        list: List of dictionaries with status and count
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
        SELECT status, COUNT(*) as count 
        FROM ContactInquiry 
        GROUP BY status
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error counting inquiries: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_contact_inquiry_by_id(inquiry_id):
    """
    Get a single inquiry by ID
    
    Args:
        inquiry_id (int): Inquiry ID
    
    Returns:
        dict: Inquiry data or None
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM ContactInquiry WHERE inquiry_id = %s"
        cursor.execute(query, (inquiry_id,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Error fetching inquiry: {e}")
        return None
    finally:
        cursor.close()
        connection.close()                                       