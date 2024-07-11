import Server.databaseFunctions as df
import mysql.connector
from mysql.connector import Error

def UserLogin(user):
    try:        
        user_type = user.get('userType')
        if user_type == 1:
            return AdminLogin(user['userID'], user['password'])
        elif user_type == 2:
            return ChefLogin(user['userID'], user['password'])
        elif user_type == 3:
            return EmployeeLogin(user['userID'], user['password'])
        else:
            return {"status": "error", "message": "Invalid user type"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def Authenticate(UserType, UserID, UserPassword):
    try:
        connection = df.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE UserRole = %s AND UserID = %s AND UserPassword = %s"
        cursor.execute(query, (UserType, UserID, UserPassword))

        result = cursor.fetchone()
        cursor.close()
        df.close_connection(connection)

        if result:
            return {"status": "success", "data": result}
        else:
            return {"status": "error", "message": "Invalid User ID or Password"}
    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def AdminLogin(AdminID, AdminPassword):
    try:
        return Authenticate("Admin", AdminID, AdminPassword)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def ChefLogin(ChefID, ChefPassword):
    try:
        return Authenticate("Chef", ChefID, ChefPassword)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def EmployeeLogin(EmployeeID, EmployeePassword):
    try:
        return Authenticate("Employee", EmployeeID, EmployeePassword)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

if __name__ == "__main__":
    try:
        user_type = int(input("Enter User Type (1 for Admin, 2 for Chef, 3 for Employee): "))
        if user_type not in [1, 2, 3]:
            print("Invalid user type")
        else:
            UserLogin(user_type)
    except ValueError:
        print("Please enter a valid integer for user type")
    except Exception as e:
        print(f"An error occurred: {e}")
