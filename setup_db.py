import sqlite3

# Connect to DB
conn = sqlite3.connect("crime_data.db")
cur = conn.cursor()

# Drop and recreate tables
cur.execute("DROP TABLE IF EXISTS zones")
cur.execute("DROP TABLE IF EXISTS crimes")

cur.execute('''
    CREATE TABLE zones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        severity TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        min_lat REAL,
        max_lat REAL,
        min_lng REAL,
        max_lng REAL
    )
''')

cur.execute('''
    CREATE TABLE crimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        crime_type TEXT NOT NULL,
        description TEXT
    )
''')

# ✅ 10 RED zones (Danger) with coordinates
zones_red = [
    ("Gujarat", "red", 22.3, 71.2, 22.0, 22.6, 70.9, 71.5),
    ("Uttar Pradesh", "red", 26.8, 80.9, 26.5, 27.0, 80.7, 81.1),
    ("Bihar", "red", 25.6, 85.1, 25.3, 25.9, 84.8, 85.4),
    ("Chhattisgarh", "red", 21.3, 81.9, 21.0, 21.5, 81.6, 82.2),
    ("Jharkhand", "red", 23.6, 85.3, 23.3, 23.9, 85.0, 85.6),
    ("Manipur", "red", 24.6, 93.9, 24.3, 24.9, 93.6, 94.2),
    ("Nagaland", "red", 26.1, 94.6, 25.8, 26.4, 94.3, 94.9),
    ("Telangana", "red", 17.1, 79.2, 16.8, 17.4, 78.9, 79.5),
    ("Tamil Nadu", "red", 11.1, 78.6, 10.8, 11.4, 78.3, 78.9),
    ("Haryana", "red", 29.0, 76.0, 28.7, 29.3, 75.7, 76.3)
]

# ✅ 10 YELLOW zones (No data)
zones_yellow = [
    ("Sikkim", "yellow", 27.5, 88.5, 27.3, 27.7, 88.3, 88.7),
    ("Goa", "yellow", 15.3, 74.1, 15.1, 15.5, 73.9, 74.3),
    ("Tripura", "yellow", 23.9, 91.9, 23.7, 24.1, 91.7, 92.1),
    ("Mizoram", "yellow", 23.1, 92.9, 22.8, 23.4, 92.6, 93.2),
    ("Meghalaya", "yellow", 25.5, 91.3, 25.3, 25.7, 91.1, 91.5),
    ("Himachal Pradesh", "yellow", 31.1, 77.1, 30.9, 31.3, 76.9, 77.4),
    ("Uttarakhand", "yellow", 30.0, 79.0, 29.7, 30.3, 78.7, 79.3),
    ("Puducherry", "yellow", 11.9, 79.8, 11.7, 12.1, 79.6, 80.0),
    ("Chandigarh", "yellow", 30.7, 76.7, 30.5, 30.9, 76.5, 76.9),
    ("Ladakh", "yellow", 34.1, 77.6, 33.9, 34.3, 77.4, 77.8)
]

# ✅ 10 GREEN zones (Safe)
zones_green = [
    ("Delhi", "green", 28.7, 77.1, 28.5, 28.9, 76.9, 77.3),
    ("Maharashtra", "green", 19.0, 72.9, 18.7, 19.3, 72.6, 73.2),
    ("Karnataka", "green", 12.9, 77.6, 12.6, 13.2, 77.3, 77.9),
    ("Kerala", "green", 10.5, 76.3, 10.2, 10.8, 76.0, 76.6),
    ("Andhra Pradesh", "green", 16.5, 80.6, 16.2, 16.8, 80.3, 80.9),
    ("Odisha", "green", 20.3, 85.8, 20.0, 20.6, 85.5, 86.1),
    ("Punjab", "green", 30.9, 75.8, 30.6, 31.2, 75.5, 76.1),
    ("Assam", "green", 26.2, 91.7, 25.9, 26.5, 91.4, 92.0),
    ("Rajasthan", "green", 26.9, 75.8, 26.6, 27.2, 75.5, 76.1),
    ("West Bengal", "green", 22.6, 88.3, 22.3, 22.9, 88.0, 88.6)
]

all_zones = zones_red + zones_yellow + zones_green

cur.executemany('''
    INSERT INTO zones (name, severity, latitude, longitude, min_lat, max_lat, min_lng, max_lng)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', all_zones)

# Crimes for RED zones only
crimes_red = [
    ("Gujarat", "Fraud", "Online banking scam affecting rural users"),
    ("Uttar Pradesh", "Assault", "Mob violence reported in Varanasi"),
    ("Bihar", "Robbery", "Armed robbery at Patna jewelry store"),
    ("Chhattisgarh", "Drug Trafficking", "Narcotics recovered from bus terminal"),
    ("Jharkhand", "Assault", "Violent clash during local protest"),
    ("Manipur", "Drug Trafficking", "Seized heroin near Moreh border"),
    ("Nagaland", "Fraud", "Fake ID documents in Kohima college"),
    ("Telangana", "Assault", "Group attack outside tech park"),
    ("Tamil Nadu", "Theft", "Pickpocketing incident in Chennai metro"),
    ("Haryana", "Robbery", "Highway cargo truck looted overnight"),
    # Extra crimes per zone for history
    ("Gujarat", "Theft", "ATM machine tampered in Ahmedabad"),
    ("Uttar Pradesh", "Fraud", "Fake land papers seized in Lucknow"),
    ("Bihar", "Assault", "Family dispute leads to hospitalisation"),
    ("Chhattisgarh", "Robbery", "Cash van looted near Durg"),
    ("Jharkhand", "Fraud", "Loan scam by fake NGO exposed"),
    ("Manipur", "Assault", "Attack during college protest"),
    ("Nagaland", "Robbery", "Robbery attempt in Dimapur market"),
    ("Telangana", "Fraud", "Credit card cloning racket"),
    ("Tamil Nadu", "Assault", "Road rage violence in Coimbatore"),
    ("Haryana", "Drug Trafficking", "Synthetic drug lab busted in Panipat")
]

cur.executemany('''
    INSERT INTO crimes (location, crime_type, description)
    VALUES (?, ?, ?)
''', crimes_red)
# Save
conn.commit()
conn.close()

"/mnt/data/crime_data.db"