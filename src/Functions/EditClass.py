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
        self.class_chosen = False
        self.user_class_choice = QuestionBlock(
            question="What is the class code that you want to change.",
            placeholder="Remember it should be in the form XXX0000",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))
        self.layout.addWidget(self.user_class_choice)
        check_button = QPushButton("Save Changes")
        check_button.setCheckable(self.class_chosen)
        check_button.clicked.connect(self.check_class)
        self.layout.addWidget(check_button)
        self.__form_questions = {}

        for value in self.__form_questions.values():
            self.layout.addWidget(value)

        if self.class_chosen:
            pass
        else:
            self.user_class_choice.set_user_access(True)

        save_button = QPushButton("Save Changes")
        save_button.setCheckable(self.class_chosen)
        save_button.clicked.connect(self.handle_save)
        self.layout.addWidget(save_button)
        self.setLayout(self.layout)


    def handle_save(self):
        """Allows for the chosen class to be altered if any valid changes have been made!"""
        print("Attempting to save changes!")


    def check_class(self):
        """Function to determine if the class code given can be used to edit the database!"""
        message = ""
        result = False
        match handle_check(self.user_class_choice.input.text(), self.course_list):
            case -1:
                message = f"Code given ({self.user_class_choice.input.text()}) was invalid (not in the format AAA0000)!"
            case 1:
                message = f"Code given({self.user_class_choice.input.text()}) was not found in the class catalog!"
            case 0:
                message = f"Code given({self.user_class_choice.input.text()}) was found in the class catalog!"
                result = True
            case _:
                message = "ERROR: function gave back invalid code!"
        print(message)
        return result
            

def handle_check(code: str, course_list: CourseList):
    """Checks if the user given class code is valid and if it exists in the dataset. Returns 0 if valid, -1 if the input is invalid and 1 if it does not exist in the dataset."""
    if len(code) < 7:
        return -1
    if  course_list.does_class_exist(code):
        return 0
    return 1