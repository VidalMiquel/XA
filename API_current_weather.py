'''
OBJECTIVE: FOR EACH OF THE REGIONS STORED IN THE DATABASE, THEIR ENCLOSURE IDENTIFIERS ARE RETRIEVED IN SUCH A WAY
THAT FOR EACH OF THEM, THE CORRESPONDING INSERT IS MADE. ONCE THE EXECUTION IS FINISHED, ALL ENCLOSURES PER REGION
ARE UPDATED WITH THE DATA OBTAINED FROM THE API CALL.
'''

import requests
import datetime
import mysql.connector


# Function to obtain current weather data using the OpenWeatherMap API
def get_weather_data(city_name, API_key):
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        min_temperature = data['main']['temp_min']
        max_temperature = data['main']['temp_max']
        cloudiness = data['clouds']['all']
        return min_temperature, max_temperature, cloudiness
    else:
        print("Error fetching weather data. Status code:", response.status_code)
        return None, None, None


# Function to insert data into the CurrentTime table
def insert_data(regions_data, api_key_geocode, api_key_weather):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    connection = mysql.connector.connect(
        host='YOUR_HOST',
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        database='YOUR_DATABASE'
    )

    cursor = connection.cursor()

    for data in regions_data:
        enclosure_identifier = get_enclosure_identifier(data["region"], cursor)
        if data["region"] is not None:
            min_temp, max_temp, cloudiness = get_weather_data(data["region"], api_key_weather)
            if min_temp is not None and max_temp is not None and cloudiness is not None:
                for enclosure in enclosure_identifier:
                    insert_query = """
                    INSERT INTO CurrentTime (Enclosure_identifier, Region, Temperature_min, Temperature_max, Cloudiness, Day, Hour)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (enclosure, data['region'], min_temp, max_temp, cloudiness, current_date, current_time)

                    cursor.execute(insert_query, values)
                    connection.commit()

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




# Call the main function to retrieve coordinates and store the data
def retrieve_and_store_data(api_key_geocode, api_key_weather):
    regions_data = []

    connection = mysql.connector.connect(
        host='YOUR_HOST',
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        database='YOUR_DATABASE'
    )

    cursor = connection.cursor()

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

    insert_data(regions_data, api_key_geocode, api_key_weather)

# Call the main function to retrieve coordinates and store the data
api_key_geocode = 'YOUR_GOOGLE_MAPS_API_KEY'
api_key_weather = 'YOUR_OPENWEATHERMAP_API_KEY'
retrieve_and_store_data(api_key_geocode, api_key_weather)
