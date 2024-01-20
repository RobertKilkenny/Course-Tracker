from PySide2.QtWidgets import QVBoxLayout, QLineEdit
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator

class AddClass(QVBoxLayout):
  def __init__(self):
    super().__init__()
    self.input_code = QLineEdit()
    self.input_code.setPlaceholderText("Put course code [ex. AAA0000]")
    input_reg = QRegExp("[A-Z]{3}[0-9]{4}")
    self.input_code.setValidator(QRegExpValidator(input_reg))
    self.input_credits = QLineEdit()
    self.input_credits.setPlaceholderText("How many credits is it worth?")
    input_reg = QRegExp("[0-9]")
    self.input_credits.setValidator(QRegExpValidator(input_reg))
    self.addWidget(self.input_code)
    self.addWidget(self.input_credits)