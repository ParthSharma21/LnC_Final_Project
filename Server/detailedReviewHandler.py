import Server.databaseFunctions as db
import RecommendationEngine.RecommendationEngine as re
from datetime import datetime
from mysql.connector import Error

def getPoorPerformingItems(threshold=2, days=30):
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = """
            SELECT 
                m.FoodItemID, m.FoodItemName, AVG(f.FoodReviewRating) AS AverageRating, AVG(f.Sentiment) AS AverageSentiment
            FROM 
                Feedback f
            JOIN 
                Menu m ON f.FoodItemID = m.FoodItemID
            WHERE 
                f.FoodReviewDate >= NOW() - INTERVAL %s DAY
                AND m.IsDiscarded = FALSE
            GROUP BY 
                m.FoodItemID, m.FoodItemName
            HAVING 
                AverageRating <= %s AND AverageSentiment < 0
            ORDER BY 
                AverageRating ASC, AverageSentiment ASC
        """
        cursor.execute(query, (days, threshold))
        poorPerformingItems = cursor.fetchall()
        cursor.close()
        db.closeConnection(connection)

        items = [{"FoodItemID": item[0], "FoodItemName": item[1], "AverageRating": re.decimalToFloat(item[2]), "AverageSentiment": item[3]} for item in poorPerformingItems]

        return {"status": "success", "data": items}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def discardFoodItem(requestData):
    try:
        if 'foodItemID' not in requestData:
            return {"status": "error", "message": "Missing food item ID"}

        foodItemID = requestData['foodItemID']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        query = """
            SELECT AVG(f.FoodReviewRating) AS AvgRating, AVG(f.Sentiment) AS AvgSentiment
            FROM Feedback f
            WHERE f.FoodItemID = %s
        """
        cursor.execute(query, (foodItemID,))
        result = cursor.fetchone()
        avgRating = result[0] if result[0] is not None else 0
        avgSentiment = result[1] if result[1] is not None else 0

        cursor.execute("SELECT FoodItemName FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", (foodItemID,))
        foodItem = cursor.fetchone()
        if not foodItem:
            return {"status": "error", "message": "Food item not found or already discarded"}

        foodItemName = foodItem[0]

        insertQuery = """
            INSERT INTO DiscardMenuItems (FoodItemID, FoodItemName, AvgRating, AvgSentiment, DiscardDate)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(insertQuery, (foodItemID, foodItemName, avgRating, avgSentiment))

        updateMenuQuery = "UPDATE Menu SET IsDiscarded = TRUE WHERE FoodItemID = %s"
        cursor.execute(updateMenuQuery, (foodItemID,))

        connection.commit()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Food item discarded successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def generateNotification(userID, message, notificationType=2):
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = """
            INSERT INTO Notifications (NotificationMessage, NotificationGeneratedAtTimeStamp, GeneratedByUserID, NotificationType)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (message, datetime.now(), userID, notificationType))
        connection.commit()

        cursor.execute("SELECT MAX(NotificationID) FROM Notifications")
        notificationID = cursor.fetchone()[0]

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Notification generated successfully", "notificationID": notificationID}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def requestDetailedReview(requestData):
    try:
        if 'foodItemID' not in requestData or 'userID' not in requestData:
            return {"status": "error", "message": "Missing food item ID or user ID"}

        foodItemID = requestData['foodItemID']
        userID = requestData['userID']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        cursor.execute("SELECT FoodItemName FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", (foodItemID,))
        foodItem = cursor.fetchone()
        if not foodItem:
            return {"status": "error", "message": "Food item not found or already discarded"}

        foodItemName = foodItem[0]

        notificationMessage = f"Chef has requested detailed review for {foodItemName}."
        notificationResponse = generateNotification(userID, notificationMessage)
        if notificationResponse["status"] == "error":
            return notificationResponse

        notificationID = notificationResponse["notificationID"]

        query = """
            INSERT INTO DetailedReviewRequiredItem(FoodItemID, FoodItemName, NotificationID)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (foodItemID, foodItemName, notificationID))
        connection.commit()

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Detailed review requested successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def checkDetailedFeedback(requestData):
    userID = requestData.get('UserID')
    if not userID:
        return {"status": "error", "message": "User ID is required"}
    
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = """
            SELECT dri.FoodItemName, dri.NotificationID, dri.FoodItemID 
            FROM DetailedReviewRequiredItem dri
            LEFT JOIN DetailedFeedback df ON dri.NotificationID = df.NotificationID AND df.UserID = %s
            WHERE df.DetailedFeedbackID IS NULL
        """
        cursor.execute(query, (userID,))
        items = cursor.fetchall()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "items": items}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def submitDetailedFeedback(requestData):
    try:
        if 'UserID' not in requestData or 'NotificationID' not in requestData or 'FoodItemID' not in requestData or 'detailedFeedback' not in requestData:
            return {"status": "error", "message": "Missing required fields"}
        
        userID = requestData['UserID']
        notificationID = requestData['NotificationID']
        foodItemID = requestData['FoodItemID']
        feedback = requestData['detailedFeedback']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        for entry in feedback:
            if 'AnswerToQueID' not in entry or 'DetailedFeedback' not in entry:
                return {"status": "error", "message": "Feedback entry missing required fields"}

            answerToQueID = entry['AnswerToQueID']
            detailedFeedback = entry['DetailedFeedback']
            query = """
                INSERT INTO DetailedFeedback (NotificationID, UserID, FoodItemID, AnswerToQueID, DetailedFeedback)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (notificationID, userID, foodItemID, answerToQueID, detailedFeedback))
        connection.commit()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Detailed feedback submitted successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}
