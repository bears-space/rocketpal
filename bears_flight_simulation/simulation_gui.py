#!/usr/bin/env python3
# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# type: ignore

import logging
import sys

from PySide6 import QtGui, QtWidgets

from bears_flight_simulation.common.common_paths import ICON_PATH
from bears_flight_simulation.gui.flight_simulation_gui import FlightSimulationGUI


def start_and_hand_over_to_simulation_gui():
    # Prepare application
    app = QtWidgets.QApplication([])
    app.setApplicationName("BEARS Flight Simulation")
    app.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))

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
