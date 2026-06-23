# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import pytest

from rocketpal.core.part import Part
from rocketpal.utilities.config_calc import calculate_center_of_mass


def test_rocket_center_of_mass__empty():
    assert calculate_center_of_mass([]) == (0.0, 0.0, 0.0)


def test_rocket_center_of_mass__single_part_centered():
    parts = [Part(42.0, 10.0)]
    com = calculate_center_of_mass(parts)
    assert com == (0.0, 0.0, 10.0)


def test_rocket_center_of_mass__two_parts_centered_equal_weight():
    parts = [
        Part(42.0, 15.0),
        Part(42.0, 25.0),
    ]
    com = calculate_center_of_mass(parts)
    assert com == (0.0, 0.0, 20.0)


def test_rocket_center_of_mass__two_parts_centered_unequal_weight():
    parts = [
        Part(42.0, 1.0),
        Part(21.0, 11.0),
    ]
    com = calculate_center_of_mass(parts)
    assert pytest.approx(com[2]) == 4.33333333


def test_rocket_center_of_mass__three_parts_centered_unequal_weight():
    parts = [
        Part(42.0, 1.0),
        Part(21.0, 11.0),
        Part(73.0, 500.0),
    ]
    com = calculate_center_of_mass(parts)
    assert pytest.approx(com[2]) == 270.38970588
