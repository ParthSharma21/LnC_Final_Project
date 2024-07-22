import socket
import threading
import json
import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
import Server.serverFunctions as sf
import RecommendationEngine.RecommendationEngine as re
import Server.detailedReviewHandler as drh
import Server.foodPreferenceUpdate as fpu
import Server.adminController as ac
import Server.chefController as cc
import Server.employeeController as ec

# Server host and port
HOST = '127.0.0.1'
PORT = 12345

def handleClient(clientSocket, clientAddress):
    print(f"[NEW CONNECTION] {clientAddress} connected.")
    
    while True:
        try:
            requestData = clientSocket.recv(1024).decode('utf-8')
            if not requestData:
                break
            
            requestData = json.loads(requestData)
            action = requestData.get('action')

            if not action:
                response = {"status": "error", "message": "No action specified"}
            elif action == 'login':
                response = sf.handleLogin(requestData)
            elif action == 'addFoodItem':
                response = ac.handleAddFoodItem(requestData)
            elif action == 'updateFoodItem':
                response = ac.handleUpdateFoodItem(requestData)
            elif action == 'deleteFoodItem':
                response = ac.handleDeleteFoodItem(requestData)
            elif action == 'viewMenu':
                response = ac.handleViewMenu()


            elif action == 'getRecommendedFoodItems':
                response = cc.getRecommendedFoodItems()
            elif action == 'rolloutMenu':
                response = cc.rolloutMenu(requestData)
            elif action == 'notifyEmployees':
                response = cc.notifyEmployees(requestData)
            elif action == 'generateReport':
                response = cc.generateReport()
            elif action == 'getPoorPerformingItems':
                response = cc.getPoorPerformingItems(requestData)
            elif action == "discardFoodItem":
                response = cc.discardFoodItem(requestData)
            elif action == "requestDetailedReview":
                response = cc.requestDetailedReview(requestData)


            elif action == 'viewDailyMenu':
                response = ec.viewDailyMenu(requestData)
            elif action == 'viewNotifications':
                response = ec.viewNotifications()
            elif action == 'orderFood':
                response = ec.orderFood(requestData)
            elif action == 'giveFeedback':
                response = ec.giveFeedback(requestData)
            elif action == 'requestFeedbackItems':
                response = ec.requestFeedbackItems(requestData)
            elif action == 'checkDetailedFeedback':
                response = ec.checkDetailedFeedback(requestData)
            elif action == 'submitDetailedFeedback':
                response = ec.submitDetailedFeedback(requestData)
            elif action == 'updateProfile':
                response = fpu.updateProfile(requestData)
            else:
                response = {"status": "error", "message": "Invalid action"}

            responseJson = json.dumps(response)
            clientSocket.send(responseJson.encode('utf-8'))
        
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Invalid JSON format"}
            clientSocket.send(json.dumps(response).encode('utf-8'))
        except ConnectionResetError:
            break
        except Exception as e:
            response = {"status": "error", "message": f"An error occurred: {e}"}
            clientSocket.send(json.dumps(response).encode('utf-8'))

    print(f"[DISCONNECTED] {clientAddress} disconnected.")
    clientSocket.close()

def startServer():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
        
        while True:
            clientSocket, clientAddress = server.accept()
            clientThread = threading.Thread(target=handleClient, args=(clientSocket, clientAddress))
            clientThread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except Exception as e:
        print(f"An error occurred while starting the server: {e}")

if __name__ == "__main__":
    startServer()
