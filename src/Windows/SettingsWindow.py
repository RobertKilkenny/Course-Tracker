import json
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide2.QtCore import QSize, Qt
from Windows.PopupWindow import PopupWindow
from typing import Dict, List
from utils.QuestionBlock import NestedQuestionBlock, SimpleQuestionBlock

class SettingsWindow(QWidget):
    """Secondary window to create a json file.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Settings")
        self.setMinimumSize(QSize(300, 600))
        self.settings = {}
        
        with open('./app-data/app_settings.json') as json_file:
            self.settings = json.load(json_file)
        print(self.settings)
        
        layout = QVBoxLayout()
        self.elements: Dict[str, QWidget] = {}
        
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
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        save_n_close_button = QPushButton("Save and Close")
        save_n_close_button.clicked.connect(self.close_n_save)
        layout.addWidget(save_n_close_button)
        
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setLayout(layout)

    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.w = PopupWindow("Do you want to save these changes?", buttons_text_list=["yes", "no"], 
                             buttons_functions_list=[self.popup_save, self.popup_no_save],
                             window_title="Before you go!!")
        self.w.show()
        return super().closeEvent(event)


    def close_n_save(self):
        self.save_settings()
        self.close()


    def popup_save(self):
        self.save_settings()
        self.w.close()
        if self.isVisible():
            self.close()
    
    def popup_no_save(self):
        self.w.close()

    def save_settings(self):
        """Function to save the user assigned settings to a file.
        """
        print("saving settings")
        with open(self.settings["Setting File Location"], "w", encoding="utf-8") as json_file:
            json.dump(self.settings, json_file, indent=4)


    def set_default_settings(self):
        """Set all settings to predetermined values by myself."""