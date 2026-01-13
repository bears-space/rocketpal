# type: ignore

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class ResultsWidget(QWidget):
    close_pressed = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
