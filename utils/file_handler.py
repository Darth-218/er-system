"""
File upload/download helper utilities
PLACEHOLDER — Member 5 will implement full file handling.
"""

import os

UPLOAD_DIR = "uploads"


def save_file(uploaded_file, patient_id):
    raise NotImplementedError("Member 5: implement file saving")


def get_file_path(patient_id, filename_or_id):
    raise NotImplementedError("Member 5: implement file path retrieval")


def list_patient_files(patient_id):
    raise NotImplementedError("Member 5: implement file listing")


def delete_file(file_id):
    raise NotImplementedError("Member 5: implement file deletion")
