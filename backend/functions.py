import sys
from concurrent.futures import ThreadPoolExecutor
from json import dump, load
from math import cos, pi, radians
from os import listdir, path
from time import sleep

import yaml
from bs4 import BeautifulSoup
from requests import get


def generate_pattern(length):
    pattern = []
    pattern.extend([1, 1, 1])  # Start with three occurrences of 1
    for i in range(2, (length - 4) // 2):
        pattern.extend([i, i])
    pattern.append((length - 3) // 2 - 1)
    return pattern


def calculate_length(metres):
    remainder = (metres + 400) % 800
    if remainder == 0:
        return metres
    else:
        return metres - remainder + 800


# Function to calculate coordinates based on steps and direction
def calculate_coordinates(lat, lon, direction, distance):
    # Radius of the Earth in kilometers
    r = 6378.1  # Earth radius in km
    # Convert latitude and longitude from degrees to radians
    lat_rad = radians(lat)

    # Calculate new latitude and longitude based on direction and distance
    if direction == "starting":
        new_lon = lon
        new_lat = lat
    elif direction == "west":
        new_lon = lon - (distance / (r * cos(lat_rad))) * (180 / pi)
        new_lat = lat
    elif direction == "south":
        new_lat = lat - (distance / r) * (180 / pi)
        new_lon = lon
    elif direction == "east":
        new_lon = lon + (distance / (r * cos(lat_rad))) * (180 / pi)
        new_lat = lat
    elif direction == "north":
        new_lat = lat + (distance / r) * (180 / pi)
        new_lon = lon
    else:
        raise ValueError("Invalid direction")
    return new_lat, new_lon


# Function to combine all json files into one
def combine_json_files(folder_path, output_file):
    combined_data = {}
    for filename in listdir(folder_path):
        file_path = path.join(folder_path, filename)
        if filename.endswith(".json") and filename != output_file:
            with open(file_path) as file:
                data = load(file)
                combined_data.update(data)  # Merge dictionaries

    with open(output_file, "w") as output:
        dump(combined_data, output, indent=4)


# Get the city based on coordinates
def get_location_details(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/reverse"
    headers = {"User-Agent": "CCTV Bot"}
    response = get(url, headers=headers, params={"lat": latitude, "lon": longitude, "format": "json"})

    if response.status_code == 200 and "application/json" in response.headers.get("Content-Type"):
        data: dict = response.json()
        if "address" in data:
            town = data["address"].get("town", "")
            city = data["address"].get("city", "")
            country = data["address"].get("country", "")
            return town, city, country

    return "", "", ""


def countdown_timer(duration):
    for remaining in range(duration, 0, -1):
        print(f"\t\t[ > ] Sleeping for {remaining} seconds before processing the next coordinates...", end="\r")
        sleep(1)
    print(" " * 100, end="\r")  # Clear the line after countdown


# Download avatars
def download_avatar(user_id, username, user_url, output_folder):
    avatar_filename = path.join(output_folder, f"{user_id}-{username}.jpg")
    if username is None:
        return

    if path.exists(avatar_filename):
        print(f"Avatar for user {user_id}-{username} already exists. Skipping download.")
        return

    try:
        response = get(user_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            meta_tag = soup.find("meta", property="og:image")
            if meta_tag and "cdn-telegram.org" in meta_tag["content"]:
                image_url = meta_tag["content"]
                response = get(image_url)
                if response.status_code == 200:
                    with open(avatar_filename, "wb") as image_file:
                        image_file.write(response.content)
                    print(f"Downloaded avatar for user {user_id}-{username} successfully")
                else:
                    print(
                        f"Failed to download avatar for user {user_id}-{username}. Status code: {response.status_code}"
                    )
            else:
                print(f"No profile photo found for user {user_id}-{username}")
        else:
            print(f"Failed to fetch user page for user {user_id}-{username}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading avatar for user {user_id}-{username}: {e}")


def download_avatars(json_file, output_folder):
    print(f"Starting avatars download based on {json_file}...")
    with open(json_file) as f:
        data = load(f)

    with ThreadPoolExecutor(max_workers=5) as executor:
        for user_id, user_data in data.items():
            # Skip users without a photo_id
            if user_data.get("photo_id") is None:
                continue
            username = user_data.get("username", "")
            user_url = f"https://t.me/{username}"
            executor.submit(download_avatar, user_id, username, user_url, output_folder)


def create_config(file_path):
    """Create a custom YAML configuration file by asking the user for input."""

    settings = {
        "api_config": {
            "phone": {
                "prompt": "TG phone number: ",
                "default": None,
                "mandatory": True
            },
            "api_id": {
                "prompt": "TG api_id: ",
                "default": None,
                "mandatory": True,
                "type": int
            },
            "api_hash": {
                "prompt": "TG api_hash:",
                "default": None,
                "mandatory": True
            },
        },
        "location": {
            "lat": {
                "prompt": "Starting latitude [51.51404]: ",
                "default": 51.51404,
                "mandatory": False,
                "type": float
            },
            "lon": {
                "prompt": "Starting longitude [-0.15063]: ",
                "default": -0.15063,
                "mandatory": False,
                "type": float,
            },
            "meters": {
                "prompt": "Search radius(meters) [1200]: ",
                "default": 1200,
                "mandatory": False,
                "type": int
            },
        },
        "misc": {
            "timesleep": {
                "prompt": "Waiting time between locations(sec) [30]: ",
                "default": 30,
                "mandatory": False,
                "type": int,
            },
            "speed_kmh": {
                "prompt": "Moving speed between locations(km/h) [50]: ",
                "default": 50,
                "mandatory": False,
                "type": int,
            },
        },
    }

    # Create a dictionary to store the configurations
    config_data = {group: {} for group in settings}

    print("\nCheck README.md and prepare required values at https://my.telegram.org/auth")
    # Iterate over the settings dictionary to prompt user for each value
    for group, group_settings in settings.items():
        for setting, details in group_settings.items():
            while True:  # Loop until valid input is given or the program exits
                user_input = input(details["prompt"])
                if details["mandatory"] and not user_input.strip():  # Check if the input is mandatory and empty
                    print(f"Value {setting} is mandatory. Exiting program.")
                    sys.exit()  # Exit the program if input is mandatory and not provided
                elif user_input.strip():
                    value = details["type"](user_input) if "type" in details else user_input
                    config_data[group][setting] = value
                    break
                elif details["default"] is not None:  # Use default if available and input is not mandatory
                    config_data[group][setting] = details["default"]
                    break
                else:
                    print(f"No input provided for {setting}, and no default available. Exiting program.")
                    sys.exit()  # Exit if no default is available and input is not provided

    # Write the collected data to a YAML file
    with open(file_path, "w") as file:
        yaml.safe_dump(config_data, file)
    print(f"Config file created at {file_path}")


def load_config(file_path):
    """Load the YAML configuration file, creating it if it does not exist."""
    if not path.exists(file_path):
        print(f"No config file found at {file_path}. Creating initial configuration...")
        create_config(file_path)

    with open(file_path) as file:
        return yaml.safe_load(file)
