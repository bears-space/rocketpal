#!/usr/bin/env python3
# type: ignore

import logging

import sys
from PySide6 import QtWidgets

from gui.flight_simulation_gui import FlightSimulationGUI

if __name__ == "__main__":
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Prepare application
    app = QtWidgets.QApplication([])
    app.setApplicationName("FSG - Flight Simulation GUI")

    # Hello world test
    widget = FlightSimulationGUI()
    widget.resize(1280, 720)
    widget.show()

    # Enter GUI main loop
    sys.exit(app.exec())
