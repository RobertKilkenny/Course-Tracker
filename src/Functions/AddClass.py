from typing import List
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import QRegExp
from utils.ProcessCourseData import CourseList
from utils.QuestionBlock import QuestionBlock

class AddClass(QWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, course_list: CourseList):
        super().__init__()
        self.layout = QVBoxLayout()
        self.course_list = course_list

        self.question_dict = {}
        self.question_dict["course-code"] = QuestionBlock(
            question="Input the new course code",
            placeholder="Put course code [ex. AAA0000]",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))
        self.question_dict["course-name"] = QuestionBlock(
            question="What is the name of the course",
            placeholder="Must be at least 3 characters long",
            regex=QRegExp("^[\w\s\-]+$"))
        self.question_dict["course-credits"] = QuestionBlock(
            question="Input the credit for the course",
            placeholder="How many credits is it worth?",
            regex=QRegExp("[0-9]"))
        
        for value in self.question_dict.values():
            self.layout.addWidget(value)
        save_button = QPushButton("Save Class")
        save_button.setCheckable(True)
        self.layout.addWidget(save_button)
        save_button.clicked.connect(self.handle_save)
        self.setLayout(self.layout)


    def is_complete_input(self) -> bool:
        """Checks if the Add Class widget has all values needed to make a new class."""
        error_list = self.validate_complete()
        if len(error_list) != 0:
            print(read_user_errors(error_list))
            return False
        else:
            return True


    def validate_complete(self)-> List[int]:
        """Handles the grunt work of is_complete_input"""
        report = []
        print("Running tests for validation, Each * means a failure")
        print_string = self.question_dict["course-code"].input.text()
        print(f"Test if course code ({print_string}) is 7 characters long", end="")
        if not len(self.question_dict["course-code"].input.text()) == 7:
            report.append(0)
            print(" *", end ="")
        print_string = self.question_dict["course-name"].input.text()
        print(f"\nTest if course name ({print_string}) is at least 3 characters long",  end=" ")
        if not len(self.question_dict["course-name"].input.text()) > 2:
            report.append(1)
            print(" *", end ="")
        print_string = self.question_dict["course-credits"].input.text()
        print(f"\nTest if course credits ({print_string}) has a value in the box",  end=" ")
        if not len(self.question_dict["course-credits"].input.text()) == 1:
            report.append(2)
            print(" *", end ="")
        else:
            print_string = self.question_dict["course-credits"].input.text()
            print(f"\nTest if course credits ({print_string}) is a valid credit number",  end=" ")
            if int(self.question_dict['course-credits'].input.text()) <= 0:
                report.append(3)
                print(" *", end ="")
        print_string = self.question_dict["course-code"].input.text()
        print(f"\nTest if course code ({print_string}) already exists",  end=" ")
        if self.course_list.does_class_exist(self.question_dict["course-code"].input.text()):
            report.append(4)
            print(" *", end ="")
        print("\n")
        return report


    def handle_save(self):
        """Function to call when input is valid and user wants to save their work."""
        is_complete = self.is_complete_input()
        if is_complete:
            print("This is a valid class!")
        else:
            print("Invalid class!")


def read_user_errors(error_list) -> str:
    """Prints all errors in report from the error array"""
    report = ""
    for number in error_list:
        match number:
            case 0:
                report += "- Course Code is not complete"
            case 1: 
                report += "- Course name is not long enough"
            case 2:
                report += "- Course credits were not given"
            case 3:
                report += "- Course credits are not greater than 0"
            case 4:
                report += "- Course code already exists"
            case _:
                report += "- Create class tester gave invalid error!!!!"
        report += "\n"
    return report
