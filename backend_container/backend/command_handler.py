import sqlite
from sqlite import db_insert as sqinsert
from sqlite import db_select as sqselect

def handlecommand(json_data):
    try:
        command = f"{json_data['command']}" 

        match command:

            #Funni ping
            case "PING":
                return "PONG" 

            #Makes the model classify user input
            case "CLASSIFY":
                print("Classify with model")
                try:
                    #Extract description as prompt
                    prompt = f"{json_data['fields']['Description']}\n{json_data['fields']['Transcription']}\n{json_data['fields']['Keywords']}" 

                    #Timestamp for identification
                    timestamp = json_data['timestamp']
                    autocorrect = "NOT IMPLEMENTED"
                    keyterms = "NOT IMPLEMENTED"

                    print(f"Received: {timestamp}") # Print the decoded data as a string

                    #predicted_label, confidence_score, topk = predict(prompt, model, default_tokenizer, id_to_label, device='cpu', max_length=512)
                    #result = f"Predicted specialty:  {predicted_label} \n\nConfidence: {confidence_score} \n\nTop: {topk}"

                    result = prompt
                    return result  # Send back model results
                except:
                    return "Error: Invalid JSON for classification"

            #Retrieves the data of the current user from the database
            case "USERDATA":
                print("Retrieve user data")

            #Inserts patient data of a specific case into the database
            #Format for 'fields' in json:
            #patient_data = {
            #'p_ssn': 24955283,
            #'d_id': 500,
            #'p_firstname': 'Brett',
            #'p_lastname': 'Lawrence',
            #'desc': 'Patient is an adolescent male...',
            #'med_specialty': 'Laparoscopy',
            #'sample_name': 'hmmmm',
            #'transcription': 'Patient presents with...'
            #}
            case "INSERTPATIENT":
                print("Inserting patient data")
                try:
                    r = sqinsert.insMedData(json_data['fields'])
                    print(r)
                    return "Inserted patient into database"
                except:
                    return "Error: Invalid JSON for patient insertion"

            #Inserts information on a new doctor into the database
            #Format for 'fields' in json: 
            #doctor_data = {
            #   'd_id': 502,
            #   'd_firstname': 'Doctor',
            #   'd_lastname': 'Jones'
            #   }
            case "INSERTDOCTOR":
                print("Inserting doctor data")
                try:
                    sqinsert.insDoctor(json_data['fields'])
                    return "Inserted doctor into database"
                except:
                    return "Error: Invalid JSON for doctor insertion"

            #Selects a doctor using a specific doctor ID
            case "SELECTDOCTOR":
                print("Selecting doctor data")
                try:
                    sqselect.searchDoctor(json_data['fields']['d_id'])
                    return "Selected doctor from database"
                except:
                    return "Error: Could not select doctor"

            case "SELECTPATIENT":
                print("Selecting doctor data")
                try:
                    sqselect.searchPatientSSN(json_data['fields']['p_ssn'])
                    return "Selected patient from database"
                except:
                    return "Error: Could not select patient"

            #Uses an ID to retrieve a specific transcription
            case "SELECTTRANSCRIPTION":
                print("Selecting transcription data")
                try:
                    sqselect.getTranscription(json_data['fields']['p_ssn'])
                    return "Selected transcription from database"
                except:
                    return "Error: Could not select transcription"

            case "DATALENGTH":
                return "new data is"

            #Returns a string to disconnect the user
            case "DISCONNECT":
                return "DISCONNECT"

            #Default case
            case _:
                return f"Unknown command: {command}"

    #Error handling for missing command key
    except KeyError as e:
        print(f"Error: {e}")
        return "Error: No command key found"
