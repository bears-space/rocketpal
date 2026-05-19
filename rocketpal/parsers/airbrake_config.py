# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import typing as t
from pathlib import Path

from rocketpal.core.library_entry import LibraryEntry
from rocketpal.utilities.airbrake_controllers import (
    disabled_controller,
    enabled_controller,
    stargaze_airbrake_controller,
    stupid_full_extension_controller,
)


class AirbrakeConfig(LibraryEntry):
    controller_function: t.Callable
    drag_curve_filepath: Path

    def __init__(self, data: dict, airbrake_folder: Path) -> None:
        self.extend_field_links(
            [
                ("sampling_rate_hz", float),
                ("controller_function_name", str),
                ("drag_curve_file", str),
                ("drag_curve_standard_deviation_factor", float),
            ]
        )
        super().__init__(data)

        match self.controller_function_name:  # type: ignore
            case "disabled_controller":
                self.controller_function = disabled_controller
            case "enabled_controller":
                self.controller_function = enabled_controller
            case "stupid_full_extension_controller":
                self.controller_function = stupid_full_extension_controller
            case "stargaze_airbrake_controller":
                self.controller_function = stargaze_airbrake_controller
            case _:
                raise NotImplementedError

        self.drag_curve_filepath = airbrake_folder / str(data["drag_curve_file"])

    @classmethod
    def new_default(cls, id: str) -> "AirbrakeConfig":
        return AirbrakeConfig(
            {
                "id": id,
                "sampling_rate_hz": 10.0,
                "controller_function_name": "disabled_controller",
                "drag_curve_file": "stargaze_airbrake_drag_curve.csv",
                "drag_curve_standard_deviation_factor": 0.1,
            },
            airbrake_folder=Path(""),
        )
