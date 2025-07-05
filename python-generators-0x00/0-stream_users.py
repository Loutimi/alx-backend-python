import os
import mysql.connector
from mysql.connector import Error


def stream_users():
    """Stream user data as dictionaries for easier access"""
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ["DB_USER"],
            database="ALX_prodev",
            password=os.environ["DB_PASSWORD"]
        )
        
        with connection.cursor(dictionary=True) as cursor:
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
        if 'connection' in locals() and connection.is_connected():
            connection.close()
