from typing import Callable
from PySide2.QtWidgets import QPushButton, QToolBar
from Windows.SettingsWindow import SettingsWindow


class MyToolBar(QToolBar):
    "Custom Toolbar to handle interactions with application."""
    def __init__(self, show_new_window: Callable):
        super().__init__()
        self.show_new_window = show_new_window
        self.change_subwindow_stack = None

        settings = QPushButton("Settings")
        settings.setCheckable(True)
        settings.clicked.connect(self.open_settings)
        self.addWidget(settings)
        add_class = QPushButton("Add Class")
        add_class.setCheckable(True)
        add_class.clicked.connect(self.open_add_class)
        self.addWidget(add_class)
        edit_class = QPushButton("Edit Class")
        edit_class.setCheckable(True)
        edit_class.clicked.connect(self.open_edit_class)
        self.addWidget(edit_class)


    def give_stack_shift_func(self, func: Callable[[int], None]):
        """Hand off function to allow for the subwindow to be changed."""
        self.change_subwindow_stack = func


    def open_settings(self):
        """Handle opening an additional settings window."""
        self.show_new_window(new_window=SettingsWindow())


    def open_add_class(self):
        """Handle changing to the subwindow to the add class widget."""
        if self.change_subwindow_stack is None:
            return
        self.change_subwindow_stack(0)


    def open_edit_class(self):
        """Handle changing to the subwindow to the edit class widget."""
        if self.change_subwindow_stack is None:
            return
        self.change_subwindow_stack(1)
