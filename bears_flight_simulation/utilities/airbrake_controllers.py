from rocketpy import AirBrakes, Environment, Rocket

import logging
import math


GRAVITY_CONSTANT = 9.80665  # in m/s²
PRINT_AIRBRAKE_STATUS = True


class State:
    x: float
    y: float
    z: float
    v_x: float
    v_y: float
    v_z: float
    e0: float
    e1: float
    e2: float
    e3: float
    w_x: float
    w_y: float
    w_z: float

    def __init__(self, data: list, offset: int = 0) -> None:
        self.x = data[0 + offset]
        self.y = data[1 + offset]
        self.z = data[2 + offset]
        self.v_x = data[3 + offset]
        self.v_y = data[4 + offset]
        self.v_z = data[5 + offset]
        self.e0 = data[6 + offset]
        self.e1 = data[7 + offset]
        self.e2 = data[8 + offset]
        self.e3 = data[9 + offset]
        self.w_x = data[10 + offset]
        self.w_y = data[11 + offset]
        self.w_z = data[12 + offset]


def calculate_mach_level(env: Environment, state: State) -> float:
    # Get winds in x and y directions
    wind_x: float = env.wind_velocity_x(state.z)  # type: ignore
    wind_y: float = env.wind_velocity_y(state.z)  # type: ignore

    # Calculate mach number
    free_stream_speed = (
        (wind_x - state.v_x) ** 2 + (wind_y - state.v_y) ** 2 + (state.v_z) ** 2
    ) ** 0.5
    return free_stream_speed / env.speed_of_sound(state.z)


def smooth_deployment_change(
    current_deployment: float,
    target_deployment: float,
    seconds_per_full_movement: float,
    delta_t_in_seconds: float,
) -> float:
    delta_deployment = target_deployment - current_deployment
    full_movements_per_second = 1.0 / seconds_per_full_movement
    max_change_in_given_delta_t = full_movements_per_second * delta_t_in_seconds
    change = max(
        min(delta_deployment, max_change_in_given_delta_t), -max_change_in_given_delta_t
    )
    return current_deployment + change


def disabled_controller(
    env: Environment,
    rocket: Rocket,
    time: float,
    sampling_rate: float,
    state_raw: list,
    state_history_raw: list,
    observed_variables: list,
    air_brakes: AirBrakes,
) -> tuple[float, float, float]:
    state_now = State(state_raw, offset=0)

    air_brakes.deployment_level = 0.0

    # NOTE: The real airbrake has to determine the mach level from acceleration only, so access to the "environment" isn't possible in real life!
    mach_number = calculate_mach_level(env, state_now)
    return (
        time,
        air_brakes.deployment_level,
        air_brakes.drag_coefficient(air_brakes.deployment_level, mach_number),  # type: ignore
    )


def enabled_controller(
    env: Environment,
    rocket: Rocket,
    time: float,
    sampling_rate: float,
    state_raw: list,
    state_history_raw: list,
    observed_variables: list,
    air_brakes: AirBrakes,
) -> tuple[float, float, float]:
    state_now = State(state_raw, offset=0)

    air_brakes.deployment_level = 1.0

    # NOTE: The real airbrake has to determine the mach level from acceleration only, so access to the "environment" isn't possible in real life!
    mach_number = calculate_mach_level(env, state_now)
    return (
        time,
        air_brakes.deployment_level,
        air_brakes.drag_coefficient(air_brakes.deployment_level, mach_number),  # type: ignore
    )


def stupid_full_extension_controller(
    env: Environment,
    rocket: Rocket,
    time: float,
    sampling_rate: float,
    state_raw: list,
    state_history_raw: list,
    observed_variables: list,
    air_brakes: AirBrakes,
) -> tuple[float, float, float]:
    state_now = State(state_raw, offset=0)
    state_history = [State(state, offset=1) for state in state_history_raw]

    max_z = 0.0
    for state in state_history:
        max_z = max(state.z, max_z)
    was_already_higher_in_the_past = state_now.z < max_z

    if state_now.z >= 1500.0 and not was_already_higher_in_the_past:
        air_brakes.deployment_level = 1.0
    else:
        air_brakes.deployment_level = 0.0

    # NOTE: The real airbrake has to determine the mach level from acceleration only, so access to the "environment" isn't possible in real life!
    mach_number = calculate_mach_level(env, state_now)
    return (
        time,
        air_brakes.deployment_level,
        air_brakes.drag_coefficient(air_brakes.deployment_level, mach_number),  # type: ignore
    )


