from PySide2.QtWidgets import QComboBox
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.course_object import Semester

class SemesterView(SubwindowWidget):
    """Create the window to show the class details by semester."""
    def __init__(self, app_manager: AppManager):
        super().__init__(app_manager, "View all classes by semester!")
        self.semester_select = QComboBox(self)
        for semester in AppManager.get_active_semesters():
            self.semester_select.addItem(semester.print_details)
