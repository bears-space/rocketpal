from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.parsers.parachute_config import ParachuteConfig


class ParachuteLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return ParachuteConfig(data)
