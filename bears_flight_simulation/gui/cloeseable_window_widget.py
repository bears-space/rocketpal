import typing as t
from PySide6 import QtCore, QtWidgets


class CloseableWindowWidget(QtWidgets.QWidget):
    close_pressed = QtCore.Signal(t.Any)  # type: ignore
    _children_to_close: list["CloseableWindowWidget"]

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._children_to_close = []

    def closeEvent(self, event):
        # Close children
        for child in self._children_to_close:
            child.close()

        # Tell possible parents that we are about to close this window
        self.close_pressed.emit(self)

        # Close this window
        event.accept()

    def add_child_to_close(self, child: "CloseableWindowWidget"):
        self._children_to_close.append(child)
        child.close_pressed.connect(self._child_close_pressed)
        self.setDisabled(True)

    def _child_close_pressed(self, child):
        self._children_to_close.remove(child)
        if len(self._children_to_close) == 0:
            self.setDisabled(False)
