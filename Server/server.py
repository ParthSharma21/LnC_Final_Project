import socket
import threading
import json
import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
import serverFunctions as sf
import RecommendationEngine.RecommendationEngine as re
import detailedReviewHandler as drh
import foodPreferenceUpdate as fpu
import adminController as ac
import chefController as cc
import employeeController as ec

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
                response = ac.handle_add_food_item(request_data)
            elif action == 'updateFoodItem':
                response = ac.handle_update_food_item(request_data)
            elif action == 'deleteFoodItem':
                response = ac.handle_delete_food_item(request_data)
            elif action == 'viewMenu':
                response = ac.handle_view_menu()

            elif action == 'getRecommendedFoodItems':
                response = cc.getRecommendedFoodItems()
            elif action == 'rolloutMenu':
                response = cc.rolloutMenu(request_data)
            elif action == 'notifyEmployees':
                response = cc.notifyEmployees(request_data)
            elif action == 'generateReport':
                response = cc.generateReport()
            elif action == 'getPoorPerformingItems':
                response = cc.getPoorPerformingItems(request_data)
            elif action == "discardFoodItem":
                response = cc.discardFoodItem(request_data)
            elif action == "requestDetailedReview":
                response = cc.requestDetailedReview(request_data)
            
            elif action == 'viewDailyMenu':
                response = ec.viewDailyMenu(request_data)
            elif action == 'viewNotifications':
                response = ec.viewNotifications()
            elif action == 'orderFood':
                response = ec.orderFood(request_data)
            elif action == 'giveFeedback':
                response = ec.giveFeedback(request_data)
            elif action == 'requestFeedbackItems':
                response = ec.requestFeedbackItems(request_data)
            elif action == 'check_detailed_feedback':
                response = ec.checkDetailedFeedback(request_data)
            elif action == 'submit_detailed_feedback':
                response = ec.submitDetailedFeedback(request_data)
            elif action == 'updateProfile':
                response = fpu.update_profile(request_data)

            else:
                response = {"status": "error", "message": "Invalid action"}

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
