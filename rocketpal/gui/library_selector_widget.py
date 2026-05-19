# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# type: ignore

import sys
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# from rocketpal.simulation.core.library import Library
# from rocketpal.simulation.core.library_entry import LibraryEntry


class LibrarySelectorWidget(QWidget):
    button_new_pressed = Signal()
    button_delete_pressed = Signal()
    selection_list_refreshed = Signal(bool)
    selection_list: QListWidget
    get_selectable_config_folders: Callable[[], set[Path]] | None

    def __init__(
        self,
        parent: QWidget | None = None,
        get_selectable_config_folders: Callable[[], set[Path]] | None = None,
    ):
        super().__init__(parent)

        self.get_selectable_config_folders = get_selectable_config_folders

        self.layout = QVBoxLayout(self)

        self.selection_list = QListWidget()
        self.layout.addWidget(self.selection_list)

        self.button_layout_widget = QWidget()
        _button_layout = QHBoxLayout()
        self.button_layout_widget.setLayout(_button_layout)
        self.layout.addWidget(self.button_layout_widget)

        self.button_delete = QPushButton(text="Delete")
        self.button_delete.clicked.connect(self._button_delete_pressed)
        _button_layout.addWidget(self.button_delete)

        self.button_new = QPushButton(text="New")
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
        self.selection_list.addItems([str(entry) for entry in location_config_folders])

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
    app = QApplication([])
    widget = LibrarySelectorWidget()
    widget.show()
    sys.exit(app.exec())
