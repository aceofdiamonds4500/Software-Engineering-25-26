import sqlite3

def searchDoctor(doctor_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    try:
        cur.execute('''
            SELECT * FROM doctors
            WHERE DOCTOR_ID = ?
        ''', (doctor_id,))

        row = cur.fetchone()
        if row:
            return row
    except sqlite3.Error as e:
        con.rollback()
        return e
    finally:
        con.close()

def searchPatientSSN(ssn):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    try:
        cur.execute('''
            SELECT * FROM med_data
            WHERE PATIENT_SSN = ?
        ''', (ssn,))

        row = cur.fetchone()
        if row:
            return f"{row[2]} {row[3]}"
    except sqlite3.Error as e:
        con.rollback()
        return e
    finally:
        con.close()

def getTranscription(ssn):
    print("NOT IMPLEMENTED")