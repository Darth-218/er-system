import os
import mysql.connector
from mysql.connector import Error


DB_NAME = os.getenv("MYSQL_DATABASE", "his_emergency")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
SEED_PATH = os.path.join(os.path.dirname(__file__), "seed.sql")


def run_sql_file(cursor, filepath, label):
    with open(filepath, "r") as f:
        statements = f.read().split(";")
    for stmt in statements:
        stripped = stmt.strip()
        if stripped:
            try:
                cursor.execute(stripped)
            except Error as e:
                print(f"[{label}] Skipped statement (likely already exists): {e}")


def main():
    # Connect without database first to create it
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
    except Error as e:
        print(f"Failed to create database: {e}")
        return

    # Run schema
    run_sql_file(cursor, SCHEMA_PATH, "SCHEMA")
    conn.commit()

    # Run seed data
    run_sql_file(cursor, SEED_PATH, "SEED")
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Database '{DB_NAME}' setup complete.")


if __name__ == "__main__":
    main()
