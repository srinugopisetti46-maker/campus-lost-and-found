import sqlite3

conn = sqlite3.connect("campus_lost_found.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE items ADD COLUMN contact TEXT")
    print("✅ Column 'contact' added successfully")
except Exception as e:
    print("⚠️ Already exists or error:", e)

conn.commit()
conn.close()