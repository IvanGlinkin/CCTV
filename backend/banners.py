from .functions import get_location_details

### Banner
banner = """
 ██████╗██╗      ██████╗ ███████╗███████╗     ██████╗██╗██████╗  ██████╗██╗   ██╗██╗████████╗                      
██╔════╝██║     ██╔═══██╗██╔════╝██╔════╝    ██╔════╝██║██╔══██╗██╔════╝██║   ██║██║╚══██╔══╝                      
██║     ██║     ██║   ██║███████╗█████╗█████╗██║     ██║██████╔╝██║     ██║   ██║██║   ██║                         
██║     ██║     ██║   ██║╚════██║██╔══╝╚════╝██║     ██║██╔══██╗██║     ██║   ██║██║   ██║                         
╚██████╗███████╗╚██████╔╝███████║███████╗    ╚██████╗██║██║  ██║╚██████╗╚██████╔╝██║   ██║                         
 ╚═════╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝     ╚═════╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝                         
                                                                                                                   
████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗    ██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║    ██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
   ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║    ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
   ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║    ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
   ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║     ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
   ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
   

[ ! ] https://www.linkedin.com/in/IvanGlinkin/
[ ! ] https://x.com/glinkinivan
[ ! ] https://t.me/EASM_HydrAttack                                                                                                               
"""

def print_geo_coordinater(lat,lon):
    print("[ * ] Harvesting information based on the next coordinates:")
    print("\t[ * * ] Latitude: ", lat)
    print("\t[ * * ] Longitude:", lon)

def pring_city_by_geo(lat,lon):
    town, city, country = get_location_details(lat, lon)
    print(f"\t[ * * ] Country:   {country}\n\t[ * * ] City:\t   {city}\n\t[ * * ] Town:\t   {town}\n")

def print_len_steps(steps, radius):
    print("[ * ] Overall steps to be performed:", steps, ", with overall diameter", radius * 2, "meters")

def print_telegram_initialization():
    print("\n[ * ] Telegram client initialization...", end="")

def print_successfully():
    print("successfully")

def print_start_harvesting():
    print("\n[ * ] Start harvesting data:")

def print_current_step(step, lat, lon):
    print(f"\t[ {step} ] Latitude {round(lat, 4)}, Longitude {round(lon, 4)}")

def print_update_local_json():
    print("\t\t[ > ] Harvesting data finished")
    print("\t\t[ > ] Generating JSON file...", end="")

def print_update_html():
    print("\t\t[ > ] Generating HTML file...", end="")

def print_files_stored(report_json_directory, report_html_directory, filename):
    print("\n[ * ] Harvesting is finished and final files are generated:")
    print("\t[ * * ] JSON:" , report_json_directory + filename + ".json")
    print("\t[ * * ] HTML:" , report_html_directory + filename + ".html")

def print_combined_data():
    print("\n[ * ] Combining all JSON files together and generating the global HTML map file")

def finishing_application():
    print("\n[ * ] Everithing has been executed successfully!")
    print("\t[ * * ] Enjoy your CCTV data!")
