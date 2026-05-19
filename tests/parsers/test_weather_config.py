# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from rocketpal.parsers.weather_config import WeatherConfig


def test_serialize():
    serialized = {
        "id": "example",
        "wind_speed_in_m_per_s": 5.0,
        "wind_direction_in_degrees": 90.0,
        "wind_x_y_factor_standard_deviation": 0.1,
    }
    weather_config = WeatherConfig(serialized)
    assert weather_config.serialize() == serialized
