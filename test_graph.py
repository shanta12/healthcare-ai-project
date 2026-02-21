import sqlite3

conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# Example Query: Show all patients
cursor.execute("SELECT * FROM patients LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()