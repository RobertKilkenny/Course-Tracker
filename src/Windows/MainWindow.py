from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from utils.StateEnums import StateEnums
from MyToolBar import MyToolBar
from OpeningMenu import OpeningMenu
from MainMenu import MainMenu
from utils.ProcessCourseData import CourseList

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Course Tracker")
    self.course_list = CourseList("./fake/the.csv")
    self.toolbar = MyToolBar(self.show_new_window, self.course_list)

    self.addToolBar(self.toolbar)
    self.load_opening_menu()
    self.setWindowIcon(QIcon("assets/Temp-Icon.png"))
    self.state = StateEnums.LOADED
  
  def open_application(self):
    self.toolbar.setVisible(True)
    self.setMinimumSize(QSize(960, 540))
    self.set_container(MainMenu(self.load_opening_menu, self.toolbar))
    self.setCentralWidget(self.container)

  def close_application(self):
    self.close()
  
  def load_opening_menu(self):
    self.toolbar.setVisible(False)
    self.setFixedSize(QSize(400, 400))
    self.set_container(OpeningMenu(self.open_application, self.show_new_window))
    self.setCentralWidget(self.container)

  def set_container(self, layout: QVBoxLayout):
    self.container = QWidget()
    exit_button = QPushButton("Exit Program")
    exit_button.setCheckable(True)
    exit_button.clicked.connect(self.close_application)
    layout.addWidget(exit_button)
    self.container.setLayout(layout)

  def show_new_window(self, new_window: QWidget):
    self.w = new_window
    self.w.show()