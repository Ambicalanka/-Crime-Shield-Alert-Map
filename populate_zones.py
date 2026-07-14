import sqlite3

# Connect to database
conn = sqlite3.connect('crime_data.db')
cur = conn.cursor()

# Recreate zones table with name as PRIMARY KEY
cur.execute('DROP TABLE IF EXISTS zones')
cur.execute('''
CREATE TABLE zones (
    name TEXT PRIMARY KEY,
    severity TEXT
)
''')

# List of Indian states and UTs with sample severity
zones = [
    ("Andhra Pradesh", "green"),
    ("Arunachal Pradesh", "green"),
    ("Assam", "red"),
    ("Bihar", "yellow"),
    ("Chhattisgarh", "red"),
    ("Goa", "green"),
    ("Gujarat", "green"),
    ("Haryana", "yellow"),
    ("Himachal Pradesh", "green"),
    ("Jharkhand", "yellow"),
    ("Karnataka", "green"),
    ("Kerala", "green"),
    ("Madhya Pradesh", "green"),
    ("Maharashtra", "red"),
    ("Manipur", "red"),
    ("Meghalaya", "yellow"),
    ("Mizoram", "green"),
    ("Nagaland", "green"),
    ("Odisha", "green"),
    ("Punjab", "green"),
    ("Rajasthan", "green"),
    ("Sikkim", "green"),
    ("Tamil Nadu", "green"),
    ("Telangana", "red"),
    ("Tripura", "yellow"),
    ("Uttar Pradesh", "red"),
    ("Uttarakhand", "green"),
    ("West Bengal", "yellow"),
    ("Andaman and Nicobar Islands", "green"),
    ("Chandigarh", "green"),
    ("Dadra and Nagar Haveli and Daman and Diu", "green"),
    ("Delhi", "red"),
    ("Jammu and Kashmir", "yellow"),
    ("Ladakh", "green"),
    ("Lakshadweep", "green"),
    ("Puducherry", "green")
]

# Insert data
for name, severity in zones:
    cur.execute("INSERT INTO zones (name, severity) VALUES (?, ?)", (name, severity))

conn.commit()
conn.close()

print("✅ Zones table recreated and populated successfully.")
