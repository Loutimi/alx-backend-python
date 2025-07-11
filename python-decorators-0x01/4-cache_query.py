import time
import sqlite3 
import functools
from . import with_db_connection



query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        else:
            print(f"Cache miss for query: {query}. Executing query.")
            result = func(query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@cache_query
@with_db_connection
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
