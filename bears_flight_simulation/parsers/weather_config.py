# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from bears_flight_simulation.core.library_entry import LibraryEntry


class WeatherConfig(LibraryEntry):
    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("wind_speed_in_m_per_s", float),
                ("wind_direction_in_degrees", float),
                ("wind_x_y_factor_standard_deviation", float),
            ]
        )
        super().__init__(data)

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return WeatherConfig(
            {
                "id": id,
                "wind_speed_in_m_per_s": 0.0,
                "wind_direction_in_degrees": 0.0,
                "wind_x_y_factor_standard_deviation": 0.0,
            }
        )
