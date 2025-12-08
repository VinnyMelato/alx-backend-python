import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query (supports keyword or positional argument)
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database using the provided SQL query."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
users = fetch_all_users(query="SELECT * FROM users")
