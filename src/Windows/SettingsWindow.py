import json
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt

class SettingsWindow(QWidget):
    """Secondary window to create a json file.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Settings")
        self.setMinimumSize(QSize(300, 600))
        self.settings = {"Menu Size": "960x540", "Setting File Location": "app-data/app_settings.json"}
        layout = QVBoxLayout()
        button = QPushButton("Save")
        button.clicked.connect(self.save_settings)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        layout.addWidget(button)
        self.setLayout(layout)

    def save_settings(self):
        """Function to save the user assigned settings to a file.
        """
        print("saving settings")
        with open(self.settings["Setting File Location"], "w", encoding="utf-8") as json_file:
            json.dump(self.settings, json_file, indent=4)
