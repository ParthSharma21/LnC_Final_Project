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
        print("4. Get Poor Performing Items")
        print("5. Logout")
        
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

                items_to_rollout = input("\nEnter the IDs of the items to rollout, separated by spaces: ")
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
            request = {"action": "getPoorPerformingItems", "userID": chefUser.userID}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if response["status"] == "success":
                poor_items = response["data"]
                print("\nPoor Performing Items:")
                for item in poor_items:
                    print(f"Id: {item['FoodItemID']}, Name: {item['FoodItemName']}, AverageRating: {item['AverageRating']}, AverageSentiment: {item['AverageSentiment']}")
                
                
                item_id = input("\nEnter the ID of the food item you want to interact with: ")
                print("\nOptions:")
                print("1. Discard Food Item")
                print("2. Ask Employees for Detailed Review")
                action_choice = input("Enter your choice: ")

                if action_choice == '1':
                    request = {"action": "discardFoodItem", "foodItemID": item_id}
                    client.send(json.dumps(request).encode('utf-8'))

                    response = client.recv(1024).decode('utf-8')
                    response = json.loads(response)
                    print(response["message"])

                elif action_choice == '2':
                    request = {"action": "requestDetailedReview", "foodItemID": item_id, "userID": chefUser.userID}
                    client.send(json.dumps(request).encode('utf-8'))

                    response = client.recv(1024).decode('utf-8')
                    response = json.loads(response)
                    print(response["message"])

                else:
                    print("Invalid choice. Please enter a valid option.")

            else:
                print(response["message"])

        elif choice == '5':
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
        print("5. Provide Detailed Feedback")
        print("6. Update Profile")
        print("7. Logout")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            request = {"action": "viewDailyMenu", "userID": employeeUser.userID}
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
            request = {'action': 'check_detailed_feedback', 'UserID': employeeUser.userID}
            client.send(json.dumps(request).encode('utf-8'))
            response = client.recv(4096).decode('utf-8')
            response = json.loads(response)

            if not response['items']:
                print("No items require detailed feedback at the moment.")
                
            else:
                for item in response['items']:
                    foodItemName = item[0]
                    notificationId = item[1]
                    foodItemId = item[2]

                    print(f"\nDetailed Feedback for {foodItemName}")
                    answerToQuestion1 = input("Q1. What didn't you like about the food item? ")
                    answerToQuestion2 = input("Q2. How would you like the food item to taste? ")
                    answerToQuestion3 = input("Q3. Share your mom's recipe: ")

                    detailedFeedback = [
                        {'AnswerToQueID': 1, 'DetailedFeedback': answerToQuestion1},
                        {'AnswerToQueID': 2, 'DetailedFeedback': answerToQuestion2},
                        {'AnswerToQueID': 3, 'DetailedFeedback': answerToQuestion3},
                    ]

                    client.send(json.dumps({
                        'action': 'submit_detailed_feedback',
                        'UserID': employeeUser.userID,
                        'NotificationID': notificationId,
                        'FoodItemID': foodItemId,
                        'detailedFeedback': detailedFeedback
                    }).encode('utf-8'))

                    server_response = client.recv(1024).decode('utf-8')
                    server_response = json.loads(server_response)
                    if server_response['status'] == 'success':
                        print(f"Detailed feedback for {foodItemName} submitted successfully.")
                    else:
                        print(f"Failed to submit detailed feedback for {foodItemName}.")

        elif choice == '6':
            print("\nUpdate Your Profile")

            print("1) Please select one-")
            print("1. Vegetarian")
            print("2. Non Vegetarian")
            print("3. Eggetarian")
            food_type = input("Enter your choice (1/2/3): ")

            print("2) Please select your spice level")
            print("1. Low")
            print("2. Medium")
            print("3. High")
            spice_level = input("Enter your choice (1/2/3): ")

            print("3) What do you prefer most?")
            print("1. North Indian")
            print("2. South Indian")
            print("3. Other")
            cuisine_type = input("Enter your choice (1/2/3): ")

            print("4) Do you have a sweet tooth?")
            print("1. Yes")
            print("2. No")
            sweet_preference = input("Enter your choice (1/2): ")

            profile_data = {
                "action": "updateProfile",
                "userID": employeeUser.userID,
                "foodType": food_type,
                "spiceLevel": spice_level,
                "cuisineType": cuisine_type,
                "sweetPreference": sweet_preference
            }

            client.send(json.dumps(profile_data).encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])

        elif choice == '7':
            print("Logging out...")
            return

        else:
            print("Invalid choice, please try again.")

