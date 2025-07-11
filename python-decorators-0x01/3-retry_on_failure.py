import time
import sqlite3 
import functools

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


def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function if it raises an exception.
    :param retries: Number of times to retry
    :param delay: Delay between retries in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        print(f"Operation failed after {retries} attempts.")
                        raise
                    print(f"Retrying after error: {e}. Attempt {attempt}/{retries}")
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)