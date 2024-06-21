# client.py
import socket
import json
import Client.classes as classes  
import ClientFunctions as cf

# Server host and port
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    while True:
        print("\nWelcome to Food Management System!!\n")
        print("Enter User type:")
        print("1. Admin")
        print("2. Chef")
        print("3. Employee")
        print("Enter 4 to Exit.\n")
        userType = int(input("Enter your choice: "))

        if userType == 4:
            print("Exiting...")
            break

        userID = input("Enter ID: ")
        password = input("Enter Password: ")

        user = {"action": "login", "userType": userType, "userID": userID, "password": password}
        client.send(json.dumps(user).encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "error":
            print(response["message"])
        else:
            print(response["data"])

            userID, userName, userType, userPassword = response["data"]
            print(f"\nLogin successful! Hello {userName}!")

            if userType == 'admin':
                adminUser = classes.Admin(userID, userName, userPassword)
                cf.adminHandler(adminUser,client)
                pass

            elif userType == 'chef':
                chefUser = classes.Chef(userID, userName, userPassword)
                cf.chefHandler(chefUser,client)
                pass

            elif userType == 'employee':
                employeeUser = classes.employee(userID, userName, userPassword)
                cf.employeeHandler(employeeUser,client)
                pass
    
    client.close()



if __name__ == "__main__":
    start_client()
