import sqlite3

conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()

# Create zones table
cursor.execute('''
CREATE TABLE IF NOT EXISTS zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone TEXT UNIQUE,
    severity TEXT,
    latitude REAL,
    longitude REAL
)
''')

# Create crime_stats table
cursor.execute('''
CREATE TABLE IF NOT EXISTS crime_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone TEXT,
    crime_type TEXT,
    count INTEGER,
    year INTEGER
)
''')

conn.commit()
conn.close()
print("zones and crime_stats tables created (if not exists).")