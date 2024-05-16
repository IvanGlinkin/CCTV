from .functions import combine_json_files
from .json_into_html import generate_html_from_json


def combine_data(report_json_directory="./reports-json/", report_html_directory="./reports-html/"):
    combine_json_files(report_json_directory, f"{report_json_directory}_combined_data.json")

    # Generate the HTML file from JSON
    generate_html_from_json(
        f"{report_json_directory}_combined_data.json", f"{report_html_directory}_combined_data.html"
    )


# Call the function to execute the functionality
if __name__ == "__main__":
    combine_data()
