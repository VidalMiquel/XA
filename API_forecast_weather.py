'''
OBJECTIVE: FOR EACH OF THE REGIONS STORED IN THE DATABASE, THEIR ENCLOSURE IDENTIFIERS ARE RETRIEVED IN SUCH A WAY
THAT FOR EACH OF THEM, THE CORRESPONDING INSERT IS MADE. WE NEED TO KEEP IN MIND THAT WE HAVE A RANGE OF INFORMATION
TO UPDATE, WE NEED TO TAKE IT INTO ACCOUNT. ONCE THE EXECUTION IS FINISHED, ALL ENCLOSURES PER REGION ARE UPDATED 
WITH THE DATA OBTAINED FROM THE API.
'''

import datetime
from multiprocessing import connection
import requests
import mysql.connector

# Function to retrieve weather forecast data and store it in the database
def get_weather_forecast(api_key, regions):
    # Get current date and time
    current_date = datetime.datetime.now().strftime('%d/%m/%Y')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    for region in regions:
        # URL for the API request
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={region}&appid={api_key}"

        # Make GET request to the API
        response = requests.get(url)
        connection, cursor = manage_DB()
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Convert the response to JSON format

            # Get forecast data for the upcoming days
            forecast_data = data['list']
            enclosure_identifier = get_enclosure_identifier(data["region"], cursor)
            for enclosure in enclosure_identifier:
                # Iterating over forecast data and performing insertions
                for forecast in forecast_data:
                    date_time = forecast['dt_txt']
                    min_temperature = forecast['main']['temp_min']
                    max_temperature = forecast['main']['temp_max']
                    cloudiness = forecast['clouds']['all']

                    # Convert date and time from text to readable format
                    date_time_formatted = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    current_hour = date_time_formatted.strftime('%H:%M:%S')

                    # Perform insertion into the database table
                    insert_query = """
                    INSERT INTO Forecast (Enclosure_identifier, Region, Minimum_temperature, Maximum_temperature, Cloudiness, Day, Hour)
                    VALUES ({enclosure}, {region}, {min_temp}, {max_temp}, {cloudiness}, '{current_date}', '{current_hour}');
                    """.format(enclosure = enclosure, region = region, min_temp=min_temperature, max_temp=max_temperature, cloudiness=cloudiness, current_date=current_date, current_hour=current_hour)

                    # Execute the query
                    cursor.execute(insert_query)

            # Commit the insertions
            connection.commit()
        else:
            print("Error fetching data. Status code:", response.status_code)
    
     # Close cursor and database connection
        cursor.close()
        connection.close()


def get_enclosure_identifier(region, cursor):
    # Query to obtain all Enclosure_identifier values for the specific region
    select_query = """
                SELECT Enclosure_identifier
                FROM Enclosure
                WHERE Region = {region}
                """

    # Execute the query to obtain Enclosure_identifier values
    cursor.execute(select_query, (region,))
    enclosure_identifiers = cursor.fetchall()  # Get all Enclosure_identifier values
    return enclosure_identifiers

# Call the main function to retrieve the weather forecast and store it in the database
def retrieve_and_store_forecast():
    api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    
    regions_data = []

    connection, cursor = manage_DB()

    region_query = "SELECT DISTINCT Region FROM Enclosure"
    cursor.execute(region_query)
    regions = cursor.fetchall()

    for region in regions:
        region_name = region[0]
        data = {
            'region': region_name
        }
        regions_data.append(data)

    cursor.close()
    connection.close()

    get_weather_forecast(api_key, regions_data)

def get_enclosure_identifier(region, cursor):
    # Query to obtain all Enclosure_identifier values for the specific region
    select_query = """
                SELECT Enclosure_identifier
                FROM Enclosure
                WHERE Region = {region}
                """

    # Execute the query to obtain Enclosure_identifier values
    cursor.execute(select_query, (region,))
    enclosure_identifiers = cursor.fetchall()  # Get all Enclosure_identifier values
    return enclosure_identifiers

def manage_DB():
     # MySQL database connection
        connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )

        # Create a cursor to execute queries
        cursor = connection.cursor()
        return connection, cursor


# Call the main function
retrieve_and_store_forecast()
