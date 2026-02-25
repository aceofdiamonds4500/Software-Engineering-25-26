import socket
import json
from time import sleep

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (HOST, PORT)   
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDR)

    for i in range(10):
    
            command = "INSERTPATIENT"
            data = {
                "command": command,
                "fields": {
                    'p_ssn': 42042067,
                    'd_id': 500,
                    'p_firstname': 'Controller',
                    'p_lastname': 'Tester',
                    'desc': 'Patient is a program that likes going to the doctor 10 times in a row',
                    'med_specialty': 'Laparoscopy',
                    'sample_name': 'yo mama',
                    'transcription': 'Patient presents with severe symptoms of doin ur mom'
                    }
                }
            json_data = json.dumps(data)
            s.sendall(json_data.encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            print(f"Response from server: {response}")
            sleep(1)
