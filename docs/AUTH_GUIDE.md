# Authentication Guide

## Session Keys

`st.session_state` stores the following keys after a successful login:

| Key | Type | Contents |
|-----|------|----------|
| `logged_in` | bool | True if authenticated |
| `user_id` | int | Primary key from the user table |
| `role` | str | One of: `visitor`, `patient`, `nurse`, `doctor`, `admin` |
| `name` | str | Display name of the authenticated user |

## Roles

Five roles with hierarchical access. Higher roles inherit access from lower roles:

| Role | Level | Can access |
|------|-------|-----------|
| `visitor` | 0 | Home page only |
| `patient` | 1 | Own dashboard, appointments, prescriptions |
| `nurse` | 2 | Patient intake, triage, bed management |
| `doctor` | 3 | Patient treatment, prescriptions, schedules |
| `admin` | 4 | All data, reports, user management, contact inbox |

## `require_role()`

**Input:** a role string (e.g. `"patient"`).  
**Behavior:** Checks `st.session_state.role` against the required level. If insufficient, shows a warning and stops the page render.  
**Placement:** Called at the top of each page, after `st.set_page_config()`.

## `login()`

**Input:** email (string), password (string).  
**Process:** Queries `auth_queries.authenticate_user()` which validates credentials against the database.  
**Output:** Returns `True` on success (and populates all session keys), `False` on failure.

## `logout()`

**Input:** None.  
**Behavior:** Clears all session auth keys. Calls `st.rerun()` to redirect to the home page.  
**Placement:** Called from a "Logout" button in the sidebar or page footer.

## Registration

- New patients can self-register through a public form on the home/login page
- New doctors, nurses, and admins are created through the admin dashboard
- Registration inserts into both the `user` table (credentials + role) and the role-specific profile table (patient info, doctor info, etc.)
- Password is hashed before storage — never stored in plain text

## Page Guard Rules

| File | Guard | Exception |
|------|-------|-----------|
| `01_Home.py` | None | Public access |
| `02_Login.py` | Redirect if `logged_in` | Already authenticated users skip to dashboard |
| `10_Patient.py` | `require_role("patient")` | — |
| `20_Doctor.py` | `require_role("doctor")` | — |
| `30_Nurse.py` | `require_role("nurse")` | — |
| `40_Admin.py` | `require_role("admin")` | — |
