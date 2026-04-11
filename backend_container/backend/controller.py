import socket
import threading
from ai.inference import load_trained_model, predict
from sqlite import db_init as sqinit
import command_handler as cmd
import json
from transformers import AutoTokenizer

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5867
ADDR = (HOST, PORT)   

model, id_to_label = load_trained_model("/app/backend/medical_classification_model", device = "cpu")

#Default tokenizer until I can change it
default_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

#Method for handling thread for a client connection
def handle_client(client, addr):
    print(f"Connected by {addr}")
    connection = True
    #client.send(b"Connected")  # Send welcome message immediately after connection
    while connection:
        try:
            data = client.recv(10000)
            if not data:
                break
            #Read received json file
            json_string = data.decode()
            json_data = json.loads(json_string)
            
            print(json_string)
            
            #Command handling logic
            result = cmd.handlecommand(json_data, model, id_to_label, default_tokenizer)

            if (result == "DISCONNECT"):
                print(f"{addr} has disconnected")
                connection = False
                break
            client.sendall(result.encode("utf-8"))

        except Exception as e:
            print(f"Exception: {e}")
            connection = False
            break
    client.close()

def main():
    sqinit.initDoctors()
    sqinit.initMedData()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Listening on {ADDR[0]}:{ADDR[1]}")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    main()
