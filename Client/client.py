import socket
import json
import Client.classes as classes  
import ClientFunctions as cf

# Server host and port
HOST = '127.0.0.1'
PORT = 12345

def mainMenu():
    print("\nWelcome to Food Management System!!\n")
    print("Enter User type:")
    print("1. Admin")
    print("2. Chef")
    print("3. Employee")
    print("Enter 4 to Exit.\n")
    userType = input("Enter your choice: ")
    return userType

def getUserCredentials():
    userID = input("Enter ID: ")
    password = input("Enter Password: ")
    return userID, password

def handleResponse(response, client):
    if response["status"] == "error":
        print(response["message"])
    else:
        userID, userName, userType, userPassword = response["data"]
        print(f"\nLogin successful! Hello {userName}!")

        if userType == 'admin':
            adminUser = classes.Admin(userID, userName, userPassword)
            cf.adminHandler(adminUser, client)

        elif userType == 'chef':
            chefUser = classes.Chef(userID, userName, userPassword)
            cf.chefHandler(chefUser, client)

        elif userType == 'employee':
            employeeUser = classes.Employee(userID, userName, userPassword)
            cf.employeeHandler(employeeUser, client)

def startClient():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    while True:
        try:
            userType = mainMenu()
            if not userType.isdigit() or int(userType) not in [1, 2, 3, 4]:
                print("Invalid choice. Please enter a valid option.")
                continue

            userType = int(userType)
            if userType == 4:
                print("Exiting...")
                break

            userID, password = getUserCredentials()

            if not userID or not password:
                print("ID and Password cannot be empty.")
                continue

            user = {"action": "login", "userType": userType, "userID": userID, "password": password}
            client.send(json.dumps(user).encode('utf-8'))
            
            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)

            handleResponse(response, client)
        except Exception as e:
            print(f"An error occurred: {e}")

    client.close()

if __name__ == "__main__":
    startClient()
