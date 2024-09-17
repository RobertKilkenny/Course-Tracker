"""Holds classes and functions that are used to process course data"""
import os
import math
from typing import List
import pandas as pd
from utils.course_object import CourseObject


EXPECTED_TYPOS = {"Course Code": ["course code", "coursecode"],
                  "Course Name": ["course name", "coursename"],
                  "Credits": ["credits", "value", "credit hours", "credithours"]}

class CourseList():
    """Class Object to hold the data of a class for the purposes of this application."""
    csv_file_path: str

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df):
        self._df = df

    def __init__(self, course_csv_location: str = None):
        """_summary_

        Args:
            course_csv_location (str): Where the csv for the course data is located
        """
        self.csv_file_path = course_csv_location
        if course_csv_location is None:
            self._df = pd.DataFrame()
            return

        self.result = self.create_dataframe_from_csv()
        match self.result:
            # Failed due to the CSV not existing!
            case -1:
                self.__send_error("CSV does not exist.")
            case 1:
                temp = pd.read_csv(course_csv_location)
                for category, typos in EXPECTED_TYPOS.items():
                    title = next((col for col in temp.columns if col.lower() in typos), None)
                    if title:
                        temp.rename(columns={title: category}, inplace=True)
                    else:
                        self.__send_error("Invalid CSV was given for program.")
                        break
            # There was no problems making the Dataframe
            case 0:
                pass

        print("\nThe result of the CSV transfer is\n------------------------------------------\n",
              self.df)


    def create_dataframe_from_csv(self):
        """Read a csv file to make the dataframe for the app.

        Returns:
            int: Returns an enum to tell
        """
        if os.path.exists(self.csv_file_path):
            print("CSV is generating the dataframe")
            temp = pd.read_csv(self.csv_file_path)

            required_columns = ["Course Code", "Course Name", "Credits"]
            if all(column in temp.columns for column in required_columns):
                self.df = temp
                self.df.set_index(['Course Code'], inplace=True)
                if "Tags" in temp.columns:
                    print(temp)
                    self.df["Tags"] = temp["Tags"].apply(from_string_to_list)
                else:
                    self.df["Tags"] = []
                return 0
            else:
                return 1
        else:
            return -1


    def add_class(self, code: str, name: str, value: int, tag_array:List[str] = None,
                tags_as_string:str = "") -> bool:
        """Adds a new class to the dataframe for the course list.

        Args:
            code (str): The course code for the class to be added. Default format is 'AAA0000'
            name (str): The name for the course.
            value (int): The number of credits for the class.
            tag_array (List[str], optional): A array holding different relevant tags.
            Defaults to None.
            tags_as_string (str, optional): a string of all tags delimited by a '|'. Defaults to "".

        Returns:
            bool: Tells if the class was made successfully.
        """
        self.df.loc[code] = {"Course Name": name, "Credits": value}
        result = (
            tag_array if tag_array
            else from_string_to_list(tags_as_string) if tags_as_string
            else None
        )
        self.df.at[code, "Tags"] = result


    def does_class_exist(self, course_code: str) -> bool:
        """Checks if the class already exists using the course code 
        which is the index for the dataframe.

        Args:
            course_code (str): Code to search with within the dataframe.

        Returns:
            bool: Returns if the course code is found in the dataframe.
        """
        return course_code in self.df.index


    def return_class(self, course_code: str) -> CourseObject:
        """Finds a class by a course code in the dataframe. 

        Args:
            course_code (str): The code for the class if it exists.

        Returns:
            Class: Object containing the class if it exists or returns None if
            it does not exist.
        """
        if not self.does_class_exist(course_code=course_code):
            return None
        information = self.df.loc[course_code]
        return CourseObject(course_code, information["Course Name"], int(information["Credits"]),
                     information["Tags"])


    def search_by_tag(self, tag: str):
        """_summary_

        Args:
            tag (str): _description_
        """


    def print_csv(self):
        """_summary_"""
        print("\nPrinting dataframe!",
              "\n------------------------------------------")
        temp = self.df.copy()
        temp["Tags"] = temp["Tags"].apply(from_list_to_string)
        temp.rename_axis("Course Code", inplace=True)
        print(temp)
        temp.to_csv(self.csv_file_path, index_label="Course Code")


    def __send_error(self, msg:str):
        """_summary_

        Raises:
            ValueError: Error to raise
        """
        raise ValueError(msg)


    def make_csv_from_list(self, course_list: List[CourseObject]):
        """Using the pathfile supplied, create a CSV for the app to use.

        Args:
            course_list (List[CourseObject]): List of all classes
            that the user wants to be added to the new csv
        """
        data = [{
        'name': course.name,
        'credits': course.credits,
        'tags': course.return_tags_as_string()
        } for course in course_list]

        self._df = pd.DataFrame(data, index=[course.code for course in course_list])
        self._df.index.name = 'code'
        self._df.to_csv(self.csv_file_path)


def from_string_to_list(tags_string: str) -> List[str]:
    """Create a List from a string that delimited by a '|'.

    Args:
        tags_string (str): The string that holds objects.

    Returns:
        List[str]: The list holding each element from the string.
    """
    if tags_string is None or (isinstance(tags_string, float) and math.isnan(tags_string)):
        return []
    return tags_string.split("|")


def from_list_to_string(tag_list: List[str]) -> str:
    """Create a string that delimits each element in the list with a '|'.

    Args:
        tag_list (List[str]): The List to transform.

    Returns:
        str: The list transformed into a string.
    """
    if not all(isinstance(tag, str) for tag in tag_list):
        for element in tag_list:
            if not isinstance(element, str):
                tag_list.remove(element)
    return "|".join(tag_list)
