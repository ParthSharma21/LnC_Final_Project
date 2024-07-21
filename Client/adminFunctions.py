import json

def adminHandler(adminUser, client):
    addFoodItemChoice = '1'
    updateFoodItemChoice = '2'
    deleteFoodItemChoice = '3'
    viewMenuChoice = '4'
    logoutChoice = '5'

    while True:
        print("\nAdmin Menu:")
        print("1. Add Food Item")
        print("2. Update Food Item")
        print("3. Delete Food Item")
        print("4. View Menu")
        print("5. Logout")
        
        choice = input("Enter your choice: ")

        if choice == addFoodItemChoice:
            addFoodItem(client)
        elif choice == updateFoodItemChoice:
            updateFoodItem(client)
        elif choice == deleteFoodItemChoice:
            deleteFoodItem(client)
        elif choice == viewMenuChoice:
            viewMenu(client)
        elif choice == logoutChoice:
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
                print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Availability: {item[3]}")
        else:
            print(response["message"])
    except Exception as e:
        print(f"An error occurred: {e}")
