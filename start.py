import argparse
import sys
import webbrowser
from datetime import datetime
from json import dump
from os import getcwd, makedirs, path

from backend.banners import (
    banner,
    finishing_application,
    pring_city_by_geo,
    print_combined_data,
    print_current_step,
    print_files_stored,
    print_geo_coordinater,
    print_len_steps,
    print_start_harvesting,
    print_successfully,
    print_telegram_initialization,
    print_update_html,
    print_update_local_json,
)
from backend.combine_data import combine_data
from backend.functions import (
    calculate_coordinates,
    calculate_length,
    countdown_timer,
    download_avatars,
    generate_pattern,
    load_config,
)
from backend.json_into_html import generate_html_from_json
from telethon import functions, types
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Custom settings for script launch')

# Add arguments for latitude, longitude, meters, and timesleep
parser.add_argument('-lat', '--latitude', type=float, help='Latitude setting')
parser.add_argument('-long', '--longitude', type=float, help='Longitude setting')
parser.add_argument('-m', '--meters', type=int, help='Meters setting')
parser.add_argument('-t', '--timesleep', type=int, help='Timesleep setting')
parser.add_argument('-s', '--speed_kmh', type=int, help='Speed setting')

# Add arguments for Telegram credentials
parser.add_argument('-tn', '--telegram_name', type=str, help='Telegram session name')
parser.add_argument('-ti', '--telegram_api_id', type=int, help='Telegram API ID')
parser.add_argument('-th', '--telegram_api_hash', type=str, help='Telegram API hash')

# Parse the command-line arguments
args = parser.parse_args()

#Load or create config file
config_file="config.yaml"
config = load_config(config_file)
# Update settings if provided in command-line arguments
latitude = args.latitude or config['location']['lat']
longitude = args.longitude or config['location']['lon']
meters = args.meters or config['location']['meters']
timesleep = args.timesleep or config['misc']['timesleep']
speed_kmh = args.speed_kmh or config['misc']['speed_kmh']
telegram_name = args.telegram_name or "cctv"
telegram_api_id = args.telegram_api_id or config['api_config']['api_id']
telegram_api_hash = args.telegram_api_hash or config['api_config']['api_hash']

phone_number = config['api_config']['phone']


