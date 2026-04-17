import typing as t
from datetime import datetime

import yaml

from bears_flight_simulation.core.library_entry import LibraryEntry


class SimulationConfig(LibraryEntry):
    launch_date: datetime

    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("location_id", str),
                ("weather_config_id", str),
                ("use_weather_forecast_instead_of_config", bool),
                ("motor_id", str),
                ("drag_curve_power_on_file", str),
                ("drag_curve_power_off_file", str),
                ("parachute_ids", list),
                ("airbrake_ids", list),
                ("rail_length_in_m", float),
                ("inclination", float),
                ("heading", float),
                ("override_parts_list", bool),
                (
                    "override_parts_list_mass_without_motor_in_g",
                    float,
                ),
                (
                    "override_parts_list_center_of_mass_in_m",
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
        # TODO think of some sensible defaults
        return SimulationConfig(
            {
                "id": id,
                "location_id": "Campo Militar de Santa Margarida B",
                "weather_config_id": "manual-launch-day-weather",
                "use_weather_forecast_instead_of_config": False,
                "motor_id": "Cesaroni_6800M3700-P",
                "parachutes": ["stargaze-main", "stargaze-drogue"],
                "airbrakes": ["stargaze-airbrake"],
                "rail_length_in_m": 12,
                "inclination": 84,
                "heading": 144,
                "drag_curve_power_on_file": None,
                "drag_curve_power_off_file": None,
                "launch_date_utc": "2025-10-13_08-00-00",
                "override_parts_list": True,
                "override_parts_list_mass_without_motor_in_g": 14788,
                "override_parts_list_center_of_mass_in_m": 1.44,
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
                "exportFlightDataTimeStepSeconds": 0.01,
            }
        )
