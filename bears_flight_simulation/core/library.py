import os
from abc import ABC, abstractmethod
from pathlib import Path

import yaml

from bears_flight_simulation.core.library_entry import LibraryEntry


class Library(ABC):
    entries: dict[str, LibraryEntry]
    library_folder: Path

    def __init__(self, library_folder: Path) -> None:
        self.entries = {}
        self.library_folder = library_folder
        self.reload()

    def reload(self) -> None:
        self.entries = {}

        # Load entries from folder
        files: list[str] = os.listdir(self.library_folder)
        files = [filename for filename in files if filename.find(".yaml") != -1]
        for filename in files:
            with open(self.library_folder / filename) as file:
                data = yaml.safe_load(file)
                entry = self.load_entry(data)
                self.entries[entry.id] = entry  # type: ignore

    @abstractmethod
    def load_entry(self, data: dict) -> LibraryEntry:
        raise NotImplementedError

    @abstractmethod
    def new_entry(self) -> LibraryEntry:
        raise NotImplementedError

    def get(self, id: str) -> LibraryEntry | None:
        return self.entries.get(id, None)

    def save(self) -> None:
        for id, entry in self.entries.items():
            with open(self.library_folder / (id + ".yaml"), "w") as file:
                file.write(yaml.dump(entry.serialize()))
