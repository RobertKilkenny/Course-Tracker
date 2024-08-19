"""Object to handle communication between subwindow, extra windows, and the main window.
Holds events and listeners so that different events can be handled without explicit connections."""
from typing import Callable
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget

class AppManager(QObject):
    __subwindow_change = Signal(int)
    __open_window_request = Signal(QWidget)
    __close_application = Signal()


    def connect_subwindow_change(self, function: Callable):
        """Connect Function to the subwindow_change Signal

        Args:
            function (Callable): The function that should be signaled on emit
        """
        self.__subwindow_change.connect(function)


    def emit_subwindow_change(self, index: int):
        """Notify Main Menu that the subwindow should be changed
        Index Legend
        * -1 = Gen CSV Window
        *  0 = Add Class Window
        *  1 = Edit Class Window
        Any other value gives the test window
        Args:
            index (int): Index of the window to be changed
        """
        self.__subwindow_change.emit(index)


    def connect_open_window_request(self, function: Callable):
        """Connect Function to the open_window_request Signal

        Args:
            function (Callable): The function that should be signaled on emit
        """
        self.__open_window_request.connect(function)


    def emit_open_window_request(self, window: QWidget):
        """Notify Main Menu that there is a new window that wants
        to be opened.
        Args:
            window (QWidget): The Widget holding the master layout for the 
            window requesting to be displayed.
        """
        self.__open_window_request.emit(window)


    def connect_close_app_request(self, function: Callable):
        """Connect Function to the close_application Signal

        Args:
            function (Callable): The function that should be signaled on emit
        """
        self.__close_application.connect(function)


    def emit_close_app_request(self):
        """Notify Main Window to kill app."""
        self.__close_application.emit()
