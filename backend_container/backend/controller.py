import socket
import threading
import json
import command_handler as cmd
import logging
from transformers import logging as tf_logging
from ai.inference import load_trained_model, predict
from mysql_connect import db_startup
from mysql.connector import errorcode
from transformers import AutoTokenizer
from dotenv import load_dotenv

#Mutes that warning about needing a token everytime the AI starts
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5867
ADDR = (HOST, PORT)

#Method for handling thread for a client connection
def handle_client(client, addr):

    #If this runs, we are connected to a client - Additional welcome message
    connection = True
    print(f"Connected by {addr}")

    #While connected: Wait for an input
    while connection:
        try:
            data = client.recv(10000)
            if not data:
                break

            #Read received json file
            json_string = data.decode()
            json_data = json.loads(json_string)
            print(json_string)
            
            #Hands the recieved JSON command to the command handler
            result = cmd.handlecommand(json_data, model, id_to_label, default_tokenizer)

            #Disconnect if command is DISCONNECT
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

#Initializes the database, then opens a network socket for connections
#Prints out the server IP and Port(IP SHOWS CONTAINER IP, NOT HOST IP)
def main():

    rc = db_startup.test_connection()

    # Initialize the model, set it to use cpu, loads the labels, and creates the tokenizer
    model, id_to_label = load_trained_model("/app/backend/best", device="cpu")
    default_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

    if rc != 0:
        print("Must have a connection to the database to initialize server. Exiting (return code 1)")
        return 1
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
        print(f"Listening on {ADDR[0]}:{ADDR[1]}")

    #Waits for a connection and then hands the client to a thread
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    main()
