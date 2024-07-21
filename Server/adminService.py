import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
from datetime import datetime, timedelta
from SentimentAnalysisEngine import SentimentalAnalyser as sentiment



def handleAddFoodItem(requestData):
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        foodItem = {
            "FoodItemName": requestData['foodItemName'],
            "FoodItemPrice": requestData['foodItemPrice'],
            "FoodItemAvailability": 1,
            "IsDiscarded": False
        }

        query = "INSERT INTO Menu (FoodItemName, FoodItemPrice, FoodItemAvailability, IsDiscarded) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (foodItem['FoodItemName'], foodItem['FoodItemPrice'], foodItem['FoodItemAvailability'], foodItem['IsDiscarded']))
        connection.commit()

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Food item added successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    


def handleUpdateFoodItem(requestData):
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        foodItem = {
            "FoodItemID": requestData['foodItemID'],
            "FoodItemName": requestData['foodItemName'],
            "FoodItemPrice": requestData['foodItemPrice'],
            "FoodItemAvailability": requestData['foodItemAvailability']
        }

        query = "UPDATE Menu SET FoodItemName = %s, FoodItemPrice = %s, FoodItemAvailability = %s WHERE FoodItemID = %s"
        cursor.execute(query, (foodItem['FoodItemName'], foodItem['FoodItemPrice'], foodItem['FoodItemAvailability'], foodItem['FoodItemID']))
        connection.commit()

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Food item updated successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}




def handleDeleteFoodItem(requestData):
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        foodItemID = requestData['foodItemID']

        query = "DELETE FROM Menu WHERE FoodItemID = %s"
        cursor.execute(query, (foodItemID,))
        connection.commit()

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Food item deleted successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}




def handleViewMenu():
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = "SELECT FoodItemID, FoodItemName, FoodItemPrice, FoodItemAvailability FROM Menu WHERE IsDiscarded = FALSE"
        cursor.execute(query)
        menu = cursor.fetchall()
        print(menu)
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "data": menu}

    except Exception as e:
        return {"status": "error", "message": str(e)}
