from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator, QFont, QFontMetrics
from utils.ProcessCourseData import CourseList
from typing import List

class AddClass(QWidget):
  def __init__(self, course_list: CourseList):
    super().__init__()
    self.layout = QVBoxLayout()
    self.course_list = course_list

    self.question_dict = {}
    self.question_dict["course-code"] = QuestionBlock(question="Input the new course code",
                                    placeholder="Put course code [ex. AAA0000]",
                                    regex=QRegExp("[A-Z]{3}[0-9]{4}"))
    
    self.question_dict["course-name"] = QuestionBlock(question="What is the name of the course",
                                    placeholder="Must be at least 3 characters long",
                                    regex=QRegExp("^[\w\s\-]+$"))

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
  
  
  def is_complete_input(self) -> bool:
    error_list = self.validate_complete()
    if not len(error_list) == 0:
      print(read_user_errors(error_list))


  def validate_complete(self)-> List[int]:
    report = []
    print("Running tests for validation, Each * means a failure")
    print("Test if course code (%s) is 7 characters long" % self.question_dict["course-code"].input.text(), end="")
    if not len(self.question_dict["course-code"].input.text()) == 7:
      report.append(0)
      print(" *", end ="")
    print("\nTest if course name (%s) is at least 3 characters long" % self.question_dict["course-name"].input.text(),  end=" ")
    if not len(self.question_dict["course-name"].input.text()) > 2:
      report.append(1)
      print(" *", end ="")
    print("\nTest if course credits (%s) has a value in the box" % self.question_dict["course-credits"].input.text(),  end=" ")
    if not len(self.question_dict["course-credits"].input.text()) == 1:
      report.append(2)
      print(" *", end ="")
    else: 
      print("\nTest if course credits (%s) is a valid credit number" % self.question_dict["course-credits"].input.text(),  end=" ")
      if not int(self.question_dict["course-credits"].input.text()) > 0:
        report.append(3)
        print(" *", end ="")
    print("\nTest if course code (%s) already exists" % self.question_dict["course-code"].input.text(),  end=" ")
    if self.course_list.does_class_exist(self.question_dict["course-code"].input.text()):
      report.append(4)
      print(" *", end ="")
    print("\n")
    return report
  

  def handle_save(self):
    isComplete = self.is_complete_input()
    if isComplete:
      print("This is a valid class!")
    else:
      print("Invalid class!")


def read_user_errors(list: List[int]) -> str:
  report = ""
  for number in list:
    match number:
      case 0:
        report += "- Course Code is not complete"
      case 1: 
        report += "- Course name is not long enough"
      case 2:
        report += "- Course credits were not given"
      case 3:
        report += "- Course credits are not greater than 0"
      case 4:
        report += "- Course code already exists"
      case _:
        report += "- Create class tester gave invalid error!!!!"
    report += "\n"
  return report


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