import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import math

from rocketpy import Flight

TIME_STEP_SECONDS = 0.1


def plot_altitude_over_time(flight: Flight, filename: str) -> None:
    # Before export, ensure the folder the file should go into exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    time_list, altitude_list, vx_list, vy_list, vz_list, v_total_list = (
        [],
        [],
        [],
        [],
        [],
        [],
    )
    max_time = flight.t_final
    for t in np.linspace(
        0.0,
        max_time,
        round(max_time / TIME_STEP_SECONDS) + 1,
        endpoint=True,
    ):
        time_list.append(t)
        altitude_list.append(flight.z.get_value(t))  # type: ignore
        vx_list.append(flight.vx.get_value(t))  # type: ignore
        vy_list.append(flight.vy.get_value(t))  # type: ignore
        vz_list.append(flight.vz.get_value(t))  # type: ignore
        v_total_list.append(
            math.sqrt(
                flight.vx.get_value(t) ** 2  # type: ignore
                + flight.vy.get_value(t) ** 2  # type: ignore
                + flight.vz.get_value(t) ** 2  # type: ignore
            )
        )

    # Setup plotting
    fig = plt.figure(figsize=(16, 9), dpi=300)
    fig.tight_layout()

    # Plot altitude over time
    plt.subplot(2, 1, 1)
    plt.plot(time_list, altitude_list)
    plt.grid(visible=True, which="both", axis="both")
    ax = plt.gca()
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    plt.xlabel("time in s")
    plt.ylim(bottom=0.0)
    plt.ylabel("altitude in m")
    plt.title("Altitude over time")

    # Plot velocities over time
    plt.subplot(2, 1, 2)
    plt.plot(time_list, vx_list, label="vx")
    plt.plot(time_list, vy_list, label="vy")
    plt.plot(time_list, vz_list, label="vz")
    plt.grid(visible=True, which="both", axis="both")
    ax = plt.gca()
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    plt.xlabel("time in s")
    plt.ylabel("velocity in m/s")
    plt.legend()
    plt.title("Velocity over time")

    # Save plot to file
    plt.savefig(filename)
    plt.close()
