#!/usr/bin/env python3
# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# type: ignore

import sys

from PySide6 import QtGui, QtWidgets

from rocketpal.common.common_paths import ICON_PATH
from rocketpal.gui.flight_simulation_gui import FlightSimulationGUI


def start_and_hand_over_to_simulation_gui():
    # Prepare application
    app = QtWidgets.QApplication([])
    app.setApplicationName("RocketPal")
    app.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))

    # Hello world test
    widget = FlightSimulationGUI()
    widget.resize(1280, 720)
    widget.show()

    # Enter GUI main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    start_and_hand_over_to_simulation_gui()
