import os
import typing as t

import yaml

from abc import ABC

from bears_flight_simulation.core.library_entry import LibraryEntry


class Library(ABC):
    entries: t.Dict[str, LibraryEntry]

    def __init__(self, library_folder: str) -> None:
        self.entries = {}

        # Load entries from folder
        files: t.List[str] = os.listdir(library_folder)
        files = [filename for filename in files if filename.find(".yaml") != -1]
        for filename in files:
            with open(library_folder + "/" + filename) as file:
                data = yaml.safe_load(file)
                entry = self.load_entry(data)
                self.entries[entry.id] = entry

    def load_entry(self, data: t.Dict) -> LibraryEntry:
        raise NotImplementedError

    def get(self, id: str) -> LibraryEntry | None:
        return self.entries.get(id, None)
