import csv
import logging
import re
import typing as t
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt


@dataclass
class Part:
    id_nr: int
    name: str
    hierarchy: list[int]
    mass: float  # in g
    length: float  # in mm
    position_from_bottom: float  # in mm
    position_from_bottom_of_compartment: float  # in mm
    center_of_mass_offset_from_position: float  # in mm
    radial_distance_to_midline: float  # in mm
    radial_direction: float  # in degrees


def is_segment_based_on_hierarchy(hierarchy: list[int]) -> bool:
    return hierarchy[len(hierarchy) - 1] == 0


def split_ci_number_and_norm(ci_number_and_norm: str) -> tuple[str, str]:
    """Given a CI Nr./Norm string, return the CI number and the name of a part.

    Parameters
    ----------
    ci_number_and_norm : str
        The CI Nr./Norm string, e.g. "01.01.02.02_Forward_Closure".

    Returns
    -------
    tuple[str, str]
        A tuple where the first entry is the CI number string and the second entry is the name of the part.
    """
    splits = ci_number_and_norm.split("_", 1)
    return (splits[0], splits[1])


def split_ci_number_into_hierarchy(ci_number: str) -> list[int]:
    hierarchy_strings = ci_number.split(".")
    return [int(s) for s in hierarchy_strings]


def determine_hierarchy_from_previous_part(previous_part: Part) -> list[int]:
    hierarchy = previous_part.hierarchy.copy()
    hierarchy[len(hierarchy) - 1] += 1
    return hierarchy


def get_parents_from_hierarchy(
    hierarchy: list[int], previous_parts: list[Part]
) -> list[Part]:
    parents = []

    for part in previous_parts:
        # only consider group parents
        if not is_segment_based_on_hierarchy(part.hierarchy):
            continue

        number_of_zeroes = 0
        for layer in part.hierarchy:
            if layer != 0:
                number_of_zeroes += 1

        is_parent = True
        for i in range(number_of_zeroes):
            if hierarchy[i] != part.hierarchy[i]:
                is_parent = False

        if is_parent:
            parents.append(part)

    return parents


def get_part_position(part: Part, parts: list[Part]) -> float:
    parents = get_parents_from_hierarchy(part.hierarchy, parts)
    position = 0.0
    for p in parents + [part]:
        position += p.position_from_bottom + p.position_from_bottom_of_compartment
    return position


def get_part_position_plus_length(part: Part, parts: list[Part]) -> float:
    return get_part_position(part, parts) + part.length


def get_part_center_of_mass(part: Part, parts: list[Part]) -> float:
    return get_part_position(part, parts) + part.center_of_mass_offset_from_position


def part_is_motor(part: Part) -> bool:
    return part.name == "Motor" and not is_segment_based_on_hierarchy(part.hierarchy)


def part_is_motor_group(part: Part) -> bool:
    return part.name == "Motor_Components" and is_segment_based_on_hierarchy(
        part.hierarchy
    )


def part_is_in_motor_group(part: Part, parts: list[Part]) -> bool:
    parents = get_parents_from_hierarchy(part.hierarchy, parts)
    for parent in parents:
        if part_is_motor_group(parent):
            return True
    return False


def get_motor_position(parts: list[Part]) -> float:
    for part in parts:
        if part_is_motor(part):
            return get_part_position(part, parts)

    # NOTE: A motor has to be included, so if there isn't one, raise an error.
    raise AssertionError


def part_is_nosecone(part: Part) -> bool:
    return part.name == "Nose Cone" and not is_segment_based_on_hierarchy(
        part.hierarchy
    )


def part_is_nosecone_tip(part: Part, parts: list[Part]) -> bool:
    return (
        part.name == "Tip"
        and not is_segment_based_on_hierarchy(part.hierarchy)
        and any(
            [
                p.name == "Nose Cone" and is_segment_based_on_hierarchy(p.hierarchy)
                for p in get_parents_from_hierarchy(part.hierarchy, parts)
            ]
        )
    )


def get_nosecone(parts: list[Part]) -> Part:
    for part in parts:
        if part_is_nosecone(part):
            return part

    # NOTE: A nosecone has to be included, so if there isn't one, raise an error.
    raise AssertionError


def get_nosecone_tip(parts: list[Part]) -> Part:
    for part in parts:
        if part_is_nosecone_tip(part, parts):
            return part

    # NOTE: A nosecone tip has to be included, so if there isn't one, raise an error.
    raise AssertionError


def get_nosecone_position(parts: list[Part]) -> float:
    return get_part_position(get_nosecone(parts), parts)


