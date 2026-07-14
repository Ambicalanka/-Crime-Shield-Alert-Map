import sqlite3

conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())
cursor.execute("PRAGMA table_info(zones);")
print("Zones table schema:")
for col in cursor.fetchall():
    print(col)
conn.close()