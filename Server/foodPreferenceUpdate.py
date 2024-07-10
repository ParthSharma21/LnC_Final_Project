# foodPreferenceUpdate.py

import Server.databaseFunctions as db

def update_profile(request_data):
    try:
        user_id = request_data['userID']
        food_type = request_data['foodType']
        spice_level = request_data['spiceLevel']
        cuisine_type = request_data['cuisineType']
        sweet_preference = request_data['sweetPreference']

        connection = db.start_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()

        cursor.execute("SELECT UserPreferenceID FROM UserPreference WHERE UserID = %s", (user_id,))
        result = cursor.fetchone()

        if result:

            query = """
                UPDATE UserPreference
                SET FoodType = %s, SpiceLevel = %s, IsSweet = %s, CusineType = %s
                WHERE UserID = %s
            """
            cursor.execute(query, (food_type, spice_level, sweet_preference, cuisine_type, user_id))
        else:

            query = """
                INSERT INTO UserPreference (UserID, FoodType, SpiceLevel, IsSweet, CusineType)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, food_type, spice_level, sweet_preference, cuisine_type))

        connection.commit()
        cursor.close()
        db.close_connection(connection)

        return {"status": "success", "message": "Profile updated successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
