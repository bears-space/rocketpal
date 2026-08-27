# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# type: ignore

from pathlib import Path
from shutil import copytree

from imgui_bundle import imgui, immapp, immvision

from rocketpal.common.common_paths import (
    OUTPUT_FOLDER,
    TEMPLATE_FOLDER,
    USER_SIMULATION_CONFIG_BASE_FOLDER,
    get_simulation_entries,
)
from rocketpal.gui.file_helpers import open_explorer
from rocketpal.simulation import load_configs_and_run_simulation


class FlightSimulationGUI:
    def __init__(self) -> None:
        self.current_selection_index: int = 0
        self.selectable_simulations: list[str] = []

        # Actually generate content for the GUI elements
        self._refresh_selectable_simulations()

    def gui(self) -> None:
        # Setup main viewport
        viewport = imgui.get_main_viewport()
        imgui.set_next_window_pos(viewport.work_pos)
        imgui.set_next_window_size(viewport.work_size)

        # Configure window flags
        window_flags = (
            imgui.WindowFlags_.no_title_bar
            | imgui.WindowFlags_.no_resize
            | imgui.WindowFlags_.no_move
            | imgui.WindowFlags_.no_collapse
        )

        imgui.begin("RocketPal", flags=window_flags)

        _changed, self.current_selection_index = imgui.combo(
            "Select Simulation",
            self.current_selection_index,
            self.selectable_simulations,
        )

        if imgui.button("Refresh simulation list"):
            self._refresh_selectable_simulations()

        if imgui.button("Run Simulation"):
            self._run_simulation()

        if imgui.button("Show results"):
            self._show_results()

        imgui.end()

    def _run_simulation(self) -> bool:
        if self.current_selection_index >= len(self.selectable_simulations):
            print("Invalid simulation index")
            return False

        # Run selected simulation
        simulation_config_path = Path(
            self.selectable_simulations[self.current_selection_index]
        )
        load_configs_and_run_simulation(
            config_folder=USER_SIMULATION_CONFIG_BASE_FOLDER / simulation_config_path,
            output_folder=OUTPUT_FOLDER,
        )

        return True

    def _show_results(self):
        # Show the output folder in a file explorer
        open_explorer(OUTPUT_FOLDER)

    def _refresh_selectable_simulations(self):
        old_selection = (
            self.selectable_simulations[self.current_selection_index]
            if self.current_selection_index < len(self.selectable_simulations)
            else None
        )

        # Update list of selectable simulations
        simulation_config_folders = get_simulation_entries()
        self.selectable_simulations = [
            str(entry) for entry in simulation_config_folders
        ]

        # Update selection index for the new list
        if old_selection in self.selectable_simulations:
            self.current_selection_index = self.selectable_simulations.index(
                old_selection
            )
        else:
            self.current_selection_index = 0
