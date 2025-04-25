import typing as t

from bears_flight_simulation.core.library_entry import LibraryEntry


class AirbrakeConfig(LibraryEntry):
    id: str
    sampling_rate: float

    def __init__(self, data: t.Dict) -> None:
        super().__init__(data)

        self.id = str(data["ID"])
        self.sampling_rate = float(data["sampling_rate"])
