import sqlite3

def initDoctors():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    
    try:
        cur.execute('''CREATE TABLE doctors(
            DOCTOR_ID INT PRIMARY KEY,
            D_FIRSTNAME VARCHAR(255),
            D_LASTNAME VARCHAR(255)
            );''')

    except sqlite3.Error as e:
        #print(f"Error code: {e}")
        con.rollback()
        return e
    finally:
        con.close()

def initMedData():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    
    try:
        cur.execute('''CREATE TABLE med_data(
            PATIENT_SSN TEXT(9) CHECK(LENGTH(PATIENT_SSN) = 8 AND PATIENT_SSN GLOB '[0-9]*'),
            DOCTOR_ID INT,
            P_FIRSTNAME VARCHAR(255) NOT NULL,
            P_LASTNAME VARCHAR(255) NOT NULL,
            DESC TEXT NOT NULL,
            MED_SPECIALTY TEXT NOT NULL,
            SAMPLE_NAME TEXT NOT NULL,
            TRANSCRIPTION TEXT NOT NULL,
            CONSTRAINT DOCTOR_ID FOREIGN KEY (DOCTOR_ID)
            REFERENCES doctors(DOCTOR_ID)
            );''') 

    except sqlite3.Error as e:
        #print(f"Error code: {e}")
        con.rollback()
        return e
    finally:
        con.close()