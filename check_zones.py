import sqlite3

conn = sqlite3.connect("crime_data.db")
cur = conn.cursor()

cur.execute("SELECT DISTINCT name FROM zones")
rows = cur.fetchall()

print("States in zones table:")
for row in rows:
    print(row[0])

conn.close()
