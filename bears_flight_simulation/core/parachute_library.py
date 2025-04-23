import typing as t

from parsers.parachute_config import ParachuteConfig

from core.library import Library
from core.library_entry import LibraryEntry


class ParachuteLibrary(Library):
    def load_entry(self, data: t.Dict) -> LibraryEntry:
        return ParachuteConfig(data)
