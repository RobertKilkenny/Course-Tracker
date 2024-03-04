from PySide2.QtWidgets import QPushButton, QToolBar
from Windows.SettingsWindow import SettingsWindow
from typing import Callable

class MyToolBar(QToolBar):
  def __init__(self, show_new_window: Callable):
    super().__init__()
    self.show_new_window = show_new_window

    settings = QPushButton("Settings")
    settings.setCheckable(True)
    settings.clicked.connect(self.open_settings)
    addClass = QPushButton("Add Class")
    addClass.setCheckable(True)
    addClass.clicked.connect(self.open_add_class)
    self.change_subwindow_stack = None
    self.addWidget(settings)
    self.addWidget(addClass)

  def give_stack_shift_func(self, func: Callable[[int], None]):
    self.change_subwindow_stack = func

  def open_settings(self):
    self.show_new_window(new_window=SettingsWindow())
  
  def open_add_class(self):
    if self.change_subwindow_stack is None:
      return
    self.change_subwindow_stack(0)