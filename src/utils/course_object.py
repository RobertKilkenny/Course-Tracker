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
    def __init__(self, code: str, name: str, credit_count: int, grade: str, semester: str,
                 tags: List[str] = None):
        self.__code = code
        self.__name = name
        self.__credits = credit_count
        self.__grade = grade
        self.__semester_taken = semester
        self.__tags = [] if tags is None else tags


    def __str__(self) -> str:
        return self.create_stats()


    def __repr__(self) -> str:
        return self.__str__()


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CourseObject):
            return False
        return (self.__code == other.code
                and self.__name == other.name
                and self.__credits == other.credits
                and sorted(self.__tags) == sorted(other.tags)
                and self.__semester_taken == self.semester_taken)
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
        print(self.create_stats())


    def create_stats(self) -> str:
        """Create a string to be printed out for print() and such

        Returns:
            str: The string to be printed directly
        """
        print_this = "\nPrinting stats for class!\n--------------------"
        print_this += print_this + f"\nClass Code: {self.__code}"
        print_this += print_this + f"\nClass Name: {self.__name}"
        print_this += print_this + f"\nCredits: {self.__credits}"
        print_this += print_this + f"\nGrade: {self.__grade}"
        print_this += print_this + f"\nSemester: {self.__semester_taken}"
        if len(self.__tags) > 0:
            print_this += print_this + f"\nTags: {self.return_tags_as_string()}"
        return print_this


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


class Semester():
    """A object to store what a semester is which is defined as section (a str) then a year (a int).
    For example to get 'Fall 2024,' it is section='Fall' year=2024.
    
    Args:
    - section(str): The reoccuring time period for college (like Fall, Spring, etc.)
    - year(int): The year it took place in
    """
    __section: str
    __year: int

    @property
    def section(self) -> str:
        """Returns the reoccuring time period for college (like Fall, Spring, etc.)"""
        return self.__section


    @property
    def year(self) -> str:
        """Returns what year it took place in."""
        return self.__year


    def __init__(self, section: str, year: int):
        """_summary_

        Args:
            section (str): Reoccuring time period for college (like Fall, Spring, etc.)
            year (int): The year it took place in.
        """
        self.__section = section
        self.__year = year

    def __str__(self) -> str:
        return self.print_details()


    def __repr__(self) -> str:
        return self.__str__()


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Semester):
            return False
        return (self.__section == other.section
                and self.__year == other.section)


    def print_details(self):
        """Print the semester in the format '[section] [year]'"""
        return self.__section + str(self.__year)
