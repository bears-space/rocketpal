from bears_flight_simulation.core.library_entry import LibraryEntry


class Location(LibraryEntry):
    # Location data
    latitude: float
    longitude: float
    elevation: float

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        # Load location data
        self.latitude = float(data["latitude"])
        self.longitude = float(data["longitude"])
        self.elevation = float(data["elevation"])

    @classmethod
    def new_default(cls, id: str) -> "Location":
        return Location(
            {
                "ID": id,
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

    def serialize(self) -> dict:
        return {
            "ID": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "elevation": self.elevation,
        }
