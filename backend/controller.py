import socket
import threading
from ai.inference import load_trained_model, predict
import json
from transformers import AutoTokenizer

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (HOST, PORT)   

#model, id_to_label = load_trained_model("./medical_classification_model", device = "cpu")

#Default tokenizer until I can change it
default_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

#Method for handling thread for a client connection
def handle_client(client, addr):

    print(f"Connected by {addr}")
    connection = True
    while connection:

        msg = client.recv(1024).decode("utf-8")
        data = client.recv(10000)
        if not data:
            break
        #Read received json file
        json_string = data.decode()
        json_data = json.loads(json_string)
        
        print(json_string)
        
        #Command handling logic
        try:
            command = f"{json_data['command']}" 

            match command:

                #Funni ping
                case "PING":
                    return "PONG"

                #Makes the model classify user input
                case "CLASSIFY":
                    print("Classify with model")
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
                    client.sendall(result.encode("utf-8"))  # Send back model results

                #Retrieves the data of the current user from the database
                case "USERDATA":
                    print("Retrieve user data")

                #Disconnects the user
                case "DISCONNECT":
                    print("Disconnecting client")
                    connection = False

                #Default case
                case _:
                    return f"Unknown command: {command}"

        #Error handling for missing command key
        except KeyError as e:
            print(f"Error: {e}")
            return "Error: No command key found"
    client.close()

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[*] Listening on {ADDR[0]}:{ADDR[1]}")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        client.send(b"Connected")

if __name__ == "__main__":
    main()