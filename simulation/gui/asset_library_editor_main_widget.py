# type: ignore

import sys
from PySide6 import QtCore, QtWidgets

from gui.location_library_editor_widget import LocationLibraryEditorWidget


class AssetLibraryEditorMainWidget(QtWidgets.QWidget):
    close_pressed = QtCore.Signal()

    location_library_editor_widget: LocationLibraryEditorWidget | None = None

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

        self.button_locations = QtWidgets.QPushButton(text="Location Library")
        self.button_locations.clicked.connect(self._button_locations_pressed)
        _main_layout.addWidget(self.button_locations)

        self.button_motors = QtWidgets.QPushButton(text="Motor Library")
        self.button_motors.clicked.connect(self._button_motors_pressed)
        _main_layout.addWidget(self.button_motors)

        self.button_parachutes = QtWidgets.QPushButton(text="Parachute Library")
        self.button_parachutes.clicked.connect(self._button_parachutes_pressed)
        _main_layout.addWidget(self.button_parachutes)

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

    def closeEvent(self, event):
        self.close_pressed.emit()
        event.accept()

    def _button_locations_pressed(self):
        # Open location library editor window if not already open
        if self.location_library_editor_widget is None:
            self.setDisabled(True)
            self.location_library_editor_widget = LocationLibraryEditorWidget()
            self.location_library_editor_widget.close_pressed.connect(
                self._location_library_editor_widget_close_pressed
            )
            self.location_library_editor_widget.resize(640, 360)
            self.location_library_editor_widget.show()

    def _location_library_editor_widget_close_pressed(self):
        self.location_library_editor_widget = None
        self.setDisabled(False)

    def _button_motors_pressed(self):
        pass

    def _button_parachutes_pressed(self):
        pass

    def _button_finish_pressed(self):
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = AssetLibraryEditorMainWidget()
    widget.show()
    sys.exit(app.exec())
