from bears_flight_simulation.parsers.parts_list_parser import (
    Part,
    is_segment_based_on_hierarchy,
    part_is_motor,
    part_is_in_motor_group,
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
        if part_is_motor(part) or part_is_in_motor_group(part, parts):
            continue
        if not is_segment_based_on_hierarchy(part.hierarchy):
            total_mass += part.mass
    return total_mass


def calculate_rocket_mass_without_motor_in_kg(parts: list[Part]) -> float:
    return calculate_rocket_mass_without_motor_in_g(parts) / 1000.0
