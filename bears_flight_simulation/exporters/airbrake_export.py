import matplotlib.pyplot as plt

from rocketpy import Flight


def plot_airbrake_deployment_over_time(flight: Flight, filename: str) -> None:
    # Example code taken from https://docs.rocketpy.org/en/latest/user/airbrakes.html for getting the airbrake states over time
    time_list, deployment_level_list, drag_coefficient_list = [], [], []
    obs_vars = flight.get_controller_observed_variables()
    # TODO: Detect if obs_vars is a list of multiple lists of controller variables (which happens if there is more than one airbrake)
    for time, deployment_level, drag_coefficient in obs_vars:
        time_list.append(time)
        deployment_level_list.append(deployment_level)
        drag_coefficient_list.append(drag_coefficient)

    # Setup plotting
    fig = plt.figure()
    fig.tight_layout()

    # Plot deployment over time
    plt.subplot(2, 1, 1)
    plt.plot(time_list, deployment_level_list)
    plt.xlabel("time in s")
    plt.ylabel("airbrake deployment level")
    plt.title("Airbrake extension over time")

    # Plot drag coefficient over time
    plt.subplot(2, 1, 2)
    plt.plot(time_list, drag_coefficient_list)
    plt.xlabel("time in s")
    plt.ylabel("airbrake drag coefficient")
    plt.title("Airbrake drag coefficient over time")

    # Save plot to file
    fig.subplots_adjust(hspace=0.5)
    plt.savefig(filename)
    plt.close()