# General variables
pattern = generate_pattern((calculate_length(meters + 400) + 800) // 200)  # Adjust the length as needed (x / 2 - 2)
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# Store the initial coordinates and initialize lists to store the coordinates for each step
initial_latitude = latitude
initial_longitude = longitude
step_coordinates = []
# Initialize variables to store coordinates and counts
coordinates = []
coordinates_count = 0
coordinates_sum = [0, 0]
# Extract users with distance 500
filtered_users = []
# Initialize an empty dictionary to store user data
users_data = {}
step = 0
filename = f'{latitude}-{longitude}-{current_datetime}'
# Directories
avatar_directory = "./avatars/"
report_json_directory = "./reports-json/"
report_html_directory = "./reports-html/"

# Check if the needed directories exist, create it if not
for dir in avatar_directory, report_json_directory, report_html_directory:
    if not path.exists(dir):
        makedirs(dir)

### Banner logo
print(banner)
### Printing geo cordinates
print_geo_coordinater(latitude,longitude)
### Printing city and country by coordinates
pring_city_by_geo(latitude,longitude)

# Perform steps according to the pattern
for i, steps in enumerate(pattern):
    if i == 0:
        direction = 'starting'
    elif i % 4 == 1:
        direction = 'west'
    elif i % 4 == 2:
        direction = 'south'
    elif i % 4 == 3:
        direction = 'east'
    else:
        direction = 'north'
    for _ in range(steps):
        latitude, longitude = calculate_coordinates(latitude, longitude, direction, 0.6)  # 600 meters in kilometers
        step_coordinates.append((latitude, longitude))

### Print number of steps
print_len_steps(len(step_coordinates), meters)

# Initialize the Telegram client
print_telegram_initialization()


with TelegramClient(telegram_name, telegram_api_id, telegram_api_hash, system_version="CCTV") as client:
    # Authenticate the client
    client.connect()
    print_successfully()

    time_adjusted = round(0.6*3600/speed_kmh) # seconds to cover distance 600 meters
    if timesleep < time_adjusted:
        print(f"[ ! ] Configured timesleep {timesleep}s is too low to cover all points with configured speed {speed_kmh} km/h")
        print(f"[ ! ] Adjusting sleep time to {time_adjusted}s according to calculated distances")
        timesleep = time_adjusted

    # Initialize the dictionary to store user data
    users_data = {}

    # Iterate over latitude and longitude pairs in step_coordinates
    print_start_harvesting()
    for latitude, longitude in step_coordinates:
        try:
          result = client(functions.contacts.GetLocatedRequest(
              geo_point=types.InputGeoPoint(
                  lat=latitude,
                  long=longitude,
                  accuracy_radius=500
              )
          ))
        except FloodWaitError as e:
          print(f"[ ! ] FloodWaitError: {e}")

          # Check if the waiting time exceeds the threshold
          if e.seconds > 300:
              print(f"[ ! ] Waiting time is too long, try again in {round(e.seconds/3600)} hours. Exiting program.")
              sys.exit()
          countdown_timer(e.seconds)
          continue

        # Print the step and its coordinates
        step += 1

        # Print current step with coordinates
        print_current_step(f"{step}/{len(step_coordinates)}", latitude, longitude)

        for update in result.updates:
            if isinstance(update, types.UpdatePeerLocated):
                for peer_located in update.peers:
                    if isinstance(peer_located, types.PeerLocated):  # Check if the peer_located is of type PeerLocated
                        if peer_located.distance == 500:
                            if isinstance(peer_located.peer, types.PeerUser):  # Check if the peer is a PeerUser
                                user_id = peer_located.peer.user_id
                                user_info = next((user for user in result.users if user.id == user_id), None)
                                if user_info:
                                    # Get current timestamp
                                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                    if user_id not in users_data:
                                        # If the user is not in the dictionary, add them with initial data
                                        username = user_info.username

                                        users_data[user_id] = {
                                            "first_name": user_info.first_name,
                                            "last_name": user_info.last_name,
                                            "username": user_info.username,
                                            "phone": user_info.phone,
                                            "photo_id": user_info.photo.photo_id if user_info.photo else None,
                                            "coordinates": [],
                                            "coordinates_average": {"latitude": 0, "longitude": 0, "timestamp": 0}
                                        }
                                    # Append new coordinates
                                    users_data[user_id]["coordinates"].append((latitude, longitude, timestamp))

                                    # Calculate average coordinates
                                    avg_latitude = sum(coord[0] for coord in users_data[user_id]["coordinates"]) / len(users_data[user_id]["coordinates"])
                                    avg_longitude = sum(coord[1] for coord in users_data[user_id]["coordinates"]) / len(users_data[user_id]["coordinates"])

                                    # Update the average coordinates
                                    users_data[user_id]["coordinates_average"] = {"latitude": avg_latitude, "longitude": avg_longitude}

        # Write the updated data to the file
        print_update_local_json()
        with open(f"{report_json_directory}{filename}.json", 'w', encoding='utf-8') as file:
            dump(users_data, file, indent=4)
        print_successfully()

        if not step == len(step_coordinates):
            countdown_timer(timesleep)

#Download avatars
download_avatars(f"{report_json_directory}{filename}.json", avatar_directory)

# Generate the HTML file from JSON
print_update_html()
generate_html_from_json(f"{report_json_directory}{filename}.json", f"{report_html_directory}{filename}.html")
print_successfully()

# Print generated JSON and HTML files path
print_files_stored(report_json_directory, report_html_directory, filename)

# Combine all JSON files together and generate the global map
print_combined_data()
combine_data(report_json_directory, report_html_directory)

current_directory = getcwd()
html_file_current = path.join(current_directory, report_html_directory + filename + ".html")
html_file_combined = path.join(current_directory, 'reports-html', '_combined_data.html')

try:
    webbrowser.open('file://' + path.realpath(html_file_current))
    webbrowser.open('file://' + path.realpath(html_file_combined))
except:
    print("HTML file not found!")

# Finishing the application
finishing_application()
