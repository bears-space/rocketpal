# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from rocketpal.core.library_entry import LibraryEntry


class NoseconeConfig(LibraryEntry):
    power_if_using_powerseries_kind: float | None
    base_radius: float | None

    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("kind", str),
                ("bluffness", float),
                ("length", float),
                ("position", float),
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
        return NoseconeConfig(
            {
                "id": id,
                "kind": "ogive",
                "bluffness": 0.1618,
                "length": 0.3,
                "position": 0.0,
                "power_if_using_powerseries_kind": None,
                "base_radius": None,
            }
        )
