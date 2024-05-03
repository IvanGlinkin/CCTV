from json import dump, load
from math import cos, pi, radians
from os import listdir, path

from requests import get


def generate_pattern(length):
    pattern = []
    pattern.extend([1, 1, 1])  # Start with three occurrences of 1
    for i in range(2, (length - 4) // 2):
        pattern.extend([i, i])
    pattern.append((length - 3) // 2 - 1)
    return pattern

def calculate_length(metres):
    remainder = ((metres + 400) % 800)
    if remainder == 0:
        return metres
    else:
        return (metres - remainder + 800)

# Function to calculate coordinates based on steps and direction
def calculate_coordinates(lat, lon, direction, distance):
    # Radius of the Earth in kilometers
    R = 6378.1  # Earth radius in km
    # Convert latitude and longitude from degrees to radians
    lat_rad = radians(lat)
    lon_rad = radians(lon)
    # Calculate new latitude and longitude based on direction and distance
    if direction == 'starting':
        new_lon = lon
        new_lat = lat
    elif direction == 'west':
        new_lon = lon - (distance / (R * cos(lat_rad))) * (180 / pi)
        new_lat = lat
    elif direction == 'south':
        new_lat = lat - (distance / R) * (180 / pi)
        new_lon = lon
    elif direction == 'east':
        new_lon = lon + (distance / (R * cos(lat_rad))) * (180 / pi)
        new_lat = lat
    elif direction == 'north':
        new_lat = lat + (distance / R) * (180 / pi)
        new_lon = lon
    else:
        raise ValueError("Invalid direction")
    return new_lat, new_lon

# Function to load existing data from file
def load_existing_data(filename):
    existing_data = {}
    if path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = load(file)
    return existing_data

# Function to combine all json files into one
def combine_json_files(folder_path, output_file):
    combined_data = {}
    for filename in listdir(folder_path):
        if filename.endswith('.json') and filename != output_file:
            file_path = path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = load(file)
                combined_data.update(data)  # Merge dictionaries

    with open(output_file, 'w') as output:
        dump(combined_data, output, indent=4)

# Get the city based on coordinates
def get_location_details(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    headers = {
    'User-Agent': 'CCTV Bot'
	}
    response = get(url, headers=headers)
    data = response.json()
    if 'address' in data:
        town = data['address'].get('town', '')
        city = data['address'].get('city', '')
        country = data['address'].get('country', '')
        return town, city, country
    else:
        return None, None, None
