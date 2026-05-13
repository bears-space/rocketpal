# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from bears_flight_simulation.parsers.location_config import LocationConfig


def test_serialize():
    serialized = {
        "id": "example",
        "latitude": 42.0,
        "longitude": 73.0,
        "elevation": 1337.0,
    }
    location = LocationConfig(serialized)
    assert location.serialize() == serialized
