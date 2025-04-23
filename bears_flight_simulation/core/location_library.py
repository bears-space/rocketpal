import typing as t

from core.library import Library
from core.library_entry import LibraryEntry
from parsers.location import Location


class LocationLibrary(Library):
    def load_entry(self, data: t.Dict) -> LibraryEntry:
        return Location(data)
