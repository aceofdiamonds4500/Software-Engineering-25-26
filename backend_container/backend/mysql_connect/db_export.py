import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

def exportData():
    print("Exporting data...")
    dbpass = os.getenv("MYSQL_PASSWORD")
    try:

        cnx = mysql.connector.connect(user='controller-user', password=dbpass,
                                      host='db',
                                      database='db')
        cursor = cnx.cursor()

        print("Query")

        query = '''
            SELECT DESCRIPTION, MEDICAL_SPECIALTY, SAMPLE_NAME, TRANSCRIPTION, KEYWORDS
            FROM training_data
            WHERE CONFIDENCE >= 0.75
            INTO OUTFILE '/app/backend/train.csv'
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\\n';
        '''

        cursor.execute(query)
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
    else:
        cursor.close()
        cnx.close()