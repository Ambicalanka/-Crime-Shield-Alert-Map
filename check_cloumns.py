import sqlite3

conn = sqlite3.connect("crime_data.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(zones)")
for col in cur.fetchall():
    print(col)

conn.close()
