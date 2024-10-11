from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel, QWidget, QHBoxLayout, QSizePolicy
from PySide2.QtCore import Qt


class LabelDetail(QWidget):
    """Object to have two parts, a bolded label next to a regular details"""
    def __init__(self, label:str, data: str = "", font_size: int = 20):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.label = QLabel(str(label))
        self.label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.label.setAlignment(Qt.AlignRight)
        label_font = QFont()
        label_font.setPointSize(font_size)
        label_font.setBold(True)
        self.label.setFont(label_font)
        self.layout.addWidget(self.label)

        self.detail = QLabel(str(data))
        self.detail.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.detail.setAlignment(Qt.AlignLeft)
        label_font = QFont()
        label_font.setPointSize(font_size)
        label_font.setBold(False)
        self.detail.setFont(label_font)
        self.layout.addWidget(self.detail)
        self.setLayout(self.layout)

    def set_label(self, label:str):
        """Change the bold part of the label"""
        self.label.setText(label)


    def set_detail(self, detail:str):
        """Change the non-bold part of the label"""
        self.detail.setText(detail)
