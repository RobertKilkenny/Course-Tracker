from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtCore import QRegExp
from utils.ProcessCourseData import CourseList
from utils.QuestionBlock import QuestionBlock


class EditClass(QWidget):
    """This is the subwindow to edit an existing class"""
    def __init__(self, course_list: CourseList):
        super().__init__()
        self.layout = QVBoxLayout()
        self.course_list = course_list
        self.__form_questions = {}
        self.__form_questions["Target-Class"] = QuestionBlock(
            question="What is the class code that you want to change.",
            placeholder="Remember it should be in the form XXX0000",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))

        for value in self.__form_questions.values():
            self.layout.addWidget(value)
            self.setLayout(self.layout)
