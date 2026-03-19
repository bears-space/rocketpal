# type: ignore

import sys

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QDoubleSpinBox,
    QApplication,
)

from bears_flight_simulation.common.common_paths import (
    get_location_entries,
)
from bears_flight_simulation.gui.library_selector_widget import LibrarySelectorWidget
from bears_flight_simulation.gui.cloeseable_window_widget import CloseableWindowWidget


class LocationLibraryEditorWidget(CloseableWindowWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)

        self.selector_widget = LibrarySelectorWidget(
            get_selectable_config_folders=get_location_entries
        )
        self.selector_widget.selection_list_refreshed.connect(
            self._selector_widget_refreshed
        )
        self.layout.addWidget(self.selector_widget)

        self.options_layout_widget = QWidget()
        _options_layout = QFormLayout()
        self.options_layout_widget.setLayout(_options_layout)
        self.layout.addWidget(self.options_layout_widget)

        self.label_latitude = QLabel()
        self.label_latitude.setText("Latitude")
        self.spinbox_latitude = QDoubleSpinBox()
        _options_layout.addRow(self.label_latitude, self.spinbox_latitude)

        self.label_longitude = QLabel()
        self.label_longitude.setText("Longitude")
        self.spinbox_longitude = QDoubleSpinBox()
        _options_layout.addRow(self.label_longitude, self.spinbox_longitude)

        self.label_height = QLabel()
        self.label_height.setText("Height")
        self.spinbox_height = QDoubleSpinBox()
        _options_layout.addRow(self.label_height, self.spinbox_height)

        self.selector_widget.force_refresh()  # NOTE: this is needed because the internal refresh happens before we connect

    def _selector_widget_refreshed(self, empty: bool):
        self.options_layout_widget.setDisabled(empty)


if __name__ == "__main__":
    app = QApplication([])
    widget = LocationLibraryEditorWidget()
    widget.show()
    sys.exit(app.exec())
