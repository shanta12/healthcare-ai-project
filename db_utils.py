import sqlite3


# ----------------------------
# GET PATIENT DATA
# ----------------------------
def get_patient_data(patient_id):
    return {
        "patient_id": patient_id,
        "name": "John Doe",
        "age": 30,
        "blood_group": "O+"
    }


# ----------------------------
# GET PRESCRIPTIONS
# ----------------------------
def get_prescriptions(patient_id):
    return [
        {"medicine": "Paracetamol", "dosage": "500mg"},
        {"medicine": "Vitamin D", "dosage": "1000 IU"}
    ]


# ----------------------------
# BOOK APPOINTMENT
# ----------------------------
def book_appointment(patient_id, doctor_name, date, time):
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        doctor_name TEXT,
        date TEXT,
        time TEXT
    )
    """)

    cursor.execute("""
    SELECT * FROM appointments
    WHERE doctor_name=? AND date=? AND time=?
    """, (doctor_name, date, time))

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "This time slot is already booked. Please choose another time."

    cursor.execute("""
    INSERT INTO appointments (patient_id, doctor_name, date, time)
    VALUES (?, ?, ?, ?)
    """, (patient_id, doctor_name, date, time))

    conn.commit()
    conn.close()

    return "Appointment booked successfully."