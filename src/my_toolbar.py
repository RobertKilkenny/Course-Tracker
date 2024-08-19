from typing import Callable
from PySide2.QtWidgets import QPushButton, QToolBar
from Windows.settings_window import SettingsWindow
from utils.app_manager import AppManager


class MyToolBar(QToolBar):
    "Custom Toolbar to handle interactions with application."""
    def __init__(self, app_manager: AppManager):
        super().__init__()
        self.app_manager = app_manager

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


    def open_settings(self):
        """Handle opening an additional settings window."""
        self.app_manager.emit_open_window_request(SettingsWindow())


    def open_add_class(self):
        """Handle changing to the subwindow to the add class widget."""
        self.app_manager.emit_subwindow_change(0)


    def open_edit_class(self):
        """Handle changing to the subwindow to the edit class widget."""
        self.app_manager.emit_subwindow_change(1)
