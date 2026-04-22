import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

def insMedData(med_data):
    dbpass = os.getenv("MYSQL_PASSWORD")
    try:
        cnx = mysql.connector.connect(user='controller-user', password=dbpass,
                                      host='db',
                                      database='db')
        cursor = cnx.cursor()

        query = '''
            INSERT INTO med_data
            (PATIENT_SSN, DOCTOR_ID,P_FIRSTNAME,P_LASTNAME,`DESC`,MED_SPECIALTY,SAMPLE_NAME,TRANSCRIPTION)
            VALUES (%(p_ssn)s,%(d_id)s,%(p_firstname)s,%(p_lastname)s,%(desc)s,%(med_specialty)s,%(sample_name)s,%(transcription)s)
        '''

        cursor.execute(query, med_data)
        cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return 1
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return 1
        elif err.errno == errorcode.ER_BAD_HOST_ERROR:
            print("Failed to connect - host not reachable.")
            return 1
        else:
            print(err)
            return 1
    finally:
        cursor.close()
        cnx.close()


def insDoctor(doctor_data):
    dbpass = os.getenv("MYSQL_PASSWORD")
    try:
        cnx = mysql.connector.connect(user='controller-user', password=dbpass,
                                      host='db',
                                      database='db')
        cursor = cnx.cursor()

        query = '''
            INSERT INTO doctors
            (DOCTOR_ID, D_FIRSTNAME, D_LASTNAME)
            VALUES (%(d_id)s,%(d_firstname)s,%(d_lastname)s)
        '''

        cursor.execute(query, doctor_data)
        cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return 1
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return 1
        elif err.errno == errorcode.ER_BAD_HOST_ERROR:
            print("Failed to connect - host not reachable.")
            return 1
        else:
            print(err)
            return 1
    finally:
        cursor.close()
        cnx.close()
