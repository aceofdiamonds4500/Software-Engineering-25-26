import socket
import load_model as m
import json
from transformers import AutoTokenizer

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65067        # Arbitrary port number
model, id_to_label = m.load_trained_model("./medical_classification_model", device = "cpu")
#Default tokenizer until I can change it
default_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

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

            #Extract description as prompt
            prompt = f"{json_data['fields']['Description']}\n{json_data['fields']['Transcription']}\n{json_data['fields']['Keywords']}" 

            #Timestamp for identification
            timestamp = json_data['timestamp']
            autocorrect = "NOT IMPLEMENTED"
            keyterms = "NOT IMPLEMENTED"

            print(f"Received: {timestamp}") # Print the decoded data as a string
            predicted_label, confidence_score, topk = m.predict(prompt, model, default_tokenizer, id_to_label, device='cpu', max_length=512)
            result = f"Predicted specialty:  {predicted_label} \n\nConfidence: {confidence_score} \n\nTop: {topk}"
            conn.sendall(result.encode("utf-8"))  # Send back model results