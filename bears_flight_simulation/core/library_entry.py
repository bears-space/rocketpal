import typing as t


from abc import ABC, abstractmethod


class LibraryEntry(ABC):
    id: str

    def __init__(self, data: t.Dict) -> None:
        # Load identifier
        self.id = str(data["ID"])

    @abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError
