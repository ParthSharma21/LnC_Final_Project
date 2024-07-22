import Server.databaseFunctions as df
from decimal import Decimal

def decimalToFloat(number):
    if isinstance(number, Decimal):
        return float(number)
    return number

def getRecommendedFoodItems():
    connection = df.startConnection()

    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()

    cursor.execute("""
            SELECT 
                m.FoodItemID, 
                m.FoodItemName, 
                m.FoodItemPrice, 
                IFNULL(AVG(f.FoodReviewRating), 0) AS AvgRating, 
                IFNULL(AVG(f.Sentiment), 0) AS AvgSentiment,
                COUNT(uo.FoodItemID) AS OrderCount,
                (1.5 * IFNULL(AVG(f.FoodReviewRating), 0) + 0.5 * IFNULL(AVG(f.Sentiment), 0)) AS RecommendationScore
            FROM 
                Menu m
            LEFT JOIN 
                Feedback f ON m.FoodItemID = f.FoodItemID
            LEFT JOIN 
                UserOrderDetails uo ON m.FoodItemID = uo.FoodItemID
            WHERE 
                m.FoodItemAvailability = 1
                AND m.IsDiscarded = FALSE
            GROUP BY 
                m.FoodItemID
            ORDER BY 
                RecommendationScore DESC
            LIMIT 5
        """)
        
    recommendedItems = cursor.fetchall()
    df.closeConnection(connection)

    if recommendedItems:
        recommendedItemsList = []
        for item in recommendedItems:
            recommendedItemsList.append({
                "foodItemID": item[0],
                "foodItemName": item[1],
                "foodItemPrice": decimalToFloat(item[2]),
                "foodItemAverageRating": decimalToFloat(item[3]),
                "foodItemAverageSentiment": decimalToFloat(item[4]),
                "foodItemBoughtCount": item[5],
                "foodItemRecommendationScore": round(decimalToFloat(item[6]), 2)
            })

        return {"status": "success", "data": recommendedItemsList}
    else:
        return {"status": "success", "data": "No Recommendation."}


# print(getRecommendedFoodItems())
