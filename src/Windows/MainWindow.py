from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from utils.StateEnums import StateEnums
from MyToolBar import MyToolBar
from OpeningMenu import OpeningMenu
from MainMenu import MainMenu
from utils.ProcessCourseData import CourseList

class MainWindow(QMainWindow):
    """Class the main window for the application to reside in.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Tracker")
        self.course_list = CourseList("./fake/the.csv")
        self.toolbar = MyToolBar(self.show_new_window)
        
        # Default to None for error checking
        self.container = None
        self.w = None

        self.addToolBar(self.toolbar)
        self.load_opening_menu()
        self.setWindowIcon(QIcon("assets/Temp-Icon.png"))
        self.state = StateEnums.LOADED
    
    def open_application(self):
        """Create the main application to load from the opening window.
        """
        self.toolbar.setVisible(True)
        self.setMinimumSize(QSize(960, 540))
        self.set_container(MainMenu(self.load_opening_menu, self.toolbar, self.course_list))
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)

    def close_application(self):
        """End the window and perform the necessary clean-up.
        """
        self.close()
    
    def load_opening_menu(self):
        """Create opening window to introduce the application.
        """
        self.toolbar.setVisible(False)
        self.setFixedSize(QSize(400, 400))
        self.set_container(OpeningMenu(self.open_application, self.show_new_window))
        self.setCentralWidget(self.container)

    def set_container(self, layout: QVBoxLayout):
        """Alter the container's value so that the system works properly.

        Args:
            layout (QVBoxLayout): The layout for the new window we want to create
        """
        self.container = QWidget()
        exit_button = QPushButton("Exit Program")
        exit_button.setCheckable(True)
        exit_button.clicked.connect(self.close_application)
        layout.addWidget(exit_button)
        self.container.setLayout(layout)

    def show_new_window(self, new_window: QWidget):
        """Switch what type of window is used for the application (opening or main window).

        Args:
            new_window (QWidget): The new window to swap to.
        """
        self.w = new_window
        self.w.show()