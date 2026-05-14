import os
import mysql.connector
from mysql.connector import Error as MySQLError


class DatabaseError(Exception):
    pass


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "his_emergency"),
        )
        return conn
    except MySQLError as e:
        raise DatabaseError(f"Failed to connect to database: {e}")
