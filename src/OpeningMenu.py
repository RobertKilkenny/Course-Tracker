from PySide2.QtWidgets import QVBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QPixmap
from Windows.SettingsWindow import SettingsWindow

class OpeningMenu(QVBoxLayout):
  def __init__(self, open_application, show_new_window):
    super().__init__()
    self.logo = QLabel()
    self.logo.setPixmap(QPixmap("assets/Temp-Icon.png"))
    self.logo.setScaledContents(True)
    self.addWidget(self.logo)

    self.show_new_window = show_new_window
    main_button = QPushButton("Main Menu")
    main_button.setCheckable(True)
    main_button.clicked.connect(open_application)
    self.addWidget(main_button)
    settings_button = QPushButton("Settings")
    settings_button.setCheckable(True)
    settings_button.clicked.connect(self.open_settings)
    self.addWidget(settings_button)

  def open_settings(self):
    self.show_new_window(SettingsWindow())