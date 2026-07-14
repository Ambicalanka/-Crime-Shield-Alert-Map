import sqlite3
from datetime import datetime, timedelta
import random

def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

def create_zones_table_if_missing(cur):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS zones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        severity TEXT
    )
    ''')

def create_crimes_table_if_missing(cur):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS crimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crime_type TEXT,
        location TEXT,
        description TEXT
        -- date_reported column added later if missing
    )
    ''')

def add_date_reported_column_if_missing(cur):
    if not column_exists(cur, 'crimes', 'date_reported'):
        print("Adding 'date_reported' column to crimes table...")
        cur.execute("ALTER TABLE crimes ADD COLUMN date_reported DATE")
    else:
        print("'date_reported' column already exists.")

def insert_sample_crimes(cur, num=100):
    crime_types = ['Theft', 'Assault', 'Robbery', 'Drug Trafficking', 'Fraud']
    locations = [
        "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Manipur", "Meghalaya",
        "Mizoram", "Nagaland", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand"
    ]
    descriptions = {
        'Theft': ['Bags stolen at market', 'Pickpocketing incident', 'Vehicle theft reported'],
        'Assault': ['Street fight broke out', 'Physical altercation reported', 'Road rage incident'],
        'Robbery': ['Armed robbery at shop', 'Jewelry store robbed', 'Bank robbery attempt'],
        'Drug Trafficking': ['Large heroin seizure', 'Illegal drug party busted', 'Cannabis plantation raided'],
        'Fraud': ['Fake job scam', 'Loan scam reported', 'Phishing attack on bank customers']
    }
    
    for _ in range(num):
        crime_type = random.choice(crime_types)
        location = random.choice(locations)
        description = random.choice(descriptions[crime_type])
        date_reported = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        
        cur.execute('''
            INSERT INTO crimes (crime_type, location, description, date_reported)
            VALUES (?, ?, ?, ?)
        ''', (crime_type, location, description, date_reported))

def update_zone_severity(cur):
    # Just an example update; you should customize based on your logic or data
    zones = [
        ("Chhattisgarh", "red"), ("Goa", "green"), ("Gujarat", "yellow"),
        ("Haryana", "red"), ("Himachal Pradesh", "green"), ("Manipur", "red"),
        ("Meghalaya", "yellow"), ("Mizoram", "green"), ("Nagaland", "red"),
        ("Sikkim", "green"), ("Tamil Nadu", "yellow"), ("Telangana", "red"),
        ("Tripura", "yellow"), ("Uttar Pradesh", "red"), ("Uttarakhand", "green")
    ]
    for name, severity in zones:
        cur.execute('''
            INSERT INTO zones (name, severity)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET severity=excluded.severity
        ''', (name, severity))


def main():
    conn = sqlite3.connect('crime_data.db')
    cur = conn.cursor()

    create_zones_table_if_missing(cur)
    create_crimes_table_if_missing(cur)
    add_date_reported_column_if_missing(cur)
    insert_sample_crimes(cur, num=300)
    update_zone_severity(cur)

    conn.commit()
    conn.close()
    print("Database setup and sample data inserted successfully.")

if __name__ == "__main__":
    main()
