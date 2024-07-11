import Server.databaseFunctions as db
import RecommendationEngine.RecommendationEngine as re
from datetime import datetime
from mysql.connector import Error

def get_poor_performing_items(threshold=2, days=30):
    try:
        connection = db.start_connection()
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
        poor_performing_items = cursor.fetchall()
        cursor.close()
        db.close_connection(connection)

        items = [{"FoodItemID": item[0], "FoodItemName": item[1], "AverageRating": re.decimal_to_float(item[2]), "AverageSentiment": item[3]} for item in poor_performing_items]

        return {"status": "success", "data": items}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def discard_food_item(request_data):
    try:
        if 'foodItemID' not in request_data:
            return {"status": "error", "message": "Missing food item ID"}

        food_item_id = request_data['foodItemID']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        query = """
            SELECT AVG(f.FoodReviewRating) AS AvgRating, AVG(f.Sentiment) AS AvgSentiment
            FROM Feedback f
            WHERE f.FoodItemID = %s
        """
        cursor.execute(query, (food_item_id,))
        result = cursor.fetchone()
        avg_rating = result[0] if result[0] is not None else 0
        avg_sentiment = result[1] if result[1] is not None else 0

        cursor.execute("SELECT FoodItemName FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", (food_item_id,))
        food_item = cursor.fetchone()
        if not food_item:
            return {"status": "error", "message": "Food item not found or already discarded"}

        food_item_name = food_item[0]

        insert_query = """
            INSERT INTO DiscardMenuItems (FoodItemID, FoodItemName, AvgRating, AvgSentiment, DiscardDate)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (food_item_id, food_item_name, avg_rating, avg_sentiment))

        update_menu_query = "UPDATE Menu SET IsDiscarded = TRUE WHERE FoodItemID = %s"
        cursor.execute(update_menu_query, (food_item_id,))

        connection.commit()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Food item discarded successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def generate_notification(user_id, message, notification_type=2):
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = """
            INSERT INTO Notifications (NotificationMessage, NotificationGeneratedAtTimeStamp, GeneratedByUserID, NotificationType)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (message, datetime.now(), user_id, notification_type))
        connection.commit()

        cursor.execute("SELECT MAX(NotificationID) FROM Notifications")
        notification_id = cursor.fetchone()[0]

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Notification generated successfully", "notification_id": notification_id}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def request_detailed_review(request_data):
    try:
        if 'foodItemID' not in request_data or 'userID' not in request_data:
            return {"status": "error", "message": "Missing food item ID or user ID"}

        food_item_id = request_data['foodItemID']
        user_id = request_data['userID']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        cursor.execute("SELECT FoodItemName FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", (food_item_id,))
        food_item = cursor.fetchone()
        if not food_item:
            return {"status": "error", "message": "Food item not found or already discarded"}

        food_item_name = food_item[0]

        notification_message = f"Chef has requested detailed review for {food_item_name}."
        notification_response = generate_notification(user_id, notification_message)
        if notification_response["status"] == "error":
            return notification_response

        notification_id = notification_response["notification_id"]

        query = """
            INSERT INTO DetailedReviewRequiredItem(FoodItemID, FoodItemName, NotificationID)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (food_item_id, food_item_name, notification_id))
        connection.commit()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Detailed review requested successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def check_detailed_feedback(request_data):
    user_id = request_data.get('UserID')
    if not user_id:
        return {"status": "error", "message": "User ID is required"}
    
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = """
            SELECT dri.FoodItemName, dri.NotificationID, dri.FoodItemID 
            FROM DetailedReviewRequiredItem dri
            LEFT JOIN DetailedFeedback df ON dri.NotificationID = df.NotificationID AND df.UserID = %s
            WHERE df.DetailedFeedbackID IS NULL
        """
        cursor.execute(query, (user_id,))
        items = cursor.fetchall()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "items": items}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}

def submit_detailed_feedback(request_data):
    try:
        if 'UserID' not in request_data or 'NotificationID' not in request_data or 'FoodItemID' not in request_data or 'detailedFeedback' not in request_data:
            return {"status": "error", "message": "Missing required fields"}
        
        user_id = request_data['UserID']
        notification_id = request_data['NotificationID']
        food_item_id = request_data['FoodItemID']
        feedback = request_data['detailedFeedback']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        for entry in feedback:
            if 'AnswerToQueID' not in entry or 'DetailedFeedback' not in entry:
                return {"status": "error", "message": "Feedback entry missing required fields"}

            answer_to_que_id = entry['AnswerToQueID']
            detailed_feedback = entry['DetailedFeedback']
            query = """
                INSERT INTO DetailedFeedback (NotificationID, UserID, FoodItemID, AnswerToQueID, DetailedFeedback)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (notification_id, user_id, food_item_id, answer_to_que_id, detailed_feedback))
        connection.commit()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Detailed feedback submitted successfully"}

    except Error as e:
        return {"status": "error", "message": f"Database error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}
