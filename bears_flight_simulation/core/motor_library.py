from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.parsers.motor_config import MotorConfig


class MotorLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return MotorConfig(data)
