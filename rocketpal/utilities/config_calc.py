# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Sequence

import numpy as np

from rocketpal.core.part import Part


def grainDensity(
    propWeight: float, grain_num: int, grain_h: float, grain_or: float, grain_ir: float
) -> float:
    """Calculates the density of the grain based on its dimensions and propellant weight.

    Parameters
    ----------
    propWeight : float
        The total weight of the propellant in kg.
    grain_num : int
        The number of grains in the motor.
    grain_h : float
        The height of each grain (longitudinal) in m.
    grain_or : float
        The outer radius of each grain in m.
    grain_ir : float
        The inner radius of each grain in m.

    Returns
    -------
    float
        The density of the grain in kg/m^3.
    """
    # calculating grain weight
    grainWeight = propWeight / grain_num
    # calculating grain volume
    grainVolume = grain_h * np.pi * (grain_or**2 - grain_ir**2)
    # calculating grain density
    grainDens = grainWeight / grainVolume
    return grainDens


def grainCom(grain_num: int, grain_h: float, grain_sep: float) -> float:
    """Calculates the center of mass of the grains in the motor.

    Parameters
    ----------
    grain_num : int
        The number of grains in the motor.
    grain_h : float
        The height of each grain (longitudinal) in m.
    grain_sep : float
        The separation gap between grains in m.

    Returns
    -------
    float
        The center of mass of the grains in m, measured from the aft end of the motor
    """
    # calculating center of mass position for every grain
    grainCOMs = [
        grain * (grain_h + grain_sep) + (grain_h / 2) for grain in range(grain_num)
    ]
    # calculating center of mass position for all grains with offset of 0.087m (aft end nozzle to first grain)
    # grainCOM: center of mass of grain in m !0.087m offset from nozzle position(aft end) to first grain;
    #           also used for center of mass for dry mass (might be later inputted from CAD model)
    grainCOM = float(np.mean(np.array(grainCOMs)) + 0.087)
    return grainCOM


def calculate_center_of_mass(parts: Sequence[Part]) -> tuple[float, float, float]:
    """Calculate the center of mass of a list of parts

    Parameters
    ----------
    parts : Sequence[Part]
        List of parts

    Returns
    -------
    tuple[float, float, float]
        The center of mass of the parts in the format (x, y, z)
    """
    # Return early if parts is empty
    if not parts:
        return (0.0, 0.0, 0.0)

    masses = np.array([p.mass for p in parts])

    # Prevent ZeroDivisionError inside np.average
    if masses.sum() == 0:
        return (0.0, 0.0, 0.0)

    # Extract geometry into arrays
    r = np.array([p.radial_distance_to_midline for p in parts])
    theta_rad = np.deg2rad([p.radial_direction for p in parts])
    z = np.array([p.center_of_mass for p in parts])

    # Polar -> Cartesian conversion
    x = r * np.cos(theta_rad)
    y = r * np.sin(theta_rad)

    # Weighted average exactly matches the center-of-mass formula
    return (
        np.average(x, weights=masses),
        np.average(y, weights=masses),
        np.average(z, weights=masses),
    )
