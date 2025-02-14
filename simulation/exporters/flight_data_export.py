import csv
from pathlib import Path
import numpy as np

from rocketpy import Flight, Environment


def export_flight_data_to_csv(
    flight: Flight, filename: str, time_step_seconds: float = 1.0
) -> None:
    """Export selected flight data in csv format, using a constant time step as specified in seconds.

    Parameters
    ----------
    flight : Flight
        The RocketPy flight simulation to extract the data from.
    filename : str
        The file to write the data into, in .csv format.
    time_step_seconds : float, optional
        The constant time step to use, by default 1.0
    """

    # Before export, ensure the folder the file should go into exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    # Open file and write content
    with open(filename, "w") as file:
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
            row.append(flight.x.get_value(t))
            row.append(flight.y.get_value(t))
            row.append(flight.z.get_value(t))

            # velocity x/y/z
            row.append(flight.vx.get_value(t))
            row.append(flight.vy.get_value(t))
            row.append(flight.vz.get_value(t))

            # angular_velocity x/y/z
            row.append(flight.w1.get_value(t))
            row.append(flight.w2.get_value(t))
            row.append(flight.w3.get_value(t))

            # acceleration x/y/z
            row.append(flight.ax.get_value(t))
            row.append(flight.ay.get_value(t))
            row.append(flight.az.get_value(t))

            # acceleration
            row.append(flight.acceleration.get_value(t))

            # pressure
            row.append(flight.pressure.get_value(t))

            writer.writerow(row)


def export_flight_data_to_csv_in_simulated_sensor_module_format(
    flight: Flight,
    filename: str,
    environment: Environment,
    time_step_seconds: float = 1.0,
) -> None:
    """Export selected flight data in csv format, using a constant time step as specified in seconds. The data is formatted in the format that will be used by the sensor module.

    Parameters
    ----------
    flight : Flight
        The RocketPy flight simulation to extract the data from.
    filename : str
        The file to write the data into, in .csv format.
    time_step_seconds : float, optional
        The constant time step to use, by default 1.0
    """

    # Before export, ensure the folder the file should go into exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    # Open file and write content
    with open(filename, "w") as file:
        # Prepare csv writer object
        writer = csv.writer(file, dialect="excel")

        # Write header
        writer.writerow(
            [
                "module_timestamp",  # t
                "temperature",  # in celsius
                "pressure",  # pressure
                "low_g_accel_x",  # ax
                "low_g_accel_y",  # ay
                "low_g_accel_z",  # az
                "high_g_accel_x",  # ax
                "high_g_accel_y",  # ay
                "high_g_accel_z",  # az
                "altitude",
                "velocity_x",  # vx
                "velocity_y",  # vy
                "velocity_z",  # vz
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

            # temperature
            row.append(21.0)

            # pressure
            row.append(flight.pressure.get_value(t))

            # low_g_accel_x, low_g_accel_y, low_g_accel_z
            g_in_ms2 = environment.gravity(0)  # at 0 m above sea
            row.append(
                _clamp_acceleration_to_multiple_of_g(
                    flight.ax.get_value(t), 16.0, g_in_ms2
                )
            )
            row.append(
                _clamp_acceleration_to_multiple_of_g(
                    flight.ay.get_value(t), 16.0, g_in_ms2
                )
            )
            row.append(
                _clamp_acceleration_to_multiple_of_g(
                    flight.az.get_value(t), 16.0, g_in_ms2
                )
            )

            # high_g_accel_x, high_g_accel_y, high_g_accel_z
            row.append(flight.ax.get_value(t))
            row.append(flight.ay.get_value(t))
            row.append(flight.az.get_value(t))

            # altitude
            row.append(flight.altitude.get_value(t))

            # velocity_x, velocity_y, velocity_z
            row.append(flight.vx.get_value(t))
            row.append(flight.vy.get_value(t))
            row.append(flight.vz.get_value(t))

            writer.writerow(row)


def _clamp_acceleration_to_multiple_of_g(
    acceleration_in_ms2: float, multiple_of_g: float, g_in_ms2: float = 9.80665
) -> float:
    abs_limit_in_ms2 = abs(multiple_of_g * g_in_ms2)
    return max(min(acceleration_in_ms2, abs_limit_in_ms2), -abs_limit_in_ms2)
