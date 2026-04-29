from mysql_connect import db_insert as sqinsert
from mysql_connect import db_select as sqselect
from mysql_connect import db_export as sqexport
from ai.inference import predict
from ai.training import train

from ai.nlp import nlp_autocorrect as nlp

import sys
import os

#Imported to handle unique values
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import TrainingConfig

def handlecommand(json_data, model, id_to_label, default_tokenizer):
    try:
        command = f"{json_data['command']}"
        match command:

            #Test case to confirm server is reachable
            case "PING":
                return "PONG" 

            #----------------------------------------

            #Classifies the data sent from the client
            #Format should be:
            #{
            #   "command": "CLASSIFY",
            #   "timestamp": "ExampleTimeStamp",
            #   "fields": {
            #       "Description": "Description",
            #       "Transcription": "TranscriptionValue",
            #       "Keywords": "KeyWords"
            #   }
            #}
            case "CLASSIFY":

                print("Attempting to classify with model...")
                try:

                    #Reads the JSON string and pulls the Description, Transcription, and KeyWords field.
                    #Also runs the prediction for medical field, confidence, and top choices.
                    prompt = f"{json_data['fields']['Description']}\n{json_data['fields']['Transcription']}\n{json_data['fields']['Keywords']}"
                    predicted_label, confidence_score, topk = predict(prompt, model, default_tokenizer, id_to_label, device='cpu', max_length=512)
                    timestamp = json_data['timestamp']
                    print(f"Received: {timestamp}")

                    autocorrect = "NOT IMPLEMENTED"
                    keyterms = "NOT IMPLEMENTED"

                    json_data['fields']['confidence'] = confidence_score
                    sqinsert.insTrainingData(json_data['fields'])

                    return f"specialty: {predicted_label} | Confidence: {confidence_score:.2f}"
                except:
                    return "Error: Invalid JSON for classification"

            #---------------------------------------

            case "AUTOCORRECT":
                print("Attempting to autocorrect data")
                try:
                    uncorrected_text = json_data['fields']['Transcription']
                    vocab = nlp.build_vocab(config.DATA_PATH, min_freq=5)
                    suggestions = nlp.suggest_corrections(uncorrected_text, vocab)
                    return suggestions
                except:
                    return "Error: Could not parse JSON for autocorrect"

            #-------------------------------------------------------------------


            #Retrieves the data of the current user from the database
            case "USERDATA":
                print("Retrieve user data")

            #-------------------------------------------------------------------

            #Inserts patient data from a specific case into the database
            #Format should be:
            #{
            #   "command": "INSERTPATIENT",
            #   "timestamp": "ExampleTimeStamp",
            #   "fields": {
            #       "p_ssn": SSN(Number),
            #       "d_id": Doctor ID(Number),
            #       "p_firstname": "Patient first name",
            #       "p_lastname": "Patient last name",
            #       "desc": "Brief description of patient",
            #       "med_specialty": "Field of medicine",
            #       "sample_name": "SampleName",
            #       "transcription": "Description of patient issues"
            #   }
            #}
            case "INSERTPATIENT":
                print("Inserting patient data")
                try:
                    r = sqinsert.insMedData(json_data['fields'])
                    print(r)
                    return "Inserted patient into database"
                except:
                    return "Error: Invalid JSON for patient insertion"

            #-------------------------------------------------------------------

            #Inserts information on a new doctor into the database
            #Format should be:
            #{
            #   "command": "INSERTDOCTOR",
            #   "timestamp": "ExampleTimeStamp",
            #   "fields": {
            #       "d_id": Doctor ID(Number),
            #       "d_firstname": "Doctor first name",
            #       "d_lastname": "Doctor last name",
            #   }
            #}
            case "INSERTDOCTOR":
                print("Inserting doctor data")
                try:
                    sqinsert.insDoctor(json_data['fields'])
                    return "Inserted doctor into database"
                except:
                    return "Error: Invalid JSON for doctor insertion"

            #-------------------------------------------------------------------

            #Selects a doctor using the primary key: d_id
            case "SELECTDOCTOR":
                print("Selecting doctor data")
                try:
                    sqselect.searchDoctor(json_data['fields']['d_id'])
                    return "Selected doctor from database"
                except:
                    return "Error: Could not select doctor"

            #-------------------------------------------------------------------

            #Selects a patient using the primary key: p_ssn
            case "SELECTPATIENT":
                print("Selecting doctor data")
                try:
                    sqselect.searchPatientSSN(json_data['fields']['p_ssn'])
                    return "Selected patient from database"
                except:
                    return "Error: Could not select patient"

            #-------------------------------------------------------------------

            #Unused command
            case "SELECTTRANSCRIPTION":
                print("Selecting transcription data")
                try:
                    sqselect.getTranscription(json_data['fields']['description'])
                    return "Selected transcription from database"
                except:
                    return "Error: Could not select transcription"

            #-------------------------------------------------------------------

            case "TRAINMODEL":
                print("Exporting CSV")
                sqexport.exportData()
                print("Training model")
                train.set_seed(42)
                train.training()
                return "Did The Thing"

            # ---------------------------------------

            #???
            case "DATALENGTH":
                return "new data is"

            #-------------------------------------------------------------------

            #Returns a string during disconnect
            case "DISCONNECT":
                return "DISCONNECT"

            #-------------------------------------------------------------------

            #Default case
            case _:
                return f"Unknown command: {command}"

            #-------------------------------------------------------------------

    #Error handling for missing command key
    except KeyError as e:
        print(f"Error: {e}")
        return "Error: No command key found"
        