import sqlite3

conn = sqlite3.connect('crime_data.db')

# Try to add the 'area' column (ignore error if it already exists)
try:
    conn.execute('ALTER TABLE crimes ADD COLUMN area TEXT;')
    print("Added 'area' column to crimes table.")
except sqlite3.OperationalError:
    print("'area' column already exists.")

# Insert a test crime row
conn.execute(
    "INSERT INTO crimes (crime_type, description, area) VALUES (?, ?, ?)",
    ('Theft', 'Stolen bike', 'Delhi')
)
conn.commit()
print("Inserted test crime row with area='Delhi'.")
conn.close()