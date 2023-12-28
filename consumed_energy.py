'''
OBJECTIVE: STORE THE DATA ASSOCIATED WITH ENERGY CONSUMPTION OF HOUSES REGISTERED IN THE SYSTEM.
'''


import requests
import datetime
import mysql.connector

def get_enclosure_identifiers(cursor):
    try:
        # SQL query to fetch all enclosure identifiers from the 'Enclosure' table
        query = "SELECT Enclosure_identifier FROM Enclosure"
        # Execute the SQL query
        cursor.execute(query)
        # Get all enclosure identifiers
        identifiers = cursor.fetchall()
        return identifiers

    except mysql.connector.Error as error:
        print("Error fetching enclosure identifiers:", error)
        return None


# Function to make a GET request to the Huawei inverter API
def make_get_request(url, params):
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

# Function to insert data into the ConsumedEnergy table
def insert_consumed_energy_data(id, consumed_energy, current_date, current_time, cursor):
    insert_query = """
    INSERT INTO ConsumedEnergy (Enclosure_identifier, Consumed_Energy, Day, Hour)
    VALUES (%s, %s, %s, %s)
    """
    values = (id, consumed_energy, current_date, current_time)

    cursor.execute(insert_query, values)

# Main function to obtain the amount of consumed energy for each enclosure
def get_energy_consumption():

    mysql_connection, mysql_cursor = configure_database()
    # Get current time
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d/%m/%Y')

    identifiers = get_enclosure_identifiers(mysql_cursor)

    for identifier in identifiers:

        # Configuration for the Huawei inverter API
        API_URL = f"https://api.huawei-inverter/q={identifier}.com/data"
        PARAMETERS = {
            "api_key": "YOUR_API_KEY",
            "required_data": ["ConsumedEnergy"]
            # Other parameters based on Huawei inverter API documentation
        }

        # Make a GET request to Huawei inverter API
        api_response = make_get_request(API_URL, PARAMETERS)

        # Insert data into the ConsumedEnergy table in the MySQL database
        if api_response:
            consumed_energy = api_response.get("consumed_energy")
            # Other data to retrieve from the API response

            insert_consumed_energy_data(identifier, consumed_energy, current_date, current_time, mysql_cursor)
            mysql_connection.commit()
            print("Data inserted successfully into the database")

    # Close connection and cursor to the MySQL database
    mysql_cursor.close()
    mysql_connection.close()


def configure_database():
     # Configuration for MySQL database connection
        mysql_connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )

        # Create a cursor to execute MySQL queries
        mysql_cursor = mysql_connection.cursor()
        return mysql_connection, mysql_cursor

# Call the main function to obtain the amount of consumed energy for each enclosure
get_energy_consumption()
