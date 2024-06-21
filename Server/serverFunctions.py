######## serverFunctions.py

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

        # Extract food item details from request_data
        food_item = {
            "FoodItemName": request_data['foodItemName'],
            "FoodItemPrice": request_data['foodItemPrice'],
            "FoodItemAvailability": 1
        }

        # Create SQL query
        query = "INSERT INTO menu (FoodItemName, FoodItemPrice, FoodItemAvailability) VALUES (%s, %s, %s)"
        
        # Execute the query
        cursor.execute(query, (food_item['FoodItemName'], food_item['FoodItemPrice'], food_item['FoodItemAvailability']))
        
        # Commit changes to the database
        connection.commit()

        # Close the cursor and connection
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

        # Extract food item details from request_data
        food_item = {
            "FoodItemID": request_data['foodItemID'],
            "FoodItemName": request_data['foodItemName'],
            "FoodItemPrice": request_data['foodItemPrice'],
            "FoodItemAvailability": request_data['foodItemAvailability']
        }

        # Create SQL query to update the existing record
        query = "UPDATE menu SET FoodItemName = %s, FoodItemPrice = %s, FoodItemAvailability = %s WHERE FoodItemID = %s"
        
        # Execute the query
        cursor.execute(query, (food_item['FoodItemName'], food_item['FoodItemPrice'], food_item['FoodItemAvailability'], food_item['FoodItemID']))
        
        # Commit changes to the database
        connection.commit()

        # Close the cursor and connection
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

        query = "DELETE FROM menu WHERE FoodItemID = %s"
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
        query = "SELECT FoodItemID, FoodItemName, FoodItemPrice, FoodItemAvailability FROM menu"
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
        
        # Insert the selected items into DailyMenu
        for item_id in foodItemsToRollOutIDs:
            cursor.execute(
                "INSERT INTO DailyMenu (FoodItemID, FoodItemName, FoodItemPrice) "
                "SELECT FoodItemID, FoodItemName, FoodItemPrice FROM Menu WHERE FoodItemID = %s", 
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
    



def handle_view_daily_menu():
    try:
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        query = "SELECT FoodItemID, FoodItemName, FoodItemPrice FROM DailyMenu"
        cursor.execute(query)
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
    print(request_data)
    try:
        food_item_ids = request_data['foodItemIDs']
        user_id = request_data['userID']
        print("---",user_id)

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        # Create a new order
        cursor.execute("INSERT INTO Orders (UserID, OrderDate) VALUES (%s, %s)", (user_id, datetime.now().date()))
        
        id_for_this_order = cursor.lastrowid  # Get the last inserted OrderID

        # Insert each food item into the order details
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
        
        print(user_id)

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
        
        print(last_order)
        
        order_id, order_date = last_order
        
        query_ordered_items = """
            SELECT m.FoodItemID, m.FoodItemName
            FROM UserOrderDetails uod
            JOIN Menu m ON uod.FoodItemID = m.FoodItemID
            WHERE uod.OrderID = %s
            AND uod.FoodItemID NOT IN (
                SELECT FoodItemID FROM Feedback
                WHERE UserID = %s AND OrderID = %s
            )
        """
        cursor.execute(query_ordered_items, (order_id, user_id, order_id))
        # query_ordered_items = """
        #     SELECT m.FoodItemID, m.FoodItemName
        #     FROM UserOrderDetails uod
        #     JOIN Menu m ON uod.FoodItemID = m.FoodItemID
        #     WHERE uod.OrderID = %s
        #     AND uod.FoodItemID NOT IN (
        #         SELECT FoodItemID FROM Feedback
        #         WHERE UserID = %s AND OrderID = %s
        #     )
        #     AND uod.OrderID IN (
        #         SELECT OrderID FROM Orders WHERE UserID = %s AND OrderDate = %s
        #     )
        # """
        # cursor.execute(query_ordered_items, (order_id, user_id, order_id, user_id, order_date))
        
        items_to_feedback = cursor.fetchall()

        if not items_to_feedback:
            return {"status": "success", "data": [], "message": "No items pending feedback for the last order"}
        
        items_list = [{"FoodItemID": item[0], "FoodItemName": item[1]} for item in items_to_feedback]
        
        print("----",items_list)

        cursor.close()
        db.close_connection(connection)
        
        return {"status": "success", "data": items_list}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_give_feedback(request_data):
    try:
        user_id = request_data['userID']
        food_item_id = request_data['foodItemID']
        rating = request_data['rating']
        comments = request_data['comments']
        
        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        
        query_last_order = """
            SELECT OrderID, OrderDate
            FROM Orders
            WHERE UserID = %s
            ORDER BY OrderDate DESC
            LIMIT 1
        """
        cursor.execute(query_last_order, (user_id,))
        last_order = cursor.fetchone()
        if not last_order:
            return {"status": "error", "message": "No orders found"}
        
        order_id, order_date = last_order
        
        query_insert_feedback = """
            INSERT INTO Feedback (UserID, OrderID, FoodItemID, FoodReviewRating, FoodReviewComments, FoodReviewDate, Sentiment)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert_feedback, (user_id, order_id, food_item_id, rating, comments, order_date, sentiment.analyze_sentiment(comments)))
        connection.commit()
        
        cursor.close()
        db.close_connection(connection)
        
        return {"status": "success", "message": "Feedback submitted successfully!"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    



# def handle_give_feedback(request_data):
#     try:
#         user_id = request_data['userID']
#         food_item_id = request_data['foodItemID']
#         rating = request_data['rating']
#         comments = request_data['comments']
        
#         # Step 1: Retrieve last order details
#         connection = db.start_connection()
#         if not connection:
#             return {"status": "error", "message": "Database connection failed"}

#         cursor = connection.cursor()
        
#         query_last_order = """
#             SELECT OrderID, OrderDate
#             FROM Orders
#             WHERE UserID = %s
#             ORDER BY OrderDate DESC
#             LIMIT 1
#         """
#         cursor.execute(query_last_order, (user_id,))
#         last_order = cursor.fetchone()
#         if not last_order:
#             return {"status": "error", "message": "No orders found"}
        
#         order_id, order_date = last_order
        
#         # Step 2: Retrieve items in that order
#         query_ordered_items = """
#             SELECT FoodItemID
#             FROM UserOrderDetails
#             WHERE OrderID = %s
#         """
#         cursor.execute(query_ordered_items, (order_id,))
#         ordered_items = cursor.fetchall()
#         if not ordered_items:
#             return {"status": "error", "message": "No items found in the last order"}
        
#         ordered_items = [item[0] for item in ordered_items]
        
#         # Step 3: Check if feedback already exists for this item
#         if food_item_id not in ordered_items:
#             return {"status": "error", "message": "The item was not part of the last order"}
        
#         query_existing_feedback = """
#             SELECT FeedbackID
#             FROM Feedback
#             WHERE UserID = %s AND OrderID = %s AND FoodItemID = %s
#         """
#         cursor.execute(query_existing_feedback, (user_id, order_id, food_item_id))
#         existing_feedback = cursor.fetchone()
        
#         if existing_feedback:
#             return {"status": "error", "message": "Feedback already provided for this item"}
        
#         # Step 4: Insert feedback into Feedback table
#         query_insert_feedback = """
#             INSERT INTO Feedback (UserID, OrderID, FoodItemID, FoodReviewRating, FoodReviewComments, FoodReviewDate)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(query_insert_feedback, (user_id, order_id, food_item_id, rating, comments, order_date))
#         connection.commit()
        
#         cursor.close()
#         db.close_connection(connection)
        
#         return {"status": "success", "message": "Feedback submitted successfully!"}
    
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

