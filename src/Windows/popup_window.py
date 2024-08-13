from typing import List, Callable, Optional
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide2.QtCore import QSize

class PopupWindow(QWidget):
    """Generic window to popup with a specific message and can 
    run a function if needed."""
    def __init__(self, message: str, buttons_text_list: List[str],
                 buttons_functions_list: Optional[List[Callable]] = None,
                 window_title: str = "ERROR", function_on_close: Optional[Callable] = None):
        super().__init__()
        self.setMinimumSize(QSize(300, 50))
        self.setWindowTitle(window_title)
        self.closer = function_on_close
        layout = QVBoxLayout()
        message = QLabel(message)
        self.elements = []
        for i, text in enumerate(buttons_text_list):
            button = QPushButton(text)
            if len(buttons_functions_list) != len(buttons_text_list):
                button.clicked.connect(buttons_functions_list)
            else:
                button.clicked.connect(buttons_functions_list[i])
            self.elements.append(button)

        layout.addWidget(message)
        for element in self.elements:
            layout.addWidget(element)
        self.setLayout(layout)


    def closeEvent(self, event: QCloseEvent) -> None:
        """Adding to the default closeEvent for the window."""
        if self.closer is not None:
            self.closer()
        return super().closeEvent(event)
