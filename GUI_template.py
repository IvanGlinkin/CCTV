import os
from sys import argv, exit
from webbrowser import open

from folium import Map, Marker
from folium.plugins import MousePosition
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from backend.general_settings import latitude, longitude, meters


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Close-Circuit Telegram Vision")
        self.setGeometry(0, 0, 1200, 800)  # Set window size to 800x800

        # Create menu bar
        menubar = self.create_menu_bar()
        self.setMenuBar(menubar)

        # Create vertical splitter for upper and bottom parts
        vertical_splitter = QSplitter(self)
        self.setCentralWidget(vertical_splitter)

        # Create horizontal splitter for upper parts
        upper_splitter = QSplitter()
        vertical_splitter.addWidget(upper_splitter)

        # Create upper left widget
        upper_left_widget = QWidget()
        upper_left_layout = QVBoxLayout(upper_left_widget)
        upper_left_layout.setContentsMargins(0, 0, 0, 0)

        # Create bottom
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet("background-color: black; color: white")  # Set background color

        # Add widgets to bottom splitter
        upper_splitter.addWidget(upper_left_widget)
        upper_splitter.addWidget(bottom_widget)

        # Set sizes for the upper parts
        upper_splitter.setSizes([600, 200])  # Initial sizes for upper parts
        upper_splitter.setOrientation(0)  # Set horizontal orientation
        upper_splitter.setStretchFactor(0, 1)  # Allow adjusting height of the upper parts

        # Create right widget
        # upper_right_widget = QWidget()
        upper_right_widget = SettingsWidget()

        # Add right widget to vertical splitter
        vertical_splitter.addWidget(upper_right_widget)

        # Set sizes for the bottom part
        vertical_splitter.setSizes([900, 300])  # Initial sizes for bottom part
        vertical_splitter.setStretchFactor(0, 1)  # Allow adjusting height of the bottom part

        self.browser = QWebEngineView()
        upper_left_layout.addWidget(self.browser)
        # Load map
        self.load_map()

    def load_map(self):
        from backend.general_settings import latitude as default_latitude
        from backend.general_settings import longitude as default_longitude

        m = Map(location=[default_latitude, default_longitude], zoom_start=12)

        MousePosition().add_to(m)  # Add mouse position display

        # Add a marker to the middle of the map
        middle_latitude = default_latitude
        middle_longitude = default_longitude
        Marker([middle_latitude, middle_longitude]).add_to(m)

        m_html = m.get_root().render()
        self.browser.setHtml(m_html)  # Load the modified Folium map HTML directly into the QWebEngineView

    def new_request(self):
        print("test")

    def open_telegram_settings_window(self):
        telegram_settings_dialog = TelegramSettingsDialog()  # Create an instance of the AboutDialog
        telegram_settings_dialog.exec_()  # Show the dialog modally, blocking the main window

    def open_general_settings_window(self):
        general_settings_dialog = GeneralSettingsDialog()  # Create an instance of the AboutDialog
        general_settings_dialog.exec_()  # Show the dialog modally, blocking the main window

    def show_about_dialog(self):
        about_dialog = AboutDialog()  # Create an instance of the AboutDialog
        about_dialog.exec_()  # Show the dialog modally, blocking the main window

    def open_global_map(self):
        # Path to your HTML file
        current_directory = os.getcwd()
        html_file_path = os.path.join(current_directory, "reports-html", "_combined_data.html")

        # Check if the HTML file exists
        if os.path.exists(html_file_path):
            open("file://" + os.path.realpath(html_file_path))
        else:
            print("HTML file not found!")

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Set style for the menu bar
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: black;
                color: white;
                padding:7px;
            }
            QMenuBar::item {
                background-color: black;
                color: white;
                margin-right: 15px;
                padding: 5px;
            }
            QMenuBar::item:selected {
                background-color: #ccc;
                color: black;
                border-radius: 5px;
            }
            QMenu {
                background-color: black;
                color: white;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QMenu::item {
                background-color: black;
                color: white;
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #ccc;
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Create File menu
        file_menu = menubar.addMenu("&File")

        # Create actions for File menu
        new_request_action = QAction("&New request", self)
        new_request_action.setShortcut("Ctrl+n")
        new_request_action.setStatusTip("New request")
        new_request_action.triggered.connect(self.new_request)
        file_menu.addAction(new_request_action)

        open_request_action = QAction("&Open request", self)
        open_request_action.setShortcut("Ctrl+o")
        open_request_action.setStatusTip("Open request")
        open_request_action.triggered.connect(self.new_request)
        file_menu.addAction(open_request_action)

        open_global_action = QAction("&Open global map", self)
        open_global_action.setShortcut("Ctrl+Shift+o")
        open_global_action.setStatusTip("Open global map")
        open_global_action.triggered.connect(self.open_global_map)
        file_menu.addAction(open_global_action)

        # Add a separator line
        separator_action = QAction(self)
        separator_action.setSeparator(True)
        file_menu.addAction(separator_action)
        file_menu.setStyleSheet("QMenu::separator { background-color: #ccc; height: 1px; margin: 5px}")

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create Settings menu
        settings_menu = menubar.addMenu("&Settings")

        telegram_settings_action = QAction("&Telegram settings", self)
        telegram_settings_action.setStatusTip("Telegram setting")
        telegram_settings_action.triggered.connect(self.open_telegram_settings_window)
        settings_menu.addAction(telegram_settings_action)

        general_settings_action = QAction("&General settings", self)
        general_settings_action.setStatusTip("General setting")
        general_settings_action.triggered.connect(self.open_general_settings_window)
        settings_menu.addAction(general_settings_action)

        # Create About menu
        about_menu = menubar.addMenu("&About")

        # Create actions for About menu
        about_action = QAction("&About", self)
        about_action.setStatusTip("&About")
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)

        return menubar


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Load settings
        self.meters = meters
        self.latitude = latitude
        self.longitude = longitude

        # Round meters to the nearest multiple of 100
        self.meters = round(self.meters / 100) * 100

        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set vertical spacing between elements

        # Create slider for meters
        self.slider_label = QLabel("Search radius (meters):")
        layout.addWidget(self.slider_label)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(400)
        self.slider.setMaximum(4000)
        self.slider.setSingleStep(1000)
        self.slider.setValue(self.meters)
        self.slider.valueChanged.connect(self.slider_changed)
        layout.addWidget(self.slider)

        # Create label for slider position
        self.slider_position_label = QLabel(f"Current radius: {self.meters} meters")
        layout.addWidget(self.slider_position_label)

        # Create layout for latitude and longitude
        # lat_long_layout = QHBoxLayout()

        # Create layout for latitude
        lat_layout = QHBoxLayout()
        self.lat_label = QLabel("Latitude:")
        lat_layout.addWidget(self.lat_label)
        self.lat_line_edit = QLineEdit()
        self.lat_line_edit.setText(str(self.latitude))
        lat_layout.addWidget(self.lat_line_edit)
        layout.addLayout(lat_layout)

        # Create layout for longitude
        long_layout = QHBoxLayout()
        self.long_label = QLabel("Longitude:")
        long_layout.addWidget(self.long_label)
        self.long_line_edit = QLineEdit()
        self.long_line_edit.setText(str(self.longitude))
        long_layout.addWidget(self.long_line_edit)
        layout.addLayout(long_layout)

        # Create buttons layout
        buttons_layout = QHBoxLayout()

        # Create Revert button
        self.revert_button = QPushButton("Revert")
        self.revert_button.clicked.connect(self.revert_settings)
        buttons_layout.addWidget(self.revert_button)

        # Create Start button
        self.start_button = QPushButton("Start")
        # Connect Start button to its functionality here...
        buttons_layout.addWidget(self.start_button)

        layout.addLayout(buttons_layout)

        # Add layout to widget
        layout.addStretch(1)  # Add stretch to push all elements to the top
        layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        self.setLayout(layout)

    def slider_changed(self, value):
        self.meters = round(value / 100) * 100
        self.slider_position_label.setText(f"Current radius: {self.meters} meters")

    def revert_settings(self):
        try:
            file_descriptor = os.open("./backend/general_settings.py", os.O_RDONLY)
            file_contents = os.read(file_descriptor, os.path.getsize("./backend/general_settings.py")).decode()
            os.close(file_descriptor)

            for line in file_contents.split("\n"):
                if line.startswith("meters"):
                    self.slider.setValue(int(line.split("=")[1].strip()))
                elif line.startswith("latitude"):
                    self.lat_line_edit.setText(line.split("=")[1].strip())
                elif line.startswith("longitude"):
                    self.long_line_edit.setText(line.split("=")[1].strip())
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "No settings file found.")


class TelegramSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Settings")
        self.setGeometry(200, 200, 400, 200)

        # Initialize variables
        self.phone_number = ""
        self.telegram_name = ""
        self.telegram_api_id = ""
        self.telegram_api_hash = ""

        layout = QVBoxLayout()

        about_text = """<h2>Get API values</h2><a href="https://my.telegram.org/auth" target=_blank>https://my.telegram.org/auth</a><br>"""
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setOpenExternalLinks(True)
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        label.setText(about_text)
        layout.addWidget(label)
        self.setLayout(layout)

        self.phone_number_label = QLabel("Phone Number:")
        layout.addWidget(self.phone_number_label)
        self.phone_number_text = QLineEdit()
        layout.addWidget(self.phone_number_text)

        self.telegram_name_label = QLabel("Telegram Name:")
        layout.addWidget(self.telegram_name_label)
        self.telegram_name_text = QLineEdit()
        layout.addWidget(self.telegram_name_text)

        self.telegram_api_id_label = QLabel("Telegram API ID:")
        layout.addWidget(self.telegram_api_id_label)
        self.telegram_api_id_text = QLineEdit()
        layout.addWidget(self.telegram_api_id_text)

        self.telegram_api_hash_label = QLabel("Telegram API Hash:")
        layout.addWidget(self.telegram_api_hash_label)
        self.telegram_api_hash_text = QLineEdit()
        layout.addWidget(self.telegram_api_hash_text)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.save_settings)
        layout.addWidget(self.submit_button)

        self.revert_button = QPushButton("Revert")
        self.revert_button.clicked.connect(self.revert_settings)
        layout.addWidget(self.revert_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Load settings from file if it exists
        self.load_settings()

    def load_settings(self):
        try:
            file_descriptor = os.open("./backend/telegram_creds.py", os.O_RDONLY)
            file_contents = os.read(file_descriptor, os.path.getsize("./backend/telegram_creds.py")).decode()
            os.close(file_descriptor)

            for line in file_contents.split("\n"):
                if line.startswith("phone_number"):
                    self.phone_number = line.split("=")[1].strip().strip("'")
                elif line.startswith("telegram_name"):
                    self.telegram_name = line.split("=")[1].strip().strip("'")
                elif line.startswith("telegram_api_id"):
                    self.telegram_api_id = line.split("=")[1].strip().strip("'")
                elif line.startswith("telegram_api_hash"):
                    self.telegram_api_hash = line.split("=")[1].strip().strip("'")

            self.phone_number_text.setText(self.phone_number)
            self.telegram_name_text.setText(self.telegram_name)
            self.telegram_api_id_text.setText(self.telegram_api_id)
            self.telegram_api_hash_text.setText(self.telegram_api_hash)
        except FileNotFoundError:
            pass

    def save_settings(self):
        self.phone_number = self.phone_number_text.text()
        self.telegram_name = self.telegram_name_text.text()
        self.telegram_api_id = self.telegram_api_id_text.text()
        self.telegram_api_hash = self.telegram_api_hash_text.text()

        file_descriptor = os.open("./backend/telegram_creds.py", os.O_WRONLY | os.O_CREAT)
        file_contents = (
            f"phone_number = '{self.phone_number}'\n"
            f"telegram_name = '{self.telegram_name}'\n"
            f"telegram_api_id = '{self.telegram_api_id}'\n"
            f"telegram_api_hash = '{self.telegram_api_hash}'\n"
        )
        os.write(file_descriptor, file_contents.encode())
        os.close(file_descriptor)

        self.close()

    def revert_settings(self):
        try:
            file_descriptor = os.open("./backend/telegram_creds.py", os.O_RDONLY)
            file_contents = os.read(file_descriptor, os.path.getsize("./backend/telegram_creds.py")).decode()
            os.close(file_descriptor)

            for line in file_contents.split("\n"):
                if line.startswith("phone_number"):
                    self.phone_number_text.setText(line.split("=")[1].strip().strip("'"))
                elif line.startswith("telegram_name"):
                    self.telegram_name_text.setText(line.split("=")[1].strip().strip("'"))
                elif line.startswith("telegram_api_id"):
                    self.telegram_api_id_text.setText(line.split("=")[1].strip().strip("'"))
                elif line.startswith("telegram_api_hash"):
                    self.telegram_api_hash_text.setText(line.split("=")[1].strip().strip("'"))
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "No settings file found.")


class GeneralSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("General Settings")
        self.setGeometry(200, 200, 400, 200)

        # Initialize variables
        self.meters = ""
        self.latitude = ""
        self.longitude = ""
        self.timesleep = ""

        layout = QVBoxLayout()

        self.meters_label = QLabel("Search radius (meters):")
        layout.addWidget(self.meters_label)
        self.meters_text = QLineEdit(str(self.meters))
        layout.addWidget(self.meters_text)

        self.latitude_label = QLabel("Starting Latitude:")
        layout.addWidget(self.latitude_label)
        self.latitude_text = QLineEdit(str(self.latitude))
        layout.addWidget(self.latitude_text)

        self.longitude_label = QLabel("Starting Longitude:")
        layout.addWidget(self.longitude_label)
        self.longitude_text = QLineEdit(str(self.longitude))
        layout.addWidget(self.longitude_text)

        self.timesleep_label = QLabel("Delay between search steps (sec):")
        layout.addWidget(self.timesleep_label)
        self.timesleep_text = QLineEdit(str(self.timesleep))
        layout.addWidget(self.timesleep_text)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.save_settings)
        layout.addWidget(self.submit_button)

        self.revert_button = QPushButton("Revert")
        self.revert_button.clicked.connect(self.revert_settings)
        layout.addWidget(self.revert_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Load settings from file if it exists
        self.load_settings()

    def load_settings(self):
        try:
            file_descriptor = os.open("./backend/general_settings.py", os.O_RDONLY)
            file_contents = os.read(file_descriptor, os.path.getsize("./backend/general_settings.py")).decode()
            os.close(file_descriptor)

            for line in file_contents.split("\n"):
                if line.startswith("meters"):
                    self.meters_text.setText(line.split("=")[1].strip())
                elif line.startswith("latitude"):
                    self.latitude_text.setText(line.split("=")[1].strip())
                elif line.startswith("longitude"):
                    self.longitude_text.setText(line.split("=")[1].strip())
                elif line.startswith("timesleep"):
                    self.timesleep_text.setText(line.split("=")[1].strip())
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "No settings file found.")

    def save_settings(self):
        try:
            self.meters = int(self.meters_text.text())
            self.latitude = float(self.latitude_text.text())
            self.longitude = float(self.longitude_text.text())
            self.timesleep = int(self.timesleep_text.text())

            file_descriptor = os.open("./backend/general_settings.py", os.O_WRONLY | os.O_CREAT)
            file_contents = (
                f"meters = {self.meters}\n"
                f"latitude = {self.latitude}\n"
                f"longitude = {self.longitude}\n"
                f"timesleep = {self.timesleep}\n"
            )
            os.write(file_descriptor, file_contents.encode())
            os.close(file_descriptor)

            self.close()
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid input for settings.")

    def revert_settings(self):
        try:
            file_descriptor = os.open("./backend/general_settings.py", os.O_RDONLY)
            file_contents = os.read(file_descriptor, os.path.getsize("./backend/general_settings.py")).decode()
            os.close(file_descriptor)

            for line in file_contents.split("\n"):
                if line.startswith("meters"):
                    self.meters_text.setText(line.split("=")[1].strip())
                elif line.startswith("latitude"):
                    self.latitude_text.setText(line.split("=")[1].strip())
                elif line.startswith("longitude"):
                    self.longitude_text.setText(line.split("=")[1].strip())
                elif line.startswith("timesleep"):
                    self.timesleep_text.setText(line.split("=")[1].strip())
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "No settings file found.")


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()
        about_text = """<h2>Close-Circuit Telegram Vision</h2>
Version 1.0<p><br>
Creator: Ivan Glinkin<br>
LinkedIn: <a href="https://www.linkedin.com/in/ivanglinkin/" target=_blank>https://www.linkedin.com/in/ivanglinkin/</a><br>
Twitter: <a href="https://twitter.com/glinkinivan" target=_blank>https://twitter.com/glinkinivan</a>"""
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setOpenExternalLinks(True)
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setWordWrap(True)
        label.setText(about_text)
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(argv)
    app.setAttribute(Qt.AA_DontUseNativeMenuBar)  # Disable native menu bar for macOS
    window = MainWindow()
    window.show()
    exit(app.exec_())
