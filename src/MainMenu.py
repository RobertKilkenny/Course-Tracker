from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QStackedWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from MyToolBar import MyToolBar
from Functions.AddClass import AddClass

class MainMenu(QVBoxLayout):
  def __init__(self, load_opening_menu, toolbar: MyToolBar):
    super().__init__()
    self.toolbar = toolbar
    self.toolbar.give_stack_shift_func(self.handle_change_subwindow)

    # Create the subwindow to display main content
    self.subwindow_stack = QStackedWidget()
    self.add_class_widget = AddClass()
    self.subwindow_stack.addWidget(self.add_class_widget)

    # self.test_frame: QWidget = make_test_frame()
    # self.subwindow_stack.addWidget(self.test_frame)
    # For testing my subwindow for user input && display
    # self.test_button = QPushButton("Test Frame")
    # self.test_button.setCheckable(True)
    # self.test_button.clicked.connect(self.run_test_frame)
    # self.addWidget(self.test_button)

    # Load back to the home screen!!!
    self.addWidget(self.subwindow_stack)
    self.button = QPushButton("Exit to App Loader")
    self.button.setCheckable(True)
    self.button.clicked.connect(load_opening_menu)
    self.addWidget(self.button)
    test = self.setAlignment(self.subwindow_stack, Qt.AlignTop)
    if not test:
      print("FML")

  def handle_change_subwindow(self, index: int):
    print("changing to index %d" % index, end=" = ")
    match index:
      case 0:
        print("Add Class Window")
        change_to = self.add_class_widget
      case _:
        print("Test Frame Window (Debug Only)")
        change_to = self.test_frame
    self.subwindow_stack.setCurrentWidget(change_to)
  
  def run_test_frame(self):
    self.handle_change_subwindow(-1)

def make_test_frame() -> QWidget:
  newLayout = QVBoxLayout()
  logo = QLabel()
  logo.setPixmap(QPixmap("assets/Temp-Icon.png"))
  logo.setScaledContents(True)
  newLayout.addWidget(logo)
  test_frame = QWidget()
  test_frame.setLayout(newLayout)
  return test_frame