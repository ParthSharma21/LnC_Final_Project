######## authenticationAndLogin.py

import Server.databaseFunctions as df
import mysql.connector
from mysql.connector import Error

def UserLogin(user):
    if user['userType'] == 1:
        return AdminLogin(user['userID'], user['password'])
    elif user['userType'] == 2:
        return ChefLogin(user['userID'], user['password'])
    else:
        return EmployeeLogin(user['userID'], user['password'])

def Authenticate(UserType, UserID, UserPassword):
    connection = df.start_connection()
    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()
    
    # Create SQL query
    query = "SELECT * FROM user WHERE UserRole = %s AND UserID = %s AND UserPassword = %s"
    
    # Execute the query
    cursor.execute(query, (UserType, UserID, UserPassword))
    
    # Fetch one result
    result = cursor.fetchone()
    
    # Close the database connection
    df.close_connection(connection)
    
    # Check if a result is returned
    if result:
        return {"status": "success", "data": result}
    else:
        return {"status": "error", "message": "Invalid User ID or Password"}

def AdminLogin(AdminID, AdminPassword):
    AuthenticationResponse = Authenticate("Admin", AdminID, AdminPassword)
    return AuthenticationResponse

def ChefLogin(ChefID, ChefPassword):
    AuthenticationResponse = Authenticate("Chef", ChefID, ChefPassword)
    return AuthenticationResponse

def EmployeeLogin(EmployeeID, EmployeePassword):
    AuthenticationResponse = Authenticate("Employee", EmployeeID, EmployeePassword)
    return AuthenticationResponse

# Example usage
if __name__ == "__main__":
    user_type = int(input("Enter User Type (1 for Admin, 2 for Chef, 3 for Employee): "))
    UserLogin(user_type)
