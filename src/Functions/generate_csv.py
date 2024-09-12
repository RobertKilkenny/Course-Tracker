from PySide2.QtWidgets import QWidget, QPushButton, QLineEdit, QFileDialog
from utils.process_course_data import CourseList
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager

class GenerateCSV(SubwindowWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, course_list: CourseList, app_manager: AppManager):
        super().__init__(course_list, app_manager)

        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_dialog.setNameFilter("CSV File (*.csv)")

        find_file_option = QWidget()
        
        gen_file_option = QWidget()

        self.complete = False
        save_button = QPushButton("Save Class")
        save_button.setCheckable(True)
        save_button.clicked.connect(self.handle_save)
        self.prompt = save_button

        #Link objects to layout to be displayed
        self.layout.addWidget(self.prompt)
        self.setLayout(self.layout)


    def handle_find_file(self):
        """Opens a file explorer window so that the user can lead the app
        to where their existing csv file is."""
        self.app_manager.emit_open_window_request(self.file_dialog)

    def handle_save(self):
        """Handle the save functionality."""
        self.complete = True
        self.app_manager.emit_generated_csv()


    def is_complete(self):
        """Returns if the CSV has been handled."""
        return self.complete
