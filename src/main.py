"""Create the application for the Course Tracker"""
import sys
import os
from PySide2.QtWidgets import QApplication
from Windows.MainWindow import MainWindow


def main():
    """"Function to create application"""
    if not os.path.exists("./app-data"):
        os.makedirs("./app-data")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    