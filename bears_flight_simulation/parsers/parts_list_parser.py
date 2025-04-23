import csv
import logging
import re
import typing as t
from dataclasses import dataclass


@dataclass
class Part:
    id_nr: int
    name: str
    hierarchy: list[int]
    mass: float  # in g
    length: float  # in mm
    position_from_bottom_of_compartment: float  # in mm
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
            f"parse_parts_list: {ci_number_and_norm} has empty mass, defaulting to 0.0!"
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
            position_from_bottom_of_compartment=(
                float(row[10]) if row[10] not in ["-", ""] else 0.0
            ),
            radial_distance_to_midline=radial_distance_to_midline,
            radial_direction=radial_direction,
        )

        # Store part
        parts.append(part)

    return parts
