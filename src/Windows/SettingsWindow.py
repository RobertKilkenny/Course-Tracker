"""Module to hold the class SettingsWindow that can be called by the application."""
import json
from typing import Dict, List
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide2.QtCore import QSize, Qt
from Windows.PopupWindow import PopupWindow
from utils.QuestionBlock import NestedQuestionBlock, SimpleQuestionBlock

CURRENT_SETTINGS_FOLDER = "./app-data/app_settings.json"
DEFAULT_SETTINGS_FOLDER = "./app-data/default_settings.json"

class SettingsWindow(QWidget):
    """Secondary window to create a json file.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Settings")
        self.setMinimumSize(QSize(300, 600))
        self.settings = {}

        with open(CURRENT_SETTINGS_FOLDER, encoding="utf-8") as json_file:
            self.settings = json.load(json_file)

        self.elements: Dict[str, QWidget] = {}

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.save_n_close_button = QPushButton("Save and Close")
        self.save_n_close_button.clicked.connect(self.close_n_save)
        self.default_button = QPushButton("Reset to Defaults")
        self.default_button.clicked.connect(self.handle_default)
        self.__update()
        self.w = None

    def __update(self):
        layout = QVBoxLayout()
        print(self.settings)
        for key, value in self.settings.items():
            if isinstance(value, Dict):
                sub_titles: List[str] = []
                answers = []
                for sub_title, answer in value.items():
                    sub_titles.append(sub_title)
                    answers.append(answer)
  
                self.elements[key] = NestedQuestionBlock(key, sub_titles)
                self.elements[key].change_multiple_line_edit_text(sub_titles, answers)
            else:
                self.elements[key] = SimpleQuestionBlock(key)
                self.elements[key].change_line_edit_text(value)
            layout.addWidget(self.elements[key])


        layout.addWidget(self.save_button)
        layout.addWidget(self.save_n_close_button)
        layout.addWidget(self.default_button)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setLayout(layout)
        self.show()


    def closeEvent(self, event: QCloseEvent) -> None:
        """In the event the window is closed with setting changes, this will pop up."""
        self.w = PopupWindow("Do you want to save these changes?", buttons_text_list=["yes", "no"],
                             buttons_functions_list=[self.popup_save, self.popup_no_save],
                             window_title="Before you go!!")
        self.w.show()
        return super().closeEvent(event)


    def close_n_save(self):
        """Handles closing the Settings window and saving progress."""
        self.save_settings()
        self.close()


    def popup_no_save(self):
        """Function to ensure popup closes when we are done with it."""
        self.w.close()


    def popup_save(self):
        """Used by the popup to save the settings and remove the popup."""
        self.save_settings()
        self.w.close()
        if self.isVisible():
            self.close()


    def save_settings(self):
        """Function to save the user assigned settings to a file."""
        for key, value in self.settings.items():
            if isinstance(value, Dict):
                for k, _ in value.items():
                    value[k] = self.elements[key].get_subquestion_answer(k)
            else:
                self.settings[key] = self.elements[key].get_answer()
        print("saving settings")
        with open(CURRENT_SETTINGS_FOLDER, "w", encoding="utf-8") as json_file:
            json.dump(self.settings, json_file, indent=4)


    def repair_settings_list(self):
        """Run this to ensure that all settings are being accounted for and if not,
        creates them with default values.
        """
        with open(CURRENT_SETTINGS_FOLDER, encoding="utf-8") as json_file:
            all_settings_questions = json.load(json_file)
        for key, value in all_settings_questions.items():
            if key not in self.elements.keys():
                self.elements[key] = value
        self.__update()


    def handle_default(self):
        """Create a popup to make sure that the user wants to reset to default settings."""
        self.w = PopupWindow("Are you sure you want to reset to default settings?",
                             buttons_text_list=["yes", "no"], 
                             buttons_functions_list=[self.set_default_settings, self.popup_no_save],
                             window_title="Just checking!")
        self.w.show()


    def set_default_settings(self):
        """Set all settings to predetermined values by default_settings.json."""
        with open(DEFAULT_SETTINGS_FOLDER, encoding="utf-8") as json_file:
            all_settings_questions = json.load(json_file)
        for key, value in all_settings_questions.items():
            self.settings[key] = value
        with open(CURRENT_SETTINGS_FOLDER, "w", encoding="utf-8") as json_file:
            json.dump(self.settings, json_file, indent=4)
        self.__update()
        try:
            self.w.close()
        except AttributeError:
            return
