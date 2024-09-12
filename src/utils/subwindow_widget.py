from PySide2.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from utils.process_course_data import CourseList
from utils.app_manager import AppManager


class SubwindowWidget(QWidget):
    def __init__(self, course_list: CourseList, app_manager: AppManager):
        super().__init__()
        self.course_list = course_list
        self.app_manager = app_manager
        self.layout = QVBoxLayout()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
