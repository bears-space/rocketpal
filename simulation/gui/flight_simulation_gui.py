# type: ignore

from pathlib import Path
import sys
import os
from PySide6 import QtCore, QtWidgets

from simulation import load_configs_and_run_simulation

INPUT_FOLDER = "./input"
OUTPUT_FOLDER = str(Path(os.path.realpath(sys.argv[0])).parent) + "/output"


class FlightSimulationGUI(QtWidgets.QWidget):
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
        _selection_layout.addWidget(self.simulation_selector_dropdown)

        self.selection_edit_button = QtWidgets.QPushButton("Edit")
        self.selection_edit_button.clicked.connect(self._selection_edit_button_pressed)
        _selection_layout.addWidget(self.selection_edit_button)

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

    def _selection_edit_button_pressed(self):
        pass

    def _run_simulation_button_pressed(self):
        load_configs_and_run_simulation(
            config_folder=INPUT_FOLDER, output_folder=OUTPUT_FOLDER
        )

    def _show_results_button_pressed(self):
        pass
