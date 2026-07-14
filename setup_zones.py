import sqlite3

DB_FILE = "crime_data.db"

states = [
    ("Andhra Pradesh", "yellow", 15.9129, 79.7400),
    ("Arunachal Pradesh", "green", 28.2180, 94.7278),
    ("Assam", "red", 26.2006, 92.9376),
    ("Bihar", "yellow", 25.0961, 85.3131),
    ("Chhattisgarh", "red", 21.2787, 81.8661),
    ("Goa", "green", 15.2993, 74.1240),
    ("Gujarat", "yellow", 22.2587, 71.1924),
    ("Haryana", "green", 29.0588, 76.0856),
    ("Himachal Pradesh", "green", 31.1048, 77.1734),
    ("Jharkhand", "red", 23.6102, 85.2799),
    ("Karnataka", "yellow", 15.3173, 75.7139),
    ("Kerala", "green", 10.8505, 76.2711),
    ("Madhya Pradesh", "red", 22.9734, 78.6569),
    ("Maharashtra", "red", 19.7515, 75.7139),
    ("Manipur", "yellow", 24.6637, 93.9063),
    ("Meghalaya", "green", 25.4670, 91.3662),
    ("Mizoram", "green", 23.1645, 92.9376),
    ("Nagaland", "green", 26.1584, 94.5624),
    ("Odisha", "yellow", 20.9517, 85.0985),
    ("Punjab", "green", 31.1471, 75.3412),
    ("Rajasthan", "yellow", 27.0238, 74.2179),
    ("Sikkim", "green", 27.5330, 88.5122),
    ("Tamil Nadu", "yellow", 11.1271, 78.6569),
    ("Telangana", "red", 18.1124, 79.0193),
    ("Tripura", "green", 23.9408, 91.9882),
    ("Uttar Pradesh", "red", 26.8467, 80.9462),
    ("Uttarakhand", "green", 30.0668, 79.0193),
    ("West Bengal", "red", 22.9868, 87.8550),
    ("Delhi", "red", 28.7041, 77.1025),
    ("Ladakh", "green", 34.1526, 77.5770)
]

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# 💣 Drop and recreate the correct schema
cur.execute("DROP TABLE IF EXISTS zones")
cur.execute('''
    CREATE TABLE zones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        severity TEXT,
        lat REAL,
        lon REAL
    )
''')

cur.executemany("INSERT INTO zones (name, severity, lat, lon) VALUES (?, ?, ?, ?)", states)

conn.commit()
conn.close()

print("✅ Zones table created and populated successfully!")