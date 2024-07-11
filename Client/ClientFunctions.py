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
            addFoodItem(client)
        elif choice == '2':
            updateFoodItem(client)
        elif choice == '3':
            deleteFoodItem(client)
        elif choice == '4':
            viewMenu(client)
        elif choice == '5':
            print("Logging OUT...")
            return
        else:
            print("Invalid choice. Please enter a valid.")

def addFoodItem(client):
    try:
        foodItemName = input("Enter food item name:")
        foodItemPrice = input("Enter price:")

        if not foodItemName or not foodItemPrice.isdigit():
            print("Invalid input. Please enter a valid name and numeric price.")
            return

        request = {"action": "addFoodItem", "foodItemName": foodItemName, "foodItemPrice": int(foodItemPrice)}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def updateFoodItem(client):
    try:
        foodItemID = input("Enter food item ID to update:")
        foodItemName = input("Enter new food item name:")
        foodItemPrice = input("Enter new price:")
        foodItemAvailability = input("Enter new availability(1/0):")

        if not foodItemID.isdigit() or not foodItemName or not foodItemPrice.isdigit() or foodItemAvailability not in ['0', '1']:
            print("Invalid input. Please enter valid data.")
            return

        request = {"action": "updateFoodItem", "foodItemID": int(foodItemID), "foodItemName": foodItemName, "foodItemPrice": int(foodItemPrice), 'foodItemAvailability': int(foodItemAvailability)}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def deleteFoodItem(client):
    try:
        foodItemID = input("Enter food item ID to delete:")

        if not foodItemID.isdigit():
            print("Invalid input. Please enter a valid ID.")
            return

        request = {"action": "deleteFoodItem", "foodItemID": int(foodItemID)}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def viewMenu(client):
    try:
        request = {"action": "viewMenu"}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "success":
            menu = response["data"]
            print("\nMenu:")
            for item in menu:
                print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Availability: {item[3]}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

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
            viewMenu(client)
        elif choice == '2':
            rolloutMenu(client, chefUser.userID)
        elif choice == '3':
            generateReport(client)
        elif choice == '4':
            getPoorPerformingItems(client, chefUser.userID)
        elif choice == '5':
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please enter a valid option.")

def rolloutMenu(client, userID):
    try:
        request = {"action": "getRecommendedFoodItems"}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "success":
            recommended_items = response["data"]
            print("\nRecommended Food Items:")
            for item in recommended_items:
                print(f"ID: {item['foodItemID']}, Name: {item['foodItemName']}, Recommendation Score: {item['foodItemRecommendationScore']}")

            items_to_rollout = input("\nEnter the IDs of the items to rollout, separated by spaces: ").split()
            if not all(item_id.isdigit() for item_id in items_to_rollout):
                print("Invalid input. Please enter valid numeric IDs.")
                return

            request = {"action": "rolloutMenu", "foodItemIDs": items_to_rollout}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])

            notification_message = "Chef has rolled out the menu for "
            date_str = (datetime.today().date() + timedelta(days=1)).isoformat()
            request = {"action": "notifyEmployees", "message": notification_message, "date": date_str, "userID": userID}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def generateReport(client):
    try:
        request = {"action": "generateReport"}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "success":
            report = response["data"]
            print("\nReport Generated Successfully:")
            for item in report:
                print(f"Name: {item['FoodItemName']}, OrderCount: {item['OrderCount']}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def getPoorPerformingItems(client, userID):
    try:
        request = {"action": "getPoorPerformingItems", "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "success":
            poor_items = response["data"]
            print("\nPoor Performing Items:")
            for item in poor_items:
                print(f"Id: {item['FoodItemID']}, Name: {item['FoodItemName']}, AverageRating: {item['AverageRating']}, AverageSentiment: {item['AverageSentiment']}")
            
            item_id = input("\nEnter the ID of the food item you want to interact with: ")
            if not item_id.isdigit():
                print("Invalid input. Please enter a valid numeric ID.")
                return
            
            print("\nOptions:")
            print("1. Discard Food Item")
            print("2. Ask Employees for Detailed Review")
            action_choice = input("Enter your choice: ")

            if action_choice == '1':
                discardFoodItem(client, item_id)
            elif action_choice == '2':
                requestDetailedReview(client, item_id, userID)
            else:
                print("Invalid choice. Please enter a valid option.")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def discardFoodItem(client, item_id):
    try:
        request = {"action": "discardFoodItem", "foodItemID": item_id}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def requestDetailedReview(client, item_id, userID):
    try:
        request = {"action": "requestDetailedReview", "foodItemID": item_id, "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

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
            viewDailyMenu(client, employeeUser.userID)
        elif choice == '2':
            viewNotifications(client)
        elif choice == '3':
            orderFood(client, employeeUser.userID)
        elif choice == '4':
            provideFeedback(client, employeeUser.userID)
        elif choice == '5':
            provideDetailedFeedback(client, employeeUser.userID)
        elif choice == '6':
            updateProfile(client, employeeUser.userID)
        elif choice == '7':
            print("Logging out...")
            return
        else:
            print("Invalid choice, please try again.")

def viewDailyMenu(client, userID):
    try:
        request = {"action": "viewDailyMenu", "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == "success":
            daily_menu = response["data"]
            print("\nTomorrow's Menu:\n")
            if not daily_menu:
                print("Menu is empty.")
            else:
                for item in daily_menu:
                    print(f"ID: {item[0]}, FoodItemName: {item[1]}, FoodItemPrice: {item[2]}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def viewNotifications(client):
    try:
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
    except Exception as e:
        print(f"An error occurred: {e}")

def orderFood(client, userID):
    try:
        orderedFoodItemIDs = input("Enter the Food Item ID you want to order (separated by space): ").split()
        if not all(item_id.isdigit() for item_id in orderedFoodItemIDs):
            print("Invalid input. Please enter valid numeric IDs.")
            return

        request = {"action": "orderFood", "foodItemIDs": orderedFoodItemIDs, "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def provideFeedback(client, userID):
    try:
        request = {"action": "requestFeedbackItems", "userID": userID}
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

                    if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                        print("Invalid rating. Please enter a number between 1 and 5.")
                        return

                    feedback_request = {
                        "action": "giveFeedback",
                        "foodItemID": item['FoodItemID'],
                        "rating": int(rating),
                        "comments": comments,
                        "userID": userID
                    }
                    client.send(json.dumps(feedback_request).encode('utf-8'))
                    feedback_response = client.recv(1024).decode('utf-8')
                    feedback_response = json.loads(feedback_response)
                    print(feedback_response["message"])
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def provideDetailedFeedback(client, userID):
    try:
        request = {'action': 'check_detailed_feedback', 'UserID': userID}
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
                    'UserID': userID,
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
    except Exception as e:
        print(f"An error occurred: {e}")

def updateProfile(client, userID):
    try:
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

        if food_type not in ['1', '2', '3'] or spice_level not in ['1', '2', '3'] or cuisine_type not in ['1', '2', '3'] or sweet_preference not in ['1', '2']:
            print("Invalid input. Please enter valid options.")
            return

        profile_data = {
            "action": "updateProfile",
            "userID": userID,
            "foodType": int(food_type),
            "spiceLevel": int(spice_level),
            "cuisineType": int(cuisine_type),
            "sweetPreference": int(sweet_preference)
        }

        client.send(json.dumps(profile_data).encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")
