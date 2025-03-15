import mysql.connector
from mysql.connector import Error

try:
    # Provide your correct credentials here
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FIroza@2003"
    )

    if connection.is_connected():
        print("Connection to MySQL server was successful!")

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # SQL query to create a new database
        create_database_query = "CREATE DATABASE IF NOT EXISTS tennis_db"
        cursor.execute(create_database_query)
        print("Database 'tennis_db' created successfully!")

except Error as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")