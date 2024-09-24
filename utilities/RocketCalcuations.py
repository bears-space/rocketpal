import typing as t

from parsers.parts_list_parser import Part


def calculate_rocket_mass_in_g(parts: t.List[Part]) -> float:
    total_mass = 0.0
    for part in parts:
        total_mass += part.mass
    return total_mass


def calculate_rocket_mass_in_kg(parts: t.List[Part]) -> float:
    return calculate_rocket_mass_in_g(parts) / 1000.0


def get_maximum_diameter_in_mm(parts: t.List[Part]) -> float:
    max_diameter = 0.0
    for part in parts:
        max_diameter = max(part.diameter, max_diameter)
    return max_diameter


def get_maximum_diameter_in_m(parts: t.List[Part]) -> float:
    return get_maximum_diameter_in_mm(parts) / 1000.0
