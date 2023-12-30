'''
OBJECTIVE:  TO OBTAIN THE VALUES OF THE LAST 24 HOURS OF CLOUDINESS AND GENERATED ENERGY, AND THE VALUES OF THE NEXT 
            24 HOURS OF CLOUDINESS, AND PREDICT THE ENERGY THAT WILL BE GENERATED UNDER THESE CONDITIONS. TO DO THIS,
            WE PERFORM A RULE OF THREE TO OBTAIN THE ARRAY OF VALUES TO BE SUBSEQUENTLY VISUALIZED THROUGH A GRAPH.
'''

import sys
import mysql.connector

def fetch_data_for_enclosure_id(enclosure_id):
    # Establish connection to the database and fetch data
    connection = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )
    cursor = connection.cursor()

    # Retrieve cloudiness data from CurrentTime table for the last 24 hours
    cursor.execute(f"SELECT Cloudiness FROM CurrentTime WHERE Enclosure_identifier = %s AND STR_TO_DATE(CONCAT(Day, ' ', Hour), '%%d-%%m-%%Y %%H-%%i-%%s') >= DATE_SUB(NOW(), INTERVAL 1 DAY)", (enclosure_id,))
    cloudiness_current = cursor.fetchall()

    # Retrieve cloudiness data from Forecast table for the next 24 hours
    cursor.execute(f"SELECT Cloudiness FROM Forecast WHERE Enclosure_identifier = %s AND STR_TO_DATE(CONCAT(Day, ' ', Hour), '%%d-%%m-%%Y %%H-%%i-%%s') > NOW() AND STR_TO_DATE(CONCAT(Day, ' ', Hour), '%%d-%%m-%%Y %%H-%%i-%%s') <= DATE_ADD(NOW(), INTERVAL 1 DAY)", (enclosure_id,))
    cloudiness_forecast = cursor.fetchall()

    # Retrieve generated energy data for the last 24 hours
    cursor.execute(f"SELECT Energy_produced FROM GeneratedData WHERE Enclosure_identifier = %s AND Day >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)", (enclosure_id,))
    generated_energy = cursor.fetchall()

    connection.close()

    return cloudiness_current, cloudiness_forecast, generated_energy

def calculate_predicted_energy(cloudiness_forecast_list, generated_energy_list, cloudiness_current_list):
    predicted_energy_list = []
    # Calculate predicted energy for each corresponding data point
    for i in range(len(cloudiness_forecast_list)):
        if None not in (cloudiness_forecast_list[i], generated_energy_list[i], cloudiness_current_list[i]):
            predicted_energy = (cloudiness_forecast_list[i][0] * generated_energy_list[i][0]) / cloudiness_current_list[i][0]
            predicted_energy_list.append(predicted_energy)
        else:
            predicted_energy_list.append(None)
    return predicted_energy_list

def get_enclosure_identifier():
    # Retrieve enclosure identifier from user input or arguments
    if len(sys.argv) < 2:
        print("No enclosure_identifier value provided.")
        return None
    else:
        enclosure_value = sys.argv[1]
        return enclosure_value

enclosure_identifier = get_enclosure_identifier()

if enclosure_identifier is not None:
    # Fetch data from the database
    data = fetch_data_for_enclosure_id(enclosure_identifier)
    cloudiness_current, cloudiness_forecast, generated_energy = data

    # Check if data exists and calculate predicted_energy_list
    if None not in (cloudiness_current, cloudiness_forecast, generated_energy):
        predicted_energy_list = calculate_predicted_energy(cloudiness_forecast, generated_energy, cloudiness_current)
        
    
