import databaseFunctions as df
from mysql.connector import Error
import recommendationEngine as RE
from datetime import datetime, timedelta

class FoodItem:
    def __init__(self, FoodItemID, FoodItemName, FoodItemPrice, FoodItemAvailability):
        self.FoodItemID = FoodItemID
        self.FoodItemName = FoodItemName
        self.FoodItemPrice = FoodItemPrice
        self.FoodItemAvailability = FoodItemAvailability

    def to_dict(self):
        return {
            'FoodItemID': self.FoodItemID,
            'FoodItemName': self.FoodItemName,
            'FoodItemPrice': self.FoodItemPrice,
            'FoodItemAvailability': self.FoodItemAvailability
        }



class user:
    def __init__(self, userID, password, name, role):
        self.userID = userID
        self.name = name
        self.role = role
        self.password = password

class Admin(user):
    def __init__(self, userID, password, name):
        super().__init__(userID, password, name, "Admin")

        def addFoodItem(self, food_item):
            connection = df.start_connection()
            if not connection:
                return "Failed to connect to the database."
            
            cursor = connection.cursor()
            query = "INSERT INTO Menu (FoodItemID, FoodItemName, FoodItemPrice, FoodItemAvailability) VALUES (%s, %s, %s, %s)"
            try:
                cursor.execute(query, (food_item.FoodItemID, food_item.FoodItemName, food_item.FoodItemPrice, 1))
                connection.commit()
                return "Food item added successfully and marked as available."
            except Error as e:
                return f"Failed to add food item. Error: {e}"
            finally:
                df.close_connection(connection)

    def updateFoodItem(self, food_item):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()
        query = "UPDATE Menu SET FoodItemName = %s, FoodItemPrice = %s WHERE FoodItemID = %s"
        try:
            cursor.execute(query, (food_item.FoodItemName, food_item.FoodItemPrice, food_item.FoodItemID))
            connection.commit()
            return "Food item updated successfully."
        except Error as e:
            return f"Failed to update food item. Error: {e}"
        finally:
            df.close_connection(connection)

    def deleteFoodItem(self, FoodItemID):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()
        query = "DELETE FROM Menu WHERE FoodItemID = %s"
        try:
            cursor.execute(query, (FoodItemID,))
            connection.commit()
            return "Food item deleted successfully."
        except Error as e:
            return f"Failed to delete food item. Error: {e}"
        finally:
            df.close_connection(connection)

    def viewMenu(self):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()
        query = "SELECT * FROM Menu"
        try:
            cursor.execute(query)
            menu_items = cursor.fetchall()
            if menu_items:
                menu_list = []
                for item in menu_items:
                    menu_list.append(FoodItem(item[0],item[1],item[2],item[3]))#{
                    #     'FoodItemID': item[0],
                    #     'FoodItemName': item[1],
                    #     'FoodItemPrice': item[2]
                    # })
                return menu_list
            else:
                return "Menu is empty."
        except Error as e:
            return f"Failed to retrieve menu. Error: {e}"
        finally:
            df.close_connection(connection)





class Chef(user):
    def __init__(self, userID, password, name):
        super().__init__(userID, password, name, "Chef")


    def viewMenu(self):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()
        query = "SELECT * FROM Menu"
        try:
            cursor.execute(query)
            menu_items = cursor.fetchall()
            if menu_items:
                menu_list = []
                for item in menu_items:
                    menu_list.append(FoodItem(item[0],item[1],item[2],item[3]))
                return menu_list
            else:
                return "Menu is empty."
        except Error as e:
            return f"Failed to retrieve menu. Error: {e}"
        finally:
            df.close_connection(connection)

    def getRecommendedFoodItems(self):
        # print("\n\n", RE.getRecommendedItems(), "\n\n")

        return RE.getRecommendedItems()

    def rollOutFoodItems(self, foodItemsToRollOutIDs):

        foodItemsToRollOutIDs = foodItemsToRollOutIDs.split(' ')

        connection = df.start_connection()

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

        df.close_connection(connection)

    def nofityEmployees(self, message, date):
        connection = df.start_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Notifications (NotificationMessage, NotificationGeneratedAtTimeStamp, GeneratedByUserID) "
            "VALUES (%s, %s, %s)", 
            (message + str(date), datetime.now(), self.userID)
        )
        connection.commit()
        df.close_connection(connection)

    def generateReport(self):
        connection = df.start_connection()
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
        df.close_connection(connection)

        print("\nSales Report for the Last 30 Days:\n")
        if not report_data:
            print("No sales in the last 30 days.")
        else:
            for item in report_data:
                print(f"FoodItemName: {item[0]}, OrderCount: {item[1]}")

