import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('crime_data.db')

# Add new columns if they do not exist
try:
    conn.execute("ALTER TABLE crimes ADD COLUMN description TEXT;")
except sqlite3.OperationalError:
    pass
try:
    conn.execute("ALTER TABLE crimes ADD COLUMN date TEXT;")
except sqlite3.OperationalError:
    pass
try:
    conn.execute("ALTER TABLE crimes ADD COLUMN victim_age INTEGER;")
except sqlite3.OperationalError:
    pass
try:
    conn.execute("ALTER TABLE crimes ADD COLUMN victim_gender TEXT;")
except sqlite3.OperationalError:
    pass
try:
    conn.execute("ALTER TABLE crimes ADD COLUMN severity TEXT;")
except sqlite3.OperationalError:
    pass
try:
    conn.execute("ALTER TABLE crimes ADD COLUMN reported_by TEXT;")
except sqlite3.OperationalError:
    pass

# 10 high-crime states/zones
zones = [
    ('Uttar Pradesh', 'red'),
    ('Maharashtra', 'red'),
    ('Delhi', 'red'),
    ('Rajasthan', 'yellow'),
    ('Madhya Pradesh', 'yellow'),
    ('Bihar', 'red'),
    ('West Bengal', 'yellow'),
    ('Tamil Nadu', 'yellow'),
    ('Karnataka', 'yellow'),
    ('Telangana', 'yellow')
]
for zone, severity in zones:
    conn.execute("INSERT OR IGNORE INTO zones (zone, severity) VALUES (?, ?)", (zone, severity))

# Crime types and descriptions
crime_types_list = [
    ('Theft', 'Stolen bike'),
    ('Robbery', 'Bank robbery'),
    ('Assault', 'Street fight'),
    ('Burglary', 'House break-in'),
    ('Fraud', 'Online scam'),
    ('Kidnapping', 'Child missing'),
    ('Murder', 'Homicide case'),
    ('Snatching', 'Chain snatching'),
    ('Cybercrime', 'Phishing attack'),
    ('Drugs', 'Drug trafficking'),
    ('Domestic Violence', 'Family dispute'),
    ('Sexual Assault', 'Harassment case'),
    ('Extortion', 'Threat for money'),
    ('Arson', 'Property set on fire'),
    ('Pickpocketing', 'Wallet stolen in crowd')
]
genders = ['Male', 'Female', 'Other']
severities = ['low', 'medium', 'high']

today = datetime.today()

# Add 3 crimes per state, with different types, dates, and new fields
for i, (zone, _) in enumerate(zones):
    for j in range(3):
        crime_type, description = random.choice(crime_types_list)
        days_ago = random.randint(1, 5*365)
        crime_date = (today - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        victim_age = random.randint(10, 70)
        victim_gender = random.choice(genders)
        severity = random.choice(severities)
        conn.execute(
            "INSERT INTO crimes (crime_type, description, area_name, date, victim_age, victim_gender, severity, reported_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (crime_type, description, zone, crime_date, victim_age, victim_gender, severity, "admin")
        )

conn.commit()
conn.close()
print("Columns added if needed and sample crimes with extra fields inserted.")