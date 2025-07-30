import sqlite3


class DatabaseConnection:
    """
    A class-based context manager to handle opening and
    closing database connections automatically
    """

    def __init__(self, query):
        self.query = query

    def __enter__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query)
        return self.cursor  # return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()  # close the connection


with DatabaseConnection("SELECT * FROM users") as cursor:
    for row in cursor:
        print(row)
