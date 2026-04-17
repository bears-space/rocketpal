from abc import ABC, abstractmethod

from bears_flight_simulation.core.config import Config


class LibraryEntry(ABC, Config):
    def __init__(self, data: dict) -> None:
        self.extend_field_links([("id", str)])
        super().__init__(data)

    @classmethod
    @abstractmethod
    def new_default(cls, id: str) -> "LibraryEntry":
        raise NotImplementedError
