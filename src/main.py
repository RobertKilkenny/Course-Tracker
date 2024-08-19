"""Create the application for the Course Tracker"""
import sys
import os
import json
from PySide2.QtWidgets import QApplication
from Windows.main_window import MainWindow


def main():
    """"Function to create application"""
    app = QApplication(sys.argv)
    window = None
    data = None
    if not os.path.exists("./app-data"):
        os.makedirs("./app-data")
    elif os.path.exists("./app-data/data.json"):
        with open('app-data/data.json', "r", encoding="utf-8") as f:
            data = json.load(f)

    if data is None:
        data = {"Class Data Path": "./class.csv"}
    window = MainWindow(data)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
