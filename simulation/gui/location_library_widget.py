# type: ignore

import sys

from PySide6 import QtWidgets

from library_selector_widget import LibrarySelectorWidget


class LocationLibraryWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.selector_widget = LibrarySelectorWidget()
        self.layout.addWidget(self.selector_widget)

        self.options_layout_widget = QtWidgets.QWidget()
        _options_layout = QtWidgets.QFormLayout()
        self.options_layout_widget.setLayout(_options_layout)
        self.layout.addWidget(self.options_layout_widget)

        self.label_latitude = QtWidgets.QLabel()
        self.label_latitude.setText("Latitude")
        self.spinbox_latitude = QtWidgets.QDoubleSpinBox()
        _options_layout.addRow(self.label_latitude, self.spinbox_latitude)

        self.label_longitude = QtWidgets.QLabel()
        self.label_longitude.setText("Longitude")
        self.spinbox_longitude = QtWidgets.QDoubleSpinBox()
        _options_layout.addRow(self.label_longitude, self.spinbox_longitude)

        self.label_height = QtWidgets.QLabel()
        self.label_height.setText("Height")
        self.spinbox_height = QtWidgets.QDoubleSpinBox()
        _options_layout.addRow(self.label_height, self.spinbox_height)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = LocationLibraryWidget()
    widget.show()
    sys.exit(app.exec())
