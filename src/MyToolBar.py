from PySide2.QtWidgets import QPushButton, QToolBar
from PySide2.QtCore import Signal
from Windows.SettingsWindow import SettingsWindow
from Functions.AddClass import AddClass

class MyToolBar(QToolBar):
  signal = Signal()
  
  def __init__(self, show_new_window, course_list):
    super().__init__()
    self.show_new_window = show_new_window
    self.course_list = course_list
    self.signal.connect(self.push_signal)
    settings = QPushButton("Settings")
    settings.setCheckable(True)
    settings.clicked.connect(self.open_settings)

    addClass = QPushButton("Add Class")
    addClass.setCheckable(True)
    addClass.clicked.connect(self.add_class)

    self.addWidget(settings)
    self.addWidget(addClass)

  def open_settings(self):
    self.show_new_window(new_window=SettingsWindow())
  
  def add_class(self):
    self.frame_layout = AddClass()
    self.signal.emit()
  
  def activate_function(self, reciever):
    self.function = reciever

  def push_signal(self):
    self.function()