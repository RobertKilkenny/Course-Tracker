"""Object to handle communication between subwindow, extra windows, and the main window.
Holds events and listeners so that different events can be handled without explicit connections."""
from typing import Callable, List
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget
from utils.course_object import CourseObject

class AppManager(QObject):
    """Class to faciliate communication between app widgets."""
    __create_csv = Signal(object)
    __subwindow_change = Signal(int)
    __open_window_request = Signal(QWidget)
    __close_application = Signal()
    __request_csv = Signal()
    __generated_csv = Signal()
    __can_change_subwindow = True
    

    @property
    def can_change_subwindow(self) -> bool:
        """Property to determine if subwindow changes should be allowed."""
        return self.__can_change_subwindow


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


    def connect_request_csv(self, function: Callable):
        """Connect functions that should be informed when a proper CSV has been
        requested to be made or found."""
        self.__request_csv.connect(function)


    def emit_request_csv(self):
        """Notify different functions that a proper CSV has been requested and
        locking routing until the CSV has been produced."""
        self.__request_csv.emit()
        self.__can_change_subwindow = False


    def connect_generated_csv(self, function: Callable):
        """Connect functions that should be informed when a proper CSV has been
        created.

        Args:
            function (Callable): The function that should be called on emit
        """
        self.__generated_csv.connect(function)


    def emit_generated_csv(self):
        """Notify different functions that a proper CSV has been made and
        handle closing the request page created."""
        self.__can_change_subwindow = True
        self.emit_subwindow_change(0)


    def connect_create_csv(self, function: Callable):
        """Connect functions that should be informed when a proper CSV needs to be
        created.

        Args:
            function (Callable): _description_
        """
        self.__create_csv.connect(function)


    def emit_create_csv(self, courses: List[CourseObject]):
        """Notify Course List to create the CSV from a ClassElement list.
        
        Args:
            courses (List[ClassElement]): A list of all classes wanted to be created.
        """
        self.__create_csv.emit(courses)
