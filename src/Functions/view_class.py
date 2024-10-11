from PySide2.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QLabel
from PySide2.QtCore import QRegExp, QPoint, Qt
from PySide2.QtGui import QFont, QColor
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.question_block import SimpleQuestionBlock
from utils.labeled_datail import LabelDetail
from utils.process_course_data import from_list_to_string
from Windows.popup_window import PopupWindow


class ViewClass(SubwindowWidget):
    """This is the subwindow to edit an existing class"""
    def __init__(self, app_manager: AppManager):
        super().__init__(app_manager, "View Class Stats")
        self.popup = None

        self.user_choice_layout = QVBoxLayout()
        self.user_choice_holder = QWidget()
        self.user_class_choice = SimpleQuestionBlock(
            question="What is the class code that you want to view?",
            placeholder="Remember it should be in the form XXX0000",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))
        self.check_button = QPushButton("Search for class!")
        self.check_button.setCheckable(True)
        self.check_button.clicked.connect(self.check_class)
        self.user_choice_layout.addWidget(self.user_class_choice)
        self.user_choice_layout.addWidget(self.check_button)
        self.user_choice_holder.setLayout(self.user_choice_layout)
        self.user_choice_holder.setSizePolicy(QSizePolicy.Expanding,
                                              QSizePolicy.Minimum)
        self.layout.addWidget(self.user_choice_holder)
        self.data_layout = QHBoxLayout()
        self.data_holder = QWidget()

        # Widget to display class details
        self.class_details_layout = QVBoxLayout()
        self.class_details_holder = QWidget()
        self.class_tags_layout = QVBoxLayout()

        tags_label = QLabel("Tags")
        tags_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        tags_label.setFont(label_font)
        self.class_tags_layout.addWidget(tags_label)
        self.class_tags_holder = QWidget()
        self.class_tags_holder.setLayout(self.class_tags_layout)

        self.__data_points = {"Class Name": LabelDetail("Name:", font_size=12),
                                 "Credits": LabelDetail("Credits:", font_size=12),
                                 "Semester": LabelDetail("Semester taken:", font_size=12),
                                 "Tags": LabelDetail("Tags:", font_size=12)}

        for value in self.__data_points.values():
            self.class_details_layout.addWidget(value)
        self.class_details_holder.setLayout(self.class_details_layout)
        self.class_details_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Widget to display the grade or lack thereoff
        self.grade_layout = QVBoxLayout()
        self.grade_layout.setAlignment(Qt.AlignTop)
        self.grade_holder = QWidget()
        grade_label = QLabel("<u>Grade</u>")
        grade_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        grade_label_font = QFont()
        grade_label_font.setPointSize(30)
        grade_label_font.setBold(True)
        grade_label.setFont(grade_label_font)
        grade_label.setAlignment(Qt.AlignCenter)
        self.grade_layout.addWidget(grade_label)
        self.grade_letter = QLabel("")
        self.grade_letter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        grade_letter_font = QFont()
        grade_letter_font.setPointSize(150)
        grade_letter_font.setBold(True)
        self.grade_letter.setFont(grade_letter_font)
        self.grade_letter.setAlignment(Qt.AlignHCenter)
        self.grade_layout.addWidget(self.grade_letter)
        self.grade_holder.setLayout(self.grade_layout)
        self.grade_holder.setSizePolicy(QSizePolicy.MinimumExpanding,
                                        QSizePolicy.Expanding)
        self.grade_holder.setStyleSheet("background-color: lightgray;")



        self.data_layout.addWidget(self.class_details_holder)
        self.data_layout.addWidget(self.grade_holder)
        self.data_holder.setLayout(self.data_layout)
        self.data_holder.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        self.layout.addWidget(self.data_holder)
        self.setLayout(self.layout)

    def __update(self, has_chosen_class: bool):
        self.check_button.setEnabled(not has_chosen_class)


    def check_class(self):
        """Function to determine if the class code given can be used to edit the database!"""
        message = ""
        result = False
        user_input = self.user_class_choice.input.text()
        match self.handle_check(user_input):
            case -1:
                message = f"Code given \"{user_input}\" was invalid (not in the format AAA0000)!"
            case 1:
                message = f"Code given \"{user_input}\" was not found in the class catalog!"
            case 0:
                message = f"Code given\"{user_input}\" was found in the class catalog!"
                result = True
            case _:
                message = "ERROR: function gave back invalid code!"
        if not result:
            self.lock_screen(message)
        self.__update(result)


    def lock_screen(self, reason: str):
        """Lock the edit screen since the class should not be edited."""
        self.popup = PopupWindow(reason, ["Okay"], [self.unlock_screen],
                                "Could not edit class!", self.unlock_screen)
        parent_center = self.parent().geometry().center()
        child_pos = parent_center + QPoint(self.popup.width() // 2, self.popup.height() // 2)
        self.popup.move(child_pos)
        self.setEnabled(False)
        self.popup.show()


    def unlock_screen(self):
        """Unlocks the screen so it can edit."""
        self.setEnabled(True)
        self.popup.close()


    def handle_check(self, code: str):
        """Checks if the user given class code is valid and if it exists in the dataset.
        Returns 0 if valid, -1 if the input is invalid and 1 if it does not exist in the dataset."""
        if len(code) < 7:
            return -1
        if  self.app_manager.does_class_exist(code):
            course = self.app_manager.get_class_details(code)
            print("Found class:", course)
            self.__data_points["Class Name"].set_detail(course.name)
            self.__data_points["Credits"].set_detail(str(course.credits))
            self.__data_points["Semester"].set_detail(str(course.semester_taken))
            temp = course.return_tags_as_string()
            self.__data_points["Tags"].set_detail(temp if temp != "No tags found" else None)
            self.grade_letter.setText(course.grade)
            GPA = self.app_manager.get_grade_letter_value(course.grade)
            color = QColor(255, 0, 0)
            if GPA > 3:
                color = QColor(0, 255, 0)
            elif GPA > 2:
                color = QColor(255, 255, 0)
            self.grade_letter.setStyleSheet(f"color: {color.name()};")
            return 0
        return 1
