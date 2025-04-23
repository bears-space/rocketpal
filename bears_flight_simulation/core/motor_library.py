import typing as t

from bears_flight_simulation.parsers.motor_config import MotorConfig

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry


class MotorLibrary(Library):
    def load_entry(self, data: t.Dict) -> LibraryEntry:
        return MotorConfig(data)
