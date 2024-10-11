from typing import Dict
import os
from PySide2.QtWidgets import QWidget, QLabel, QScrollArea, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSizePolicy, QMessageBox
from PySide2.QtGui import QFont, QPalette, QColor, QRegExpValidator
from PySide2.QtCore import QRegExp, QSize
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.course_object import CourseObject


class GenerateCSV(SubwindowWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, app_manager: AppManager):
        super().__init__(app_manager, "No CSV found for the app. Choose a way to resolve this:")
        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_dialog.setNameFilter("CSV File (*.csv)")
        self.file_dialog.fileSelected.connect(self.update_file_path)
        self.popup = QWidget()

        self.prompt = GenerateWindowWidget(self)
        self.prompt.filepath_line_edit.setText(self.gen_default_csv_path())
        self.courses = self.prompt.class_elements
        self.__csv_file_path = None

        #Link objects to layout to be displayed
        self.layout.addWidget(self.prompt)
        self.setLayout(self.layout)


    def handle_find_file(self):
        """Opens a file explorer window so that the user can lead the app
        to where their existing csv file is."""
        dir_list = self.prompt.filepath_line_edit.text().split("\\")
        if len(dir_list) > 1:
            if len(dir_list[-1]) > 4 and dir_list[-1][-4:] == ".csv":
                dir_list = dir_list[:-1]
            dir_path = "\\".join(dir_list)
            if os.path.exists(dir_path):
                self.file_dialog.setDirectory(dir_path)
        self.app_manager.emit_open_window_request(self.file_dialog)


    def update_file_path(self, file_path):
        """Updates the QLineEdit with the new file path when a file is selected."""
        if os.path.isfile(file_path):
            self.prompt.filepath_line_edit.setText(file_path)
            self.check_if_new_path_works()


    def check_if_new_path_works(self) -> bool:
        """Used to see if user gave a CSV with correct formatting."""
        selected_file = self.prompt.filepath_line_edit.text()
        if selected_file:
            if (isinstance(selected_file, str) and
                    self.app_manager.change_csv_location(selected_file, True)):
                self.app_manager.emit_generated_csv()
                self.__csv_file_path = selected_file
                return True
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                if isinstance(selected_file, str):
                    msg_box = (f'The selected file ("{selected_file}") is not formatted correctly.'+
                               ' You can use create a proper CSV for this app using the option 2.')
                else:
                    msg = f'The selected file ("{selected_file}") does not exist.'
                msg_box.setText(msg)
                msg_box.setWindowTitle("File Error")
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("No file was selected.")
            msg_box.setWindowTitle("No File Selected")
            msg_box.exec_()
            self.__csv_file_path = self.gen_default_csv_path()
            self.prompt.filepath_line_edit.setText(self.__csv_file_path)


    def gen_default_csv_path(self) -> str:
        """Create a baseline csv location that could hold the data.

        Returns:
            path (str): returns the generic csv location
        """
        temp = os.path.dirname(os.path.abspath(__file__)).split("\\")[:-2]
        path = "\\".join(temp)
        return os.path.join(path, "app-data", "classes.csv")


    def get_csv_path(self) -> str | None:
        """Pull the the CSV path if it is valid.

        Returns:
            path (str | None): The literal path of the csv or None if the path is invalid
        """
        return self.__csv_file_path


    def popup_for_gen_new_csv(self):
        """Handle making a popup to make sure that the user wants the new CSV saved at the path
        saved."""
        self.popup.setFixedSize(QSize(500, 250))
        self.popup.setWindowTitle("Are you sure?")
        layout = QVBoxLayout()
        label = QLabel("The CSV will be saved here:")
        data = QLineEdit()
        data.setText(self.prompt.filepath_line_edit.text())
        layout.addWidget(label)
        layout.addWidget(data)

        button_holder_layout = QHBoxLayout()
        accept_btn = QPushButton(text="accept")
        accept_btn.clicked.connect(self.__gen_new_csv)
        decline_btn = QPushButton(text="go back")
        decline_btn.clicked.connect(self.popup.close)
        button_holder_layout.addWidget(accept_btn)
        button_holder_layout.addWidget(decline_btn)
        button_holder = QWidget()
        button_holder.setLayout(button_holder_layout)
        layout.addWidget(button_holder)
        self.popup.setLayout(layout)
        self.app_manager.emit_open_window_request(self.popup)


    def __gen_new_csv(self):
        """Use the data given by the user to make a proper CSV file."""
        result = []
        self.popup.close()
        for course in self.courses:
            temp = course.get_values()
            if temp["code"] is None or temp["name"] is None or temp["credits"] is None:
                continue
            class_obj = CourseObject(temp["code"], temp["name"], temp["credits"])
            if len(class_obj.make_list_of_vars_failing()) == 0:
                result.append(class_obj)
        self.__csv_file_path = self.prompt.filepath_line_edit.text()
        did_work = self.app_manager.create_new_csv(self.__csv_file_path, result)
        if did_work:
            self.app_manager.emit_generated_csv()


