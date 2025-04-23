import typing as t

from core.library_entry import LibraryEntry


class Location(LibraryEntry):
    # Location data
    latitude: float
    longitude: float
    elevation: float

    def __init__(self, data: t.Dict) -> None:
        super().__init__(data)

        # Load location data
        self.latitude = float(data["latitude"])
        self.longitude = float(data["longitude"])
        self.elevation = float(data["elevation"])
