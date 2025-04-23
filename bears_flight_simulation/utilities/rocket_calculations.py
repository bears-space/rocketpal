from parsers.parts_list_parser import (
    Part,
    is_segment_based_on_hierarchy,
)


def calculate_rocket_mass_in_g(parts: list[Part]) -> float:
    total_mass = 0.0
    for part in parts:
        if not is_segment_based_on_hierarchy(part.hierarchy):
            total_mass += part.mass
    return total_mass


def calculate_rocket_mass_in_kg(parts: list[Part]) -> float:
    return calculate_rocket_mass_in_g(parts) / 1000.0
