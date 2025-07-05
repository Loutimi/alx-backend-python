import os
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Stream user data using a generator in batches"""

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
            batch = cursor.fetchall()

            if not batch:
                break

            yield batch
            offset += batch_size

    except Error as e:
        print(f"Database error: {e}")
        raise

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size, min_age=25):
    """
    Process users in batches, filtering by age.

    Args:
        batch_size (int): Number of users to process per batch.
        min_age (int): Minimum age filter (default: 25).

    Yields:
        list: Filtered users from each batch.
    """
    try:
        for batch in stream_users_in_batches(batch_size):
            try:
                filtered = [
                    user for user in batch
                    if isinstance(user.get("age"), (int, float)) and user["age"] > min_age
                ]
                if filtered:
                    yield filtered
            except Exception as inner:
                print(f"Error processing batch: {inner}")
                continue

    except Exception as e:
        print(f"Error in batch processing: {e}")
        raise
