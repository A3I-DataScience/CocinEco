import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table for storing users
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
"""
)

print("Database setup complete.")
conn.commit()
conn.close()


import bcrypt


def add_user(username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash)
    )
    conn.commit()
    conn.close()


add_user("antoine", "asdf1234")
add_user("maria", "password2025")
add_user("cocinecouser", "cocineco2025")
