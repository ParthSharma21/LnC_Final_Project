import classes
from datetime import datetime, timedelta

def adminMenu(adminUser):
    
    while True:
        print("\nAdmin Menu:")
        print("1. Add Food Item")
        print("2. Update Food Item")
        print("3. Delete Food Item")
        print("4. View Menu")
        print("5. Logout")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            FoodItemID = input("Enter Food Item ID: ")
            FoodItemName = input("Enter Food Item Name: ")
            FoodItemPrice = input("Enter Food Item Price: ")
            foodItem = classes.FoodItem(FoodItemID, FoodItemName, FoodItemPrice, 1)
            result = adminUser.addFoodItem(foodItem)
            print(result)
        
        elif choice == 2:
            FoodItemID = input("Enter Food Item ID to update: ")
            FoodItemName = input("Enter new Food Item Name: ")
            FoodItemPrice = input("Enter new Food Item Price: ")
            foodItem = classes.FoodItem(FoodItemID, FoodItemName, FoodItemPrice)
            result = adminUser.updateFoodItem(foodItem)
            print(result)
        
        elif choice == 3:
            FoodItemID = input("Enter Food Item ID to delete: ")
            result = adminUser.deleteFoodItem(FoodItemID)
            print(result)

        elif choice == 4:
            menu_list = adminUser.viewMenu()

            print("\nFood Menu:\n")

            if menu_list == "Menu is empty.":
                print("Menu is empty.")
            else:
                for item in menu_list:
                    availability = 'Available' if item.FoodItemAvailability == 1 else 'Not Available'
                    
                    print(f"ID: {item.FoodItemID}, FoodItemName: {item.FoodItemName}, FoodItemPrice: {item.FoodItemPrice}, Availability: {availability}")
            
        elif choice == 5:
            print("Logging out...")
            return
        
        else:
            print("Invalid choice, please try again.")



def chefMenu(chefUser):
    while True:
        print("\nChef Menu:")
        print("1. View Menu")
        print("2. Rollout Tomorrow's Menu")
        print("3. Generate Report")
        print("4. Logout")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            menuList = chefUser.viewMenu()

            print("\nFood Menu:\n")

            if menuList == "Menu is empty.":
                print("Menu is empty.")
            else:
                for item in menuList:
                    availability = 'Available' if item.FoodItemAvailability == 1 else 'Not Available'
                    print(f"ID: {item.FoodItemID}, FoodItemName: {item.FoodItemName}, FoodItemPrice: {item.FoodItemPrice}, Availability: {availability}")
            
        elif choice == 2:

            recommandedFoodItems = chefUser.getRecommendedFoodItems()

            print("\nRecommended Food Items:\n")

            if recommandedFoodItems == "No Recommendation.":
                print("No Recommendation.")
            else:
                for item in recommandedFoodItems:
                    print(f"ID: {item['foodItemID']},    FoodItemName: {item['foodItemName']},    FoodItemRecommendationScore: {item['foodItemRecommendationScore']}")

                
                itemsToRollOut = input("\nEnter the IDs of the items to rollout, separated by spaces: ")

                chefUser.rollOutFoodItems(itemsToRollOut)
                chefUser.nofityEmployees("Chef has rolled out the menu for ", datetime.today().date() + timedelta(days=1))

                print("Menu Rolled Out and employees has been notified.")
        
        elif choice == 3:
            
            print("Generating report...")
            chefUser.generateReport()  

            print("Report generated successfully.")
        
        elif choice == 4:
            print("Logging out...")
            return
        
        else:
            print("Invalid choice, please try again.")








# ----------------------------------------------------------------   EMPLOYEE ---------------------


def employeeMenu(employeeUser):
    while True:
        print("\nEmployee Menu:")
        print("1. View Tomorrow's Menu")
        print("2. View Notifications")
        print("3. Order Food")
        print("4. Provide Feedback")
        print("5. Logout")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            dailMenu = employeeUser.viewDailyMenu()
            print("\nDaily Menu:\n")
            if dailMenu == "Menu is empty.":
                print("Menu is empty.")
            else:
                for item in dailMenu:
                    print(f"ID: {item.FoodItemID}, FoodItemName: {item.FoodItemName}, FoodItemPrice: {item.FoodItemPrice}")

        elif choice == 2:
            notifications = employeeUser.viewNotifications()
            print("\nNotifications from last 24 hrs:\n")
            if notifications == "No notifications.":
                print("No notifications.")
            else:
                for notification in notifications:
                    print(f"{notification}")

        elif choice == 3:
            orderedFoodItemIDs = input("Enter the Food Item ID you want to order (separated by space): ")
            result = employeeUser.orderFood(orderedFoodItemIDs)
            print(result)

        elif choice == 4:
            result = employeeUser.give_feedback()
            print(result)

        elif choice == 5:
            print("Logging out...")
            return

        else:
            print("Invalid choice, please try again.")
