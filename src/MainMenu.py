from PySide2.QtWidgets import QVBoxLayout, QPushButton
from utils.ProcessCourseData import CourseList

class MainMenu(QVBoxLayout):
  def __init__(self, load_opening_menu):
    super().__init__()
    self.button = QPushButton("Exit to App Loader")
    self.button.setCheckable(True)
    self.button.clicked.connect(load_opening_menu)
    self.addWidget(self.button)