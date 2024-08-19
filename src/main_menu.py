from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel
from PySide2.QtWidgets import QStackedWidget, QSizePolicy, QLayout
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QFont
from my_toolbar import MyToolBar
from Functions.add_class import AddClass
from Functions.edit_class import EditClass
from Functions.generate_csv import GenerateCSV
from utils.process_course_data import CourseList

class MainMenu(QVBoxLayout):
    """Make the layout"""
    def __init__(self, load_opening_menu, toolbar: MyToolBar, course_list: CourseList):
        super().__init__()
        self.setSizeConstraint(QLayout.SetNoConstraint)
        self.toolbar = toolbar
        self.toolbar.give_stack_shift_func(self.handle_change_subwindow)

        # Create the subwindow to display main content
        self.subwindow_stack = QStackedWidget()
        self.subwindow_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.opening_widget = make_opener()
        self.add_class_widget = AddClass(course_list= course_list)
        self.add_class_widget.setParent(self)
        self.edit_class_widget = EditClass(course_list= course_list)
        self.edit_class_widget.setParent(self)
        self.gen_csv_widget = GenerateCSV(course_list= course_list)
        self.gen_csv_widget.setParent(self)
        self.subwindow_stack.addWidget(self.opening_widget)
        self.subwindow_stack.addWidget(self.add_class_widget)
        self.subwindow_stack.addWidget(self.edit_class_widget)
        self.subwindow_stack.addWidget(self.gen_csv_widget)

        # Load back to the home screen!!!
        self.addWidget(self.subwindow_stack)
        self.button = QPushButton("Exit to App Loader")
        self.button.setCheckable(True)
        self.button.clicked.connect(load_opening_menu)
        self.addWidget(self.button)
        test = self.setAlignment(self.subwindow_stack, Qt.AlignTop)
        if not test:
            print("Well, that sucks lol")
        if course_list.csv_file_path is None:
            self.handle_change_subwindow(-1)


    def grab_generated_csv(self):
        """Called by the GenerateCSV Object when it is ready to pull
        the data and make the backup dataframe."""
        self.gen_csv_widget.get_csv_path()


    def handle_change_subwindow(self, index: int):
        """Change the subwindow via an index reference
        * -1 = Gen CSV Window
        *  0 = Add Class Window
        *  1 = Edit Class Window
        Anything else is the debug window"""
        print(f"changing to index {index}", end=" = ")
        match index:
            case -1:
                print("Generate CSV Window")
                change_to = self.gen_csv_widget
            case 0:
                print("Add Class Window")
                change_to = self.add_class_widget
            case 1:
                print("Edit Class Window")
                change_to = self.edit_class_widget
            case _:
                print("Test Frame Window (Debug Only)")
                change_to = self.test_frame
        self.subwindow_stack.setCurrentWidget(change_to)


    def run_test_frame(self):
        """Run the test from to see if subwindow changes work."""
        self.handle_change_subwindow(1000)


def make_test_frame() -> QWidget:
    """Create an testing message to show when it is opened."""
    new_layout = QVBoxLayout()
    logo = QLabel()
    logo.setPixmap(QPixmap("assets/Temp-Icon.png"))
    logo.setScaledContents(True)
    new_layout.addWidget(logo)
    test_frame = QWidget()
    test_frame.setLayout(new_layout)
    return test_frame


def make_opener() -> QWidget:
    """Create an opening message to show when it is opened."""
    layout = QVBoxLayout()
    text = QLabel("Welcome to my Course Tracker! Pick a tab to get started.")
    font = QFont()
    font.setPointSize(20)
    text.setFont(font)
    layout.addWidget(text)
    layout.setAlignment(Qt.AlignHCenter)
    result = QWidget(layout= layout)
    result.setStyleSheet("background: lightgray;")
    result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return result
