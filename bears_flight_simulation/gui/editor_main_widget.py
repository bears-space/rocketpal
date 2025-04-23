# type: ignore

import sys
from PySide6 import QtCore, QtWidgets


class EditorMainWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        _spacer_top = QtWidgets.QSpacerItem(
            20,
            40,
            hData=QtWidgets.QSizePolicy.Policy.Preferred,
            vData=QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_top)

        self.horizontal_centering_widget = QtWidgets.QWidget()
        _horizontal_centering_layout = QtWidgets.QHBoxLayout()
        _horizontal_centering_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.horizontal_centering_widget)
        self.horizontal_centering_widget.setLayout(_horizontal_centering_layout)

        self.main_layout_widget = QtWidgets.QWidget()
        _main_layout = QtWidgets.QVBoxLayout()
        _main_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.main_layout_widget.setMaximumWidth(1024)
        _horizontal_centering_layout.addWidget(self.main_layout_widget)
        self.main_layout_widget.setLayout(_main_layout)

        # TODO content

        # locations
        # motors
        # parachutes
        # TODO the above are selectors from the respective "asset libraries", for which we might want separate editors, although creating these by hand might be fine...

        self.button_finish = QtWidgets.QPushButton(text="Finish")
        self.button_finish.clicked.connect(self._button_finish_pressed)
        _main_layout.addWidget(self.button_finish)

        _spacer_bottom = QtWidgets.QSpacerItem(
            20,
            40,
            hData=QtWidgets.QSizePolicy.Policy.Preferred,
            vData=QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_bottom)

    def _button_finish_pressed(self):
        # TODO Close widget / dialog / window / whatever idk
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = EditorMainWidget()
    widget.show()
    sys.exit(app.exec())
