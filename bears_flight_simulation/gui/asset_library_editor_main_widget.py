# type: ignore

import sys
from PySide6.QtCore import QMargins
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QApplication,
    QPushButton,
)

from bears_flight_simulation.gui.location_library_editor_widget import (
    LocationLibraryEditorWidget,
)
from bears_flight_simulation.gui.cloeseable_window_widget import CloseableWindowWidget


class AssetLibraryEditorMainWidget(CloseableWindowWidget):
    location_library_editor_widget: LocationLibraryEditorWidget | None

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.location_library_editor_widget = None

        self.layout = QVBoxLayout(self)

        _spacer_top = QSpacerItem(
            20,
            40,
            hData=QSizePolicy.Policy.Preferred,
            vData=QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_top)

        self.horizontal_centering_widget = QWidget()
        _horizontal_centering_layout = QHBoxLayout()
        _horizontal_centering_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.horizontal_centering_widget)
        self.horizontal_centering_widget.setLayout(_horizontal_centering_layout)

        self.main_layout_widget = QWidget()
        _main_layout = QVBoxLayout()
        _main_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.main_layout_widget.setMaximumWidth(1024)
        _horizontal_centering_layout.addWidget(self.main_layout_widget)
        self.main_layout_widget.setLayout(_main_layout)

        self.button_locations = QPushButton(text="Location Library")
        self.button_locations.clicked.connect(self._button_locations_pressed)
        _main_layout.addWidget(self.button_locations)

        self.button_motors = QPushButton(text="Motor Library")
        self.button_motors.clicked.connect(self._button_motors_pressed)
        _main_layout.addWidget(self.button_motors)

        self.button_parachutes = QPushButton(text="Parachute Library")
        self.button_parachutes.clicked.connect(self._button_parachutes_pressed)
        _main_layout.addWidget(self.button_parachutes)

        self.button_finish = QPushButton(text="Finish")
        self.button_finish.clicked.connect(self._button_finish_pressed)
        _main_layout.addWidget(self.button_finish)

        _spacer_bottom = QSpacerItem(
            20,
            40,
            hData=QSizePolicy.Policy.Preferred,
            vData=QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_bottom)

    def _button_locations_pressed(self):
        # Open location library editor window if not already open
        if (
            self.location_library_editor_widget is None
            or self.location_library_editor_widget not in self._children_to_close
        ):
            self.location_library_editor_widget = LocationLibraryEditorWidget()
            self.add_child_to_close(self.location_library_editor_widget)
            self.location_library_editor_widget.resize(640, 360)
            self.location_library_editor_widget.show()

    def _button_motors_pressed(self):
        pass

    def _button_parachutes_pressed(self):
        pass

    def _button_finish_pressed(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = AssetLibraryEditorMainWidget()
    widget.show()
    sys.exit(app.exec())
