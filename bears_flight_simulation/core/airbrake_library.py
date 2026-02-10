from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry


class AirbrakeLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return AirbrakeConfig(data, self.library_folder)
