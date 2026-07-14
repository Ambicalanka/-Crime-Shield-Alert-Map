import sqlite3

conn = sqlite3.connect('crime_data.db')
cursor = conn.execute('PRAGMA table_info(crimes);')
for row in cursor:
    print(row)
conn.close()