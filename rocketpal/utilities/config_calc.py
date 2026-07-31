# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import numpy as np

from rocketpal.core.part import Part


def grainDensity(
    propWeight: float, grain_num: int, grain_h: float, grain_or: float, grain_ir: float
) -> float:
    """
    Calculates the density of the grain based on its dimensions and propellant weight.

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
    """
    Calculates the center of mass of the grains in the motor.

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


def rocket_cog(
    aft_end_comps: list[float],
    radial_dis_comps: list[float],
    radial_dir_comps: list[float],
    len_comps: list[float],
    mass_comps: list[float],
) -> tuple[float, float, float]:
    """
    Calculates the center of gravity of the rocket in reference to the aft end of the rocket.
    Depending on the chosen coordinate system, this position must be shifted.

    Parameters
    ----------
    aft_end_comps : list[float]
        List of distances of aft ends of components to aft end of rocket (z component of position); components must be in order of radial_dis_comps, radial_dir_comps, diam_comps, len_comps, mass_comps.
    radial_dis_comps : list[float]
        List of radial distances to rocket's rotational axis in m; components must be in order of aft_end_comps, radial_dir_comps, diam_comps, len_comps, mass_comps.
    radial_dir_comps : list[float]
        List of radial directions in degrees (=0°: direction of x-axis of reference point); components must be in order of aft_end_comps, radial_dis_comps, diam_comps, len_comps, mass_comps.
    len_comps : list[float]
        List of lengths/heights of components in m; components must be in order of aft_end_comps, radial_dis_comps, radial_dir_comps, diam_comps, mass_comps.
    mass_comps : list[float]
        List of components masses in kg; components must be in order of aft_end_comps, radial_dis_comps, radial_dir_comps, diam_comps, len_comps.

    Returns
    -------
    tuple[float, float, float]
        The center of gravity of the rocket in m, in the format (x, y, z).
    """
    COG_temp = np.array([0, 0, 0])
    mass_total = 0
    for index, comp in enumerate(mass_comps):
        mass_total += comp
        COG_temp[0] += (
            comp * radial_dis_comps[index] * np.cos(np.deg2rad(radial_dir_comps[index]))
        )
        COG_temp[1] += (
            comp * radial_dis_comps[index] * np.sin(np.deg2rad(radial_dir_comps[index]))
        )
        COG_temp[2] += comp * (aft_end_comps[index] + len_comps[index] / 2)

    # rocketCOG: tuple of position of center of gravity of rocket in m. FORMAT: (x,y,z)
    rocketCOG = COG_temp / mass_total
    return (rocketCOG[0], rocketCOG[1], rocketCOG[2])


def calculate_center_of_mass(
    parts: list[Part],
) -> tuple[float, float, float]:
    """Calculate the center of mass of a list of parts

    Parameters
    ----------
    parts : list[Part]
        List of parts

    Returns
    -------
    tuple[float, float, float]
        The center of mass of the parts in the format (x, y, z)
    """

    # Return early if parts is empty
    if len(parts) == 0:
        return (0.0, 0.0, 0.0)

    center_of_mass = np.array([0.0, 0.0, 0.0])
    mass_total = 0.0
    for part in parts:
        mass_total += part.mass
        center_of_mass[0] += (
            part.mass
            * part.radial_distance_to_midline
            * np.cos(np.deg2rad(part.radial_direction))
        )
        center_of_mass[1] += (
            part.mass
            * part.radial_distance_to_midline
            * np.sin(np.deg2rad(part.radial_direction))
        )
        center_of_mass[2] += part.mass * part.center_of_mass

    # Return early if total mass is zero to avoid division by zero
    if mass_total == 0:
        return (0.0, 0.0, 0.0)

    center_of_mass /= mass_total
    return (center_of_mass[0], center_of_mass[1], center_of_mass[2])


def inertia_component(
    refPoint: tuple[float, float, float],
    aftEndComp: float,
    radialDis: float,
    radialDir: float,
    diam: float,
    len: float,
    mass: float,
) -> tuple[float, float, float, float, float, float]:
    """
    Calculate the inertia tensor contribution of one rocket component.

    Parameters
    ----------
    refPoint : tuple[float, float, float]
        The reference point for the inertia tensor calculation, typically the center of mass of the rocket.
    aftEndComp : float
        The distance from the aft end of the rocket to the aft end of the component.
    radialDis : float
        The radial distance of the component from the rocket's central axis.
    radialDir : float
        The radial direction of the component in degrees, where 0° is aligned with the x-axis of the reference point.
    diam : float
        The diameter of the component.
    len : float
        The length of the component.
    mass : float
        The mass of the component.

    Returns
    -------
    tuple[float, float, float, float, float, float]
        The inertia tensor contribution of the component, represented as a tuple of six unique elements in the order (I_11, I_22, I_33, I_12, I_13, I_23).
    """
    radius = diam / 2
    # calculating cylindrical inertia w.r.t. local center of mass (assumend uniform density)
    inertia_local = np.array(
        [
            [mass * (3 * radius**2 + len**2) / 12, 0, 0],
            [0, mass * (3 * radius**2 + len**2) / 12, 0],
            [0, 0, mass * radius**2 / 2],
        ]
    )
    z_local = aftEndComp + len / 2
    y_local = radialDis * np.sin(np.deg2rad(radialDir))
    x_local = radialDis * np.cos(np.deg2rad(radialDir))

    # distance between reference point (COG of rocket) and COG of component
    distance_ref_local = [
        refPoint[0] - x_local,
        refPoint[1] - y_local,
        refPoint[2] - z_local,
    ]

    # calculation of inertia shift due to distance between reference and local COG
    inertia_diff = np.array(
        [
            [
                distance_ref_local[1] ** 2 + distance_ref_local[2] ** 2,
                -distance_ref_local[0] * distance_ref_local[1],
                -distance_ref_local[0] * distance_ref_local[2],
            ],
            [
                -distance_ref_local[0] * distance_ref_local[1],
                distance_ref_local[0] ** 2 + distance_ref_local[2] ** 2,
                -distance_ref_local[1] * distance_ref_local[2],
            ],
            [
                -distance_ref_local[0] * distance_ref_local[2],
                -distance_ref_local[1] * distance_ref_local[2],
                distance_ref_local[0] ** 2 + distance_ref_local[1] ** 2,
            ],
        ]
    )
    # calculating inertia w.r.t. reference point (COG of rocket)
    inertia = inertia_local + mass * inertia_diff
    # inertia reference point is center_of_mass_without_motor (dry mass)
    return (
        inertia[0][0],
        inertia[1][1],
        inertia[2][2],
        inertia[0][1],
        inertia[0][2],
        inertia[1][2],
    )
