"""Object to handle communication between subwindow, extra windows, and the main window.
Holds events and listeners so that different events can be handled without explicit connections."""
import os
import pandas as pd
from typing import Callable, List
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget
from utils.course_object import CourseObject
from utils.process_course_data import CourseList

class AppManager(QObject):
    """Class to faciliate communication between app widgets."""
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


    def __init__(self, course_list: CourseList, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.course_list = course_list


#region Handle connecting and emitting Signals
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
#endregion


    def create_new_csv(self, path:str, classes: List[CourseObject]) -> bool:
        """Create a new CSV using list of classes. Args are not checked in this function
        to make sure it will run properly!!! 

        Args:
            path (str): Path to save to
            classes (List[CourseObject]): List of class objects to add to csv

        Returns:
            bool: Returns if creation was successful
        """
        if self.course_list.csv_location != path:
            self.course_list.csv_location = path
        self.course_list.make_csv_from_list(classes)
        return os.path.exists(self.course_list.csv_location)


    def save_changes(self):
        """Save changes to class CSV"""
        self.course_list.save_to_csv()


#region CourseList Access points
    def does_class_exist(self, code: str) -> bool:
        """Checks if the class already exists using the course code 
        which is the index for the dataframe.

        Args:
            course_code (str): Code to search with within the dataframe.

        Returns:
            bool: Returns if the course code is found in the dataframe.
        """
        return self.course_list.does_class_exist(code)


    def get_class_details(self, code: str) -> CourseList:
        """Get the class object given the code

        Args:
            code (str): Index to find the object from DF

        Returns:
            CourseList: The course details saved
        """
        return self.course_list.return_class(code)


    def change_csv_location(self, new_location: str, is_new_file: bool = False) -> bool:
        """Change the path for the CSV and create a new DF if it is a new file

        Args:
            new_location (str): New absolute path for the file
            is_new_file (bool, optional): Boolean to identify if a new dataframe be created
                (Defaults to False).

        Returns:
            bool: Returns if the change was successful
        """
        print(f'changing location to {new_location}')
        if is_new_file:
            if os.path.exists(new_location):
                result = self.course_list.create_dataframe_from_csv(new_location)
                print(f'Result is {result}')
                return  result == 0
            else:
                return False
        else:
            self.course_list.csv_location = new_location

        return True


    def add_class(self, code: str, name: str, value: int, tag_array:List[str] = None,
                tags_as_string:str = "") -> int:
        """Adds a new class to the dataframe for the course list.

        Args:
            code (str): The course code for the class to be added. Default format is 'AAA0000'
            name (str): The name for the course.
            value (int): The number of credits for the class.
            tag_array (List[str], optional): A array holding different relevant tags.
            Defaults to None.
            tags_as_string (str, optional): a string of all tags delimited by a '|'. Defaults to "".

        Returns:
            int: Enumerable to define what happened
                * 0: Succeeded
                * 1: Failed because vital info was missing
                * 2: Failed as it already exists
        """
        if tags_as_string != "" and tag_array is None:
            tag_array = tags_as_string.split("|")
        if self.add_class_from_object(CourseObject(code,name,value,tag_array)) == 0:
            self.course_list.print_csv()
            return 0


    def add_class_from_object(self, new_class: CourseObject) -> int:
        """Attempts to add a new class to the dataframe.

        Args:
            new_class (CourseObject): The new class being requested to be added

        Returns:
            int: Enumerable to define what happened
                * 0: Succeeded
                * 1: Failed because vital info was missing
                * 2: Failed as it already exists
        """
        if self.course_list.does_class_exist(new_class.code):
            return 2
        if not new_class.make_list_of_vars_failing():
            return 1
        try:
            self.course_list.add_class_from_object()
        except Exception as e:
            print(e)
            return -1


    def edit_class(self, code: str, name: str | None, value: int | None,
                   tag_array:List[str] = None) -> int:
        """Adds a new class to the dataframe for the course list.

        Args:
            code (str): The course code for the class to be changed. Default format is 'AAA0000'
            name (str, optional): The new name for the course.
            value (int, optional): The new number of credits for the class.
            tag_array (List[str], optional): A array holding the new relevant tags.
            Defaults to None.

        Returns:
            int: Enumerable to define what happened
                * 0: Succeeded
                * 1: Failed because vital info was missing
                * 2: Failed as it does not exist
        """
        print(f"New values for {code} are\nName: {name}\nCredits: {value}\ntags: {tag_array}")
        if name is None and value is None and tag_array is None:
            return 1
        if not self.does_class_exist(code):
            return 2
        if self.course_list.edit_class(code, name, value, tag_array):
            self.course_list.print_csv()
            return 0
        else:
            return -1
#endregion
