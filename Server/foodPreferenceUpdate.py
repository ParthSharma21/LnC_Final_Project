import Server.databaseFunctions as db
from mysql.connector import Error

def updateProfile(requestData):
    try:

        userID = requestData['userID']
        foodType = requestData['foodType']
        spiceLevel = requestData['spiceLevel']
        cuisineType = requestData['cuisineType']
        sweetPreference = requestData['sweetPreference']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        cursor.execute("SELECT UserPreferenceID FROM UserPreference WHERE UserID = %s", (userID,))
        result = cursor.fetchone()

        if result:
            query = """
                UPDATE UserPreference
                SET FoodType = %s, SpiceLevel = %s, IsSweet = %s, CusineType = %s
                WHERE UserID = %s
            """
            cursor.execute(query, (foodType, spiceLevel, sweetPreference, cuisineType, userID))
        else:
            query = """
                INSERT INTO UserPreference (UserID, FoodType, SpiceLevel, IsSweet, CusineType)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (userID, foodType, spiceLevel, sweetPreference, cuisineType))

        connection.commit()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Profile updated successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}
