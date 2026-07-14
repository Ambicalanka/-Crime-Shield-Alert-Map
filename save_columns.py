import sqlite3

conn = sqlite3.connect('crime_data.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(zones)")
columns = cursor.fetchall()
conn.close()

# Specify an output file
output_path = 'zones_columns.txt'

with open(output_path, 'w') as f:
    f.write(" Columns in 'zones' table:\n")
    for col in columns:
        # col is a tuple: (cid, name, type, notnull, dflt_value, pk)
        line = f"{col}\n"
        f.write(line)

print(f"Columns saved to {output_path}")
