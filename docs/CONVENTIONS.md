# Project Conventions

## Naming

| Item | Convention | Example |
|------|-----------|---------|
| Python files | `snake_case` | `patient_queries.py` |
| Python functions | `snake_case` | `get_patient_by_id()` |
| Python variables | `snake_case` | `patient_name` |
| Python classes | `PascalCase` | `DatabaseError` |
| Streamlit pages | `NN_Name.py` | `10_Patient.py` |
| SQL keywords | `UPPER_CASE` | `SELECT`, `INSERT INTO` |
| SQL tables/columns | `snake_case` | `patient`, `first_name` |
| DB connection env vars | `UPPER_SNAKE` | `MYSQL_HOST`, `MYSQL_USER` |

## Streamlit Page Numbering

```
01_Home.py            — visitor / public
02_Login.py           — login page
10_Patient.py         — patient dashboard
20_Doctor.py          — doctor dashboard
30_Nurse.py           — nurse dashboard
40_Admin.py           — admin dashboard
```

Numbers group by role. Gaps allow inserting new pages later.

## Query Function Naming

| Prefix | SQL Operation | Example |
|--------|--------------|---------|
| `get_*` | SELECT (one or many) | `get_patient_by_id()` |
| `add_*` | INSERT | `add_appointment()` |
| `update_*` | UPDATE | `update_medical_status()` |
| `delete_*` | DELETE | `delete_prescription()` |
| `count_*` | SELECT COUNT | `count_patients_by_department()` |
| `search_*` | SELECT with filters | `search_doctors_by_specialty()` |
| `list_*` | SELECT multiple rows | `list_appointments_by_date()` |

## Import Order

```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party
import streamlit as st
import mysql.connector

# 3. Local modules
from db.connection import get_connection
from utils.auth import require_role
```

## Query Function Return Format

All query functions return a **list of dicts** where keys are column names:

```python
[
    {"id": 1, "first_name": "John", "last_name": "Doe"},
    {"id": 2, "first_name": "Jane", "last_name": "Smith"},
]
```

Single-row queries return `None` if no result found, or a single dict.
