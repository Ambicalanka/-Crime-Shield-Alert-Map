import sqlite3
conn = sqlite3.connect('crime_data.db')
more_states = [
    ('Punjab', 'yellow'),
    ('Kerala', 'green'),
    ('Gujarat', 'yellow'),
    ('Assam', 'red'),
    ('Odisha', 'yellow')
]
for zone, severity in more_states:
    conn.execute("INSERT OR IGNORE INTO zones (zone, severity) VALUES (?, ?)", (zone, severity))
conn.commit()
conn.close()
print("More states added to zones table.")