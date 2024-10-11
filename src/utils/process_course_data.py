"""Holds classes and functions that are used to process course data"""
import os
import math
from typing import List
import pandas as pd
from utils.course_object import CourseObject


EXPECTED_TYPOS = {"Course Code": ["course code", "coursecode", "Code", "code"],
                  "Course Name": ["course name", "coursename", "Name", "name"],
                  "Credits": ["credit", "credits", "value", "credit hours", "credithours"]}

class CourseList():
    """Class Object to hold the data of a class for the purposes of this application."""

#region Properties
    @property
    def csv_location(self):
        """Get absolute file location for CSV holding class data."""
        return self._csv_location

    @csv_location.setter
    def csv_location(self, csv_location: str):
        """Set absolute file location for CSV holding class data."""
        self._csv_location = csv_location

    @property
    def df(self):
        """Get a copy of the data for all classes."""
        return self._df
#endregion


    def __init__(self, course_csv_location: str = None):
        """_summary_

        Args:
            course_csv_location (str): Where the csv for the course data is located
        """
        self._df = pd.DataFrame()
        self._csv_location = course_csv_location
        if course_csv_location is None:
            return

        self.result = self.create_dataframe_from_csv(self._csv_location)
        match self.result:
            # Failed due to the CSV not existing!
            case -1:
                self.__send_error(f'CSV does not exist.\nPath is: "{self._csv_location}"')
            case 1:
                temp = pd.read_csv(self._csv_location)
                print(temp)
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
              self._df)


#region Unique functions
    def create_dataframe_from_csv(self, location: str = None):
        """Read a csv file to make the dataframe for the app.
        Args:
            location (str, optional): Passes in a new location

        Returns:
            int: Returns an enum to tell if it succeeded or how it failed.
                * -1: File path does not exist
                * 0: Succeeded
                * 1: File is not formatted correctly
        """
        if location is not None:
            test_dir = os.path.dirname(location.replace("\\", "/"))
            if os.path.exists(test_dir):
                self._csv_location = location
            else:
                print(f'Could not find folder location {test_dir}')
                return -1
        elif self._csv_location is not None and len(self._csv_location) > 0:
            test_dir = os.path.dirname(self._csv_location.replace("\\", "/"))
            if not os.path.exists(test_dir):
                print(f'Could not find folder location {test_dir}')
                return -1
        else:
            return -1

        print("CSV is generating the dataframe")
        try:
            temp = pd.read_csv(self.csv_location)
        except FileNotFoundError:
            return -1
        except pd.errors.EmptyDataError:
            return 1

        # Rename the columns to the expected names
        temp.rename(columns={
            'code': 'Course Code',
            'name': 'Course Name',
            'credits': 'Credits',
            'tags': 'Tags'
        }, inplace=True)

        # Check if required columns are present
        required_columns = ["Course Code", "Course Name", "Credits"]
        if all(column in temp.columns for column in required_columns):
            self._df = temp
            self._df.set_index(['Course Code'], inplace=True)

            # Handle NaN values in the Tags column (if present)
            if "Tags" in temp.columns:
                self._df["Tags"] = temp["Tags"].apply(lambda tags: from_string_to_list(tags) if pd.notna(tags) else [])
            else:
                self._df["Tags"] = []
            return 0
        else:
            return 1


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
        self._df.loc[code] = {"Course Name": name, "Credits": value}
        result = (
            tag_array if tag_array
            else from_string_to_list(tags_as_string) if tags_as_string
            else None
        )
        self._df.at[code, "Tags"] = result


    def edit_class(self, code: str | None, name: str | None, value: int | None,
                   tag_array: List[str] = None) -> bool:
        """Edits existing class to the dataframe for the course list. Does not check if it exists!

        Args:
            code (str): The course code for the class to be added. Default format is 'AAA0000'
            name (str): The name for the course.
            value (int): The number of credits for the class.
            tag_array (List[str], optional): A array holding different relevant tags.
            Defaults to None.

        Returns:
            bool: Tells if the class was made successfully.
        """
        try:
            self._df.loc[code, 'Course Name'] = name
            self._df.loc[code, 'Credits'] = int(value)
            if tag_array is not None:
                self._df.loc[code, "Tags"] = tag_array
        except Exception as err:
            print(err)
            return False
        return True


    def add_class_from_object(self, course: CourseObject) -> bool:
        """Add class using CourseObject instead of literal values

        Args:
            course (CourseObject): Course to add

        Returns:
            bool: Returns if it worked
        """
        return self.add_class(course.code, course.name, course.credits, course.tags)


    def does_class_exist(self, course_code: str) -> bool:
        """Checks if the class already exists using the course code 
        which is the index for the dataframe.

        Args:
            course_code (str): Code to search with within the dataframe.

        Returns:
            bool: Returns if the course code is found in the dataframe.
        """
        return course_code in self._df.index


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
        information = self._df.loc[course_code]
        return CourseObject(course_code, information["Course Name"], int(information["Credits"]),
                     information["Tags"])


    def search_by_tag(self, tag: str):
        """_summary_

        Args:
            tag (str): _description_
        """


    def print_csv(self):
        """Prints the dataframe to console and saves it to CSV."""
        print("\nPrinting dataframe!",
            "\n------------------------------------------")

        temp = self._df.copy()
        if "Tags" not in temp.columns:
            temp["Tags"] = [[] for _ in range(len(temp))]
        temp["Tags"] = temp["Tags"].apply(lambda tags: [] if pd.isna(tags) else tags)
        temp["Tags"] = temp["Tags"].apply(from_list_to_string)

        temp.rename_axis("Course Code", inplace=True)
        print(temp)
        temp.to_csv(self.csv_location, index_label="Course Code")


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
        print("Creating CSV :\n", course_list)
        if len(course_list) < 1:
            self._df = pd.DataFrame(columns=["Course Code", "Course Name", "Credits", "tags"])
        else:
            data = [{
                'Course Code': course.code,
                'Course Name': course.name,
                'Credits': course.credits,
                'tags': course.return_tags_as_string()
            } for course in course_list]

            self._df = pd.DataFrame(data)
            self._df.set_index('code', inplace=True)

        print("Finished DF being printed:\n", self._df)
        print("Printing CSV to location:", self.csv_location)
        self._df.to_csv(path_or_buf=self.csv_location)
#endregion

#region External Functions
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


def from_list_to_string(tag_list: List[str]| None) -> str:
    """Create a string that delimits each element in the list with a '|'.

    Args:
        tag_list (List[str]): The List to transform.

    Returns:
        str: The list transformed into a string.
    """
    if tag_list is None:
        return "No tags!"
    
    if not all(isinstance(tag, str) for tag in tag_list):
        for element in tag_list:
            if not isinstance(element, str):
                tag_list.remove(element)
    return "|".join(tag_list)
#endregion
