# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import dataclass


@dataclass
class Part:
    mass: float  # in g
    center_of_mass: float  # in mm
    name: str = "unnamed"
    length = 0.0  # in mm
    parent: Part | None = None
    position_relative_to_parent: float = 0.0  # in mm
    radial_distance_to_midline: float = 0.0  # in mm
    radial_direction: float = 0.0  # in degrees
