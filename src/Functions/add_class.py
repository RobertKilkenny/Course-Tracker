from typing import List
from PySide2.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget
from PySide2.QtCore import QRegExp
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.question_block import SimpleQuestionBlock

class AddClass(SubwindowWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, app_manager: AppManager):
        super().__init__(app_manager, "Add Class to Database")

        #Define subwindow objects
        self.question_dict = {}
        self.optional_dict = {}
        self.question_dict["course-code"] = SimpleQuestionBlock(
            question="Input the new course code",
            placeholder="Put course code [ex. AAA0000]",
            regex=QRegExp(r'[A-Z]{3}[0-9]{4}'))
        self.question_dict["course-name"] = SimpleQuestionBlock(
            question="What is the name of the course",
            placeholder="Must be at least 3 characters long",
            regex=QRegExp(r'[^\\t\\b\\n\\r]{3}[^\\t\\b\\n\\r]*'))
        self.question_dict["course-credits"] = SimpleQuestionBlock(
            question="Input the credit for the course",
            placeholder="How many credits is it worth?",
            regex=QRegExp(r'[0-9]{1}'))
        self.optional_dict["grade"] = SimpleQuestionBlock(
            question="Grade earned",
            placeholder="What letter grade [optional]?",
            regex=QRegExp(r'^[+-]?[A-D]|[E-F]$'))
        self.optional_dict["semester"] = SimpleQuestionBlock(
            question="Semester taken",
            placeholder="When was it taken [optional]?",
            regex=QRegExp(r'[\\D\\w]+[0-9]{4}'))

        #Link objects to layout to be displayed
        questions_layout = QHBoxLayout()
        questions_widget = QWidget(self)
        required_questions_layout = QVBoxLayout()
        required_questions_widget = QWidget(questions_widget)
        for value in self.question_dict.values():
            required_questions_layout.addWidget(value)
        required_questions_widget.setLayout(required_questions_layout)
        questions_layout.addWidget(required_questions_widget)

        optional_questions_layout = QVBoxLayout()
        optional_questions_widget = QWidget(questions_widget)
        for value in self.question_dict.values():
            optional_questions_layout.addWidget(value)
        optional_questions_widget.setLayout(optional_questions_layout)
        questions_layout.addWidget(optional_questions_widget)
        
        questions_widget.setLayout(questions_layout)
        self.layout.addWidget(questions_widget)
        save_button = QPushButton("Save Class")
        save_button.setCheckable(True)
        save_button.clicked.connect(self.handle_save)
        self.layout.addWidget(save_button)
        self.setLayout(self.layout)


    def is_complete_input(self) -> bool:
        """Checks if the Add Class widget has all values needed to make a new class."""
        error_list = self.validate_complete()
        if len(error_list) != 0:
            error_msg = read_user_errors(error_list)
            self.display_error_messages(error_msg)
            return False
        else:
            return True


    def display_error_messages(self, error_msg: str):
        """Display the error messages in a QMessageBox."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Input Error")
        msg_box.setText("There are errors in your info for a new class:")
        msg_box.setInformativeText(error_msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


    def validate_complete(self)-> List[int]:
        """Handles the grunt work of is_complete_input"""
        report = []
        print("\nRunning tests for validation, Each * at the end of a check means a failure")
        print_string = self.question_dict["course-code"].input.text()
        print(f"\tTest if course code ({print_string}) is 7 characters long", end="")
        if not len(self.question_dict["course-code"].input.text()) == 7:
            report.append(0)
            print(" *", end ="")
        print_string = self.question_dict["course-name"].input.text()
        print(f"\n\tTest if course name ({print_string}) is at least 3 characters long",  end=" ")
        if not len(self.question_dict["course-name"].input.text()) > 2:
            report.append(1)
            print(" *", end ="")
        print_string = self.question_dict["course-credits"].input.text()
        print(f"\n\tTest if course credits ({print_string}) has a value in the box",  end=" ")
        if not len(self.question_dict["course-credits"].input.text()) == 1:
            report.append(2)
            print(" *", end ="")
        else:
            print_string = self.question_dict["course-credits"].input.text()
            print(f"\n\tTest if course credits ({print_string}) is a valid credit number",  end=" ")
            if int(self.question_dict['course-credits'].input.text()) <= 0:
                report.append(3)
                print(" *", end ="")
        print_string = self.question_dict["course-code"].input.text()
        print(f"\n\tTest if course code ({print_string}) already exists",  end=" ")
        if self.app_manager.does_class_exist(self.question_dict["course-code"].input.text()):
            report.append(4)
            print(" *", end ="")
        print("\n")
        return report


    def handle_save(self):
        """Function to call when input is valid and user wants to save their work."""
        is_complete = self.is_complete_input()
        if is_complete:
            print("This is a valid class!")
            self.app_manager.add_class(code=self.question_dict["course-code"].input.text(),
                                       name=self.question_dict["course-name"].input.text(),
                                       value=int(self.question_dict["course-credits"].input.text()))
            if self.optional_dict["grade"].is_complete():
                self.app_manager.change_grade(self.question_dict["course-code"].input.text(),
                                              self.optional_dict["semester"].input.text())
            if self.optional_dict["semester"].is_complete():
                self.app_manager.change_grade(self.question_dict["course-code"].input.text(),
                                              self.optional_dict["semester"].input.text())
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
