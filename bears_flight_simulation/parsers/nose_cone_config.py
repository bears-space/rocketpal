import typing as t

import yaml

from bears_flight_simulation.core.library_entry import LibraryEntry


class NoseConeConfig(LibraryEntry):
    power_if_using_powerseries_kind: float | None
    base_radius: float | None

    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("kind", str),
                ("bluffness", float),
            ]
        )
        super().__init__(data)

        # Load nose cone data
        self.power_if_using_powerseries_kind = data["power_if_using_powerseries_kind"]
        assert type(self.power_if_using_powerseries_kind) in [float, type(None)]
        self.base_radius = data["base_radius"]
        assert type(self.base_radius) in [float, type(None)]

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return NoseConeConfig(
            {
                "id": id,
                "kind": "ogive",
                "bluffness": 0.1618,
                "power_if_using_powerseries_kind": None,
                "base_radius": None,
            }
        )
