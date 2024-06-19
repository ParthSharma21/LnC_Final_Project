import socket
import json
import classes  
import clientFunctions as cf

HOST = '127.0.0.1'
PORT = 12345

def startClient():
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

        user = {"userType": userType, "userID": userID, "password": password}
        client.send(json.dumps(user).encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "error":
            print(response["message"])
        else:
            loginAllowed(response["data"])
    
    client.close()

def loginAllowed(userDetails):

    userID, userName, userType, userPassword = userDetails
    print(f"\nLogin successful! Hello {userName}!")

    if userType == 'admin':
        adminUser = classes.Admin(userID, userPassword, userName)
        cf.adminMenu(adminUser)

    elif userType == 'chef':
        chefUser = classes.Chef(userID, userPassword, userName)
        cf.chefMenu(chefUser)

    elif userType == 'employee':
        employeeUser = classes.employee(userID, userPassword, userName)
        cf.employeeMenu(employeeUser)


if __name__ == "__main__":
    startClient()
