import typing as t

from parsers.motor_config import MotorConfig

from core.library import Library
from core.library_entry import LibraryEntry


class MotorLibrary(Library):
    def load_entry(self, data: t.Dict) -> LibraryEntry:
        return MotorConfig(data)
