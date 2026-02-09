import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS MED_DATA(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DESC TEXT NOT NULL,
    MEDICAL_SPECIALTY TEXT NOT NULL,
    SAMPLE_NAME TEXT NOT NULL,
    TRANSCRIPTION TEXT NOT NULL,
    KEYWORDS TEXT NOT NULL
);''')
cur.execute('''CREATE TABLE IF NOT EXISTS DOCTORS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    HOSPITAL TEXT NOT NULL
);''')
conn.commit()
conn.close()
print('database.db created at', db_path)
