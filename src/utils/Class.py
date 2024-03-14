"""Module containing the class to hold data for a specific course."""
from typing import List


class Class:
    """Class to hold the data of a class for the purposes of this application."""
    def __init__(self, code: str, name: str, credit_count: int, tags: List[str] = None):
        self.__code = code
        self.__name = name
        self.__credits = credit_count
        self.__tags = [] if tags is None else tags

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
    def tags(self) -> List[str]:
        """Property for list of tags."""
        return self.__tags

    @tags.setter
    def tags(self, tags: List[str]) -> None:
        """Setter for tags."""
        for tag in tags:
            if tag not in self.__tags:
                self.__tags.append(tag)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Class):
            return False
        return (self.__code == other.code
                and self.__name == other.name
                and self.__credits == other.credits
                and sorted(self.__tags) == sorted(other.tags))

    def check_data_match(self, code: str, name: str, credit_value: int, tags: List[str]) -> bool:
        """Function to check if the given data matches the data within this class."""
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
        """Convert the list of tags to a string."""
        return ';'.join(self.__tags)
