#!/bin/bash

echo "Please enter the following values to register a new habitat:"

read -p "Enclosure Identifier: " Enclosure_identifier
read -p "Region: " Region
read -p "Quantity of Panels: " Quantity_of_panels
read -p "Panels Orientation: " Panels_orientation
read -p "Estimated Energy Generation: " Estimated_energy_generation

# Call the Python script with the provided values as arguments
python register_enclosure.py "$Enclosure_identifier" "$Region" "$Quantity_of_panels" "$Panels_orientation" "$Estimated_energy_generation"
