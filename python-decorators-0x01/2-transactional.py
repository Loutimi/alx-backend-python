import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        class Connect:
            def __enter__(self):
                print("Opening connection...")
                self.conn = sqlite3.connect("users.db")
                return self.conn

            def __exit__(self, exc_type, exc_val, exc_tb):
                print("Connection closed.")
                self.conn.close()

        with Connect() as conn:
            result = func(conn, *args, **kwargs)
            print(result)
            return result

    return wrapper


def transactional(func):
    """
    Decorator to manage database transactions.
    Commits changes if the function executes successfully, otherwise rolls back.
    """

    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the wrapped function
            result = func(conn, *args, **kwargs)
            # Commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # Rollback on error
            conn.rollback()
            raise e

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update the email address of a user in the database.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
print("Email updated successfully.")
