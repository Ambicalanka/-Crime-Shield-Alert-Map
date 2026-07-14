import sqlite3

zones_data = [
    # Name, min_lat, max_lat, min_lng, max_lng, severity
    ("Andhra Pradesh", 12.0, 19.0, 77.0, 84.0, "green"),
    # ... rest of your data ...
]

def create_zones_table():
    conn = sqlite3.connect('crime_data.db')
    cur = conn.cursor()

    # Drop the existing table if it exists
    cur.execute('DROP TABLE IF EXISTS zones')

    cur.execute('''
        CREATE TABLE zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            min_lat REAL,
            max_lat REAL,
            min_lng REAL,
            max_lng REAL,
            severity TEXT
        )
    ''')

    # Insert zones data
    for zone in zones_data:
        try:
            cur.execute('''
                INSERT OR REPLACE INTO zones (name, min_lat, max_lat, min_lng, max_lng, severity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', zone)
        except Exception as e:
            print(f"Error inserting {zone[0]}: {e}")

    conn.commit()
    conn.close()
    print("Zones table created and populated successfully.")

if __name__ == "__main__":
    create_zones_table()