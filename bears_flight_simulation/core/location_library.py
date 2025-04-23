import typing as t

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.parsers.location import Location


class LocationLibrary(Library):
    def load_entry(self, data: t.Dict) -> LibraryEntry:
        return Location(data)
