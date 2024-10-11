from PySide2.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSizePolicy
from PySide2.QtCore import QRegExp, QPoint
from PySide2.QtGui import QFont, QPalette, QColor
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.question_block import SimpleQuestionBlock
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
        self.user_class_choice.set_user_access(True)
        self.check_button = QPushButton("Search for class!")
        self.check_button.setCheckable(True)
        self.check_button.clicked.connect(self.check_class)
        self.user_choice_layout.addWidget(self.user_class_choice)
        self.user_choice_layout.addWidget(self.check_button)
        self.user_choice_holder.setLayout(self.user_choice_layout)
        self.user_choice_holder.setSizePolicy(QSizePolicy.Expanding,
                                              QSizePolicy.Minimum)
        self.layout.addWidget(self.user_choice_holder)
        self.data_layout = QVBoxLayout()
        self.data_holder = QWidget()

        self.__data_points = {"Class Name": SimpleQuestionBlock("New Course Name"),
                                 "Credits": SimpleQuestionBlock("New Credits Value")}

        for value in self.__data_points.values():
            value.set_user_access(False)
            self.data_layout.addWidget(value)
        self.data_holder.setLayout(self.data_layout)
        self.data_holder.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        self.layout.addWidget(self.data_holder)
        self.setLayout(self.layout)

    def __update(self, has_chosen_class: bool):
        self.user_class_choice.set_user_access(not has_chosen_class)
        self.check_button.setEnabled(not has_chosen_class)
        for value in self.__data_points.values():
            value.set_user_access(has_chosen_class, True)
        self.save_button.setEnabled(has_chosen_class)


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
            self.__data_points["Class Name"].change_line_edit_placeholder(
                "Name was " + course.name)
            self.__data_points["Credits"].change_line_edit_placeholder(
                "Credits' value was " + str(course.credits))
            return 0
        return 1
