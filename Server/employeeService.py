import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
from datetime import datetime, timedelta
from SentimentAnalysisEngine import SentimentalAnalyser as sentiment



def handleViewDailyMenu(requestData):
    try:
        userID = requestData['userID']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("""
            SELECT FoodType, SpiceLevel, IsSweet, CusineType
            FROM UserPreference
            WHERE UserID = %s
        """, (userID,))
        userPreferences = cursor.fetchone()

        if not userPreferences:
            return {"status": "error", "message": "User preferences not found"}

        foodType, spiceLevel, isSweet, cusineType = userPreferences

        print(userPreferences)

        query = """
            SELECT dm.FoodItemID, dm.FoodItemName, dm.FoodItemPrice,
						(CASE WHEN IFNULL(fd.FoodType, 0) = %s THEN 1 ELSE 0 END +
						 CASE WHEN IFNULL(fd.SpiceLevel, 0) = %s THEN 1 ELSE 0 END +
						 CASE WHEN IFNULL(fd.IsSweet, 0) = %s THEN 1 ELSE 0 END +
						 CASE WHEN IFNULL(fd.CusineType, 0) = %s THEN 1 ELSE 0 END) AS PreferenceScore
            FROM DailyMenu dm
            LEFT JOIN FoodDetails fd ON dm.FoodItemID = fd.FoodItemID
            ORDER BY PreferenceScore DESC, dm.FoodItemName
        """
        cursor.execute(query, (foodType, spiceLevel, isSweet, cusineType))
        dailyMenu = cursor.fetchall()

        print(dailyMenu)

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "data": dailyMenu}

    except Exception as e:
        return {"status": "error", "message": str(e)}




def handleViewNotifications():
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = """
            SELECT NotificationMessage FROM Notifications
            WHERE NotificationGeneratedAtTimeStamp >= NOW() - INTERVAL 1 DAY
        """
        cursor.execute(query)
        notifications = cursor.fetchall()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "data": [n[0] for n in notifications]}

    except Exception as e:
        return {"status": "error", "message": str(e)}



def handleOrderFood(requestData):
    try:
        foodItemIDs = requestData['foodItemIDs']
        userID = requestData['userID']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("INSERT INTO Orders (UserID, OrderDate) VALUES (%s, %s)", (userID, datetime.now().date()))
        idForThisOrder = cursor.lastrowid

        for foodItemID in foodItemIDs:
            cursor.execute("INSERT INTO UserOrderDetails (OrderID, FoodItemID) VALUES (%s, %s)", (idForThisOrder, foodItemID))

        connection.commit()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Order placed successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}




def getLastOrderDetails(userID):
    connection = db.startConnection()
    if not connection:
        return None, "Failed to connect to the database."

    cursor = connection.cursor()
    query = """
        SELECT OrderID, OrderDate
        FROM Orders
        WHERE UserID = %s
        ORDER BY OrderDate DESC, OrderID DESC
        LIMIT 1
    """
    try:
        cursor.execute(query, (userID,))
        orderDetails = cursor.fetchone()
        if orderDetails:
            return orderDetails[0], orderDetails[1]
        else:
            return None, "No orders found."
    except Exception as e:
        return None, f"Failed to retrieve order details. Error: {e}"
    finally:
        cursor.close()
        db.closeConnection(connection)

def getOrderedFoodItems(orderID, userID):
    connection = db.startConnection()
    if not connection:
        return None, "Failed to connect to the database."

    cursor = connection.cursor()
    query = """
        SELECT m.FoodItemID, m.FoodItemName
        FROM UserOrderDetails uod
        JOIN Menu m ON uod.FoodItemID = m.FoodItemID
        WHERE uod.OrderID = %s
        AND m.IsDiscarded = FALSE
        AND uod.FoodItemID NOT IN (
            SELECT FoodItemID FROM Feedback
            WHERE UserID = %s AND OrderID = %s
        )
    """
    try:
        cursor.execute(query, (orderID, userID, orderID))
        orderedItems = cursor.fetchall()
        if orderedItems:
            return [{"FoodItemID": item[0], "FoodItemName": item[1]} for item in orderedItems]
        else:
            return []
    except Exception as e:
        return None, f"Failed to retrieve ordered items. Error: {e}"
    finally:
        cursor.close()
        db.closeConnection(connection)

def insertFeedback(userID, orderID, foodItemID, rating, comments, orderDate):
    connection = db.startConnection()
    if not connection:
        return "Failed to connect to the database."

    cursor = connection.cursor()
    query = """
        INSERT INTO Feedback (UserID, OrderID, FoodItemID, FoodReviewRating, FoodReviewComments, FoodReviewDate, Sentiment)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        sentimentValue = sentiment.analyzeSentiment(comments)
        cursor.execute(query, (userID, orderID, foodItemID, rating, comments, orderDate, sentimentValue))
        connection.commit()
        return "Feedback submitted successfully!"
    except Exception as e:
        return f"Failed to submit feedback. Error: {e}"
    finally:
        cursor.close()
        db.closeConnection(connection)




def handleGiveFeedback(requestData):
    try:
        userID = requestData['userID']
        foodItemID = requestData['foodItemID']
        rating = requestData['rating']
        comments = requestData['comments']

        orderID, orderDateMessage = getLastOrderDetails(userID)
        if not orderID:
            return {"status": "error", "message": orderDateMessage}

        orderedItems = getOrderedFoodItems(orderID, userID)
        if not orderedItems:
            return {"status": "error", "message": "No items found in the last order or feedback already given for all items."}

        itemExists = any(item['FoodItemID'] == foodItemID for item in orderedItems)
        if not itemExists:
            return {"status": "error", "message": "Invalid food item ID or feedback already given for this item."}

        feedbackMessage = insertFeedback(userID, orderID, foodItemID, rating, comments, orderDateMessage)
        if "successfully" in feedbackMessage:
            return {"status": "success", "message": feedbackMessage}
        else:
            return {"status": "error", "message": feedbackMessage}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


def handleRequestFeedbackItems(requestData):
    try:
        userID = requestData['userID']
        
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}
        
        cursor = connection.cursor()
        
        queryLastOrder = """
            SELECT OrderID, OrderDate
            FROM Orders
            WHERE UserID = %s
            ORDER BY OrderDate DESC, OrderID DESC
            LIMIT 1
        """
        cursor.execute(queryLastOrder, (userID,))
        lastOrder = cursor.fetchone()
        if not lastOrder:
            return {"status": "error", "message": "No orders found"}
        
        orderID, orderDate = lastOrder
        
        queryOrderedItems = """
            SELECT m.FoodItemID, m.FoodItemName
            FROM UserOrderDetails uod
            JOIN Menu m ON uod.FoodItemID = m.FoodItemID
            WHERE uod.OrderID = %s
            AND m.IsDiscarded = FALSE
            AND uod.FoodItemID NOT IN (
                SELECT FoodItemID FROM Feedback
                WHERE UserID = %s AND OrderID = %s
            )
        """
        cursor.execute(queryOrderedItems, (orderID, userID, orderID))
        itemsToFeedback = cursor.fetchall()

        if not itemsToFeedback:
            return {"status": "success", "data": [], "message": "No items pending feedback for the last order"}
        
        itemsList = [{"FoodItemID": item[0], "FoodItemName": item[1]} for item in itemsToFeedback]

        cursor.close()
        db.closeConnection(connection)
        
        return {"status": "success", "data": itemsList}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
