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


# Task 1: Add a Member
def add_member(member_id, name, age):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        add_member_query = """
        INSERT INTO Members (id, name, age)
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_member_query, (member_id, name, age))
        connection.commit()
        print(f"Member {name} added successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("Error: Duplicate member ID.")
        else:
            print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Task 2: Add a Workout Session
def add_workout_session(member_id, session_date, session_time, activity):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        add_session_query = """
        INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(add_session_query, (member_id, session_date, session_time, activity))
        connection.commit()
        print("Workout session added successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_FIELD_ERROR:
            print("Error: Invalid column name.")
        else:
            print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Task 3: Update Member Information
def update_member_age(member_id, new_age):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        # Check if member exists
        check_member_query = "SELECT id FROM Members WHERE id = %s"
        cursor.execute(check_member_query, (member_id,))
        if cursor.fetchone() is None:
            print("Member ID not found.")
            return
        # Update age
        update_age_query = "UPDATE Members SET age = %s WHERE id = %s"
        cursor.execute(update_age_query, (new_age, member_id))
        connection.commit()
        print("Member age updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Task 4: Delete a Workout Session
def delete_workout_session(session_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        # Check if session exists
        check_session_query = "SELECT session_id FROM WorkoutSessions WHERE session_id = %s"
        cursor.execute(check_session_query, (session_id,))
        if cursor.fetchone() is None:
            print("Workout session ID not found.")
            return
        # Delete session
        delete_session_query = "DELETE FROM WorkoutSessions WHERE session_id = %s"
        cursor.execute(delete_session_query, (session_id,))
        connection.commit()
        print("Workout session deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Example usage
if __name__ == "__main__":
    # Ensure these IDs and values do not conflict with existing data
    add_member(4, "Michael Smith", 28)  # Use ID 4
    add_workout_session(4, "2024-06-22", "08:00:00", "Yoga")  # Match column names exactly
    update_member_age(4, 29)
    
    # Ensure the session ID exists in the database before attempting to delete
    # Retrieve an existing session_id to use for deletion
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT session_id FROM WorkoutSessions LIMIT 1")
    session_id = cursor.fetchone()
    if session_id:
        delete_workout_session(session_id[0])  # Use an existing session ID
    else:
        print("No workout sessions available to delete.")
    cursor.close()
    connection.close()
