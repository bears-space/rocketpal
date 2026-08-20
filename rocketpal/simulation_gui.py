#!/usr/bin/env python3

# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# type: ignore

from imgui_bundle import hello_imgui, immapp

from rocketpal.common.common_paths import GUI_ASSETS_PATH
from rocketpal.gui.flight_simulation_gui import FlightSimulationGUI


def start_and_hand_over_to_simulation_gui():
    app = FlightSimulationGUI()
    hello_imgui.set_assets_folder(GUI_ASSETS_PATH.as_posix())
    immapp.run(gui_function=app.gui, window_title="RocketPal", window_size=(1280, 720))


if __name__ == "__main__":
    start_and_hand_over_to_simulation_gui()
