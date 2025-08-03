import sqlite3
from utils.db import get_db_connection
from utils.auth import hash_password

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    cursor.execute("DELETE FROM users")

    users = [
        ('John Doe', 'john@example.com', hash_password('password123')),
        ('Jane Smith', 'jane@example.com', hash_password('secret456')),
        ('Bob Johnson', 'bob@example.com', hash_password('qwerty789')),
    ]

    cursor.executemany("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", users)
    conn.commit()
    conn.close()
    print("Database initialized with hashed sample data")

if __name__ == '__main__':
    init_db()
