from typing import Callable
from PySide2.QtWidgets import QPushButton, QToolBar
from Windows.settings_window import SettingsWindow
from utils.app_manager import AppManager


class MyToolBar(QToolBar):
    "Custom Toolbar to handle interactions with application."""
    def __init__(self, app_manager: AppManager):
        super().__init__()
        self.app_manager = app_manager
        self.options = []

        #Create the buttons to route to different options
        settings = QPushButton("Settings")
        settings.setCheckable(True)
        settings.clicked.connect(self.open_settings)
        self.options.append(settings)
        add_class = QPushButton("Add Class")
        add_class.setCheckable(True)
        add_class.clicked.connect(self.open_add_class)
        self.options.append(add_class)
        edit_class = QPushButton("Edit Class")
        edit_class.setCheckable(True)
        edit_class.clicked.connect(self.open_edit_class)
        self.options.append(edit_class)
        view_class = QPushButton("View Class")
        view_class.setCheckable(True)
        view_class.clicked.connect(self.open_view_class)
        self.options.append(view_class)

        #Link them to the parent to be displayed
        for option in self.options:
            self.addWidget(option)

        #Connect functions to the proper events from App manager
        self.app_manager.connect_request_csv(self.lock_options)
        self.app_manager.connect_generated_csv(self.unlock_options)


    def lock_options(self):
        """Lock all routing from the toolbar"""
        for option in self.options:
            option.setCheckable(False)


    def unlock_options(self):
        """Reallow routing (For forced events)"""
        for option in self.options:
            option.setCheckable(True)


    def open_settings(self):
        """Handle opening an additional settings window."""
        self.app_manager.emit_open_window_request(SettingsWindow())


    def open_add_class(self):
        """Handle changing to the subwindow to the add class widget."""
        self.app_manager.emit_subwindow_change(0)


    def open_edit_class(self):
        """Handle changing to the subwindow to the edit class widget."""
        self.app_manager.emit_subwindow_change(1)


    def open_view_class(self):
        """Handle changing to the subwindow to the view class widget."""
        self.app_manager.emit_subwindow_change(2)
