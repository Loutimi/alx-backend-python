import os
import mysql.connector
from mysql.connector import Error


def stream_users():
    """Stream user data as dictionaries for easier access"""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev",
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        for row in cursor:
            yield row

    except Error as e:
        print(f"Database error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
