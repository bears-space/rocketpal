# type: ignore

import sys
from PySide6 import QtCore, QtWidgets

# from simulation.core.library import Library
# from simulation.core.library_entry import LibraryEntry


class LibrarySelectorWidget(QtWidgets.QWidget):
    button_new_pressed = QtCore.Signal()
    button_delete_pressed = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.selection_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.selection_list)

        self.button_layout_widget = QtWidgets.QWidget()
        _button_layout = QtWidgets.QHBoxLayout()
        self.button_layout_widget.setLayout(_button_layout)
        self.layout.addWidget(self.button_layout_widget)

        self.button_delete = QtWidgets.QPushButton(text="Delete")
        self.button_delete.clicked.connect(self._button_delete_pressed)
        _button_layout.addWidget(self.button_delete)

        self.button_new = QtWidgets.QPushButton(text="New")
        self.button_new.clicked.connect(self._button_new_pressed)
        _button_layout.addWidget(self.button_new)

    def _button_new_pressed(self):
        self.button_new_pressed.emit()

    def _button_delete_pressed(self):
        self.button_delete_pressed.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = LibrarySelectorWidget()
    widget.show()
    sys.exit(app.exec())
