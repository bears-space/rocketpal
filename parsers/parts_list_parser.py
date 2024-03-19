import csv
from dataclasses import dataclass
import logging
import typing as t


@dataclass
class Part:
    id_nr: int
    name: str
    hierarchy: t.List[int]
    mass: float  # in g
    length: float  # in mm
    diameter: float  # in mm
    distance_aft_end_to_aft_end_of_compartment_tube: float  # in mm
    radial_distance_to_midline: float  # in mm
    radial_direction: float  # in degrees


class PartsListParser:
    parts: t.List[Part]

    def __init__(self, parts_list_csv_file: t.TextIO) -> None:
        # Initialize parts list
        self.parts = []

        # Create CSV reader
        reader = csv.reader(parts_list_csv_file, dialect="excel")

        # Skip the first row
        next(reader)

        # From each row, create a Part
        for row in reader:
            # Skip row if any field is "-"
            if "-" in row:
                logging.info(
                    "PartsListParser: Skipping a row because a field is '-' ..."
                )
                continue

            # Convert comma to point in all fields that contain numbers
            for i in [0, 2, 3, 4, 5, 6, 7]:
                row[i] = row[i].replace(",", ".")

            # Create Part
            part = Part(
                id_nr=int(row[0]),
                name=str(row[1]),
                hierarchy=[],
                mass=float(row[2]),
                length=float(row[3]),
                diameter=float(row[4]),
                distance_aft_end_to_aft_end_of_compartment_tube=float(row[5]),
                radial_distance_to_midline=float(row[6]),
                radial_direction=float(row[7]),
            )

            # Parse and add hierarchy info to Part
            segments = part.name.split("_")
            identifiers = segments[0].split(".")
            part.hierarchy = [int(i) for i in identifiers]

            # Store part
            self.parts.append(part)
