import mysql.connector
from mysql.connector import errorcode

# Establish connection to the database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='****************',
            host='localhost',
            database='fitness_center_db'
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

# Task 1: Retrieve members within a specific age range using SQL BETWEEN
def get_members_in_age_range(start_age, end_age):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
    try:
        query = """
        SELECT id, name, age
        FROM Members
        WHERE age BETWEEN %s AND %s
        """
        cursor.execute(query, (start_age, end_age))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f"ID: {row['id']}, Name: {row['name']}, Age: {row['age']}")
        else:
            print(f"No members found between ages {start_age} and {end_age}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Example usage
if __name__ == "__main__":
    get_members_in_age_range(25, 30)
