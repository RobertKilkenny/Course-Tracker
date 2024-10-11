"""Module containing the class to hold data for a specific course."""
import re
from typing import List


class CourseObject():
    """Class to hold the data of a class for the purposes of this application."""
    __code = None
    __name = None
    __credits = None
    __grade = None
    __semester_taken = None
    __tags = None
#region Class function overrides
    def __init__(self, code: str, name: str, credit_count: int, tags: List[str] = None):
        self.__code = code
        self.__name = name
        self.__credits = credit_count
        self.__tags = [] if tags is None else tags


    def __str__(self) -> str:
        val = f"({self.__name} (Code: {self.__code})\n   *Credits: {self.__credits}"
        if len(self.__tags) > 0:
            val = val + f"\n   *tags: {self.__tags}"
        val = val + ")\r"
        return val


    def __repr__(self) -> str:
        return self.__str__()


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CourseObject):
            return False
        return (self.__code == other.code
                and self.__name == other.name
                and self.__credits == other.credits
                and sorted(self.__tags) == sorted(other.tags))
#endregion


#region Properties / class variable
    @property
    def code(self) -> str:
        """Property for class code."""
        return self.__code


    @code.setter
    def code(self, code: str) -> None:
        self.__code = code


    @property
    def name(self) -> str:
        """Property for class name."""
        return self.__name


    @name.setter
    def name(self, name: str) -> None:
        self.__name = name


    @property
    def credits(self) -> int:
        """Property for credit value."""
        return self.__credits


    @credits.setter
    def credits(self, value: int) -> None:
        self.__credits = value


    @property
    def grade(self) -> str:
        """Property for letter grade."""
        return self.__grade


    @grade.setter
    def grade(self, grade: str) -> None:
        self.__grade = grade


    @property
    def semester_taken(self) -> str:
        """Property for semester taken."""
        return self.__semester_taken


    @semester_taken.setter
    def semester_taken(self, semester_taken: str) -> None:
        self.__semester_taken = semester_taken


    @property
    def tags(self) -> List[str]:
        """Property for list of tags."""
        return self.__tags


    @tags.setter
    def tags(self, tags: List[str]) -> None:
        """Setter for tags."""
        for tag in tags:
            if tag not in self.__tags:
                self.__tags.append(tag)
#endregion


#region Unique class functionality
    def check_data_match(self, code: str, name: str, credit_value: int, tags: List[str]) -> bool:
        """Function to check if the given data matches the data within this class.

        Args:
            code (str): _description_
            name (str): _description_
            credit_value (int): _description_
            tags (List[str]): _description_

        Returns:
            bool: _description_
        """
        return (self.__code == code
                and self.__name == name
                and self.__credits == credit_value
                and sorted(self.__tags) == sorted(tags))


    def add_tags(self, tags: List[str]) -> None:
        """Add a list of tags to the classes existing tags."""
        for tag in tags:
            if tag not in self.__tags:
                self.__tags.append(tag)


    def remove_tag(self, tag: str) -> None:
        """Remove a tag if it exists."""
        if tag in self.__tags:
            self.__tags.remove(tag)


    def remove_tags(self, tags: List[str]) -> None:
        """Remove a list of tags if they exist."""
        for tag in tags:
            if tag in self.__tags:
                self.__tags.remove(tag)


    def return_tags_as_string(self) -> str:
        """Convert the list of tags to a string.
        Returns:
            str: A string of all tags delimited by one comma and a space(", ")
        """
        if len(self.__tags) < 1:
            return "No tags found"

        return ', '.join(self.__tags)


    def print_stats(self) -> None:
        """A function for debugging to print all stats in the class object."""
        print("\nPrinting stats for class!\n--------------------")
        print(f"Class Code: {self.__code}")
        print(f"Class Name: {self.__name}")
        print(f"Credits: {self.__credits}")
        if len(self.__tags) > 0:
            print(f'Tags: {self.return_tags_as_string()}')


    def make_list_of_vars_failing(self) -> List[str]:
        """Makes Regex checks for the different variables

        Returns:
            List[str]: A list of all elements that failed (empty if is valid)
        """
        errors = []
        if not re.match(r'[A-Z]{3}[0-9]{4}', self.__code):
            errors.append("code")
        if not re.match(r'[^\\t\\b\\n\\r]{3}[^\\t\\b\\n\\r]*', self.__name):
            errors.append("name")
        if not re.match(r'[0-9]{1}', str(self.__credits)):
            errors.append("credits")
        for tag in self.__tags:
            if not re.match(r'[\W]+', tag):
                errors.append("tags")
                break
        return errors
#endregion
