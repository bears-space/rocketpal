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


def stupid_full_extension_controller(
    env: Environment,
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
