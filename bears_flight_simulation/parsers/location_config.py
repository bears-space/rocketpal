from bears_flight_simulation.core.library_entry import LibraryEntry


class LocationConfig(LibraryEntry):
    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("latitude", float),
                ("longitude", float),
                ("elevation", float),
            ]
        )
        super().__init__(data)

    @classmethod
    def new_default(cls, id: str) -> "LocationConfig":
        return LocationConfig(
            {
                "id": id,
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )
