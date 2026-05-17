"""
Migration script — Member 2 changes
Adds new columns and updates password hashes for an existing database.
Safe to run multiple times (idempotent).

Usage:
    python db/migration_member2.py
"""

import os
import mysql.connector
from mysql.connector import Error

DB_NAME = os.getenv("MYSQL_DATABASE", "his_emergency")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "")

PASSWORD_HASHES = {
    "admin@his.com":   "$2b$12$Z68Vv4.sqa0bDUgMMbYmMexewtNT/YfhZUcUOQsJdl2A0./PBKhHq",
    "doctor@his.com":  "$2b$12$MqbWsFFtGoSO/TvseO6qEuPUfe0ADyjEbSvtzUtZFfrKxFEAgzxYW",
    "nurse@his.com":   "$2b$12$ybdDf0/BHuoWqFxRq8vfae2RiOnQtmt0JRYbzgujezfnm/lD0pCUe",
    "patient@his.com": "$2b$12$qr7kj39YzXd0gjoK1T8NDeb8CeVCuh1KnYlMrLziz4E/lSCFLoqhG",
}


def run():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conn.cursor()
    except Error as e:
        print(f"Failed to connect to database '{DB_NAME}': {e}")
        return

    try:
        cursor.execute("ALTER TABLE patient ADD COLUMN spo2 TINYINT AFTER temperature")
        print("  Added `spo2` column to `patient` table")
    except Error as e:
        if "Duplicate column" in str(e):
            print("  `spo2` column already exists — skipping")
        else:
            print(f"  Failed to add `spo2`: {e}")

    try:
        cursor.execute("ALTER TABLE appointment ADD COLUMN symptoms TEXT AFTER payment_status")
        print("  Added `symptoms` column to `appointment` table")
    except Error as e:
        if "Duplicate column" in str(e):
            print("  `symptoms` column already exists — skipping")
        else:
            print(f"  Failed to add `symptoms`: {e}")

    for email, hashed in PASSWORD_HASHES.items():
        try:
            cursor.execute(
                "UPDATE user SET password_hash = %s WHERE email = %s",
                (hashed, email),
            )
            if cursor.rowcount > 0:
                print(f"  Updated password for {email}")
            else:
                print(f"  No user found for {email} — skipping")
        except Error as e:
            print(f"  Failed to update {email}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    run()
