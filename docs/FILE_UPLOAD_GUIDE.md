# File Upload Guide

## Overview

Patient medical files (scans, X-rays, lab results, documents) are stored on disk with their metadata tracked in the database. Files are never served directly — access is always gated through Streamlit page auth checks.

## Storage Pattern

```
uploads/{patient_id}/{timestamp}_{original_filename}
```

- Root directory: `uploads/` (gitignored)
- Subdirectory per patient (using their patient ID)
- Filename prefixed with a timestamp to prevent collisions

## `save_file()`

**Input:**
- Uploaded file object (from `st.file_uploader`)
- Patient ID (int)

**Process:**
1. Create `uploads/{patient_id}/` directory if it doesn't exist
2. Write file to disk with a timestamp prefix
3. Insert a metadata record into the database (file_id, patient_id, original_name, stored_path, uploaded_at, file_type, file_size)

**Output:** The stored file path (string). Returns `None` on failure.

## `get_file_path()`

**Input:**
- Patient ID (int)
- Filename or file_id (string or int)

**Output:** Absolute path to the file on disk (string), or `None` if not found.

## `list_patient_files()`

**Input:** Patient ID (int)

**Output:** List of dicts, each containing: `file_id`, `file_name`, `file_type`, `file_size`, `uploaded_at`, `stored_path`.

## `delete_file()`

**Input:** File ID (int)

**Process:** Deletes the file from disk and removes its metadata record from the database.

**Output:** Boolean — `True` if deleted, `False` if not found or error.

## Displaying Files

- **Images** (PNG, JPG, DICOM renders): Displayed via Streamlit's image component using the file path
- **PDFs** (reports, lab results): Offered as a download button
- **Other types** (DOCX, TXT): Offered as a download button with appropriate mime type

## Access Control

- Only authenticated users with the right role can access files
- Patients can only view their own files
- Doctors and nurses can view files of patients they treat
- Admins can view all files

## Accepted File Types

| Type | Extensions | Max Size |
|------|-----------|----------|
| Medical images | `.png`, `.jpg`, `.jpeg`, `.dcm` | 50 MB |
| Documents | `.pdf`, `.docx`, `.txt` | 25 MB |
| Lab results | `.pdf`, `.csv`, `.xlsx` | 25 MB |

Reject uploads that exceed size limits or use disallowed extensions, returning an error message to the user.
