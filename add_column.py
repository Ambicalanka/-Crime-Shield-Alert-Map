import sqlite3

# Connect to the database
conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()

# Check if the column exists
cursor.execute("PRAGMA table_info(crimes)")
columns = [row[1] for row in cursor.fetchall()]
if 'date_reported' not in columns:
    # Add the column if it doesn't exist
    cursor.execute("ALTER TABLE crimes ADD COLUMN date_reported TEXT")
    conn.commit()
    print("date_reported column added.")
else:
    print("date_reported column already exists.")

# Close the connection
conn.close()