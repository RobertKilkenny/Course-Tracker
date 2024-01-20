from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QColor, QPalette
from MyToolBar import MyToolBar

class MainMenu(QVBoxLayout):
  def __init__(self, load_opening_menu, toolbar: MyToolBar):
    super().__init__()
    self.toolbar = toolbar
    self.toolbar.activate_function(self.set_frame_layout)
    self.menu_widget = QWidget()
    self.menu_widget.setLayout(QVBoxLayout())
    self.menu_widget.setMaximumSize(QSize(500, 200))
    # self.menu_widget.setSizeIncrement(250, 100)
    self.menu_widget.setAutoFillBackground(True)
    palette = self.menu_widget.palette()
    palette.setColor(QPalette.Window, QColor("Gray"))
    self.menu_widget.setPalette(palette)
    self.test_button = QPushButton("Test Frame")
    self.test_button.setCheckable(True)
    self.test_button.clicked.connect(self.test_frame)
    self.button = QPushButton("Exit to App Loader")
    self.button.setCheckable(True)
    self.button.clicked.connect(load_opening_menu)
    self.addWidget(self.menu_widget)
    self.addWidget(self.test_button)
    self.addWidget(self.button)
    test = self.setAlignment(self.menu_widget, Qt.AlignCenter)
    if not test:
      print("FML")

  def set_frame_layout(self):
    self.menu_widget.setLayout(self.toolbar.frame_layout)

  def test_frame(self):
    newLayout = QVBoxLayout()
    logo = QLabel()
    logo.setPixmap(QPixmap("assets/Temp-Icon.png"))
    logo.setScaledContents(True)
    newLayout.addWidget(logo)
    self.menu_widget.setLayout(newLayout)