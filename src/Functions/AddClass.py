from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator, QFont, QFontMetrics

class AddClass(QWidget):
  def __init__(self):
    super().__init__()
    self.layout = QVBoxLayout()
    
    self.question_dict = {}
    self.question_dict["course-code"] = QuestionBlock(question="Input the new course code",
                                    placeholder="Put course code [ex. AAA0000]",
                                    regex=QRegExp("[A-Z]{3}[0-9]{4}"))
    
    self.question_dict["course-credits"] = QuestionBlock(question="Input the credit for the course",
                                    placeholder="How many credits is it worth?",
                                    regex=QRegExp("[0-9]"))
    
    for value in self.question_dict.values():
      self.layout.addWidget(value)
    saveButton = QPushButton("Save Class")
    saveButton.setCheckable(True)
    self.layout.addWidget(saveButton)
    saveButton.clicked.connect(self.handle_save)
    self.setLayout(self.layout)
  
  def validate_complete(self)->bool:
    print("Test if course code (%s) is 7 characters long" % self.question_dict["course-code"].input.text())
    complete = len(self.question_dict["course-code"].input.text()) == 7
    print("Test if course code (%s) is a valid credit number" % self.question_dict["course-credits"].input.text())
    complete = complete and int(self.question_dict["course-credits"].input.text()) > 0
    return complete
  
  def handle_save(self):
    isComplete = self.validate_complete()
    if isComplete:
      print("This is a valid class!")
    else:
      print("Invalid class!")

def get_min_size(text: QLineEdit) -> int:
  font_metrics = QFontMetrics(text.font())
  max_width = font_metrics.width(text.text())
  return max_width

def create_title(text: str, font_size: int = 14) -> QLabel:
  text = QLabel(text)
  text.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
  font = QFont()
  font.setPointSize(font_size)
  text.setFont(font)
  return text


class QuestionBlock(QWidget):
  def __init__(self, question: str, question_size: int = 14, placeholder:str = None, regex: QRegExp = None) -> QWidget:
    super().__init__()
    layout = QVBoxLayout()
    self.text = create_title(question, question_size)
    layout.addWidget(self.text)
    self.input = QLineEdit()
    if placeholder != None:
      self.input.setPlaceholderText(placeholder)
    if regex != None:
      self.input.setValidator(QRegExpValidator(regex))
    self.input.setMaximumWidth(get_min_size(self.text))
    layout.addWidget(self.input)
    self.setLayout(layout)
    
  