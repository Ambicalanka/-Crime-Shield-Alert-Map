import sqlite3

# Connect to the existing crime_data.db database
conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()

# Add bounding box columns to the zones table if they don't exist
try:
    cursor.execute("ALTER TABLE zones ADD COLUMN min_lat REAL")
    cursor.execute("ALTER TABLE zones ADD COLUMN max_lat REAL")
    cursor.execute("ALTER TABLE zones ADD COLUMN min_lng REAL")
    cursor.execute("ALTER TABLE zones ADD COLUMN max_lng REAL")
except sqlite3.OperationalError:
    print("Bounding box columns already exist. Continuing...")

# Complete bounding box data for Indian zones
zone_boundaries = {
    'Delhi': {'min_lat': 28.40, 'max_lat': 28.90, 'min_lng': 76.80, 'max_lng': 77.30},
    'Mumbai': {'min_lat': 18.90, 'max_lat': 19.30, 'min_lng': 72.70, 'max_lng': 73.10},
    'Bengaluru': {'min_lat': 12.80, 'max_lat': 13.10, 'min_lng': 77.45, 'max_lng': 77.75},
    'Hyderabad': {'min_lat': 17.30, 'max_lat': 17.60, 'min_lng': 78.30, 'max_lng': 78.60},
    'Chennai': {'min_lat': 12.85, 'max_lat': 13.10, 'min_lng': 80.15, 'max_lng': 80.30},
    'Kolkata': {'min_lat': 22.45, 'max_lat': 22.70, 'min_lng': 88.25, 'max_lng': 88.45},
    'Ahmedabad': {'min_lat': 22.90, 'max_lat': 23.10, 'min_lng': 72.50, 'max_lng': 72.70},
    'Pune': {'min_lat': 18.45, 'max_lat': 18.65, 'min_lng': 73.75, 'max_lng': 73.95},
    'Surat': {'min_lat': 21.15, 'max_lat': 21.25, 'min_lng': 72.75, 'max_lng': 72.95},
    'Jaipur': {'min_lat': 26.80, 'max_lat': 27.05, 'min_lng': 75.75, 'max_lng': 75.95},
    'Lucknow': {'min_lat': 26.80, 'max_lat': 27.10, 'min_lng': 80.80, 'max_lng': 81.10},
    'Kanpur': {'min_lat': 26.40, 'max_lat': 26.50, 'min_lng': 80.25, 'max_lng': 80.40},
    'Nagpur': {'min_lat': 21.75, 'max_lat': 21.95, 'min_lng': 79.00, 'max_lng': 79.30},
    'Visakhapatnam': {'min_lat': 17.60, 'max_lat': 17.80, 'min_lng': 83.20, 'max_lng': 83.40},
    'Bhopal': {'min_lat': 23.10, 'max_lat': 23.40, 'min_lng': 77.30, 'max_lng': 77.60},
    'Patna': {'min_lat': 25.50, 'max_lat': 25.65, 'min_lng': 85.05, 'max_lng': 85.15},
    'Vadodara': {'min_lat': 22.25, 'max_lat': 22.40, 'min_lng': 73.15, 'max_lng': 73.30},
    'Ludhiana': {'min_lat': 30.85, 'max_lat': 31.05, 'min_lng': 75.75, 'max_lng': 76.00},
    'Agra': {'min_lat': 27.10, 'max_lat': 27.25, 'min_lng': 77.95, 'max_lng': 78.05},
    'Nashik': {'min_lat': 19.90, 'max_lat': 20.05, 'min_lng': 73.75, 'max_lng': 73.90},
}

# Insert or update zones with bounding box data
for zone_name, bounds in zone_boundaries.items():
    cursor.execute("""
        INSERT INTO zones (name, min_lat, max_lat, min_lng, max_lng)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            min_lat = excluded.min_lat,
            max_lat = excluded.max_lat,
            min_lng = excluded.min_lng,
            max_lng = excluded.max_lng
    """, (zone_name, bounds['min_lat'], bounds['max_lat'], bounds['min_lng'], bounds['max_lng']))

conn.commit()
conn.close()

print("Zone boundaries updated successfully in the database!")
