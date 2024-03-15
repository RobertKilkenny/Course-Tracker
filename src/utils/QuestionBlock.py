from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QLineEdit, QSizePolicy
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator, QFont, QFontMetrics
from typing import List, Dict

class SimpleQuestionBlock(QWidget):
    """"A default construction for a question and answer which 
    can limit user input for the lineEdit using Regex!"""
    def __init__(self, question: str, question_size: int = 14, placeholder:str = None, 
                 regex: QRegExp = None) -> QWidget:
        super().__init__()
        layout = QVBoxLayout()
        self.text = create_title(question, question_size)
        layout.addWidget(self.text)
        self.input = QLineEdit()
        if placeholder is not None:
            self.input.setPlaceholderText(placeholder)
        if regex is not None:
            self.input.setValidator(QRegExpValidator(regex))
            self.input.setMaximumWidth(get_min_size(self.text))
        layout.addWidget(self.input)
        self.setLayout(layout)


    def set_user_access(self, can_edit: bool, should_delete_text: bool = False):
        """Set Question Block to either allow user input or not allow changes."""
        self.input.setEnabled(can_edit)
        if should_delete_text and not can_edit:
            self.input.setText("")


    def change_line_edit_text(self, new_text: str):
        """Change the text value for the answer part of the Question Block."""
        self.input.setText(new_text)


    def change_line_edit_placeholder(self, new_text: str):
        """Change the placeholder text for the answer part of the Question Block."""
        self.input.setPlaceholderText(new_text)


class NestedQuestionBlock(QWidget):
    """"A variation of the Simple Question Block which allows for a multiple QLineEdits for a single question"""
    def __init__(self, title: str, question_list: List[str], regex_list: List[QRegExp] = None, placeholder_list = None,
                 title_size: int = 14, sub_title_size: int = 10) -> QWidget:
        super().__init__()
        layout = QVBoxLayout()
        self.text = create_title(title, title_size)
        layout.addWidget(self.text)
        self.input = QLineEdit()
        
        self.elements: Dict[str, SimpleQuestionBlock] = {}
        for i in range(len(question_list)):    
            if regex_list is None or len(question_list) != len(regex_list):
                regex = None
            else:
                regex = regex_list[i]
            if placeholder_list is None or len(question_list) != len(placeholder_list):
                placeholder = None
            else:
                placeholder = placeholder_list[i]
                
            self.elements[question_list[i]] = SimpleQuestionBlock(question_list[i], regex=regex,
                                                                  placeholder=placeholder,
                                                                  question_size=sub_title_size)
            layout.addWidget(self.elements[question_list[i]])
        self.setLayout(layout)


    def set_user_access(self, can_edit: bool, should_delete_text: bool = False):
        """Set each Question Block to either allow user input or not allow changes."""
        for question in self.elements.values():
            question.input.setEnabled(can_edit)
            if should_delete_text and not can_edit:
                question.input.setText("")


    def change_multiple_line_edit_text(self, keys: List[str], values: List[str]):
        """Change the text value for each of the answer part of the Question Block using the keys given!"""
        if len(keys) != len(values):
            return False
        for i in range(len(keys)):
            value = str(values[i])
            self.elements[keys[i]].input.setText(value)
        return True


def get_min_size(text: QLineEdit) -> int:
    """"Given a QLineEdit object, return the minimum length to be that size."""
    font_metrics = QFontMetrics(text.font())
    max_width = font_metrics.width(text.text())
    return max_width


def create_title(text: str, font_size: int = 14) -> QLabel:
    """"Creating a QLabel given the text and size wanted."""
    text = QLabel(text)
    text.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    font = QFont()
    font.setPointSize(font_size)
    text.setFont(font)
    return text

def get_min_size(text: QLineEdit) -> int:
    """"Given a QLineEdit object, return the minimum length to be that size."""
    font_metrics = QFontMetrics(text.font())
    max_width = font_metrics.width(text.text())
    return max_width


def create_title(text: str, font_size: int = 14) -> QLabel:
    """"Creating a QLabel given the text and size wanted."""
    text = QLabel(text)
    text.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    font = QFont()
    font.setPointSize(font_size)
    text.setFont(font)
    return text
