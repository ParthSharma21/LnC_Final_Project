import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
from datetime import datetime, timedelta
from SentimentAnalysisEngine import SentimentalAnalyser as sentiment

def handleLogin(requestData):
    user = {
        "userType": requestData['userType'],
        "userID": requestData['userID'],
        "password": requestData['password']
    }
    AuthenticationResponse = Login.UserLogin(user)
    return AuthenticationResponse
'''
# def handleAddFoodItem(requestData):
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

# def handleUpdateFoodItem(requestData):
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

# def handleDeleteFoodItem(requestData):
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

# def handleViewMenu():
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

# def rolloutMenu(requestData):
    try:
        foodItemsToRollOutIDs = requestData['foodItemIDs']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE DailyMenu")
        for itemID in foodItemsToRollOutIDs:
            cursor.execute(
                "INSERT INTO DailyMenu (FoodItemID, FoodItemName, FoodItemPrice) "
                "SELECT FoodItemID, FoodItemName, FoodItemPrice FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", 
                (itemID,)
            )
        connection.commit()

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Food items rolled out successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# def notifyEmployees(requestData):
    try:
        message = requestData['message']
        date = requestData['date']
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Notifications (NotificationMessage, NotificationGeneratedAtTimeStamp, GeneratedByUserID) "
            "VALUES (%s, %s, %s)", 
            (message + str(date), datetime.now(), requestData['userID'])
        )
        connection.commit()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Employees notified successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# def generateReport():
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        date30DaysAgo = datetime.now() - timedelta(days=30)

        cursor.execute("""
            SELECT 
                m.FoodItemName, 
                COUNT(uod.FoodItemID) AS OrderCount
            FROM 
                UserOrderDetails uod
            JOIN 
                Orders o ON uod.OrderID = o.OrderID
            JOIN 
                Menu m ON uod.FoodItemID = m.FoodItemID
            WHERE 
                o.OrderDate >= %s
                AND m.IsDiscarded = FALSE
            GROUP BY 
                m.FoodItemName
            ORDER BY 
                OrderCount DESC
        """, (date30DaysAgo,))

        reportData = cursor.fetchall()
        db.closeConnection(connection)

        if not reportData:
            return {"status": "success", "data": [], "message": "No sales in the last 30 days."}

        report = []
        for item in reportData:
            report.append({"FoodItemName": item[0], "OrderCount": item[1]})

        return {"status": "success", "data": report, "message": "Sales report generated successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# def handleViewDailyMenu(requestData):
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

# def handleViewNotifications():
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

# def handleOrderFood(requestData):
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

# def handleRequestFeedbackItems(requestData):
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

# def getLastOrderDetails(userID):
#     connection = db.startConnection()
#     if not connection:
#         return None, "Failed to connect to the database."

#     cursor = connection.cursor()
#     query = """
#         SELECT OrderID, OrderDate
#         FROM Orders
#         WHERE UserID = %s
#         ORDER BY OrderDate DESC, OrderID DESC
#         LIMIT 1
#     """
#     try:
#         cursor.execute(query, (userID,))
#         orderDetails = cursor.fetchone()
#         if orderDetails:
#             return orderDetails[0], orderDetails[1]
#         else:
#             return None, "No orders found."
#     except Exception as e:
#         return None, f"Failed to retrieve order details. Error: {e}"
#     finally:
#         cursor.close()
#         db.closeConnection(connection)

# def getOrderedFoodItems(orderID, userID):
#     connection = db.startConnection()
#     if not connection:
#         return None, "Failed to connect to the database."

#     cursor = connection.cursor()
#     query = """
#         SELECT m.FoodItemID, m.FoodItemName
#         FROM UserOrderDetails uod
#         JOIN Menu m ON uod.FoodItemID = m.FoodItemID
#         WHERE uod.OrderID = %s
#         AND m.IsDiscarded = FALSE
#         AND uod.FoodItemID NOT IN (
#             SELECT FoodItemID FROM Feedback
#             WHERE UserID = %s AND OrderID = %s
#         )
#     """
#     try:
#         cursor.execute(query, (orderID, userID, orderID))
#         orderedItems = cursor.fetchall()
#         if orderedItems:
#             return [{"FoodItemID": item[0], "FoodItemName": item[1]} for item in orderedItems]
#         else:
#             return []
#     except Exception as e:
#         return None, f"Failed to retrieve ordered items. Error: {e}"
#     finally:
#         cursor.close()
#         db.closeConnection(connection)

# def insertFeedback(userID, orderID, foodItemID, rating, comments, orderDate):
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

# def handleGiveFeedback(requestData):
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
'''