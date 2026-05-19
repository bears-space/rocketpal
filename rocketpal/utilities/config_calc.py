# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import numpy as np

from rocketpal.parsers.parts_list_parser import (
    Part,
    get_part_center_of_mass,
    is_segment_based_on_hierarchy,
    part_is_in_motor_group,
    part_is_motor,
)


def grainDensity(
    propWeight: float, grain_num: int, grain_h: float, grain_or: float, grain_ir: float
) -> float:
    """
    propWeight: propellant weight in kg
    grain_num: amount of grains in motor
    grain_h: height of grain(longitudinal) in m
    grain_or: outer radius of grain in m
    grain_ir: inner radius of grain in m

    grainDens: grain density in kg/m^3
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
    grain_num: amount of grains in motor
    grain_h: height of grain(longitudinal) in m
    grain_sep: seperation gap between grains in m

    grainCOM: center of mass of grain in m !0.087m offset from nozzle position(aft end) to first grain;
              also used for center of mass for dry mass(might be later inputted from CAD model)
    """
    # calculating center of mass position for every grain
    grainCOMs = [
        grain * (grain_h + grain_sep) + (grain_h / 2) for grain in range(grain_num)
    ]
    # calculating center of mass position for all grains with offset of 0.087m (aft end nozzle to first grain)
    grainCOM = float(np.mean(np.array(grainCOMs)) + 0.087)
    return grainCOM


def rocket_cog(
    aft_end_comps, radial_dis_comps, radial_dir_comps, len_comps, mass_comps
):
    """
    Calculates the center of gravity of rocket in reference to the aft end of the rocket!
    Depending on chosen coordinate system this position must be shifted!

    aft_end_comps: list of distances of aft ends of components to aft end of rocket
                   (z component of position); components must be in order of radial_dis_comps,
                   radial_dir_comps, diam_comps, len_comps, mass_comps!
    radial_dis_comps: list of radial distances to rocket's rotational axis in m; components
                      must be in order of aft_end_comps, radial_dir_comps, diam_comps, len_comps,
                      mass_comps!
    radial_dir_comps: list of radial directions in degree (=0°: direction of x-axis of reference point);
                      components must be in order of aft_end_comps, radial_dis_comps, diam_comps, len_comps,
                      mass_comps!
    len_comps: list of lengths/heights of components in m; components must be in order of aft_end_comps, radial_dis_comps,
               radial_dir_comps, diam_comps, mass_comps!
    mass_comps: list of components masses in kg; components must be in order of aft_end_comps, radial_dis_comps,
               radial_dir_comps, diam_comps, len_comps!

    rocketCOG: tuple of position of center of gravity of rocket in m
               FORMAT: (x,y,z)
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
    rocketCOG = COG_temp / mass_total
    return (rocketCOG[0], rocketCOG[1], rocketCOG[2])


def rocket_center_of_mass(
    parts: list[Part],
    ignore_motor: bool = True,
) -> tuple[float, float, float]:
    # Return early if parts is empty
    if len(parts) == 0:
        return (0.0, 0.0, 0.0)

    center_of_mass = np.array([0.0, 0.0, 0.0])
    mass_total = 0.0
    for part in parts:
        # Ignore motor
        if ignore_motor and (
            part_is_motor(part) or part_is_in_motor_group(part, parts)
        ):
            continue

        # Ignore groups
        if is_segment_based_on_hierarchy(part.hierarchy):
            continue

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
        center_of_mass[2] += part.mass * get_part_center_of_mass(part, parts)
    center_of_mass /= mass_total
    return (center_of_mass[0], center_of_mass[1], center_of_mass[2])


def inertia_component(
    refPoint,
    aftEndComp: float,
    radialDis: float,
    radialDir: float,
    diam: float,
    len: float,
    mass: float,
):
    """
    For calculation of inertia of rocket, this function needs to be used for inertia for the corresponding component.
    Then all the resulting inertias need to be summed up to get the inertia of the rocket!

    refPoint: tuple or list of center of dry mass of rocket in m
              (x-axis in direction of radial direction = 0°; y-axis perpendicular;
              z-axis is rocket's rotational axis)
    aftEndComp: distance of aft end of component to reference point of refPoint definition
                (z component of position)
    radialDis: radial distance to rocket's rotational axis in m
    radialDir: radial direction in degree (=0°: direction of x-axis of reference point)
    diam: diameter of component in m
    len: length/height of component in m
    mass: components mass in kg

    inertia: tuple of inertia tensor of rocket without motor in kg*m^2
             (this is recommended to be measured by RocketPy developers)
             FORMAT: (I_11,I_22,I_33,I_12,I_13,I_23)

    It is assummed that I_12=I_13=I_23=0 for the component with local coordinate system (full cylindrical(uniform density and not hollow)).
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