def get_nosecone_tip_position(parts: list[Part]) -> float:
    return get_part_position(get_nosecone_tip(parts), parts)


def get_nosecone_tip_position_plus_length(parts: list[Part]) -> float:
    return get_part_position_plus_length(get_nosecone_tip(parts), parts)


def get_nosecone_total_length(parts: list[Part]) -> float:
    return get_nosecone_tip_position_plus_length(parts) - get_nosecone_position(parts)


def parse_parts_list(parts_list_csv_file: t.TextIO) -> list[Part]:
    # Initialize parts list
    parts: list[Part] = []

    # Create CSV reader
    reader = csv.reader(parts_list_csv_file, dialect="excel")

    # Skip the first two rows (header)
    next(reader)
    next(reader)

    # From each row, create a Part
    id_nr_resetter = 9999
    for row in reader:
        # Convert comma to point in all fields that contain numbers
        for i in [0, 2, 6, 7, 8, 9, 10, 11, 12, 13, 17]:
            row[i] = row[i].replace(",", ".")

        name: str
        hierarchy: list[int]
        ci_number_and_norm = str(row[1])
        if re.search("\\..._", ci_number_and_norm) is not None:
            ci_nr, name = split_ci_number_and_norm(ci_number_and_norm)
            hierarchy = split_ci_number_into_hierarchy(ci_nr)
        else:
            name = ci_number_and_norm
            if parts == []:
                raise AssertionError
            hierarchy = determine_hierarchy_from_previous_part(parts[len(parts) - 1])

        # Only consider parts belonging to top-level hierarchy 1 (aka the rocket, not any support equipment)
        if hierarchy[0] != 1:
            continue

        length: float
        if row[8] == "":
            logging.warning(
                f"parse_parts_list: {ci_number_and_norm} has empty length, defaulting to 0.0!"
            )
            length = 0.0
        else:
            length = float(row[8])

        radial_distance_to_midline: float
        if row[12] == "TBD":
            logging.warning(
                f"parse_parts_list: {ci_number_and_norm} has radial_distance_to_midline='TBD', defaulting to 0.0!"
            )
            radial_distance_to_midline = 0.0
        elif row[12] in ["-", ""]:
            radial_distance_to_midline = 0.0
        else:
            radial_distance_to_midline = float(row[12])

        id_nr: int
        if row[0] == "":
            logging.warning(
                f"parse_parts_list: {ci_number_and_norm} has empty id_nr, counting back from 9999!"
            )
            id_nr = id_nr_resetter
            id_nr_resetter -= 1
        else:
            id_nr = int(row[0])

        mass: float
        if row[7] == "":
            logging.warning(
                f"parse_parts_list: {ci_number_and_norm} has empty mass, defaulting to 0.0!"
            )
            mass = 0.0
        else:
            mass = float(row[7])

        radial_direction: float
        if row[13] == "TBD":
            logging.warning(
                f"parse_parts_list: {ci_number_and_norm} has radial_direction='TBD', defaulting to 0.0!"
            )
            radial_direction = 0.0
        elif row[13] in ["-", ""]:
            radial_direction = 0.0
        else:
            radial_direction = float(row[13])

        # Create Part
        part = Part(
            id_nr=id_nr,
            name=name,
            hierarchy=hierarchy,
            mass=mass,
            length=length,
            position_from_bottom=(float(row[9]) if row[9] not in ["-", ""] else 0.0),
            position_from_bottom_of_compartment=(
                float(row[10]) if row[10] not in ["-", ""] else 0.0
            ),
            center_of_mass_offset_from_position=(
                float(row[11]) if row[11] not in ["", "-"] else 0.0
            ),
            radial_distance_to_midline=radial_distance_to_midline,
            radial_direction=radial_direction,
        )

        # Store part
        parts.append(part)

    return parts


def visualize_mass_distribution(parts: list[Part]):
    parts_that_are_not_groups = [
        part for part in parts if not is_segment_based_on_hierarchy(part.hierarchy)
    ]

    plt.figure()

    for part in parts_that_are_not_groups:
        plt.scatter(
            x=get_part_center_of_mass(part, parts),
            y=part.mass,
            color="blue",
            marker="o",
        )

    plt.xlabel("x")
    plt.ylabel("mass in g")
    plt.title("Mass distribution of parts list")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    parts_list_path = (
        Path(__file__).parent.parent.parent / "template" / "parts_list.csv"
    )
    parts: list[Part] = []
    with parts_list_path.open("r") as file:
        parts = parse_parts_list(file)

    visualize_mass_distribution(parts)
