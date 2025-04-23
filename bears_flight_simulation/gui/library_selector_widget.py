# type: ignore

from collections.abc import Callable
import sys
from PySide6 import QtCore, QtWidgets

# from simulation.core.library import Library
# from simulation.core.library_entry import LibraryEntry


class LibrarySelectorWidget(QtWidgets.QWidget):
    button_new_pressed = QtCore.Signal()
    button_delete_pressed = QtCore.Signal()
    selection_list_refreshed = QtCore.Signal(bool)
    selection_list: QtWidgets.QListWidget
    get_selectable_config_folders: Callable[[], set[str]] | None

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        get_selectable_config_folders: Callable[[], set[str]] | None = None,
    ):
        super().__init__(parent)

        self.get_selectable_config_folders = get_selectable_config_folders

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

        # Actually generate content for the GUI elements
        self._refresh_selectable_entries()

    def force_refresh(self):
        self._refresh_selectable_entries()

    def _button_new_pressed(self):
        self.button_new_pressed.emit()

    def _button_delete_pressed(self):
        self.button_delete_pressed.emit()

    def _refresh_selectable_entries(self):
        # Abort early if get_selectable_config_folders is not set
        if self.get_selectable_config_folders is None:
            return

        old_selection = self.selection_list.currentItem()

        location_config_folders = self.get_selectable_config_folders()
        self.selection_list.clear()
        self.selection_list.addItems(location_config_folders)

        if old_selection is not None:
            index_equal_to_old_selection = self.selection_list.findItems(
                old_selection.text()
            )
            if index_equal_to_old_selection >= 0:
                self.selection_list.setCurrentIndex(index_equal_to_old_selection)

        no_locations_exist = (
            location_config_folders is None or len(location_config_folders) == 0
        )
        self.selection_list_refreshed.emit(no_locations_exist)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = LibrarySelectorWidget()
    widget.show()
    sys.exit(app.exec())
