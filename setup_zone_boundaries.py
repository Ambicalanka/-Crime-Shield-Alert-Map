import sqlite3

conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()

# Fetch column names
cursor.execute("PRAGMA table_info(zones)")
columns = [col[1] for col in cursor.fetchall()]
print(f"Column names detected: {columns}")

# Detect zone column
if 'zone' in columns:
    zone_column = 'zone'
elif 'location' in columns:
    zone_column = 'location'
else:
    raise ValueError("No zone column found.")

print(f"Using '{zone_column}' as the zone name column.")

# Add bounding box columns if missing
for col in ['min_lat', 'max_lat', 'min_lng', 'max_lng']:
    if col not in columns:
        cursor.execute(f"ALTER TABLE zones ADD COLUMN {col} REAL")
        print(f"Added column {col}")

# Zone boundaries (example, add more zones as needed)
zone_boundaries = {
    'Delhi': {'min_lat': 28.40, 'max_lat': 28.90, 'min_lng': 76.80, 'max_lng': 77.30},
    'Mumbai': {'min_lat': 18.90, 'max_lat': 19.30, 'min_lng': 72.70, 'max_lng': 73.10},
    # Add other zones here...
}

# Update or insert each zone
for zone_name, bounds in zone_boundaries.items():
    cursor.execute(f"""
        UPDATE zones SET 
            min_lat=?, max_lat=?, min_lng=?, max_lng=?
        WHERE {zone_column}=?
    """, (bounds['min_lat'], bounds['max_lat'], bounds['min_lng'], bounds['max_lng'], zone_name))
    
    if cursor.rowcount == 0:
        if zone_column == 'zone':
            cursor.execute(f"""
                INSERT INTO zones (zone, location, severity, crimes, min_lat, max_lat, min_lng, max_lng)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (zone_name, zone_name, 'Low', 0, bounds['min_lat'], bounds['max_lat'], bounds['min_lng'], bounds['max_lng']))
        else:
            cursor.execute(f"""
                INSERT INTO zones (location, zone, severity, crimes, min_lat, max_lat, min_lng, max_lng)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (zone_name, zone_name, 'Low', 0, bounds['min_lat'], bounds['max_lat'], bounds['min_lng'], bounds['max_lng']))
    
    print(f"Updated or inserted {zone_name}")
