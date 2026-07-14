import sqlite3

conn = sqlite3.connect('crime_data.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS crimes")

cur.execute('''
CREATE TABLE crimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crime_type TEXT,
    location TEXT,
    description TEXT,
    date_reported DATE
)
''')

conn.commit()
conn.close()
print("Crimes table recreated with date_reported column.")
