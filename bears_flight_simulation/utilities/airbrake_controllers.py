from rocketpy import AirBrakes, Environment


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

    def __init__(self, data: list) -> None:
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]
        self.v_x = data[3]
        self.v_y = data[4]
        self.v_z = data[5]
        self.e0 = data[6]
        self.e1 = data[7]
        self.e2 = data[8]
        self.e3 = data[9]
        self.w_x = data[10]
        self.w_y = data[11]
        self.w_z = data[12]


def calculate_mach_level(env: Environment, state: State) -> float:
    # Get winds in x and y directions
    wind_x: float = env.wind_velocity_x(state.z)  # type: ignore
    wind_y: float = env.wind_velocity_y(state.z)  # type: ignore

    # Calculate mach number
    free_stream_speed = (
        (wind_x - state.v_x) ** 2 + (wind_y - state.v_y) ** 2 + (state.v_z) ** 2
    ) ** 0.5
    return free_stream_speed / env.speed_of_sound(state.z)


def stupid_full_extension_controller(
    env: Environment,
    time: float,
    sampling_rate: float,
    state_raw: list,
    state_history_raw: list,
    observed_variables: list,
    air_brakes: AirBrakes,
) -> tuple[float, float, float]:
    state_now = State(state_raw)
    state_history = [State(state) for state in state_history_raw]

    was_already_higher_in_the_past = any(
        [state.z > state_now.z for state in state_history]
    )

    if state_now.z >= 1500.0 and not was_already_higher_in_the_past:
        air_brakes.deployment_level = 100.0
    else:
        air_brakes.deployment_level = 0.0

    # NOTE: The real airbrake has to determine the mach level from acceleration only, so access to the "environment" isn't possible in real life!
    mach_number = calculate_mach_level(env, state_now)
    return (
        time,
        air_brakes.deployment_level,
        air_brakes.drag_coefficient(air_brakes.deployment_level, mach_number),  # type: ignore
    )
