import csv
from pathlib import Path

from rocketpy import Flight


def export_flight_data_to_csv(flight: Flight, filename: str) -> None:
    # Before export, ensure the folder the file should go into exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    # Open file and write content
    with open(filename, "w") as file:
        # Prepare csv writer object
        writer = csv.writer(file, dialect="excel-tab")

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
        for t in range(0, flight.max_time):
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
