# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

from rocketpal.core.library_entry import LibraryEntry


class SimulationConfig(LibraryEntry):
    launch_date: datetime

    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("location_id", str),
                ("weather_config_id", str),
                ("use_weather_forecast_instead_of_config", bool),
                ("motor_id", str),
                ("motor_position", float),
                ("drag_curve_power_on_file", str),
                ("drag_curve_power_off_file", str),
                ("parachute_ids", list),
                ("airbrake_ids", list),
                ("rail_length_in_m", float),
                ("inclination", float),
                ("heading", float),
                (
                    "mass_without_motor_in_g",
                    float,
                ),
                (
                    "center_of_mass_in_m",
                    float,
                ),
                ("diameter_in_m", float),
                ("inertia_11", float),
                ("inertia_22", float),
                ("inertia_33", float),
                (
                    "mass_standard_deviation_factor",
                    float,
                ),
                (
                    "center_of_mass_standard_deviation_factor",
                    float,
                ),
                (
                    "inertia_standard_deviation_factor",
                    float,
                ),
                (
                    "power_off_drag_factor_standard_deviation",
                    float,
                ),
                (
                    "power_on_drag_factor_standard_deviation",
                    float,
                ),
                (
                    "enable_monte_carlo_simulation",
                    bool,
                ),
                (
                    "number_of_simulations",
                    int,
                ),
                (
                    "parallel",
                    bool,
                ),
                (
                    "n_workers",
                    int,
                ),
                (
                    "export_flight_data_time_step_seconds",
                    float,
                ),
            ]
        )
        super().__init__(data)

        self.launch_date = datetime.strptime(
            str(data["launch_date_utc"]), "%Y-%m-%d_%H-%M-%S"
        )

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return SimulationConfig(
            {
                "id": id,
                "location_id": "Ernst-Reuter-Platz",
                "weather_config_id": "manual-launch-day-weather",
                "use_weather_forecast_instead_of_config": False,
                "motor_id": "Cesaroni_6800M3700-P",  #
                "motor_position": 0.0225,
                "parachute_ids": ["demo-main", "demo-drogue"],
                "airbrake_ids": [""],
                "rail_length_in_m": 12,
                "inclination": 84,
                "heading": 133,
                "drag_curve_power_on_file": None,
                "drag_curve_power_off_file": None,
                "launch_date_utc": "2025-10-13_08-00-00",  # TODO make this dynamic based on current date
                "mass_without_motor_in_g": 15000,
                "center_of_mass_in_m": 1.5,
                "diameter_in_m": 0.1236,
                "inertia_11": 6.321,
                "inertia_22": 6.321,
                "inertia_33": 0.034,
                "mass_standard_deviation_factor": 0.05,
                "center_of_mass_standard_deviation_factor": 0.05,
                "inertia_standard_deviation_factor": 0.1,
                "power_off_drag_factor_standard_deviation": 0.1,
                "power_on_drag_factor_standard_deviation": 0.1,
                "enable_monte_carlo_simulation": False,
                "number_of_simulations": 100,
                "parallel": True,
                "n_workers": 8,
                "export_flight_data_time_step_seconds": 0.01,
            }
        )
