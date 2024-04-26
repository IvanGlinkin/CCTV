from .functions import combine_json_files
from .json_into_html import generate_html_from_json

def combine_data():
    report_json_directory = "./reports-json/"

    # Specify the folder containing JSON files and the output file name
    json_folder_path = './reports-json/'
    html_folder_path = './reports-html/'
    json_output_file = json_folder_path + '_combined_data.json'
    html_output_file = html_folder_path + '_combined_data.html'

    combine_json_files(json_folder_path, json_output_file)

    # Generate the HTML file from JSON
    generate_html_from_json(json_output_file, html_output_file)

# Call the function to execute the functionality
if __name__ == "__main__":
    combine_data()