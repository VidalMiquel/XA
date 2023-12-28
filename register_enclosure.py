'''
OBJECTIVE:   REGISTER A NEW HABITAT IN THE SYSTEM, FOR WHICH THE USER NEEDS TO PROVIDE A SET OF NECESSARY DATA. 
             THESE ARE STORED IN THE CORRESPONDING DATABASE TABLE
'''

import sys
import mysql.connector

# Function to register a new habitat in the system
def register_habitat(Enclosure_identifier, Region, Quantity_of_panels, Panels_orientation, Estimated_energy_generation):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )

    # Create a cursor to execute queries
    cursor = connection.cursor()

    # Insert values into the Enclosure table
    insert_query = """
    INSERT INTO Enclosure (Enclosure_identifier, Region, Quantity_of_panels, Panels_orientation, Estimated_energy_generation)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Assemble values for the query
    values = (
        Enclosure_identifier,
        Region,
        Quantity_of_panels,
        Panels_orientation,
        Estimated_energy_generation
    )

    # Execute the insertion query
    cursor.execute(insert_query, values)

    # Confirm the insertion
    connection.commit()

    # Close cursor and database connection
    cursor.close()
    connection.close()

# Main function to retrieve arguments and call register_habitat
def main():
    # Check if the necessary arguments have been provided
    if len(sys.argv) != 6:
        print("Error: 5 arguments are required.")
        print("Usage: python alta_habitat.py Enclosure_identifier Region Quantity_of_panels Panels_orientation Estimated_energy_generation")
        sys.exit(1)

    # Assign the arguments to respective variables
    Enclosure_identifier, Region, Quantity_of_panels, Panels_orientation, Estimated_energy_generation = sys.argv[1:]

    # Call the function register_habitat with the provided arguments
    register_habitat(Enclosure_identifier, Region, Quantity_of_panels, Panels_orientation, Estimated_energy_generation)

# Call the main function
if __name__ == "__main__":
    main()
