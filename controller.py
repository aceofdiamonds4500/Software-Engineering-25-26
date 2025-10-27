import socket
import load_model as m

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65067      # Random-ass port number
tokenizer, model, device = m.load_trained_model()

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
            prompt = data.decode()
            print(f"Received: {prompt}") # Print the decoded data as a string
            pred_label, probs = m.predict(prompt, tokenizer, model, device)
            result = f"Predicted specialty:  {pred_label} \n\nProbabilities: {probs}"
            conn.sendall(result.encode("utf-8"))  # Send back model results