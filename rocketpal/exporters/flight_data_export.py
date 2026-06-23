# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import csv
from pathlib import Path

import numpy as np
from rocketpy import Environment, Flight


def export_flight_data_to_csv(
    flight: Flight, filepath: Path, time_step_seconds: float = 1.0
) -> None:
    """Export selected flight data in csv format, using a constant time step as specified in seconds.

    Parameters
    ----------
    flight : Flight
        The RocketPy flight simulation to extract the data from.
    filepath : Path
        The file to write the data into, in .csv format.
    time_step_seconds : float, optional
        The constant time step to use, by default 1.0
    """

    # Before export, ensure the folder the file should go into exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Open file and write content
    with open(filepath, "w") as file:
        # Prepare csv writer object
        writer = csv.writer(file, dialect="excel")

        # Write header
        writer.writerow(
            [
                "time",  # t
                "position_x",  # x
                "position_y",  # y
                "position_z",  # z
                "velocity_x",  # vx
                "velocity_y",  # vy
                "velocity_z",  # vz
                "angular_velocity_1",  # w1
                "angular_velocity_2",  # w2
                "angular_velocity_3",  # w3
                "acceleration_x",  # ax
                "acceleration_y",  # ay
                "acceleration_z",  # az
                "acceleration",  # acceleration
                "pressure",  # pressure
                # "flight_phases", # flight_phases
            ]
        )

        # Write flight data row-by-row
        for t in np.linspace(
            0.0,
            flight.max_time,
            round(flight.max_time / time_step_seconds) + 1,
            endpoint=True,
        ):
            row = []

            # time
            row.append(t)

            # position x/y/z
            row.append(flight.x.get_value(t))  # type: ignore
            row.append(flight.y.get_value(t))  # type: ignore
            row.append(flight.z.get_value(t))  # type: ignore

            # velocity x/y/z
            row.append(flight.vx.get_value(t))  # type: ignore
            row.append(flight.vy.get_value(t))  # type: ignore
            row.append(flight.vz.get_value(t))  # type: ignore

            # angular_velocity x/y/z
            row.append(flight.w1.get_value(t))  # type: ignore
            row.append(flight.w2.get_value(t))  # type: ignore
            row.append(flight.w3.get_value(t))  # type: ignore

            # acceleration x/y/z
            row.append(flight.ax.get_value(t))  # type: ignore
            row.append(flight.ay.get_value(t))  # type: ignore
            row.append(flight.az.get_value(t))  # type: ignore

            # acceleration
            row.append(flight.acceleration.get_value(t))  # type: ignore

            # pressure
            row.append(flight.pressure.get_value(t))  # type: ignore

            writer.writerow(row)


