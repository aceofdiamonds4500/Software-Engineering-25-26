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
            (P_FIRSTNAME,P_LASTNAME,`DESC`,MED_SPECIALTY,SAMPLE_NAME,TRANSCRIPTION)
            VALUES (%(p_firstname)s,%(p_lastname)s,%(desc)s,%(med_specialty)s,%(sample_name)s,%(transcription)s)
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

def insTrainingData(training_data):
    dbpass = os.getenv("MYSQL_PASSWORD")
    try:
        cnx = mysql.connector.connect(user='controller-user', password=dbpass,
                                      host='db',
                                      database='db')
        cursor = cnx.cursor()

        query = '''
            INSERT INTO training_data
            (DESCRIPTION, MEDICAL_SPECIALTY, SAMPLE_NAME, TRANSCRIPTION, KEYWORDS, CONFIDENCE)
            VALUES (%s,%s,%s,%s,%s,%s)
        '''

        print("Values Thing")
        values = (
            training_data["Description"],
            training_data["MedicalSpecialty"],
            training_data["SampleName"],
            training_data["Transcription"],
            training_data["Keywords"],
            float(training_data["confidence"])
        )

        print("Starting to insert training data")
        cursor.execute(query, values)
        cnx.commit()
        print("Done")

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