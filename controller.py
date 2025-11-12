import socket
import inference as m
import json
from transformers import AutoTokenizer
import ctypes

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65067        # Arbitrary port number
model, id_to_label = m.load_trained_model("./medical_classification_model", device = "cpu")

#Default tokenizer until I can change it
default_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

#Load dll for sqlite
clib = ctypes.CDLL('./sqlite/data_control.so')
clib.get_db.argtypes = []
clib.get_db.restype = ctypes.c_void_p

#set up tables and open database
clib.create_tables()
clib.init_db()
db = clib.get_db()

clib.insert_transcript.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
clib.insert_transcript.restype = ctypes.c_int

print(f"Started server on IP {HOST} and port {PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            #Red received json file
            json_string = data.decode()
            json_data = json.loads(json_string)
            json_fields = json_data['fields']

            #Extract description as prompt
            prompt = f"{json_fields['Description']}\n{json_fields['Transcription']}\n{json_fields['Keywords']}" 
            desc, specialty, sample_name, transcription, keywords = {  json_fields['Description'],
                                                                        json_fields['Specialty'],
                                                                        json_fields['SampleName'],
                                                                        json_fields['Transcription'],
                                                                        json_fields['Keywords']}

            if (clib.insert_transcript(desc,specialty,sample_name,transcription,keywords) == 0):
                print("Data successfully inserted")
            else:
                print("failed")
            #Timestamp for identification
            timestamp = json_data['timestamp']

            print(f"Received: {timestamp}") # Print the decoded data as a string
            predicted_label, confidence_score, topk = m.predict(prompt, model, default_tokenizer, id_to_label, device='cpu', max_length=512)
            result = f"Predicted specialty:  {predicted_label} \n\nConfidence: {confidence_score} \n\nTop: {topk}"
            conn.sendall(result.encode("utf-8"))  # Send back model results
        clib.close_db()