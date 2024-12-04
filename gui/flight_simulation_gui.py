#!/usr/bin/env python3
# type: ignore

import logging

import sys
import random
from PySide6 import QtCore, QtWidgets


class HelloWorldWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World!", alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(f"Hello World! Random number is {random.randint(0, 1000)}.")


if __name__ == "__main__":
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Prepare application
    app = QtWidgets.QApplication([])
    app.setApplicationName("FSG - Flight Simulation GUI")

    # Hello world test
    widget = HelloWorldWidget()
    widget.resize(1280, 720)
    widget.show()

    # Enter GUI main loop
    sys.exit(app.exec())
