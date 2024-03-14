from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt

class PopupWindow(QWidget):
    """Generic window to popup with a specific message and can 
    run a function if needed."""
    def __init__(self, message: str, button_text: str, function = None, window_title: str = "ERROR"):
        super().__init__()
        self.setMinimumSize(QSize(300, 50))
        self.setWindowTitle(window_title)
        self.run_this_function = function
        layout = QVBoxLayout()
        message = QLabel(message)
        button = QPushButton(button_text)
        button.clicked.connect(function)
        # layout.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        layout.addWidget(message)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.run_this_function()
        return super().closeEvent(event)
