import sqlite3
    
def insMedData(med_data):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    try:
        cur.execute('''
            INSERT INTO med_data 
            (PATIENT_SSN, DOCTOR_ID,P_FIRSTNAME,P_LASTNAME,DESC,MED_SPECIALTY,SAMPLE_NAME,TRANSCRIPTION)
            VALUES (:p_ssn, :d_id, :p_firstname, :p_lastname, :desc, :med_specialty, :sample_name, :transcription)
        ''', med_data)

        con.commit()

    except sqlite3.Error as e:
        con.rollback()
        return e
    finally:
        con.close()

def insDoctor(doctor_data):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    try:
        cur.execute('''
            INSERT INTO doctors
            (DOCTOR_ID, D_FIRSTNAME, D_LASTNAME)
            VALUES (:d_id, :d_firstname, :d_lastname)
        ''', doctor_data)

        con.commit()
        
    except sqlite3.Error as e:
        con.rollback()
        return e
    finally:
        con.close()