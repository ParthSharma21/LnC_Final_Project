import json
from datetime import datetime, timedelta

def chefHandler(chefUser, client):
    viewMenuChoice = '1'
    rolloutMenuChoice = '2'
    generateReportChoice = '3'
    getPoorPerformingItemsChoice = '4'
    logoutChoice = '5'

    while True:
        print("\nChef Menu:")
        print(f"1. View Menu")
        print(f"2. Rollout Tomorrow's Menu")
        print(f"3. Generate Report")
        print(f"4. Get Poor Performing Items")
        print(f"5. Logout")

        choice = input("Enter your choice: ")

        if choice == viewMenuChoice:
            viewMenu(client)
        elif choice == rolloutMenuChoice:
            rolloutMenu(client, chefUser.userID)
        elif choice == generateReportChoice:
            generateReport(client)
        elif choice == getPoorPerformingItemsChoice:
            getPoorPerformingItems(client, chefUser.userID)
        elif choice == logoutChoice:
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please enter a valid option.")

def viewMenu(client):
    responseSuccessStatus = "success"
    try:
        request = {"action": "viewMenu"}
        client.send(json.dumps(request).encode('utf-8'))
        
        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            menu = response["data"]
            print("\nMenu:")
            for item in menu:
                availability = 'Available' if item[3] == 1 else 'Not Available'
                print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Availability: {availability}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def rolloutMenu(client, userID):
    responseSuccessStatus = "success"
    try:
        request = {"action": "getRecommendedFoodItems"}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            recommendedItems = response["data"]
            print("\nRecommended Food Items:")
            for item in recommendedItems:
                print(f"ID: {item['foodItemID']}, Name: {item['foodItemName']}, Recommendation Score: {item['foodItemRecommendationScore']}")

            itemsToRollout = input("\nEnter the IDs of the items to rollout, separated by spaces: ").split()
            if not all(itemID.isdigit() for itemID in itemsToRollout):
                print("Invalid input. Please enter valid numeric IDs.")
                return

            request = {"action": "rolloutMenu", "foodItemIDs": itemsToRollout}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])

            notificationMessage = "Chef has rolled out the menu for "
            dateStr = (datetime.today().date() + timedelta(days=1)).isoformat()
            request = {"action": "notifyEmployees", "message": notificationMessage, "date": dateStr, "userID": userID}
            client.send(json.dumps(request).encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            response = json.loads(response)
            print(response["message"])
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def generateReport(client):
    responseSuccessStatus = "success"
    try:
        request = {"action": "generateReport"}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            report = response["data"]
            print("\nReport Generated Successfully:")
            for item in report:
                print(f"Name: {item['FoodItemName']}, OrderCount: {item['OrderCount']}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def getPoorPerformingItems(client, userID):
    responseSuccessStatus = "success"
    try:
        request = {"action": "getPoorPerformingItems", "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(4096).decode('utf-8')
        response = json.loads(response)

        if response["status"] == responseSuccessStatus:
            poorItems = response["data"]
            print("\nPoor Performing Items:")
            for item in poorItems:
                print(f"Id: {item['FoodItemID']}, Name: {item['FoodItemName']}, AverageRating: {item['AverageRating']}, AverageSentiment: {item['AverageSentiment']}")
            
            itemID = input("\nEnter the ID of the food item you want to interact with: ")
            if not itemID.isdigit():
                print("Invalid input. Please enter a valid numeric ID.")
                return
            
            discardFoodChoice = '1'
            requestDetailedReviewChoice = '2'
            print("\nOptions:")
            print(f"{discardFoodChoice}. Discard Food Item")
            print(f"{requestDetailedReviewChoice}. Ask Employees for Detailed Review")
            actionChoice = input("Enter your choice: ")

            if actionChoice == discardFoodChoice:
                discardFoodItem(client, itemID)
            elif actionChoice == requestDetailedReviewChoice:
                requestDetailedReview(client, itemID, userID)
            else:
                print("Invalid choice. Please enter a valid option.")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def discardFoodItem(client, itemID):
    try:
        request = {"action": "discardFoodItem", "foodItemID": itemID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")

def requestDetailedReview(client, itemID, userID):
    try:
        request = {"action": "requestDetailedReview", "foodItemID": itemID, "userID": userID}
        client.send(json.dumps(request).encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        response = json.loads(response)
        print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")
