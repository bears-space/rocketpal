# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from bears_flight_simulation.parsers.motor_config import MotorConfig


def test_serialize():
    serialized = {
        "id": "example",
        "engine_filename": "Cesaroni_6800M3700-P.eng",
        "dry_mass": 2.760,
        "dry_inertia": [0.0, 0.0, 0.0],
        "nozzle_radius": 33.0,
        "throat_radius": 11.0,
        "prop_mass": 3.019,
        "grain_number": 6,
        "grain_outer_radius": 0.033,
        "grain_initial_inner_radius": 0.015,
        "grain_initial_height": 0.120,
        "grain_separation": 0.005,
        "burn_time": 1.83,
        "nozzle_position": 0.0,
        "total_impulse_standard_deviation_factor": 0.1,
    }
    motor_config = MotorConfig(serialized)
    assert motor_config.serialize() == serialized