class employee(user):
    def __init__(self, userID, password, name):
        super().__init__(userID, password, name, "Employee")
    
    def viewDailyMenu(self):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."
        
        cursor = connection.cursor()
        query = "SELECT * FROM DailyMenu"
        try:
            cursor.execute(query)
            menu_items = cursor.fetchall()
            if menu_items:
                menu_list = []
                for item in menu_items:
                    menu_list.append(FoodItem(item[0], item[1], item[2], 1))
                return menu_list
            else:
                return "Menu is empty."
        except Error as e:
            return f"Failed to retrieve daily menu. Error: {e}"
        finally:
            df.close_connection(connection)

    def viewNotifications(self):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."
        
        cursor = connection.cursor()
        query = """
            SELECT NotificationMessage 
            FROM Notifications 
            WHERE NotificationGeneratedAtTimeStamp >= %s 
            ORDER BY NotificationGeneratedAtTimeStamp DESC
        """
        last_24_hours = datetime.now() - timedelta(days=1)
        try:
            cursor.execute(query, (last_24_hours,))
            notifications = cursor.fetchall()
            if notifications:
                return [notification[0] for notification in notifications]
            else:
                return "No notifications."
        except Error as e:
            return f"Failed to retrieve notifications. Error: {e}"
        finally:
            df.close_connection(connection)



    def orderFood(self, orderedFoodItemIDs):
        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()
        try:
            # Step 1: Insert into Orders to get OrderID
            cursor.execute(
                "INSERT INTO Orders (UserID, OrderDate) VALUES (%s, %s)",
                (self.userID, datetime.now().date())
            )
            idForThisOrder = cursor.lastrowid  # Get the last inserted OrderID

            # Step 2: Insert into UserOrderDetails with the obtained OrderID
            orderedFoodItemIDs = orderedFoodItemIDs.split()
            for foodItemID in orderedFoodItemIDs:
                cursor.execute(
                    "INSERT INTO UserOrderDetails (OrderID, FoodItemID) VALUES (%s, %s)",
                    (idForThisOrder, foodItemID)
                )

            connection.commit()
            return "Food items ordered successfully."
        except df.mysql.connector.Error as e:
            return f"Failed to order food items. Error: {e}"
        finally:
            df.close_connection(connection)




    def get_last_order_details(self):
        connection = df.start_connection()
        if not connection:
            return None, "Failed to connect to the database."
        
        cursor = connection.cursor()
        query = """
            SELECT OrderID, OrderDate
            FROM Orders
            WHERE UserID = %s
            ORDER BY OrderDate DESC
            LIMIT 1
        """
        try:
            cursor.execute(query, (self.userID,))
            order_details = cursor.fetchone()
            if order_details:
                return order_details[0], order_details[1]
            else:
                return None, "No orders found."
        except Error as e:
            return None, f"Failed to retrieve order details. Error: {e}"
        finally:
            df.close_connection(connection)



    def get_ordered_food_items(self, order_id):
        connection = df.start_connection()
        if not connection:
            return None, "Failed to connect to the database."
        
        cursor = connection.cursor()
        query = """
            SELECT FoodItemID
            FROM UserOrderDetails
            WHERE OrderID = %s
        """
        try:
            cursor.execute(query, (order_id,))
            ordered_items = cursor.fetchall()
            if ordered_items:
                return [item[0] for item in ordered_items]
            else:
                return []
        except Error as e:
            return None, f"Failed to retrieve ordered items. Error: {e}"
        finally:
            df.close_connection(connection)




    def give_feedback(self):
        order_id, order_date = self.get_last_order_details()
        if not order_id:
            return "No orders found."

        ordered_items = self.get_ordered_food_items(order_id)
        if not ordered_items:
            return "No items found in the last order."

        connection = df.start_connection()
        if not connection:
            return "Failed to connect to the database."
        
        cursor = connection.cursor()
        try:
            feedback_given = False
            for food_item_id in ordered_items:
                # Check if feedback exists for this item
                query_existing_feedback = """
                    SELECT FeedbackID
                    FROM Feedback
                    WHERE UserID = %s AND OrderID = %s AND FoodItemID = %s
                """
                cursor.execute(query_existing_feedback, (self.userID, order_id, food_item_id))
                existing_feedback = cursor.fetchone()

                if existing_feedback:
                    print(f"Feedback already provided for FoodItemID: {food_item_id}.")
                    continue

                # Fetch FoodItemName from Menu table
                query_get_item_name = """
                    SELECT FoodItemName
                    FROM Menu
                    WHERE FoodItemID = %s
                """
                cursor.execute(query_get_item_name, (food_item_id,))
                menu_item_name = cursor.fetchone()

                if not menu_item_name:
                    print(f"Food item with ID {food_item_id} not found in the Menu.")
                    continue

                menu_item_name = menu_item_name[0]  # Extract the actual name from the tuple

                # Allow employee to provide feedback
                rating = None
                while not rating or rating not in range(1, 6):
                    try:
                        rating = int(input(f"Enter your rating (1-5) for {menu_item_name}: "))
                        if rating not in range(1, 6):
                            print("Rating must be between 1 and 5. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                review = input(f"Enter your review for {menu_item_name}: ")

                # Insert feedback into Feedback table
                query_insert_feedback = """
                    INSERT INTO Feedback (UserID, OrderID, FoodItemID, FoodReviewRating, FoodReviewComments, FoodReviewDate)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_insert_feedback, (self.userID, order_id, food_item_id, rating, review, order_date))
                feedback_given = True

            if feedback_given:
                connection.commit()
                return "Feedback provided successfully."
            else:
                return "No new feedback provided."
        except Error as e:
            return f"Failed to provide feedback. Error: {e}"
        finally:
            df.close_connection(connection)




# a= Admin(1,1,1)
# print(a.userID)






# # classes.py
# import database_connection as db

# class FoodItem:
#     def __init__(self, FoodItemID, FoodItemName, FoodItemPrice):
#         self.FoodItemID = FoodItemID
#         self.FoodItemName = FoodItemName
#         self.FoodItemPrice = FoodItemPrice

#     def to_dict(self):
#         return {
#             'FoodItemID': self.FoodItemID,
#             'FoodItemName': self.FoodItemName,
#             'FoodItemPrice': self.FoodItemPrice
#         }


# class User:
#     def __init__(self, userID, password, name, role):
#         self.userID = userID
#         self.name = name
#         self.role = role
#         self.password = password

# class Admin(User):
#     def __init__(self, userID, password, name):
#         super().__init__(userID, password, name, "Admin")

#     def add_food_item(self, food_item):
#         connection = db.start_connection()
#         if not connection:
#             return "Failed to connect to the database."

#         cursor = connection.cursor()
#         query = "INSERT INTO Menu (FoodItemID, FoodItemName, FoodItemPrice) VALUES (%s, %s, %s)"
#         try:
#             cursor.execute(query, (food_item.FoodItemID, food_item.FoodItemName, food_item.FoodItemPrice))
#             connection.commit()
#             return "Food item added successfully."
#         except Exception as e:  # Catch any exception here
#             return f"Failed to add food item. Error: {e}"
#         finally:
#             db.close_connection(connection)

#     def update_food_item(self, food_item):
#         connection = db.start_connection()
#         if not connection:
#             return "Failed to connect to the database."

#         cursor = connection.cursor()
#         query = "UPDATE Menu SET FoodItemName = %s, FoodItemPrice = %s WHERE FoodItemID = %s"
#         try:
#             cursor.execute(query, (food_item.FoodItemName, food_item.FoodItemPrice, food_item.FoodItemID))
#             connection.commit()
#             return "Food item updated successfully."
#         except Exception as e:
#             return f"Failed to update food item. Error: {e}"
#         finally:
#             db.close_connection(connection)

#     def delete_food_item(self, FoodItemID):
#         connection = db.start_connection()
#         if not connection:
#             return "Failed to connect to the database."

#         cursor = connection.cursor()
#         query = "DELETE FROM Menu WHERE FoodItemID = %s"
#         try:
#             cursor.execute(query, (FoodItemID,))
#             connection.commit()
#             return "Food item deleted successfully."
#         except Exception as e:
#             return f"Failed to delete food item. Error: {e}"
#         finally:
#             db.close_connection(connection)

#     def viewMenu(self):
#         connection = db.start_connection()
#         if not connection:
#             return "Failed to connect to the database."

#         cursor = connection.cursor()
#         query = "SELECT * FROM Menu"
#         try:
#             cursor.execute(query)
#             menu_items = cursor.fetchall()
#             if menu_items:
#                 menu_list = []
#                 for item in menu_items:
#                     menu_list.append({
#                         'FoodItemID': item[0],
#                         'FoodItemName': item[1],
#                         'FoodItemPrice': item[2]
#                     })
#                 return menu_list
#             else:
#                 return "Menu is empty."
#         except Exception as e:
#             return f"Failed to retrieve menu. Error: {e}"
#         finally:
#             db.close_connection(connection)


# class Chef(User):
#     def __init__(self, userID, password, name):
#         super().__init__(userID, password, name, "Chef")

#     # You can define Chef-specific methods here


# class Employee(User):
#     def __init__(self, userID, password, name):
#         super().__init__(userID, password, name, "Employee")

#     # You can define Employee-specific methods here
