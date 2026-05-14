"""
Appointment CRUD Queries
PLACEHOLDER — Member 2 will implement.
"""

from db.connection import get_connection, DatabaseError


def schedule_appointment(patient_id, doctor_id, appointment_datetime):
    raise NotImplementedError("Member 2: implement appointment scheduling")


def cancel_appointment(appointment_id):
    raise NotImplementedError("Member 2: implement appointment cancellation")
