import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("campus_lost_found.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    details TEXT,
    place TEXT,
    status TEXT,
    contact TEXT
)""")

# Default admin
c.execute("DELETE FROM users WHERE role='admin'")
c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
          ("admin", generate_password_hash("admin123"), "admin"))

conn.commit()
conn.close()

print("Database Ready ✅")