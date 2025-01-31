# type: ignore

import sys

from PySide6 import QtWidgets

from common.common_paths import (
    get_location_config_folders,
)
from gui.library_selector_widget import LibrarySelectorWidget
from gui.cloeseable_window_widget import CloseableWindowWidget


class LocationLibraryEditorWidget(CloseableWindowWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.selector_widget = LibrarySelectorWidget(
            get_selectable_config_folders=get_location_config_folders
        )
        self.selector_widget.selection_list_refreshed.connect(
            self._selector_widget_refreshed
        )
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

        self.selector_widget.force_refresh()  # NOTE: this is needed because the internal refresh happens before we connect

    def _selector_widget_refreshed(self, empty: bool):
        self.options_layout_widget.setDisabled(empty)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = LocationLibraryEditorWidget()
    widget.show()
    sys.exit(app.exec())
