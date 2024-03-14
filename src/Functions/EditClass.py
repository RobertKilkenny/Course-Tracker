from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import QRegExp
from utils.ProcessCourseData import CourseList
from utils.QuestionBlock import QuestionBlock


class EditClass(QWidget):
    """This is the subwindow to edit an existing class"""
    def __init__(self, course_list: CourseList):
        super().__init__()
        self.layout = QVBoxLayout()
        self.course_list = course_list

        self.user_class_choice = QuestionBlock(
            question="What is the class code that you want to change.",
            placeholder="Remember it should be in the form XXX0000",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))
        self.user_class_choice.set_user_access(True)
        self.check_button = QPushButton("Search for class!")
        self.check_button.setCheckable(True)
        self.check_button.clicked.connect(self.check_class)
        self.layout.addWidget(self.user_class_choice)
        self.layout.addWidget(self.check_button)

        self.__form_questions = {"Class Name": QuestionBlock("New Course Name")}

        for value in self.__form_questions.values():
            value.set_user_access(False)
            self.layout.addWidget(value)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setCheckable(True)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.handle_save)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def __update(self, has_chosen_class: bool):
        self.user_class_choice.set_user_access(not has_chosen_class)
        self.check_button.setEnabled(not has_chosen_class)
        for value in self.__form_questions.values():
            value.set_user_access(has_chosen_class, True)
        self.save_button.setEnabled(has_chosen_class)

    def handle_save(self):
        """Allows for the chosen class to be altered if any valid changes have been made!"""
        print("Attempting to save changes!")
        self.__update(False)


    def check_class(self):
        """Function to determine if the class code given can be used to edit the database!"""
        message = ""
        result = False
        user_input = self.user_class_choice.input.text()
        match handle_check(user_input, self.course_list):
            case -1:
                message = f"Code given ({user_input}) was invalid (not in the format AAA0000)!"
            case 1:
                message = f"Code given ({user_input}) was not found in the class catalog!"
            case 0:
                message = f"Code given({user_input}) was found in the class catalog!"
                self.course_list.return_class(user_input).print_stats()
                result = True
            case _:
                message = "ERROR: function gave back invalid code!"
        print(message)
        self.__update(result)


def handle_check(code: str, course_list: CourseList):
    """Checks if the user given class code is valid and if it exists in the dataset. Returns 0 if valid, -1 if the input is invalid and 1 if it does not exist in the dataset."""
    if len(code) < 7:
        return -1
    if  course_list.does_class_exist(code):
        return 0
    return 1