from abc import ABC, abstractmethod


class LibraryEntry(ABC):
    id: str

    def __init__(self, data: dict) -> None:
        # Load identifier
        self.id = str(data["ID"])

    @classmethod
    @abstractmethod
    def new_default(cls, id: str) -> "LibraryEntry":
        raise NotImplementedError

    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError
