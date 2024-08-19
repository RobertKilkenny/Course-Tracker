from PySide2.QtWidgets import QPushButton
from utils.process_course_data import CourseList
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager

class GenerateCSV(SubwindowWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, course_list: CourseList, app_manager: AppManager):
        super().__init__(course_list, app_manager)

        self.complete = False
        save_button = QPushButton("Save Class")
        save_button.setCheckable(True)
        save_button.clicked.connect(self.handle_save)
        self.prompt = save_button

        #Link objects to layout to be displayed
        self.layout.addWidget(self.prompt)
        self.setLayout(self.layout)


    def handle_save(self):
        """Handle the save functionality."""
        self.complete = True
        self.app_manager.emit_generated_csv()


    def is_complete(self):
        """Returns if the CSV has been handled."""
        return self.complete
