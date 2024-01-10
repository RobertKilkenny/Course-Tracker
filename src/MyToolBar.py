from PySide2.QtWidgets import QWidget, QPushButton, QToolBar
from Windows.SettingsWindow import SettingsWindow

class MyToolBar(QToolBar):
  def __init__(self, show_new_window):
    super().__init__()
    self.show_new_window = show_new_window
    settings_action = QPushButton("Settings")
    settings_action.setCheckable(True)
    settings_action.clicked.connect(self.open_settings)
    self.addWidget(settings_action)

  def open_settings(self):
    self.show_new_window(new_window=SettingsWindow())