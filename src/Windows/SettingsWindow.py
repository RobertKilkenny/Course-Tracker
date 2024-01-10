from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt
import json

class SettingsWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Application Settings")
    self.setMinimumSize(QSize(300, 600))
    self.settings = [{"Menu Size": "960x540"}]
    layout = QVBoxLayout()
    button = QPushButton("Save")
    button.clicked.connect(self.save_settings)
    layout.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
    layout.addWidget(button)
    self.setLayout(layout)
  
  def save_settings(self):
    print("saving settings")
    with open("app-data/settings.json", "w") as json_file:
      json.dump(self.settings, json_file, indent=4)