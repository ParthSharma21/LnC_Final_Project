import socket
import threading
import json
import authenticationAndLogin as Login

# Server host and port
HOST = '127.0.0.1'
PORT = 12345

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    while True:
        try:
            user_data = client_socket.recv(1024).decode('utf-8')
            if not user_data:
                break
            # print(f"[{client_address}] {user_data}")
            # print(type(user_data))

            AuthenticationResponse = Login.UserLogin(json.loads(user_data))
            print(AuthenticationResponse)
            
            # Respond to the client
            response = json.dumps(AuthenticationResponse)
            client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            break

    print(f"[DISCONNECTED] {client_address} disconnected.")
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
