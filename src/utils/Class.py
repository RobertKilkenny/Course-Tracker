from typing import List


class Class():
    """Class created to hold and compare data for classes."""
    @property
    def code(self):
        """Property for classcode for given class."""
        return self.__code
    @code.setter
    def code(self, code: str):
        self.__code = code

    @property
    def name(self):
        """Property for class name for given class."""
        return self.__name
    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def credits(self):
        """Property for credit value for given class."""
        return self.__credits
    @credits.setter
    def credits(self, value: int):
        self.__credits = value

    @property
    def tags(self):
        """Property for list of tags associated with the class!"""
        return self.__tags
    @tags.setter
    def tags(self, tags: List[str]):
        for tag in tags:
            if tag not in self.__tags:
                self.__tags.append(tag)


    def __init__(self, code: str, name: str, credit_count: int, tags: List[str] = None):
        self.__code = code
        self.__name = name
        self.__credits = credit_count
        self.__tags: List[str]
        if tags is not None:
            self.__tags = tags


    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Class):
            return False
        if __value.code is not self.__code:
            return False
        if __value.name is not self.__name:
            return False
        if __value.credits != self.__credits:
            return False
        if len(__value.tags) != len(self.__tags):
            return False
        test = __value.tags
        for tag in self.__tags:
            if tag not in test:
                return False
        return True

    def check_data_match(self, code: str, name: str, credit_value: int, tags: List[str]):
        """Function to check if the given data matches the data within this class."""
        if code is not self.__code:
            return False
        if name is not self.__name:
            return False
        if credit_value != self.__credits:
            return False
        if len(tags) != len(self.__tags):
            return False
        for tag in self.__tags:
            if tag not in tags:
                return False
        return True

    def add_tags(self, tags: List[str]):
        """Add a list of tags to the classes existing tags."""
        self.__tags.append(tags)


    def remove_tag(self, tag: str):
        """Searches if a tag exists for this class and removes it."""
        if tag in self.__tags:
            self.__tags.remove(tag)

    def remove_tags(self, tags: List[str]):
        """Searches if a tag exists for this class and removes it."""
        for tag in tags:
            if tag in self.__tags:
                self.__tags.remove(tag)
