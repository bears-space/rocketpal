# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import typing as t

import yaml

from bears_flight_simulation.core.library_entry import LibraryEntry


class RailButtonConfig(LibraryEntry):
    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("upper_button_position", float),
                ("lower_button_position", float),
                ("angular_position", float),
            ]
        )
        super().__init__(data)

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return RailButtonConfig(
            {
                "id": id,
                "upper_button_position": 2.0,
                "lower_button_position": 0.1,
                "angular_position": 45.0,
            }
        )
