import sqlite3
conn = sqlite3.connect('crime_data.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables:", tables)
rows = conn.execute("SELECT * FROM zones").fetchall()
print("Zones table data:")
for row in rows:
    print(row)
conn.close()