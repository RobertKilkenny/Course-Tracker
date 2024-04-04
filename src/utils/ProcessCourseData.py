import os
from typing import List
import pandas as pd
from utils.Class import Class

EXPECTED_TYPOS = {"Course Code": ["course code", "coursecode"],
                  "Course Name": ["course name", "coursename"],
                  "Credits": ["credits", "value", "credit hours", "credithours"]}

class CourseList():
    csv_file_path: str
    """Class Object to hold the data of a class for the purposes of this application."""
    def __init__(self, course_csv_location: str):
        self.csv_file_path = course_csv_location
        match self.create_dataframe_from_csv():
            case -1:
                self.gen_default_dataframe()
            case 1:
                # Testing for issues with naming conventions
                temp = pd.read_csv(course_csv_location)
                for [category, typos] in EXPECTED_TYPOS:
                    title = [col for col in temp.columns if col.lower() in typos]
                    if title is not None:
                        temp[title].rename(category)
                    else:
                        self.__send_error()
                        break

        print("\nThe result of the CSV transfer is\n------------------------------------------\n"
              , self.df)
        self.print_csv()


    def create_dataframe_from_csv(self):
        """Tests if a csv can be used to generate a dataframe.

        Args:
            course_csv_location (str): File path to the CSV to create dataframe from
        
        Returns:
            -1: CSV does not exist
             0: Dataframe was created
             1: CSV is not formated correctly
        """
        if os.path.exists(self.csv_file_path):
            print("CSV is generating the dataframe")
            temp = pd.read_csv(self.csv_file_path)

            required_columns = ["Course Code", "Course Name", "Credits"]
            if all(column in temp.columns for column in required_columns):
                self.df = temp
                self.df.set_index(['Course Code'], inplace=True)
                if "Tags" in temp.columns:
                    self.df["Tags"] = temp["Tags"]
                    self.df["Tags"] = self.df["Tags"].apply(from_string_to_list)
                else:
                    self.df["Tags"] = []
                return 0
            else:
                return 1
        else:
            return -1


    def gen_default_dataframe(self):
        """Sets the Course List's dataframe to default values."""
        path_pieces = self.csv_file_path.split("/")
        path = path_pieces[0]
        for piece in path_pieces[1:-1]:
            path += "/" + piece
            if not os.path.exists(path):
                print("path:", path, "did not exist")
                os.makedirs(path)
        self.df = pd.DataFrame({'Course Name':"Example Class", 'Credits':-1, 
                                'Tags': ["example", "do not use"]}, index=["AAA0000"])


    def add_class(self, code: str, name: str, value: int, tag_array:List[str] = None, tags_as_string:str = "") -> bool:
        """Adds class requiring a class code, name, and number of credits.
            code(str): String that acts as the index for the classes using the course codes.
            name(str): String of the title/ class name for the class in question.
            value(int): The number of credits that the class is worth. 
            tag_array(List[str], optional): Allows for a list of strings, each being one tag.
            tags_as_string(str, optional): Allows for tags to be implemented as a string, 
            as that is how they are saved in the CSV using "|" as a delimiter.
        """
        self.df.loc[code]= ({"Course Name": name, "Credits":value})
        if tag_array is not None:
                self.df["Tags"] = tag_array
        elif tags_as_string != "":
                self.df["Tags"] = from_string_to_list(tags_as_string)


    def does_class_exist(self, course_code: str) -> bool:
        """Checks Dataframe to see if the class exists."""
        return course_code in self.df.index


    def return_class(self, course_code: str) -> Class:
        """Looks for the class and returns it as a Class object if it exists and `None` if not."""
        if not self.does_class_exist(course_code=course_code):
            return None
        information = self.df.loc[course_code]
        return Class(course_code, information["Course Name"], int(information["Credits"]),
                     information["Tags"])


    def search_by_tag(self, tag: str):
        """Iterate through the dataframe and find all classes with the tag given."""


    def print_csv(self):
        """Turns Dataframe into a CSV that is consistent to save for the program."""
        print("\nPrinting dataframe!",
              "\n------------------------------------------")
        temp = self.df.copy()
        temp["Tags"] = temp["Tags"].apply(from_list_to_string)
        temp.rename_axis("Course Code")
        print(temp)
        temp.to_csv(self.csv_file_path, index_label="Course Code")


    def __send_error(self):
        raise ValueError("Invalid CSV was given for program.")


def from_string_to_list(tags_string: str) -> List[str]:
    """Convert a string to a list of tags."""
    if not isinstance(tags_string, str):
        return None
    return tags_string.split("|")

def from_list_to_string(tag_list: List[str]) -> str:
    """Convert a list of tags to a string."""
    if not isinstance(tag_list, list) or not all(isinstance(tag, str) for tag in tag_list):
        return None
    return "|".join(tag_list)
