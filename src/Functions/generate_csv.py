from typing import List
from time import sleep
import asyncio
from PySide2.QtWidgets import QPushButton
from utils.process_course_data import CourseList
from utils.subwindow_widget import SubwindowWidget

class GenerateCSV(SubwindowWidget):
    """Create the window to have the user make a new class."""
    def __init__(self, course_list: CourseList):
        super().__init__(course_list)

        self.complete = False
        save_button = QPushButton("Save Class")
        save_button.setCheckable(True)
        save_button.clicked.connect(self.handle_save)
        self.prompt = save_button

        #Link objects to layout to be displayed
        self.layout.addWidget(self.prompt)
        self.setLayout(self.layout)


    def handle_save(self):
        """Handle the save functionality."""
        self.complete = True


    def is_complete(self):
        """Returns if the CSV has been handled."""
        return self.complete

async def wait_for_completion(gen_csv_window: GenerateCSV, check_interval: float = 1.0):
    """Async function to wait until all attributes of the user_data are filled."""
    while not gen_csv_window.is_complete():
        await asyncio.sleep(check_interval)
