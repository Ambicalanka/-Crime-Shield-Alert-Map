from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect('crime_data.db')
conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
             ('admin', generate_password_hash('ambicaa')))
conn.commit()
conn.close()
print("Admin user added successfully.")