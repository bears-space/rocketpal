import typing as t

from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.utilities.airbrake_controllers import (
    stupid_full_extension_controller,
)


class AirbrakeConfig(LibraryEntry):
    sampling_rate_hz: float
    controller_function: t.Callable
    drag_curve_filepath: str

    def __init__(self, data: t.Dict, airbrake_folder: str) -> None:
        super().__init__(data)

        self.id = str(data["ID"])
        self.sampling_rate_hz = float(data["sampling_rate_hz"])

        controller_name = str(data["controller_function_name"])

        match controller_name:
            case "stupid_full_extension_controller":
                self.controller_function = stupid_full_extension_controller
            case _:
                raise NotImplementedError

        self.drag_curve_filepath = airbrake_folder + "/" + str(data["drag_curve_file"])
