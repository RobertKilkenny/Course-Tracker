from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QLineEdit, QSizePolicy
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator, QFont, QFontMetrics

class QuestionBlock(QWidget):
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