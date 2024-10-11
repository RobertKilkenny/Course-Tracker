from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPalette, QColor
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from my_toolbar import MyToolBar
from opening_menu import OpeningMenu
from main_menu import MainMenu
from utils.app_manager import AppManager
from utils.process_course_data import CourseList
from utils.state_enums import StateEnums
from utils.grading_settings import GradingSettings

class MainWindow(QMainWindow):
    """Class the main window for the application to reside in.
    """
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Course Tracker")
        self.app_data = data
        try:
            print(self.app_data["Class Data Path"])
            self.course_list = CourseList(self.app_data["Class Data Path"])
        except (ValueError, FileNotFoundError) as err:
            print(f'Course List could not be made because of:\n{err}')
            self.course_list = CourseList()
        grading_settings = GradingSettings(data, self)
        self.app_manager = AppManager(self.course_list, grading_settings, self)
        self.toolbar = MyToolBar(self.app_manager)

        #Connect events to the proper functions
        self.app_manager.connect_open_window_request(self.show_new_window)
        self.app_manager.connect_close_app_request(self.close_application)

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
        self.setMinimumSize(QSize(1200, 600))
        self.set_container(MainMenu(self.load_opening_menu,
                                    self.toolbar,
                                    self.course_list,
                                    self.app_manager,
                                    self.app_data))
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)


    def close_application(self):
        """End the window and perform the necessary clean-up.
        """
        self.app_manager.save_changes()
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
