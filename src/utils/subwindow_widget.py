from PySide2.QtWidgets import QWidget, QVBoxLayout
from utils.process_course_data import CourseList


class SubwindowWidget(QWidget):
    def __init__(self, course_list: CourseList):
        super().__init__()
        self.course_list = course_list
        self.layout = QVBoxLayout()
