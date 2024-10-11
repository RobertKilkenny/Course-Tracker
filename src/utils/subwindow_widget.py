from PySide2.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel
from PySide2.QtGui import QFont
from utils.app_manager import AppManager


class SubwindowWidget(QWidget):
    def __init__(self, app_manager: AppManager, label: str):
        super().__init__()
        self.app_manager = app_manager
        self.layout = QVBoxLayout()
        self.label = QLabel(label)
        self.label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
