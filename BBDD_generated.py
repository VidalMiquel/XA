'''
OBJECTIVE: DYNAMICALLY INTRODUCE THE TABLES THAT WILL FORM OUR DATABASE
'''


import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# SQL statements to create tables
table_queries = [
    """CREATE TABLE IF NOT EXISTS CurrentTime (
        Enclosure_identifier INT PRIMARY KEY,
        Region VARCHAR(255),
        Temperature_min FLOAT,
        Temperature_max FLOAT,
        Cloudiness INT,
        Day INT,
        Hour INT
    )""",
    """CREATE TABLE IF NOT EXISTS Forecast (
        Enclosure_identifier INT,
        Identifier_region VARCHAR(255),
        Minimum_temperature FLOAT,
        Maximum_temperature FLOAT,
        Cloudiness INT,
        Day INT,
        Hour INT,
        PRIMARY KEY (Enclosure_identifier)
    )""",
    """CREATE TABLE IF NOT EXISTS GeneratedData(
        Enclosure_identifier INT PRIMARY KEY,
        Energy_produced FLOAT,
        Day INT,
        Hour INT
    )""",
    """CREATE TABLE IF NOT EXISTS ConsumptionData (
        Enclosure_identifier INT PRIMARY KEY,
        Consumed_Energy DECIMAL(10, 2),
        Day INT,
        Hour INT
    )""",
    """CREATE TABLE IF NOT EXISTS Enclosure(
        Enclosure_identifier INT PRIMARY KEY,
        Region VARCHAR(255),
        Quantity_of_panels FLOAT,
        Panels_orientation INT,
        Estimated_energy_generation FLOAT
    )"""
]

# Execute queries to create tables
for query in table_queries:
    cursor.execute(query)

# Close cursor and connection
cursor.close()
conn.close()
