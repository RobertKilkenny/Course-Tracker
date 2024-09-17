from PySide2.QtWidgets import QWidget, QLabel, QScrollArea, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSizePolicy
from PySide2.QtGui import QFont, QPalette, QColor
from PySide2.QtCore import QRegExp, Qt
from utils.process_course_data import CourseList
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.question_block import SimpleQuestionBlock
from utils.course_object import CourseObject


class GenerateCSV(SubwindowWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, course_list: CourseList, app_manager: AppManager):
        super().__init__(course_list, app_manager)
        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_dialog.setNameFilter("CSV File (*.csv)")

        self.prompt = GenerateWindowWidget(self)
        self.courses = self.prompt.class_elements

        #Link objects to layout to be displayed
        self.layout.addWidget(self.prompt)
        self.setLayout(self.layout)


    def handle_find_file(self):
        """Opens a file explorer window so that the user can lead the app
        to where their existing csv file is."""
        self.app_manager.emit_open_window_request(self.file_dialog)


    def check_if_new_path_works(self):
        """Used to see if user gave a CSV with correct formatting."""
        self.app_manager.emit_generated_csv()


    def gen_new_csv(self):
        """Use the data given by the user to make a proper CSV file."""
        result = []
        for course in self.courses:
            temp = course.get_values()
            if temp["code"] is None or temp["name"] is None or temp["credits"] is None:
                continue
            result.append(CourseObject(temp["code"], temp["name"], temp["credits"]))
        self.app_manager.emit_create_csv(result)


class GenerateWindowWidget(QWidget):
    """Seperate class to define the widgets for the window (done seperately to make the 
    class object less cluttered)."""

    def __init__(self, parent_window: GenerateCSV):
        super().__init__(None)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        self.num_classes_edit = 0
        self.class_elements = []

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("blue"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        #Create Option 1: Find a new CSV to Check
        self.find_file_label = QLabel()
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.find_file_label.setFont(font)
        self.find_file_label.setText("Choose CSV File Path")
        layout.addWidget(self.find_file_label)

        self.find_file_widget = QWidget()
        find_file_layout = QVBoxLayout()
        file_search_holder = QHBoxLayout()
        filepath_line_edit = QLineEdit(parent=self)
        browse_file_explorer = QPushButton(parent=self, text="Browse...")
        submit_file_location_btn = QPushButton(parent=self, text="Save CSV File Path")
        submit_file_location_btn.clicked.connect(parent_window.check_if_new_path_works)

        file_search_holder.addWidget(filepath_line_edit)
        file_search_holder.addWidget(browse_file_explorer)
        find_file_layout.addLayout(file_search_holder)
        find_file_layout.addWidget(submit_file_location_btn)
        self.find_file_widget.setLayout(find_file_layout)
        layout.addWidget(self.find_file_widget)

        #Create Option 2: Aid the user in making a new CSV
        self.make_csv_label = QLabel()
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.make_csv_label.setFont(font)
        self.make_csv_label.setText("Make a New CSV")
        layout.addWidget(self.make_csv_label)
        self.notice = QLabel()
        font = QFont()
        font.setPointSize(10)
        self.notice.setFont(font)
        self.notice.setText("Note: If you don't want to add a class, you don't need to!")
        layout.addWidget(self.notice)

        make_csv_widget = QWidget()
        make_csv_layout = QVBoxLayout()
        submit_new_csv_btn = QPushButton(parent=self, text="Generate a CSV with this information!")
        submit_new_csv_btn.clicked.connect(parent_window.gen_new_csv)

        # Make SubWidget for user to add classes
        self.add_classes_widget = QWidget()
        self.add_classes_scroll = QScrollArea()
        self.add_classes_layout = QVBoxLayout()
        make_new_row_btn = QPushButton(parent=self.add_classes_widget, text="Add new class")
        make_new_row_btn.clicked.connect(self.make_new_row)
        self.add_classes_layout.addWidget(make_new_row_btn, alignment=Qt.AlignBottom)
        palette = self.add_classes_widget.palette()
        palette.setColor(QPalette.Window, QColor("darkgray"))
        self.add_classes_widget.setPalette(palette)
        self.add_classes_widget.setAutoFillBackground(True)
        self.add_classes_widget.setLayout(self.add_classes_layout)

        self.add_classes_scroll.setWidget(self.add_classes_widget)
        self.add_classes_scroll.setWidgetResizable(True)
        make_csv_layout.addWidget(self.add_classes_scroll)
        make_csv_layout.addWidget(submit_new_csv_btn)
        make_csv_widget.setLayout(make_csv_layout)
        layout.addWidget(make_csv_widget)

        #Connect all the work to the Base Widget and send it back!
        self.setLayout(layout)


    def make_new_row(self):
        """Make a new row for the user to enter data into."""
        self.num_classes_edit = self.num_classes_edit + 1
        self.remake_add_classes_widget()


    def remake_add_classes_widget(self):
        """Update widget when changes are made."""
        clear_layout(self.add_classes_layout)
        for _ in range(self.num_classes_edit):
            class_element_widget = ClassElement()
            self.class_elements.append(class_element_widget)
            self.add_classes_layout.addWidget(class_element_widget)

        make_new_row_btn = QPushButton(parent=self.add_classes_widget, text="Add new class")
        make_new_row_btn.clicked.connect(self.make_new_row)
        self.add_classes_layout.addWidget(make_new_row_btn, alignment=Qt.AlignBottom)
        self.add_classes_widget.setLayout(self.add_classes_layout)


class ClassElement(QWidget):
    """Class for each list element inside of add class for making new CSV"""
    def __init__(self):
        super().__init__(None)
        self.question_dict = {}
        self.question_dict["course-code"] = SimpleQuestionBlock(
            question="Input the new course code",
            placeholder="Put course code [ex. AAA0000]",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))
        self.question_dict["course-name"] = SimpleQuestionBlock(
            question="What is the name of the course",
            placeholder="Must be at least 3 characters long",
            regex=QRegExp(r"^[\w\s\-]+$"))
        self.question_dict["course-credits"] = SimpleQuestionBlock(
            question="Credit value",
            regex=QRegExp("[0-9]"))
        self.layout = QHBoxLayout()
        for value in self.question_dict.values():
            self.layout.addWidget(value)
        self.setLayout(self.layout)


    def get_values(self):
        """Gives all values in the ClassElement, returning a dictionary with 'code', 'name', 
        and 'credits' with either the value or None values if it isn't valid."""
        result = {}
        temp = self.question_dict["course-code"].get_answers()
        result["code"] = temp if len(temp) == 7 else None
        temp = self.question_dict["course-name"].get_answers()
        result["name"] = temp if len(temp) < 3 else None
        temp = self.question_dict["course-credits"].get_answers()
        result["credits"] = temp if not isinstance(temp, int) or temp < 1 else None


def clear_layout(layout):
    """Remove all widgets and layouts from the given layout"""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clear_layout(child.layout())
