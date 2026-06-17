# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import typing as t

from rocketpal.core.library_entry import LibraryEntry


class FinsConfig(LibraryEntry):
    sweep_length: t.Union[float, None]
    sweep_angle: t.Union[float, None]
    radius: t.Union[float, None]

    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("n", int),
                ("root_chord", float),
                ("tip_chord", float),
                ("span", float),
                ("position", float),
                ("cant_angle", float),
            ]
        )
        super().__init__(data)

        self.sweep_length = data["sweep_length"]
        assert type(self.sweep_length) in [float, type(None)]
        self.sweep_angle = data["sweep_angle"]
        assert type(self.sweep_angle) in [float, type(None)]
        self.radius = data["radius"]
        assert type(self.radius) in [float, type(None)]

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return FinsConfig(
            {
                "id": id,
                "n": 3,
                "root_chord": 0.236,
                "tip_chord": 0.136,
                "span": 0.091,
                "position": 0.246,
                "cant_angle": 0.0,
                "sweep_length": 0.0498,
                "sweep_angle": None,
                "radius": None,
            }
        )
