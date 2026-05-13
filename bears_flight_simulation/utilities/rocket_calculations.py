# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from bears_flight_simulation.parsers.parts_list_parser import (
    Part,
    is_segment_based_on_hierarchy,
    part_is_motor,
)


def calculate_rocket_mass_in_g(parts: list[Part]) -> float:
    total_mass = 0.0
    for part in parts:
        if not is_segment_based_on_hierarchy(part.hierarchy):
            total_mass += part.mass
    return total_mass


def calculate_rocket_mass_in_kg(parts: list[Part]) -> float:
    return calculate_rocket_mass_in_g(parts) / 1000.0


def calculate_rocket_mass_without_motor_in_g(parts: list[Part]) -> float:
    total_mass = 0.0
    for part in parts:
        if part_is_motor(part):
            continue
        if not is_segment_based_on_hierarchy(part.hierarchy):
            total_mass += part.mass
    return total_mass


def calculate_rocket_mass_without_motor_in_kg(parts: list[Part]) -> float:
    return calculate_rocket_mass_without_motor_in_g(parts) / 1000.0
