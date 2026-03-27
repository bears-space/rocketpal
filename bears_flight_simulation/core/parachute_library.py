from uuid import uuid4

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.parsers.parachute_config import ParachuteConfig


class ParachuteLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return ParachuteConfig(data)

    def new_entry(self) -> LibraryEntry:
        id = str(uuid4())
        entry = ParachuteConfig.new_default(id)
        self.entries[id] = entry
        self.save()
        return entry
