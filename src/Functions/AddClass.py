from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator, QFont, QFontMetrics

class AddClass(QWidget):
  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout()
    
    text = create_title("Input the new course code")
    self.layout.addWidget(text)
    self.input_code = QLineEdit()
    self.input_code.setPlaceholderText("Put course code [ex. AAA0000]")
    self.input_code.setMaximumWidth(get_min_size(text=text))
    input_reg = QRegExp("[A-Z]{3}[0-9]{4}")
    self.input_code.setValidator(QRegExpValidator(input_reg))
    self.layout.addWidget(self.input_code)

    text = create_title("Input the credit for the course")
    self.layout.addWidget(text)
    self.input_credits = QLineEdit()
    self.input_credits.setPlaceholderText("How many credits is it worth?")
    input_reg = QRegExp("[0-9]")
    self.input_credits.setValidator(QRegExpValidator(input_reg))
    self.layout.addWidget(self.input_credits)

    self.setLayout(self.layout)

def get_min_size(text: QLineEdit) -> int:
  font_metrics = QFontMetrics(text.font())
  max_width = font_metrics.width(text.text())
  return max_width

def create_title(text: str) -> QLabel:
  text = QLabel(text)
  text.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
  font = QFont()
  font.setPointSize(14)
  text.setFont(font)
  return text

def create_question(question: str, placeholder:str = ""):
  pass