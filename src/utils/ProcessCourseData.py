import os
from typing import List
import pandas as pd
from utils.Class import Class


class CourseList():
    """Class Object to hold the data of a class for the purposes of this application."""
    def __init__(self, course_csv_location: str):
        if os.path.exists(course_csv_location):
            temp = pd.read_csv(course_csv_location)
            required_columns = ["Course Code", "Course Name", "Credits", "Tags"]
            if all(column in temp.columns for column in required_columns):
                self.df = temp
                self.df.set_index(['Course Code'], inplace=True)
            else:
                print("Invalid CSV was given")
        else:
            print("CSV did not exist")
            path_pieces = course_csv_location.split("/")
            print(path_pieces)
            path = path_pieces[0]
            for piece in path_pieces[1:-1]:
                path += "/" + piece
                if not os.path.exists(path):
                    print("path:", path, "did not exist")
                    os.makedirs(path)
            self.df = pd.DataFrame({'Course Name':"Example Class", 'Credits':-1, 'Tags': "example, do not use"}, index=["AAA0000"])

        self.df.rename_axis("Course Code")
        self.df.to_csv(course_csv_location, index_label="Course Code")
        print("The result of the CSV transfer is:\n", self.df)

    def does_class_exist(self, course_code: str) -> bool:
        """Checks Dataframe to see if the class exists."""
        return course_code in self.df.index

    def return_class(self, course_code: str) -> Class:
        """Looks for the class and returns it as a Class object if it exists and `None` if not."""
        if not self.does_class_exist(course_code=course_code):
            return None
        information = self.df.loc[course_code]
        return Class(course_code, information["Course Name"], int(information["Credits"]), 
                     from_string_to_list(information["Tags"]))

    def search_by_tag(self, tag: str):
        """Iterate through the dataframe and find all classes with the tag given."""


def from_string_to_list(tags_string: str) -> List[str]:
    """Convert a string to list of tags."""
    return tags_string.split(",")
