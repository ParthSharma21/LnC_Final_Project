import mysql.connector
from mysql.connector import Error

def startConnection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='recomendationengine'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def closeConnection(connection):
    if connection.is_connected():
        connection.close()
