# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytest

from bears_flight_simulation.parsers.parts_list_parser import Part
from bears_flight_simulation.utilities.config_calc import rocket_center_of_mass


def test_rocket_center_of_mass__empty():
    assert rocket_center_of_mass([]) == (0.0, 0.0, 0.0)


def test_rocket_center_of_mass__single_part_centered():
    parts = [Part(1, "some part", [1, 1, 1, 1], 42.0, 1.0, 5.0, 2.0, 1.0, 0.0, 0.0)]
    com = rocket_center_of_mass(parts)
    assert com == (0.0, 0.0, 8.0)


def test_rocket_center_of_mass__two_parts_centered_equal_weight():
    parts = [
        Part(1, "some part", [1, 1, 1, 1], 42.0, 1.0, 5.0, 2.0, 1.0, 0.0, 0.0),
        Part(2, "another part", [1, 1, 1, 2], 42.0, 1.0, 5.0, 2.0, 11.0, 0.0, 0.0),
    ]
    com = rocket_center_of_mass(parts)
    assert com == (0.0, 0.0, 13.0)


def test_rocket_center_of_mass__two_parts_centered_unequal_weight():
    parts = [
        Part(1, "some part", [1, 1, 1, 1], 42.0, 1.0, 5.0, 2.0, 1.0, 0.0, 0.0),
        Part(2, "another part", [1, 1, 1, 2], 21.0, 1.0, 5.0, 2.0, 11.0, 0.0, 0.0),
    ]
    com = rocket_center_of_mass(parts)
    assert pytest.approx(com[2]) == 11.33333333


def test_rocket_center_of_mass__three_parts_centered_unequal_weight():
    parts = [
        Part(1, "some part", [1, 1, 1, 1], 42.0, 1.0, 5.0, 2.0, 1.0, 0.0, 0.0),
        Part(2, "another part", [1, 1, 1, 2], 21.0, 1.0, 5.0, 2.0, 11.0, 0.0, 0.0),
        Part(3, "ye olde part", [1, 1, 1, 3], 73.0, 1.0, 5.0, 2.0, 500.0, 0.0, 0.0),
    ]
    com = rocket_center_of_mass(parts)
    assert pytest.approx(com[2]) == 277.38970588
