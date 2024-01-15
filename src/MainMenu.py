from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtGui import QPixmap

class MainMenu(QVBoxLayout):
  def __init__(self, load_opening_menu):
    super().__init__()
    self.menu_widget = QWidget()
    self.test_button = QPushButton("Test Frame")
    self.test_button.setCheckable(True)
    self.test_button.clicked.connect(self.test_frame)
    self.button = QPushButton("Exit to App Loader")
    self.button.setCheckable(True)
    self.button.clicked.connect(load_opening_menu)
    self.addWidget(self.menu_widget)
    self.addWidget(self.test_button)
    self.addWidget(self.button)

  def set_frame_layout(self, layout):
    self.menu_widget.setLayout(layout)

  def test_frame(self):
    newLayout = QVBoxLayout()
    logo = QLabel()
    logo.setPixmap(QPixmap("assets/Temp-Icon.png"))
    logo.setScaledContents(True)
    newLayout.addWidget(logo)
    self.set_frame_layout(newLayout)