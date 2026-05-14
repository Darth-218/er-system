"""
File upload and management utilities
Handles saving, retrieving, and deleting patient medical files
"""

import os
from pathlib import Path
from datetime import datetime
import streamlit as st
from db.connection import get_connection

UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.dcm', '.docx', '.txt', '.csv', '.xlsx'}

class FileError(Exception):
    """Custom exception for file operations"""
    pass

def init_upload_dir():
    """Initialize upload directory if it doesn't exist"""
    UPLOAD_DIR.mkdir(exist_ok=True)

def validate_file(uploaded_file):
    """
    Validate file type and size
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error(f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)} MB")
        return False
    
    # Check file extension
    file_extension = Path(uploaded_file.name).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        st.error(f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")
        return False
    
    return True

def save_file(patient_id, uploaded_file, description=""):
    """
    Save uploaded file to disk and record metadata in database
    
    Args:
        patient_id (int): Patient ID
        uploaded_file: Streamlit uploaded file object
        description (str): File description
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not validate_file(uploaded_file):
        return False
    
    init_upload_dir()
    
    # Create patient subdirectory
    patient_dir = UPLOAD_DIR / str(patient_id)
    patient_dir.mkdir(exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = uploaded_file.name
    safe_name = f"{timestamp}_{original_name}"
    file_path = patient_dir / safe_name
    
    try:
        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Save metadata to database
        connection = get_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO PatientFile (patient_id, file_name, file_path, file_size, description, upload_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            patient_id, original_name, str(file_path), 
            uploaded_file.size, description, datetime.now()
        ))
        connection.commit()
        
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        # Clean up file if database insert failed
        if file_path.exists():
            file_path.unlink()
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def get_file_path(patient_id, file_name):
    """
    Get absolute path to a file
    
    Args:
        patient_id (int): Patient ID
        file_name (str): Name of the file
    
    Returns:
        Path: File path or None if not found
    """
    patient_dir = UPLOAD_DIR / str(patient_id)
    file_path = patient_dir / file_name
    
    if file_path.exists():
        return file_path
    return None

def list_patient_files(patient_id):
    """
    Get list of all files for a patient
    
    Args:
        patient_id (int): Patient ID
    
    Returns:
        list: List of file dictionaries
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
        SELECT * FROM PatientFile 
        WHERE patient_id = %s 
        ORDER BY upload_date DESC
        """
        cursor.execute(query, (patient_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error listing files: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def delete_file(file_id):
    """
    Delete a file from disk and database
    
    Args:
        file_id (int): File ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get file info first
        cursor.execute("SELECT * FROM PatientFile WHERE file_id = %s", (file_id,))
        file_info = cursor.fetchone()
        
        if not file_info:
            return False
        
        # Delete from disk
        file_path = Path(file_info['file_path'])
        if file_path.exists():
            file_path.unlink()
        
        # Delete from database
        cursor.execute("DELETE FROM PatientFile WHERE file_id = %s", (file_id,))
        connection.commit()
        
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False
    finally:
        cursor.close()
        connection.close()