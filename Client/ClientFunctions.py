#ClientFunctions.py
import json
from datetime import datetime, timedelta

def adminHandler(adminUser, client):
    while True:
        print("\nAdmin Menu:")
        print("1. Add Food Item")
        print("2. Update Food Item")
        print("3. Delete Food Item")
        print("4. View Menu")
        print("5. Logout")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            foodItemName = input("Enter food item name:")
            foodItemPrice = input("Enter price:")

            user = {"action": "addFoodItem", "foodItemName": foodItemName, "foodItemPrice": foodItemPrice}
            client.send(json.dumps(user).encode('utf-8'))
            
            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)

            print(response["message"])
            pass


        elif choice == '2':
            foodItemID = input("Enter food item ID to update:")
            foodItemName = input("Enter new food item name:")
            foodItemPrice = input("Enter new price:")
            foodItemAvailability = input("Enter new availability(1/0):")

            request = {"action": "updateFoodItem", "foodItemID": foodItemID, "foodItemName": foodItemName, "foodItemPrice": foodItemPrice, 'foodItemAvailability': foodItemAvailability}
            client.send(json.dumps(request).encode('utf-8'))
            
            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])
            # cf.handle_update_food_item_response(response)
        
        elif choice == '3':
            foodItemID = input("Enter food item ID to delete:")

            request = {"action": "deleteFoodItem", "foodItemID": foodItemID}
            client.send(json.dumps(request).encode('utf-8'))
            
            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])
            # cf.handle_delete_food_item_response(response)
        
        elif choice == '4':
            request = {"action": "viewMenu"}
            client.send(json.dumps(request).encode('utf-8'))
            
            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                menu = response["data"]
                print("\nMenu:")
                for item in menu:
                    print(f"ID: {item[0]},     Name: {item[1]},     Price: {item[2]},       Availability: {item[3]}")
            else:
                print("Invalid choice. Please enter a valid option.")
        
        
        elif choice == '5':
            print("Loging OUT...")
            return
        
        else:
            print("Invalid choice. Please enter a valid.")




def chefHandler(chefUser, client):
    while True:
        print("\nChef Menu:")
        print("1. View Menu")
        print("2. Rollout Tomorrow's Menu")
        print("3. Generate Report")
        print("4. Logout")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            request = {"action": "viewMenu"}
            client.send(json.dumps(request).encode('utf-8'))
            
            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                menu = response["data"]
                print("\nMenu:")
                for item in menu:
                    availability = 'Available' if item[3] == 1 else 'Not Available'
                    print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Availability: {availability}")
            else:
                print(response["message"])

        elif choice == '2':
            request = {"action": "getRecommendedFoodItems"}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                recommended_items = response["data"]
                print("\nRecommended Food Items:")
                for item in recommended_items:
                    print(f"ID: {item['foodItemID']}, Name: {item['foodItemName']}, Recommendation Score: {item['foodItemRecommendationScore']}")

                items_to_rollout = input("Enter the IDs of the items to rollout, separated by spaces: ")
                request = {"action": "rolloutMenu", "foodItemIDs": items_to_rollout.split()}
                client.send(json.dumps(request).encode('utf-8'))

                response = client.recv(1024).decode('utf-8')
                response = json.loads(response)
                print(response["message"])

                notification_message = "Chef has rolled out the menu for "
                date_str = (datetime.today().date() + timedelta(days=1)).isoformat()
                request = {"action": "notifyEmployees", "message": notification_message, "date": date_str, "userID": chefUser.userID}
                client.send(json.dumps(request).encode('utf-8'))

                response = client.recv(1024).decode('utf-8')
                response = json.loads(response)
                print(response["message"])


        elif choice == '3':
            request = {"action": "generateReport"}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                report = response["data"]
                print("\nReport Generated Successfully:")
                # print(report)
                for item in report:
                    print(f"Name: {item['FoodItemName']}, OrderCount: {item['OrderCount']}")

            else:
                print(response["message"])

        elif choice == '4':
            print("Logging out...")
            return
        
        else:
            print("Invalid choice. Please enter a valid option.")

def employeeHandler(employeeUser, client):
    while True:
        print("\nEmployee Menu:")
        print("1. View Tomorrow's Menu")
        print("2. View Notifications")
        print("3. Order Food")
        print("4. Provide Feedback")
        print("5. Logout")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            request = {"action": "viewDailyMenu"}
            client.send(json.dumps(request).encode('utf-8'))
            
            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                daily_menu = response["data"]
                print("\nTomorrow's Menu:\n")
                if not daily_menu:
                    print("Menu is empty.")
                else:
                    # print(daily_menu)
                    for item in daily_menu:
                        print(f"ID: {item[0]}, FoodItemName: {item[1]}, FoodItemPrice: {item[2]}") # item example [1, 'Pav Bhaji', 70]
            else:
                print(response["message"])

        elif choice == '2':
            request = {"action": "viewNotifications"}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                notifications = response["data"]
                print("\nNotifications from last 24 hrs:\n")
                if not notifications:
                    print("No notifications.")
                else:
                    for notification in notifications:
                        print(f"{notification}")
            else:
                print(response["message"])

        elif choice == '3':
            orderedFoodItemIDs = input("Enter the Food Item ID you want to order (separated by space): ")
            request = {"action": "orderFood", "foodItemIDs": orderedFoodItemIDs.split(), "userID": employeeUser.userID}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])

        
        elif choice == '4':
            request = {"action": "requestFeedbackItems", "userID": employeeUser.userID}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                items_to_feedback = response["data"]
                if not items_to_feedback:
                    print("No pending feedback for the last order.")
                else:
                    for item in items_to_feedback:
                        print(f"\nID: {item['FoodItemID']}, FoodItemName: {item['FoodItemName']}")
                        rating = input("Enter your rating (1-5): ")
                        comments = input("Enter your comments: ")
                        feedback_request = {
                            "action": "giveFeedback",
                            "foodItemID": item['FoodItemID'],
                            "rating": rating,
                            "comments": comments,
                            "userID": employeeUser.userID
                        }
                        client.send(json.dumps(feedback_request).encode('utf-8'))
                        feedback_response = client.recv(1024).decode('utf-8')
                        feedback_response = json.loads(feedback_response)
                        print(feedback_response["message"])
            else:
                print(response["message"])


        elif choice == '5':
            print("Logging out...")
            return

        else:
            print("Invalid choice, please try again.")

