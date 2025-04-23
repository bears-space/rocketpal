# type: ignore

from PySide6 import QtCore, QtWidgets


class ResultsWidget(QtWidgets.QWidget):
    close_pressed = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
