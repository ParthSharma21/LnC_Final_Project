# RecommendationEngine.py
import Server.databaseFunctions as df
from decimal import Decimal

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def getRecommendedFoodItems():
    connection = df.start_connection()

    if not connection:
        return {"status": "error", "message": "Database connection failed"}

    cursor = connection.cursor()

    cursor.execute("""
            SELECT 
                m.FoodItemID, 
                m.FoodItemName, 
                m.FoodItemPrice, 
                IFNULL(AVG(f.FoodReviewRating), 0) AS AvgRating, 
                COUNT(uo.FoodItemID) AS OrderCount,
                (1.5 * IFNULL(AVG(f.FoodReviewRating), 0) + 0.5 * COUNT(uo.FoodItemID)) AS RecommendationScore
            FROM 
                Menu m
            LEFT JOIN 
                Feedback f ON m.FoodItemID = f.FoodItemID
            LEFT JOIN 
                UserOrderDetails uo ON m.FoodItemID = uo.FoodItemID
            WHERE 
                m.FoodItemAvailability = 1
            GROUP BY 
                m.FoodItemID
            ORDER BY 
                RecommendationScore DESC
            LIMIT 5
        """)
        
    recommended_items = cursor.fetchall()
    df.close_connection(connection)

    if recommended_items:
        recommended_items_list = []
        for item in recommended_items:
            recommended_items_list.append({
                "foodItemID": item[0],
                "foodItemName": item[1],
                "foodItemPrice": decimal_to_float(item[2]),
                "foodItemAverageRating": decimal_to_float(item[3]),
                "foodItemBoughtCount": item[4],
                "foodItemRecommendationScore": decimal_to_float(item[5])
            })

        return {"status": "success", "data": recommended_items_list}
    else:
        return {"status": "success", "data": "No Recommendation."}
    



# Test the function
# print(getRecommendedFoodItems())