def export_flight_data_to_csv_in_simulated_sensor_module_format(
    flight: Flight,
    filepath: Path,
    environment: Environment,
    time_step_seconds: float = 1.0,
) -> None:
    """Export selected flight data in csv format, using a constant time step as specified in seconds. The data is formatted in the format that will be used by the sensor module.

    Parameters
    ----------
    flight : Flight
        The RocketPy flight simulation to extract the data from.
    filepath : Path
        The file to write the data into, in .csv format.
    time_step_seconds : float, optional
        The constant time step to use, by default 1.0
    """

    # Before export, ensure the folder the file should go into exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Open file and write content
    with open(filepath, "w") as file:
        # Prepare csv writer object
        writer = csv.writer(file, dialect="excel")

        # Write header
        writer.writerow(
            [
                "module_timestamp",  # t
                "gps_longitude",
                "gps_latitude",
                "gps_altitude",
                "gps_time",
                "temperature",  # in celsius
                "pressure",  # pressure
                "low_g_accel_x",  # ax
                "low_g_accel_y",  # ay
                "low_g_accel_z",  # az
                "angular_velocity_1",  # w1
                "angular_velocity_2",  # w2
                "angular_velocity_3",  # w3
                "high_g_accel_x",  # ax
                "high_g_accel_y",  # ay
                "high_g_accel_z",  # az
            ]
        )

        # Write flight data row-by-row
        for t in np.linspace(
            0.0,
            flight.max_time,
            round(flight.max_time / time_step_seconds) + 1,
            endpoint=True,
        ):
            row = []

            # module_timestamp
            row.append(t)

            # gps_longitude, gps_latitude, gps_altitude, gps_time
            row.append(flight.longitude.get_value(t))  # type: ignore
            row.append(flight.latitude.get_value(t))  # type: ignore
            row.append(flight.altitude.get_value(t))  # type: ignore
            row.append("placeholder")

            # temperature
            row.append(21.0)

            # pressure
            row.append(flight.pressure.get_value(t))  # type: ignore

            # low_g_accel_x, low_g_accel_y, low_g_accel_z at 0m above sea level
            g_in_ms2 = float(environment.gravity(0))  # type: ignore
            (
                converted_acceleration_x,
                converted_acceleration_y,
                converted_acceleration_z,
            ) = _convert_acceleration_from_ground_reference_frame_to_rocket_reference_frame(
                flight.ax.get_value(t),  # type: ignore
                flight.ay.get_value(t),  # type: ignore
                flight.az.get_value(t),  # type: ignore
                flight.phi.get_value(t),  # type: ignore
                flight.theta.get_value(t),  # type: ignore
                flight.psi.get_value(t),  # type: ignore
            )
            row.append(
                _clamp_acceleration_to_multiple_of_g(
                    converted_acceleration_x, 16.0, g_in_ms2
                )
            )
            row.append(
                _clamp_acceleration_to_multiple_of_g(
                    converted_acceleration_y, 16.0, g_in_ms2
                )
            )
            row.append(
                _clamp_acceleration_to_multiple_of_g(
                    converted_acceleration_z, 16.0, g_in_ms2
                )
            )

            # angular_velocity x/y/z
            row.append(flight.w1.get_value(t))  # type: ignore
            row.append(flight.w2.get_value(t))  # type: ignore
            row.append(flight.w3.get_value(t))  # type: ignore

            # high_g_accel_x, high_g_accel_y, high_g_accel_z
            row.append(converted_acceleration_x)
            row.append(converted_acceleration_y)
            row.append(converted_acceleration_z)

            writer.writerow(row)


def _convert_acceleration_from_ground_reference_frame_to_rocket_reference_frame(
    ax: float, ay: float, az: float, phi: float, theta: float, psi: float
):
    # NOTE this is black magic, do not touch
    az = -az
    theta = theta + 90.0
    phi = np.deg2rad(phi)
    theta = np.deg2rad(theta)
    psi = np.deg2rad(psi)
    t_fg = np.array(
        [
            [np.cos(psi) * np.cos(theta), np.cos(theta) * np.sin(psi), -np.sin(theta)],
            [
                np.cos(psi) * np.sin(phi) * np.sin(theta) - np.cos(phi) * np.sin(psi),
                np.cos(phi) * np.cos(psi) + np.sin(phi) * np.sin(psi) * np.sin(theta),
                np.cos(theta) * np.sin(phi),
            ],
            [
                np.sin(phi) * np.sin(psi) + np.cos(phi) * np.cos(psi) * np.sin(theta),
                np.cos(phi) * np.sin(psi) * np.sin(theta) - np.cos(psi) * np.sin(phi),
                np.cos(phi) * np.cos(theta),
            ],
        ]
    )
    acceleration = np.array([[ax], [ay], [az]])
    converted_acceleration = np.dot(t_fg, acceleration)
    return (
        converted_acceleration[0][0],
        converted_acceleration[1][0],
        converted_acceleration[2][0],
    )


def _clamp_acceleration_to_multiple_of_g(
    acceleration_in_ms2: float, multiple_of_g: float, g_in_ms2: float = 9.80665
) -> float:
    abs_limit_in_ms2 = abs(multiple_of_g * g_in_ms2)
    return max(min(acceleration_in_ms2, abs_limit_in_ms2), -abs_limit_in_ms2)
