import typing as t

from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.utilities.airbrake_controllers import (
    disabled_controller,
    enabled_controller,
    stupid_full_extension_controller,
    stargaze_airbrake_controller,
)


class AirbrakeConfig(LibraryEntry):
    sampling_rate_hz: float
    controller_function: t.Callable
    drag_curve_filepath: str
    drag_curve_standard_deviation_factor: float

    def __init__(self, data: t.Dict, airbrake_folder: str) -> None:
        super().__init__(data)

        self.id = str(data["ID"])
        self.sampling_rate_hz = float(data["sampling_rate_hz"])

        controller_name = str(data["controller_function_name"])

        match controller_name:
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

        self.drag_curve_filepath = airbrake_folder + "/" + str(data["drag_curve_file"])
        self.drag_curve_standard_deviation_factor = float(
            data["drag_curve_standard_deviation_factor"]
        )
