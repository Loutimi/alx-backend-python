import sqlite3
import functools
from datetime import datetime  

# Decorator to log SQL queries with timestamps
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log = f"{datetime.now()} — Calling {func.__name__} with args: {args}, kwargs: {kwargs}\n"
        log += "Query is logged in\n\n"  
        print(log)
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")