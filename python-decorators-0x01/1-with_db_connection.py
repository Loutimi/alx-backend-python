import sqlite3 
import functools

# Decorator that opens a sqlite database connection, passes it to the function and closes it afterword"
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        class Connect:
            def __enter__(self):
                print("Opening connection...")
                self.conn = sqlite3.connect('users.db')
                return self.conn  

            def __exit__(self, exc_type, exc_val, exc_tb):
                print("Connection closed.")
                self.conn.close()
                

        with Connect() as conn:
            result = func(conn, *args, **kwargs)
            print(result)
            return result
    return wrapper


@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)