def estimate_apogee_via_propagation(
    env: Environment,
    airbrake: AirBrakes,
    rocket: Rocket,
    state_now: State,
    time_step_seconds: float = 0.1,
) -> float:
    vx = state_now.v_x
    vy = state_now.v_y
    v_horizontal = math.sqrt(vx**2 + vy**2)
    vz = state_now.v_z

    A = rocket.area
    mass_burnout = rocket.dry_mass

    z = state_now.z
    while True:
        z += vz * time_step_seconds

        density = env.density(z)
        adjusted_state = State(
            [
                state_now.x,
                state_now.y,
                z,
                v_horizontal,
                0.0,
                vz,
                state_now.e0,
                state_now.e1,
                state_now.e2,
                state_now.e3,
                state_now.w_x,
                state_now.w_y,
                state_now.w_z,
            ]
        )
        mach_level = calculate_mach_level(env, adjusted_state)
        drag_coefficient = airbrake.drag_coefficient(
            airbrake.deployment_level, mach_level
        ) + rocket.power_off_drag(mach_level)  # type: ignore
        a_drag = (
            density
            * (v_horizontal**2 + vz**2)
            * 0.5
            * A
            * drag_coefficient
            / mass_burnout
        )

        elevation_angle_radians = math.atan(vz / v_horizontal)

        a_horizontal = -a_drag * math.cos(elevation_angle_radians)
        v_horizontal += a_horizontal * time_step_seconds

        az_total = -GRAVITY_CONSTANT - (a_drag * math.sin(elevation_angle_radians))
        assert az_total < 0.0
        vz += az_total * time_step_seconds

        if vz <= 0.0:
            return z


def stargaze_airbrake_controller(
    env: Environment,
    rocket: Rocket,
    time: float,
    sampling_rate: float,
    state_raw: list,
    state_history_raw: list,
    observed_variables: list,
    air_brakes: AirBrakes,
) -> tuple[float, float, float]:
    state_now = State(state_raw, offset=0)
    state_history = [State(state, offset=1) for state in state_history_raw]

    TARGET_APOGEE = float(env.elevation) + 3000.0
    TIME_FOR_FULL_EXTENSION = 0.8  # in seconds

    launched = any([state.z > 0.0 for state in state_history])
    above_1500m = state_now.z >= float(env.elevation) + 1500.0
    above_2500m = state_now.z >= float(env.elevation) + 2500.0
    apogee_reached = any([state.z > state_now.z for state in state_history])

    # Decide on the airbrake deployment level to select
    selected_deployment: float
    if not launched or not above_1500m or apogee_reached:
        selected_deployment = 0.0
        if PRINT_AIRBRAKE_STATUS:
            logging.info(f"AIRBRAKE: t={time}, z={state_now.z}")
    else:
        if above_2500m:
            selected_deployment = 1.0
        else:
            # Estimate apogee
            apogee_estimation: float = estimate_apogee_via_propagation(
                env,
                air_brakes,
                rocket,
                state_now,
                time_step_seconds=1.0 / sampling_rate,
            )
            if PRINT_AIRBRAKE_STATUS:
                logging.info(
                    f"AIRBRAKE: t={time}, z={state_now.z}, vz={state_now.v_z}, apogee_estimation={apogee_estimation}, deployment={air_brakes.deployment_level}"
                )

            # Change selected deployment level accordingly
            # TODO better control logic
            if apogee_estimation > TARGET_APOGEE:
                selected_deployment = 1.0
            else:
                selected_deployment = 0.0

    air_brakes.deployment_level = smooth_deployment_change(
        current_deployment=air_brakes.deployment_level,
        target_deployment=selected_deployment,
        seconds_per_full_movement=TIME_FOR_FULL_EXTENSION,
        delta_t_in_seconds=1.0 / sampling_rate,
    )

    # NOTE: The real airbrake has to determine the mach level from acceleration only, so access to the "environment" isn't possible in real life!
    mach_number = calculate_mach_level(env, state_now)
    return (
        time,
        air_brakes.deployment_level,
        air_brakes.drag_coefficient(air_brakes.deployment_level, mach_number),  # type: ignore
    )
