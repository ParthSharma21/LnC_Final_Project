#######    server.py

import socket
import threading
import json
import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
import serverFunctions as sf
import RecommendationEngine.RecommendationEngine as re

# Server host and port
HOST = '127.0.0.1'
PORT = 12345

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    while True:
        try:
            request_data = client_socket.recv(1024).decode('utf-8')
            if not request_data:
                break
            
            request_data = json.loads(request_data)
            action = request_data.get('action')
            
            if action == 'login':
                response = sf.handle_login(request_data)
            elif action == 'addFoodItem':
                response = sf.handle_add_food_item(request_data)
            elif action == 'updateFoodItem':
                response = sf.handle_update_food_item(request_data)
            elif action == 'deleteFoodItem':
                response = sf.handle_delete_food_item(request_data)
            elif action == 'viewMenu':
                response = sf.handle_view_menu()

            
            elif action == 'getRecommendedFoodItems':
                response = re.getRecommendedFoodItems()
            elif action == 'rolloutMenu':
                response = sf.rolloutMenu(request_data)
            elif action == 'notifyEmployees':
                response = sf.notifyEmployees(request_data)
            elif action == 'generateReport':
                response = sf.generateReport()


            elif action == 'viewDailyMenu':
                response = sf.handle_view_daily_menu()
            elif action == 'viewNotifications':
                response = sf.handle_view_notifications()
            elif action == 'orderFood':
                response = sf.handle_order_food(request_data)
            elif action == 'giveFeedback':
                response = sf.handle_give_feedback(request_data)
            elif action == 'requestFeedbackItems':
                response = sf.handle_request_feedback_items(request_data)

            else:
                response = {"status": "error", "message": "Invalid action"}

            # Respond to the client

            print(response)
            response_json = json.dumps(response)
            client_socket.send(response_json.encode('utf-8'))
        
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
