import socket
import json
from time import sleep

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5867
ADDR = (HOST, PORT)   
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDR)

    for i in range(10):
    
        command = "AUTOCORRECT"
        data = {
            "command": command,
            "fields": {
                'transcription': "me speek worbs n stoof"
                }
            }
        json_data = json.dumps(data)
        s.sendall(json_data.encode("utf-8"))
        response = s.recv(1024).decode("utf-8")
        print(f"Response from server: {response}")
        sleep(1)

    command = "DISCONNECT"
    data = {"command": command}
    json_data = json.dumps(data)
    s.sendall(json_data.encode("utf-8"))