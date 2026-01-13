#!/usr/bin/env python3
# type: ignore

import logging

from pathlib import Path
import sys
from PySide6 import QtWidgets, QtGui

from bears_flight_simulation.gui.flight_simulation_gui import FlightSimulationGUI

ICON_PATH = str(Path(__file__).parent.parent) + "/img/BEARS_Logo_white_circle.png"


def start_and_hand_over_to_simulation_gui():
    # Prepare application
    app = QtWidgets.QApplication([])
    app.setApplicationName("BEARS Flight Simulation")
    app.setWindowIcon(QtGui.QIcon(ICON_PATH))

    # Hello world test
    widget = FlightSimulationGUI()
    widget.resize(1280, 720)
    widget.show()

    # Enter GUI main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    start_and_hand_over_to_simulation_gui()
