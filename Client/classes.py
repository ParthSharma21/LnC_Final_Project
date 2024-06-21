# classes.py

import Server.databaseFunctions as df
from mysql.connector import Error
# import recommendationEngine as RE
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
    def __init__(self, userID, name, password, role):
        self.userID = userID
        self.name = name
        self.role = role
        self.password = password

class Admin(user):
    def __init__(self, userID, name, password):
        super().__init__(userID, name, password, "Admin")


class Chef(user):
    def __init__(self, userID, name, password):
        super().__init__(userID, name, password, "Chef")

class employee(user):
    def __init__(self, userID, name, password):
        super().__init__(userID, name, password, "Employee")
