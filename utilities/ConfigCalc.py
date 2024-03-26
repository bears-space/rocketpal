import numpy as np


def _grainDensity(propWeight, grain_num, grain_h, grain_or, grain_ir):
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


def _COMs(grain_num, grain_h, grain_sep):
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
    grainCOM = np.mean(np.array(grainCOMs)) + 0.087
    return grainCOM
