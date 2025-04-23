import typing as t

from bears_flight_simulation.parsers.parachute_config import ParachuteConfig

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry


class ParachuteLibrary(Library):
    def load_entry(self, data: t.Dict) -> LibraryEntry:
        return ParachuteConfig(data)
