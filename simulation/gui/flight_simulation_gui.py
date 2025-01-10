# type: ignore

import platformdirs
from pathlib import Path
import sys
import os
from PySide6 import QtCore, QtWidgets

from simulation import load_configs_and_run_simulation

SIMULATION_CONFIG_BASE_FOLDER = (
    platformdirs.user_config_dir() + "/bears-flight-simulation/simulations"
)
OUTPUT_FOLDER = str(Path(os.path.realpath(sys.argv[0])).parent) + "/output"


class FlightSimulationGUI(QtWidgets.QWidget):
    current_selection: str | None = None

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        _spacer_top = QtWidgets.QSpacerItem(
            20,
            40,
            hData=QtWidgets.QSizePolicy.Policy.Preferred,
            vData=QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_top)

        self.selection_layout_widget = QtWidgets.QWidget()
        _selection_layout = QtWidgets.QHBoxLayout()
        _selection_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.selection_layout_widget)

        self.selection_layout_widget.setLayout(_selection_layout)
        self.simulation_selector_dropdown = QtWidgets.QComboBox()
        self.simulation_selector_dropdown.currentTextChanged.connect(
            self._simulation_selector_dropdown_changed
        )
        self._refresh_selectable_simulations()
        _selection_layout.addWidget(self.simulation_selector_dropdown)

        self.selection_edit_button = QtWidgets.QPushButton("Edit")
        self.selection_edit_button.clicked.connect(self._selection_edit_button_pressed)
        _selection_layout.addWidget(self.selection_edit_button)

        self.selection_new_button = QtWidgets.QPushButton("New")
        self.selection_new_button.clicked.connect(self._selection_new_button_pressed)
        _selection_layout.addWidget(self.selection_new_button)

        self.run_simulation_button = QtWidgets.QPushButton("Run Simulation")
        self.run_simulation_button.clicked.connect(self._run_simulation_button_pressed)
        self.layout.addWidget(self.run_simulation_button)

        self.show_results_button = QtWidgets.QPushButton("Show Results")
        self.show_results_button.clicked.connect(self._show_results_button_pressed)
        self.layout.addWidget(self.show_results_button)

        _spacer_bottom = QtWidgets.QSpacerItem(
            20,
            40,
            hData=QtWidgets.QSizePolicy.Policy.Preferred,
            vData=QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_bottom)

    def _simulation_selector_dropdown_changed(self, new_text):
        self.current_selection = new_text

    def _selection_edit_button_pressed(self):
        # TODO Launch config editor for the currently selected simulation
        pass

    def _selection_new_button_pressed(self):
        self._refresh_selectable_simulations()

    def _run_simulation_button_pressed(self):
        load_configs_and_run_simulation(
            config_folder=SIMULATION_CONFIG_BASE_FOLDER + "/" + self.current_selection,
            output_folder=OUTPUT_FOLDER,
        )

    def _show_results_button_pressed(self):
        pass

    def _refresh_selectable_simulations(self):
        old_selection = self.simulation_selector_dropdown.currentText()

        self.simulation_selector_dropdown.clear()
        self.simulation_selector_dropdown.addItems(get_config_folders())

        index_equal_to_old_selection = self.simulation_selector_dropdown.findText(
            old_selection
        )
        if index_equal_to_old_selection >= 0:
            self.simulation_selector_dropdown.setCurrentIndex(
                index_equal_to_old_selection
            )


def get_config_folders() -> set[str]:
    # Create the simulation config folder if it doesn't exist yet
    Path(SIMULATION_CONFIG_BASE_FOLDER).mkdir(parents=True, exist_ok=True)

    return os.listdir(SIMULATION_CONFIG_BASE_FOLDER)
