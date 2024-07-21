import Server.authenticationAndLogin as Login
import Server.databaseFunctions as db
from datetime import datetime, timedelta
from SentimentAnalysisEngine import SentimentalAnalyser as sentiment


def rolloutMenu(requestData):
    try:
        foodItemsToRollOutIDs = requestData['foodItemIDs']

        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE DailyMenu")
        for itemID in foodItemsToRollOutIDs:
            cursor.execute(
                "INSERT INTO DailyMenu (FoodItemID, FoodItemName, FoodItemPrice) "
                "SELECT FoodItemID, FoodItemName, FoodItemPrice FROM Menu WHERE FoodItemID = %s AND IsDiscarded = FALSE", 
                (itemID,)
            )
        connection.commit()

        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Food items rolled out successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}




def notifyEmployees(requestData):
    try:
        message = requestData['message']
        date = requestData['date']
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Notifications (NotificationMessage, NotificationGeneratedAtTimeStamp, GeneratedByUserID) "
            "VALUES (%s, %s, %s)", 
            (message + str(date), datetime.now(), requestData['userID'])
        )
        connection.commit()
        cursor.close()
        db.closeConnection(connection)

        return {"status": "success", "message": "Employees notified successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}



def generateReport():
    try:
        connection = db.startConnection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        date30DaysAgo = datetime.now() - timedelta(days=30)

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
                AND m.IsDiscarded = FALSE
            GROUP BY 
                m.FoodItemName
            ORDER BY 
                OrderCount DESC
        """, (date30DaysAgo,))

        reportData = cursor.fetchall()
        db.closeConnection(connection)

        if not reportData:
            return {"status": "success", "data": [], "message": "No sales in the last 30 days."}

        report = []
        for item in reportData:
            report.append({"FoodItemName": item[0], "OrderCount": item[1]})

        return {"status": "success", "data": report, "message": "Sales report generated successfully!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
