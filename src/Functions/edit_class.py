from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QRegExp, QPoint
from utils.subwindow_widget import SubwindowWidget
from utils.app_manager import AppManager
from utils.question_block import SimpleQuestionBlock
from Windows.popup_window import PopupWindow


class EditClass(SubwindowWidget):
    """This is the subwindow to edit an existing class"""
    def __init__(self, app_manager: AppManager):
        super().__init__(app_manager)
        self.popup = None

        self.user_class_choice = SimpleQuestionBlock(
            question="What is the class code that you want to change.",
            placeholder="Remember it should be in the form XXX0000",
            regex=QRegExp("[A-Z]{3}[0-9]{4}"))
        self.user_class_choice.set_user_access(True)
        self.check_button = QPushButton("Search for class!")
        self.check_button.setCheckable(True)
        self.check_button.clicked.connect(self.check_class)
        self.layout.addWidget(self.user_class_choice)
        self.layout.addWidget(self.check_button)

        self.__form_questions = {"Class Name": SimpleQuestionBlock("New Course Name"),
                                 "Credits": SimpleQuestionBlock("New Credits Value")}

        for value in self.__form_questions.values():
            value.set_user_access(False)
            self.layout.addWidget(value)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setCheckable(True)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.handle_save)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def __update(self, has_chosen_class: bool):
        self.user_class_choice.set_user_access(not has_chosen_class)
        self.check_button.setEnabled(not has_chosen_class)
        for value in self.__form_questions.values():
            value.set_user_access(has_chosen_class, True)
        self.save_button.setEnabled(has_chosen_class)


    def handle_save(self):
        """Allows for the chosen class to be altered if any valid changes have been made!"""
        print("Attempting to save changes!")
        result = self.app_manager.edit_class(self.user_class_choice.get_answer(),
                                    self.__form_questions["Class Name"].get_answer(),
                                    self.__form_questions["Credits"].get_answer())
        self.__update(result == 0)
        self.__form_questions["Class Name"].change_line_edit_placeholder("")
        self.__form_questions["Credits"].change_line_edit_placeholder("")


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
            self.__form_questions["Class Name"].change_line_edit_placeholder(
                "Name was " + course.name)
            self.__form_questions["Credits"].change_line_edit_placeholder(
                "Credits' value was " + str(course.credits))
            return 0
        return 1
