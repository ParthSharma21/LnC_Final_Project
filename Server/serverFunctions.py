import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
from datetime import datetime, timedelta
from SentimentAnalysisEngine import SentimentalAnalyser as sentiment

def handle_login(request_data):
    user = {
        "userType": request_data['userType'],
        "userID": request_data['userID'],
        "password": request_data['password']
    }
    AuthenticationResponse = Login.UserLogin(user)
    return AuthenticationResponse

def handle_add_food_item(request_data):
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        food_item = {
            "FoodItemName": request_data['foodItemName'],
            "FoodItemPrice": request_data['foodItemPrice'],
            "FoodItemAvailability": 1,
            "IsDiscarded": False
        }

        query = "INSERT INTO Menu (FoodItemName, FoodItemPrice, FoodItemAvailability, IsDiscarded) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (food_item['FoodItemName'], food_item['FoodItemPrice'], food_item['FoodItemAvailability'], food_item['IsDiscarded']))
        connection.commit()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Food item added successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_update_food_item(request_data):
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        food_item = {
            "FoodItemID": request_data['foodItemID'],
            "FoodItemName": request_data['foodItemName'],
            "FoodItemPrice": request_data['foodItemPrice'],
            "FoodItemAvailability": request_data['foodItemAvailability']
        }

        query = "UPDATE Menu SET FoodItemName = %s, FoodItemPrice = %s, FoodItemAvailability = %s WHERE FoodItemID = %s"
        cursor.execute(query, (food_item['FoodItemName'], food_item['FoodItemPrice'], food_item['FoodItemAvailability'], food_item['FoodItemID']))
        connection.commit()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Food item updated successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_delete_food_item(request_data):
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        food_item_id = request_data['foodItemID']

        query = "DELETE FROM Menu WHERE FoodItemID = %s"
        cursor.execute(query, (food_item_id,))
        connection.commit()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Food item deleted successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_view_menu():
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = "SELECT FoodItemID, FoodItemName, FoodItemPrice, FoodItemAvailability FROM Menu WHERE IsDiscarded = FALSE"
        cursor.execute(query)
        menu = cursor.fetchall()
        print(menu)
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "data": menu}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def rolloutMenu(request_data):
    try:
        foodItemsToRollOutIDs = request_data['foodItemIDs']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE DailyMenu")
        for item_id in foodItemsToRollOutIDs:
            cursor.execute(
                "INSERT INTO DailyMenu (FoodItemID, FoodItemName, FoodItemPrice) "
                "SELECT FoodItemID, FoodItemName, FoodItemPrice FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", 
                (item_id,)
            )
        connection.commit()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Food items rolled out successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def notifyEmployees(request_data):
    try:
        message = request_data['message']
        date = request_data['date']
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Notifications (NotificationMessage, NotificationGeneratedAtTimeStamp, GeneratedByUserID) "
            "VALUES (%s, %s, %s)", 
            (message + str(date), datetime.now(), request_data['userID'])
        )
        connection.commit()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Employees notified successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def generateReport():
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        date_30_days_ago = datetime.now() - timedelta(days=30)

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
        """, (date_30_days_ago,))

        report_data = cursor.fetchall()
        db.close_connection(connection)

        if not report_data:
            return {"status": "success", "data": [], "message": "No sales in the last 30 days."}

        report = []
        for item in report_data:
            report.append({"FoodItemName": item[0], "OrderCount": item[1]})

        return {"status": "success", "data": report, "message": "Sales report generated successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_view_daily_menu(request_data):
    try:
        user_id = request_data['userID']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("""
            SELECT FoodType, SpiceLevel, IsSweet, CusineType
            FROM UserPreference
            WHERE UserID = %s
        """, (user_id,))
        user_preferences = cursor.fetchone()

        if not user_preferences:
            return {"status": "error", "message": "User preferences not found"}

        food_type, spice_level, is_sweet, cusine_type = user_preferences

        query = """
            SELECT dm.FoodItemID, dm.FoodItemName, dm.FoodItemPrice,
                (CASE WHEN fd.FoodType = %s THEN 1 ELSE 0 END +
                 CASE WHEN fd.SpiceLevel = %s THEN 1 ELSE 0 END +
                 CASE WHEN fd.IsSweet = %s THEN 1 ELSE 0 END +
                 CASE WHEN fd.CusineType = %s THEN 1 ELSE 0 END) AS PreferenceScore
            FROM DailyMenu dm
            JOIN FoodDetails fd ON dm.FoodItemID = fd.FoodItemID
            ORDER BY PreferenceScore DESC, dm.FoodItemName
        """
        cursor.execute(query, (food_type, spice_level, is_sweet, cusine_type))
        daily_menu = cursor.fetchall()

        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "data": daily_menu}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_view_notifications():
    try:
        connection = db.start_connection()
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
        db.close_connection(connection)

        return {"status": "success", "data": [n[0] for n in notifications]}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_order_food(request_data):
    try:
        food_item_ids = request_data['foodItemIDs']
        user_id = request_data['userID']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("INSERT INTO Orders (UserID, OrderDate) VALUES (%s, %s)", (user_id, datetime.now().date()))
        id_for_this_order = cursor.lastrowid

        for food_item_id in food_item_ids:
            cursor.execute("INSERT INTO UserOrderDetails (OrderID, FoodItemID) VALUES (%s, %s)", (id_for_this_order, food_item_id))

        connection.commit()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Order placed successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_request_feedback_items(request_data):
    try:
        user_id = request_data['userID']
        
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}
        
        cursor = connection.cursor()
        
        query_last_order = """
            SELECT OrderID, OrderDate
            FROM Orders
            WHERE UserID = %s
            ORDER BY OrderDate DESC, OrderID DESC
            LIMIT 1
        """
        cursor.execute(query_last_order, (user_id,))
        last_order = cursor.fetchone()
        if not last_order:
            return {"status": "error", "message": "No orders found"}
        
        order_id, order_date = last_order
        
        query_ordered_items = """
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
        cursor.execute(query_ordered_items, (order_id, user_id, order_id))
        items_to_feedback = cursor.fetchall()

        if not items_to_feedback:
            return {"status": "success", "data": [], "message": "No items pending feedback for the last order"}
        
        items_list = [{"FoodItemID": item[0], "FoodItemName": item[1]} for item in items_to_feedback]

        cursor.close()
        db.close_connection(connection)
        
        return {"status": "success", "data": items_list}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_last_order_details(user_id):
    connection = db.start_connection()
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
        cursor.execute(query, (user_id,))
        order_details = cursor.fetchone()
        if order_details:
            return order_details[0], order_details[1]
        else:
            return None, "No orders found."
    except Exception as e:
        return None, f"Failed to retrieve order details. Error: {e}"
    finally:
        cursor.close()
        db.close_connection(connection)

