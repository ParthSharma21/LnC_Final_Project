import json

def employeeHandler(employeeUser, client):
    viewDailyMenuChoice = '1'
    viewNotificationsChoice = '2'
    orderFoodChoice = '3'
    provideFeedbackChoice = '4'
    provideDetailedFeedbackChoice = '5'
    updateProfileChoice = '6'
    logoutChoice = '7'

    while True:
        print("\nEmployee Menu:")
        print(f"1. View Tomorrow's Menu")
        print(f"2. View Notifications")
        print(f"3. Order Food")
        print(f"4. Provide Feedback")
        print(f"5. Provide Detailed Feedback")
        print(f"6. Update Profile")
        print(f"7. Logout")
        
        choice = input("Enter your choice: ")

        if choice == viewDailyMenuChoice:
            viewDailyMenu(client, employeeUser.userID)
        elif choice == viewNotificationsChoice:
            viewNotifications(client)
        elif choice == orderFoodChoice:
            orderFood(client, employeeUser.userID)
        elif choice == provideFeedbackChoice:
            provideFeedback(client, employeeUser.userID)
        elif choice == provideDetailedFeedbackChoice:
            provideDetailedFeedback(client, employeeUser.userID)
        elif choice == updateProfileChoice:
            updateProfile(client, employeeUser.userID)
        elif choice == logoutChoice:
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please try again.")

def viewDailyMenu(client, userID):
    responseSuccessStatus = "success"
    try:
        request = {"action": "viewDailyMenu", "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            dailyMenu = response["data"]
            print("\nTomorrow's Menu:\n")
            if not dailyMenu:
                print("Menu is empty.")
            else:
                for item in dailyMenu:
                    print(f"ID: {item[0]}, FoodItemName: {item[1]}, FoodItemPrice: {item[2]}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def viewNotifications(client):
    responseSuccessStatus = "success"
    try:
        request = {"action": "viewNotifications"}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
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
    responseSuccessStatus = "success"
    try:
        orderedFooditemIDs = input("Enter the Food Item ID you want to order (separated by space): ").split()
        if not all(itemID.isdigit() for itemID in orderedFooditemIDs):
            print("Invalid input. Please enter valid numeric IDs.")
            return

        request = {"action": "orderFood", "fooditemIDs": orderedFooditemIDs, "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def provideFeedback(client, userID):
    responseSuccessStatus = "success"
    try:
        request = {"action": "requestFeedbackItems", "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            itemsToFeedback = response["data"]
            if not itemsToFeedback:
                print("No pending feedback for the last order.")
            else:
                for item in itemsToFeedback:
                    print(f"\nID: {item['FooditemID']}, FoodItemName: {item['FoodItemName']}")
                    rating = input("Enter your rating (1-5): ")
                    comments = input("Enter your comments: ")

                    if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                        print("Invalid rating. Please enter a number between 1 and 5.")
                        return

                    feedbackRequest = {
                        "action": "giveFeedback",
                        "fooditemID": item['FooditemID'],
                        "rating": int(rating),
                        "comments": comments,
                        "userID": userID
                    }
                    client.send(json.dumps(feedbackRequest).encode('utf-8'))
                    feedbackResponse = client.recv(1024).decode('utf-8')
                    feedbackResponse = json.loads(feedbackResponse)
                    print(feedbackResponse["message"])
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def provideDetailedFeedback(client, userID):
    responseSuccessStatus = "success"
    try:
        request = {'action': 'checkDetailedFeedback', 'UserID': userID}
        client.send(json.dumps(request).encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            items = response['items']
            if not items:
                print("No items require detailed feedback at the moment.")
            else:
                for item in items:
                    foodItemName = item[0]
                    notificationId = item[1]
                    fooditemID = item[2]

                    print(f"\nDetailed Feedback for {foodItemName}")
                    answerToQuestion1 = input("Q1. What didn't you like about the food item? ")
                    answerToQuestion2 = input("Q2. How would you like the food item to taste? ")
                    answerToQuestion3 = input("Q3. Share your mom's recipe: ")

                    detailedFeedback = [
                        {'AnswerToQueID': 1, 'DetailedFeedback': answerToQuestion1},
                        {'AnswerToQueID': 2, 'DetailedFeedback': answerToQuestion2},
                        {'AnswerToQueID': 3, 'DetailedFeedback': answerToQuestion3},
                    ]

                    feedbackRequest = {
                        'action': 'submitDetailedFeedback',
                        'UserID': userID,
                        'NotificationID': notificationId,
                        'FooditemID': fooditemID,
                        'detailedFeedback': detailedFeedback
                    }

                    client.send(json.dumps(feedbackRequest).encode('utf-8'))
                    serverResponse = client.recv(1024).decode('utf-8')
                    serverResponse = json.loads(serverResponse)
                    if serverResponse['status'] == responseSuccessStatus:
                        print(f"Detailed feedback for {foodItemName} submitted successfully.")
                    else:
                        print(f"Failed to submit detailed feedback for {foodItemName}.")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def updateProfile(client, userID):
    responseSuccessStatus = "success"
    try:
        print("\nUpdate Your Profile")

        print("1) Please select one-")
        print("1. Vegetarian")
        print("2. Non Vegetarian")
        print("3. Eggetarian")
        foodType = input("Enter your choice (1/2/3): ")

        print("2) Please select your spice level")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        spiceLevel = input("Enter your choice (1/2/3): ")

        print("3) What do you prefer most?")
        print("1. North Indian")
        print("2. South Indian")
        print("3. Other")
        cuisineType = input("Enter your choice (1/2/3): ")

        print("4) Do you have a sweet tooth?")
        print("1. Yes")
        print("2. No")
        sweetPreference = input("Enter your choice (1/2): ")

        if foodType not in ['1', '2', '3'] or spiceLevel not in ['1', '2', '3'] or cuisineType not in ['1', '2', '3'] or sweetPreference not in ['1', '2']:
            print("Invalid input. Please enter valid options.")
            return

        profileData = {
            "action": "updateProfile",
            "userID": userID,
            "foodType": int(foodType),
            "spiceLevel": int(spiceLevel),
            "cuisineType": int(cuisineType),
            "sweetPreference": int(sweetPreference)
        }

        client.send(json.dumps(profileData).encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")
