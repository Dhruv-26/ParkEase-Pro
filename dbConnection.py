# import sqlite3
#
#
# connection = sqlite3.connect('parking.db')
# mycursor = connection.cursor()
# mycursor.execute("""CREATE TABLE IF NOT EXISTS users (number_plate text PRIMARY KEY, entered_time text)""")
# connection.commit()
#
# connection.commit()
# #connection.close()

import mysql.connector

# Replace these with your MySQL server details
host='localhost',
user='root',
password='pwd12345',
database='users'

# Establish a connection to the MySQL server
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pwd12345',
        database='users'
    )
    if connection.is_connected():
        print("Connected to MySQL server")

        # Create a cursor object to interact with the database
        mycursor = connection.cursor()

        # Create the 'users' table if it doesn't exist
        mycursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            number_plate VARCHAR(255) PRIMARY KEY,
                            entered_time VARCHAR(255)
                        )""")

        # Commit the changes to the database
        connection.commit()

        print("Table 'users' created successfully.")

    else:
        print("Failed to connect to MySQL server")

except mysql.connector.Error as e:
    print(f"Error: {e}")

# finally:
#     # Close the connection when done
#     if 'connection' in locals() and connection.is_connected():
#         mycursor.close()  # Close the cursor before closing the connection
#         connection.close()
#         print("MySQL connection closed")
