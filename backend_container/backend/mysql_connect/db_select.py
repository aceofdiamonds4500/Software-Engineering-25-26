import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

def searchDoctor(doctor_id):
    dbpass = os.getenv("MYSQL_PASSWORD")
    try:
        cnx = mysql.connector.connect(user='controller-user', password=dbpass,
                                      host='db',
                                      database='db')
        cursor = cnx.cursor()

        cursor.execute('''
            SELECT * FROM doctors
            WHERE DOCTOR_ID = %s
        ''', (doctor_id,))

        row = cursor.fetchone()
        return row

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


def searchPatientSSN(ssn):
    dbpass = os.getenv("MYSQL_PASSWORD")
    try:
        cnx = mysql.connector.connect(user='controller-user', password=dbpass,
                                      host='db',
                                      database='db')
        execute('''
            SELECT * FROM med_data
            WHERE PATIENT_SSN = %s
        ''', (ssn,))

        row = cur.fetchone()
        return row

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

def getTranscription(ssn):
    print("NOT IMPLEMENTED")
