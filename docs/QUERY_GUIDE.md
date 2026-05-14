# Query Guide

## Database Connection

Import `get_connection` from `db.connection`. Each query function must:
- Open a connection via `get_connection()`
- Use parameterized queries (`%s` placeholders) — never string formatting or f-strings
- Close the connection in a `finally` block

**Input:** Connection params read from environment variables (`MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`).  
**Output:** A connection object used to create cursors.

## Parameterized Queries

All SQL must use `%s` placeholders. Arguments passed as a tuple to `cursor.execute()`.

```
cursor.execute("SELECT * FROM patient WHERE id = %s", (patient_id,))
cursor.execute("SELECT * FROM appointment WHERE doctor_id = %s AND status = %s", (doctor_id, status))
```

## Return Format

| Query type | Return |
|-----------|--------|
| Single row SELECT | `dict` or `None` if not found |
| Multi-row SELECT | `list[dict]` (empty list if none) |
| INSERT | `int` (lastrowid) |
| UPDATE/DELETE | `int` (rows affected) |
| COUNT/AGG | single value or `dict` with result |

All dict keys match the column names in snake_case.

## Transactions

Group multiple writes (INSERT/UPDATE/DELETE) in a transaction so they commit or rollback together. Pattern:
1. `conn.start_transaction()` before any writes
2. Execute all statements
3. `conn.commit()` on success
4. `conn.rollback()` on any exception

Used for: payment + appointment creation, cancellation + refund, prescription + medication tracking.

## Error Handling

Define a custom `DatabaseError` exception. Every query function wraps database calls in try/except, catching `mysql.connector.Error` and raising `DatabaseError` with a descriptive message.

## Query Module Pattern

Each file in `queries/`:
- Has one domain focus (patients, doctors, appointments, etc.)
- Contains only functions — no Streamlit imports, no UI logic
- Every function follows: connect → execute → return → close

## Spatial Queries (Geo-location)

Use MySQL `ST_Distance_Sphere(POINT(lng1, lat1), POINT(lng2, lat2))` for distance calculations. Input: latitude/longitude floats. Output: list of nearby locations with distance in meters, ordered by proximity.

## Date Filtering

Functions that filter by date range accept `start_date` and `end_date` as strings in `YYYY-MM-DD` format, and use `BETWEEN %s AND %s` in the WHERE clause.

## Query Module Assignments

| Module | Key inputs | Key outputs |
|--------|-----------|-------------|
| `auth_queries.py` | email, password, role | user dict, login success bool, new user id |
| `patient_queries.py` | patient fields, patient_id | patient dict/list, insert id, update count |
| `doctor_queries.py` | doctor fields, department_id | doctor dict/list, hours tracked |
| `appointment_queries.py` | patient_id, doctor_id, date, amount | appointment dict, insert id, cancel/refund status |
| `prescription_queries.py` | patient_id, doctor_id, medication fields | prescription dict, insert id |
| `emergency_queries.py` | triage fields, bed_id, lat/lng | triage record, bed status, queue position, nearest locations |
| `contact_queries.py` | name, email, subject, message | inquiry id, submission status |
| `report_queries.py` | date range, doctor_id, department_id | aggregated dicts/lists with counts and sums |