def get_ordered_food_items(order_id, user_id):
    connection = db.start_connection()
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
        cursor.execute(query, (order_id, user_id, order_id))
        ordered_items = cursor.fetchall()
        if ordered_items:
            return [{"FoodItemID": item[0], "FoodItemName": item[1]} for item in ordered_items]
        else:
            return []
    except Exception as e:
        return None, f"Failed to retrieve ordered items. Error: {e}"
    finally:
        cursor.close()
        db.close_connection(connection)

def insert_feedback(user_id, order_id, food_item_id, rating, comments, order_date):
    connection = db.start_connection()
    if not connection:
        return "Failed to connect to the database."

    cursor = connection.cursor()
    query = """
        INSERT INTO Feedback (UserID, OrderID, FoodItemID, FoodReviewRating, FoodReviewComments, FoodReviewDate, Sentiment)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        sentiment_value = sentiment.analyze_sentiment(comments)
        cursor.execute(query, (user_id, order_id, food_item_id, rating, comments, order_date, sentiment_value))
        connection.commit()
        return "Feedback submitted successfully!"
    except Exception as e:
        return f"Failed to submit feedback. Error: {e}"
    finally:
        cursor.close()
        db.close_connection(connection)

def handle_give_feedback(request_data):
    try:
        user_id = request_data['userID']
        food_item_id = request_data['foodItemID']
        rating = request_data['rating']
        comments = request_data['comments']

        order_id, order_date_message = get_last_order_details(user_id)
        if not order_id:
            return {"status": "error", "message": order_date_message}

        ordered_items = get_ordered_food_items(order_id, user_id)
        if not ordered_items:
            return {"status": "error", "message": "No items found in the last order or feedback already given for all items."}

        item_exists = any(item['FoodItemID'] == food_item_id for item in ordered_items)
        if not item_exists:
            return {"status": "error", "message": "Invalid food item ID or feedback already given for this item."}

        feedback_message = insert_feedback(user_id, order_id, food_item_id, rating, comments, order_date_message)
        if "successfully" in feedback_message:
            return {"status": "success", "message": feedback_message}
        else:
            return {"status": "error", "message": feedback_message}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
