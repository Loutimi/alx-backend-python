"""
Set up the MySQL database, ALX_prodev with the table user_data with the following fields:
user_id(Primary Key, UUID, Indexed)
name (VARCHAR, NOT NULL)
email (VARCHAR, NOT NULL)
age (DECIMAL,NOT NULL)
"""

import os
import csv
import uuid
import mysql.connector
from mysql.connector import Error


def connect_db():
    """Connects to the MySQL database server."""

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )

        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it doesn't already exist"""

    try:
        my_cursor = connection.cursor()
        my_cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev checked/created")
    except Error as e:
        print(f"Error occured creating database: {e}")
    finally:
        if my_cursor:
            my_cursor.close()


def connect_to_prodev():
    """Connects directly to the ALX_prodev database"""

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ["DB_USER"],
            database="ALX_prodev",
            password=os.environ["DB_PASSWORD"],
        )

        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """Creates user_data table in the ALX_prodev database"""
    try:
        my_cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data(
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        my_cursor.execute(create_table_query)
        print("Table user_data checked/created")

    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if my_cursor:
            my_cursor.close()


def insert_data(connection, data):
    """Inserts data into the user_data table if it doesn't already exist"""

    try:
        with connection.cursor() as cursor:
            # Check if user already exists (by email or user_id)
            check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
            cursor.execute(check_query, (data["email"],))

            if cursor.fetchone()[0] > 0:
                print(
                    f"User with email {data['email']} already exists. Skipping insertion."
                )
                return False

            # Insert new user if doesn't exist
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (data["user_id"], data["name"], data["email"], data["age"]),
            )
            connection.commit()
            print(f"User {data['name']} inserted successfully")
            return True

    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        return False


def load_csv_to_database(csv_file_path, connection):
    """Load CSV data into user_data table"""

    inserted = 0
    skipped = 0
    errors = 0

    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, 1):
                try:
                    # Prepare data
                    data = {
                        "user_id": str(uuid.uuid4()),
                        "name": row["name"].strip(),
                        "email": row["email"].strip().lower(),
                        "age": int(row["age"]),
                    }

                    # Basic validation
                    if not data["name"] or not data["email"] or data["age"] <= 0:
                        print(f"Row {row_num}: Invalid data, skipping")
                        skipped += 1
                        continue

                    # Insert data
                    if insert_data(connection, data):
                        inserted += 1
                        print(f"✓ Inserted: {data['name']}")
                    else:
                        skipped += 1
                        print(f"- Skipped: {data['name']} (already exists)")

                except (ValueError, KeyError) as e:
                    print(f"Row {row_num}: Error - {e}")
                    errors += 1

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Summary
    print(f"\n--- Summary ---")
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")


# Usage
if __name__ == "__main__":
    # Connect to database
    conn = connect_to_prodev()
    if conn:
        # Load CSV data
        load_csv_to_database("user_data.csv", conn)
        conn.close()
    else:
        print("Failed to connect to database")
