import sqlite3
import db_init as sqinit
import db_insert as sqinsert

def main():
    #ret = sqlite.init_db()
    
    #if ret is not None:
    #    print(ret)

    doctor_data = {
    'd_id': 502,
    'd_firstname': 'Doctor',
    'd_lastname': 'Jones'
    }

    ret = sqinsert.insDoctor(doctor_data)
    if ret is not None:
        print(ret)

    patient_data = {
    'p_ssn': 24955283,
    'd_id': 500,
    'p_firstname': 'Brett',
    'p_lastname': 'Lawrence',
    'desc': 'Patient is an adolescent male...',
    'med_specialty': 'Laparoscopy',
    'sample_name': 'hmmmm',
    'transcription': 'Patient presents with...'
    }

    ret = sqinsert.insMedData(patient_data)
    if ret is not None:
        print(ret)

if __name__ == "__main__":
  main()