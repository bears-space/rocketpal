import matplotlib.pyplot as plt
from pathlib import Path
import math

from rocketpy import Flight


def plot_airbrake_deployment_over_time(flight: Flight, filepath: Path) -> None:
    # Before export, ensure the folder the file should go into exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Example code taken from https://docs.rocketpy.org/en/latest/user/airbrakes.html for getting the airbrake states over time
    (
        time_list,
        deployment_level_list,
        drag_coefficient_list,
        total_drag_coefficient_list,
    ) = [], [], [], []
    obs_vars = flight.get_controller_observed_variables()
    # TODO: Detect if obs_vars is a list of multiple lists of controller variables (which happens if there is more than one airbrake)
    for time, deployment_level, drag_coefficient in obs_vars:
        time_list.append(time)
        deployment_level_list.append(deployment_level)
        drag_coefficient_list.append(drag_coefficient)
        total_drag_coefficient_list.append(
            drag_coefficient
            + flight.rocket.power_off_drag(
                math.sqrt(
                    flight.vx(time) ** 2 + flight.vy(time) ** 2 + flight.vz(time) ** 2  # type: ignore
                )
            )
        )

    # Setup plotting
    fig = plt.figure(figsize=(16, 9), dpi=300)
    fig.tight_layout()

    # Plot deployment over time
    plt.subplot(2, 1, 1)
    plt.plot(time_list, deployment_level_list)
    plt.grid(visible=True, which="both", axis="both")
    ax = plt.gca()
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    plt.xlabel("time in s")
    plt.ylim(0.0, 1.0)
    plt.ylabel("airbrake deployment level")
    plt.title("Airbrake extension over time")

    # Plot drag coefficient over time
    plt.subplot(2, 1, 2)
    plt.plot(time_list, drag_coefficient_list, label="airbrake")
    plt.plot(time_list, total_drag_coefficient_list, label="total (rocket+airbrake)")
    plt.grid(visible=True, which="both", axis="both")
    ax = plt.gca()
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    plt.xlabel("time in s")
    plt.ylim(bottom=0.0)
    plt.ylabel("airbrake drag coefficient")
    plt.legend()
    plt.title("Airbrake drag coefficient over time")

    # Save plot to file
    fig.subplots_adjust(hspace=0.5)
    plt.savefig(filepath)
    plt.close()
