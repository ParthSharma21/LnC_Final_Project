# detailedReviewHandler.py

import Server.databaseFunctions as db
import RecommendationEngine.RecommendationEngine as re
from datetime import datetime

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

    except Exception as e:
        return {"status": "error", "message": str(e)}
    



# response = get_poor_performing_items(2,30)

# print(response)


def discard_food_item(request_data):
    try:
        food_item_id = request_data['foodItemID']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        # Insert into DiscardMenuItems
        insert_query = """
            INSERT INTO DiscardMenuItems (FoodItemID, FoodItemName, DiscardDate)
            SELECT FoodItemID, FoodItemName, NOW()
            FROM Menu
            WHERE FoodItemID = %s
        """
        cursor.execute(insert_query, (food_item_id,))

        # Remove from Menu
        delete_query = "DELETE FROM Menu WHERE FoodItemID = %s"
        cursor.execute(delete_query, (food_item_id,))

        connection.commit()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Food item discarded successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    



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

    except Exception as e:
        return {"status": "error", "message": str(e)}
    


def request_detailed_review(request_data):
    try:
        food_item_id = request_data['foodItemID']
        user_id = request_data['userID']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        # Fetch food item name for notification
        cursor.execute("SELECT FoodItemName FROM Menu WHERE FoodItemID = %s", (food_item_id,))
        food_item_name = cursor.fetchone()[0]

        # Generate notification
        notification_message = f"Chef has requested detailed review for {food_item_name}."
        notification_response = generate_notification(user_id, notification_message)
        if notification_response["status"] == "error":
            return notification_response

        notification_id = notification_response["notification_id"]

        # Insert into DetailedReviewRequiredItem
        query = """
            INSERT INTO DetailedReviewRequiredItem(FoodItemID, FoodItemName, NotificationID)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (food_item_id, food_item_name, notification_id))
        connection.commit()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Detailed review requested successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    

# def request_detailed_review(request_data):
#     try:
#         food_item_id = request_data['foodItemID']
#         user_id = request_data.get('userID')

#         connection = db.start_connection()
#         if not connection:
#             return {"status": "error", "message": "Database connection failed"}

#         cursor = connection.cursor()

#         # Fetch food item name for notification
#         cursor.execute("SELECT FoodItemName FROM Menu WHERE FoodItemID = %s", (food_item_id,))
#         food_item_name = cursor.fetchone()[0]

#         # Insert into DetailedReviewRequiredItem
#         query = """
#             INSERT INTO DetailedReviewRequiredItem(FoodItemID, FoodItemName)
#             VALUES (%s, %s)
#         """
#         cursor.execute(query, (food_item_id, food_item_name))
#         connection.commit()

#         # Generate notification
#         notification_message = f"Chef has requested detailed review for {food_item_name}."
#         notification_response = generate_notification(user_id, notification_message)
#         if notification_response["status"] == "error":
#             return notification_response

#         cursor.close()
#         db.close_connection(connection)

#         return {"status": "success", "message": "Detailed review requested successfully"}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}

