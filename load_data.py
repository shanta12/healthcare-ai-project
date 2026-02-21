import pandas as pd
import sqlite3

# 1️⃣ Connect to SQLite database (creates healthcare.db file)
conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# 2️⃣ Read CSV files
patients = pd.read_csv("patients.csv")
conditions = pd.read_csv("conditions.csv")
prescriptions = pd.read_csv("prescriptions.csv")
appointments = pd.read_csv("appointments.csv")

# 3️⃣ Store data into database tables
patients.to_sql("patients", conn, if_exists="replace", index=False)
conditions.to_sql("conditions", conn, if_exists="replace", index=False)
prescriptions.to_sql("prescriptions", conn, if_exists="replace", index=False)
appointments.to_sql("appointments", conn, if_exists="replace", index=False)

print("✅ Data successfully loaded into healthcare.db")

conn.close()