class GenerateWindowWidget(QWidget):
    """Separate class to define the widgets for the window (done separately to make the 
    class object less cluttered)."""

    def __init__(self, parent_window: GenerateCSV):
        super().__init__(None)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        self.row_count = 0
        self.class_elements = []
        self.find_file_label = QLabel()
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        # Create Option 1: Find a new CSV to Check
        self.find_file_label = QLabel()
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.find_file_label.setFont(font)
        self.find_file_label.setText("Option 1: Choose CSV File Path")
        layout.addWidget(self.find_file_label)

        self.find_file_widget = QWidget()
        find_file_layout = QVBoxLayout()
        file_search_holder = QHBoxLayout()
        self.filepath_line_edit = QLineEdit(parent=self)
        browse_file_explorer = QPushButton(parent=self, text="Browse...")
        browse_file_explorer.clicked.connect(parent_window.handle_find_file)
        submit_file_location_btn = QPushButton(parent=self, text="Save CSV File Path")
        submit_file_location_btn.clicked.connect(parent_window.check_if_new_path_works)

        file_search_holder.addWidget(self.filepath_line_edit)
        file_search_holder.addWidget(browse_file_explorer)
        find_file_layout.addLayout(file_search_holder)
        find_file_layout.addWidget(submit_file_location_btn)
        self.find_file_widget.setLayout(find_file_layout)
        layout.addWidget(self.find_file_widget)

        # Create Option 2: Aid the user in making a new CSV
        self.make_csv_label = QLabel()
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.make_csv_label.setFont(font)
        self.make_csv_label.setText("Option 2: Make a New CSV")
        layout.addWidget(self.make_csv_label)

        self.notice = QLabel()
        font = QFont()
        font.setPointSize(10)
        self.notice.setFont(font)
        self.notice.setText("Note: If you don't want to add any classes yet, you don't need to!")
        layout.addWidget(self.notice)

        make_csv_widget = QWidget()
        make_csv_layout = QVBoxLayout()
        submit_new_csv_btn = QPushButton(parent=self, text="Generate a CSV with this information!")
        submit_new_csv_btn.clicked.connect(parent_window.popup_for_gen_new_csv)

        # SubWidget for user to add classes
        self.add_classes_widget = QWidget()
        self.add_classes_scroll = QScrollArea()
        self.add_classes_layout = QVBoxLayout()
        make_new_row_btn = QPushButton(parent=self.add_classes_widget, text="Add new class")
        make_new_row_btn.clicked.connect(self.make_new_row)

        palette = self.add_classes_widget.palette()
        palette.setColor(QPalette.Window, QColor("darkgray"))
        self.add_classes_widget.setPalette(palette)
        self.add_classes_widget.setAutoFillBackground(True)
        self.add_classes_widget.setLayout(self.add_classes_layout)

        self.add_classes_scroll.setWidget(self.add_classes_widget)
        self.add_classes_scroll.setWidgetResizable(True)
        make_csv_layout.addWidget(self.add_classes_scroll)
        make_csv_layout.addWidget(make_new_row_btn)
        make_csv_layout.addWidget(submit_new_csv_btn)
        make_csv_widget.setLayout(make_csv_layout)
        layout.addWidget(make_csv_widget)

        self.setLayout(layout)


    def make_new_row(self):
        """Make a new row for the user to enter data into."""
        class_element_widget = ClassElement()  # Create a new ClassElement instance
        self.class_elements.append(class_element_widget)  # Add to the list
        self.add_classes_layout.addWidget(class_element_widget)  # Add the widget to the layout
        self.row_count = len(self.class_elements)  # Update row count


    def remake_add_classes_widget(self):
        """Rebuild the widget when changes are made."""
        clear_layout(self.add_classes_layout)  # Clear the layout
        for element in self.class_elements:  # Re-add all the existing class elements
            self.add_classes_layout.addWidget(element)
        self.add_classes_widget.setLayout(self.add_classes_layout)


class ClassElement(QWidget):
    """Class for each list element inside of add class for making new CSV"""
    def __init__(self):
        super().__init__(None)
        self.question_dict: Dict[str, QLineEdit] = {}
        self.question_dict["course-code"] = QLineEdit()
        self.question_dict["course-code"].setPlaceholderText("Put course code [ex. AAA0000]")
        self.question_dict["course-code"].setValidator(
            QRegExpValidator(QRegExp("[A-Z]{3}[0-9]{4}")))

        self.question_dict["course-name"] = QLineEdit()
        self.question_dict["course-name"].setPlaceholderText("Must be at least 3 characters long")
        self.question_dict["course-name"].setValidator(QRegExpValidator(QRegExp(r"^[\w\s\-]+$")))

        self.question_dict["course-credits"] = QLineEdit()
        self.question_dict["course-credits"].setPlaceholderText("Credit value")
        self.question_dict["course-credits"].setValidator(QRegExpValidator(QRegExp("[0-9]")))

        self.layout = QHBoxLayout()
        for value in self.question_dict.values():
            self.layout.addWidget(value)
        self.setLayout(self.layout)

    def get_values(self):
        """Returns a dictionary with 'code', 'name', and 'credits' or None if values are invalid."""
        result = {}
        temp = self.question_dict["course-code"].text()
        result["code"] = temp if len(temp) == 7 else None

        temp = self.question_dict["course-name"].text()
        result["name"] = temp if len(temp) > 2 else None

        temp = self.question_dict["course-credits"].text()
        result["credits"] = None
        if len(temp) > 0:
            result["credits"] = int(temp)
        return result


def clear_layout(layout):
    """Remove all widgets and layouts from the given layout."""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clear_layout(child.layout())
