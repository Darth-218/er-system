# Streamlit Page Guide

## Page Structure

Every page file follows the same structure:

1. **Docstring** — file purpose
2. **Imports** — standard lib → third-party → local modules
3. **`st.set_page_config()`** — page title and layout
4. **Auth guard** — `require_role()` call to restrict access
5. **Page content** — title, filters, data display, forms
6. **Event handlers** — form submissions, button clicks (before render or inline)

## Auth Guard

Every page except the home page must restrict access by role:

| Page | Guard | Redirects if… |
|------|-------|---------------|
| `01_Home.py` | None (public) | — |
| `02_Login.py` | Redirect if already logged in | Already authenticated |
| `10_Patient.py` | `require_role("patient")` | Role < patient |
| `20_Doctor.py` | `require_role("doctor")` | Role < doctor |
| `30_Nurse.py` | `require_role("nurse")` | Role < nurse |
| `40_Admin.py` | `require_role("admin")` | Role < admin |

## Layout Template

- **Title** at the top via `st.title()` or `st.header()`
- **Sidebar filters** (date ranges, dropdowns, checkboxes) grouped with `st.sidebar`
- **Main content** in columns or full-width
- **Metrics** via `st.metric()` for key numbers
- **Tables** via `st.dataframe()` for interactive or `st.table()` for static
- **Charts** via `st.bar_chart()`, `st.line_chart()`, or Altair for complex visualizations

## Forms

- Wrap input fields in `st.form()` with a unique key
- Include one `st.form_submit_button()` per form
- On submit: call the appropriate query function, show success/error feedback via `st.success()` or `st.error()`, then `st.rerun()` to refresh

## Display States

Every data display should handle three states:

| State | What to show |
|-------|-------------|
| **Loading** | `st.spinner()` while fetching data |
| **Empty** | `st.info()` message when no results |
| **Error** | `st.error()` with the DatabaseError message, `st.stop()` |

## File Display

- Images (X-rays, scans): `st.image()` with the file path
- PDFs/Reports: `st.download_button()` with the file contents as bytes
- File list: `st.dataframe()` showing metadata (filename, date, type)

## Navigation

- Use `st.switch_page("pages/NN_Name.py")` to programmatically redirect
- Use `st.page_link()` for clickable links between pages
- `app.py` acts as the entry point and routes logged-in users to their role page

## Page Assignments

| Page | Owner | Content |
|------|-------|---------|
| `01_Home.py` | Member 2 | Hospital info, visitor content, contact form |
| `02_Login.py` | Member 2 | Email/password login, link to visitor home |
| `10_Patient.py` | Member 2 | Profile, appointments list, prescriptions, medical history, uploaded scans |
| `20_Doctor.py` | Member 3+4 | Schedule, patient list, write prescriptions, room reservation, treatment hours |
| `30_Nurse.py` | Member 4 | Triage intake form, ER bed status board, waiting room queue |
| `40_Admin.py` | Member 5 | Reports, user management, contact inquiry inbox, statistics dashboard |
| `app.py` | Member 5 | Root entry point, auth-based role routing |
