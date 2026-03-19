import math
from pathlib import Path

import pytest
from rocketpy import AirBrakes, Environment, Rocket

from bears_flight_simulation.utilities.airbrake_controllers import (
    State,
    stupid_full_extension_controller,
)

ZERO_DRAG_CURVE_PATH = (
    Path(__file__).parent.parent / "__assets__" / "airbrake_zero_drag_curve.csv"
)
ROCKET_POWER_OFF_DRAG_CURVE_PATH = (
    Path(__file__).parent.parent / "__assets__" / "stargaze_power_off_drag_curve.csv"
)
ROCKET_POWER_ON_DRAG_CURVE_PATH = (
    Path(__file__).parent.parent / "__assets__" / "stargaze_power_on_drag_curve.csv"
)
REFERENCE_AREA = math.pi * ((0.1236 / 2.0) ** 2.0)  # A = πr²


@pytest.fixture
def standard_airbrakes() -> AirBrakes:
    return AirBrakes(
        drag_coefficient_curve=str(ZERO_DRAG_CURVE_PATH),
        reference_area=REFERENCE_AREA,
        clamp=True,
    )


@pytest.fixture
def standard_rocket() -> Rocket:
    return Rocket(
        radius=0.1236,
        mass=18.38121,
        inertia=(6.321, 6.321, 0.034),
        power_off_drag=str(ROCKET_POWER_OFF_DRAG_CURVE_PATH),
        power_on_drag=str(ROCKET_POWER_OFF_DRAG_CURVE_PATH),
        center_of_mass_without_motor=0,
    )


def test_state__now_format():
    X = 42.0
    Y = 43.0
    Z = 44.0
    V_X = 45.0
    V_Y = 46.0
    V_Z = 47.0
    E0 = 48.0
    E1 = 49.0
    E2 = 50.0
    E3 = 51.0
    W_X = 52.0
    W_Y = 53.0
    W_Z = 54.0
    state = State([X, Y, Z, V_X, V_Y, V_Z, E0, E1, E2, E3, W_X, W_Y, W_Z], offset=0)
    assert state.x == X
    assert state.y == Y
    assert state.z == Z
    assert state.v_x == V_X
    assert state.v_y == V_Y
    assert state.v_z == V_Z
    assert state.e0 == E0
    assert state.e1 == E1
    assert state.e2 == E2
    assert state.e3 == E3
    assert state.w_x == W_X
    assert state.w_y == W_Y
    assert state.w_z == W_Z


def test_state__history_format():
    TIME = 41.0
    X = 42.0
    Y = 43.0
    Z = 44.0
    V_X = 45.0
    V_Y = 46.0
    V_Z = 47.0
    E0 = 48.0
    E1 = 49.0
    E2 = 50.0
    E3 = 51.0
    W_X = 52.0
    W_Y = 53.0
    W_Z = 54.0
    state = State(
        [TIME, X, Y, Z, V_X, V_Y, V_Z, E0, E1, E2, E3, W_X, W_Y, W_Z], offset=1
    )
    assert state.x == X
    assert state.y == Y
    assert state.z == Z
    assert state.v_x == V_X
    assert state.v_y == V_Y
    assert state.v_z == V_Z
    assert state.e0 == E0
    assert state.e1 == E1
    assert state.e2 == E2
    assert state.e3 == E3
    assert state.w_x == W_X
    assert state.w_y == W_Y
    assert state.w_z == W_Z


def test_stupid_full_extension_controller__pad_no_history(
    standard_airbrakes, standard_rocket
):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
        rocket=standard_rocket,
        time=2.0,
        sampling_rate=10.0,
        state_raw=[
            0.0,
            0.0,
            0.0,  # z = 0m
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        state_history_raw=[],
        observed_variables=[],
        air_brakes=standard_airbrakes,
    )
    assert deployment_level == 0.0


def test_stupid_full_extension_controller__pad_with_history(
    standard_airbrakes, standard_rocket
):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
        rocket=standard_rocket,
        time=2.0,
        sampling_rate=10.0,
        state_raw=[
            0.0,
            0.0,
            0.0,  # z = 0m
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        state_history_raw=[[0] * 15] * 100,  # 100 on-pad states with z=0m
        observed_variables=[],
        air_brakes=standard_airbrakes,
    )
    assert deployment_level == 0.0


def test_stupid_full_extension_controller__ascent_before_treshold(
    standard_airbrakes, standard_rocket
):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
        rocket=standard_rocket,
        time=2.0,
        sampling_rate=10.0,
        state_raw=[
            0.0,
            0.0,
            1100.0,  # z = 1100m
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        state_history_raw=[
            [0.0] * 3 + [i * 10.0] + [0.0] * 11 for i in range(100)
        ],  # 100 ascent states with 0.0 <= z <= 1000.0
        observed_variables=[],
        air_brakes=standard_airbrakes,
    )
    assert deployment_level == 0.0


def test_stupid_full_extension_controller__ascent_after_treshold(
    standard_airbrakes, standard_rocket
):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
        rocket=standard_rocket,
        time=2.0,
        sampling_rate=10.0,
        state_raw=[
            0.0,
            0.0,
            2500.0,  # z = 2500m
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        state_history_raw=[
            [0.0] * 3 + [i * 10.0] + [0.0] * 11 for i in range(200)
        ],  # 100 ascent states with 0.0 <= z <= 2000.0
        observed_variables=[],
        air_brakes=standard_airbrakes,
    )
    assert deployment_level == 1.0


def test_stupid_full_extension_controller__after_apogee(
    standard_airbrakes, standard_rocket
):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
        rocket=standard_rocket,
        time=30.0,
        sampling_rate=10.0,
        state_raw=[
            0.0,
            0.0,
            1700.0,  # z = 1700m
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        state_history_raw=[
            [0.0] * 3 + [i * 100.0] + [0.0] * 11 for i in range(30)
        ]  # 30 ascent states with 0.0 <= z <= 3000.0
        + [
            [0.0] * 3 + [3000.0 - i * 100.0] + [0.0] * 11 for i in range(10)
        ],  # 10 descent states with 0.0 <= z <= 3000.0
        observed_variables=[],
        air_brakes=standard_airbrakes,
    )
    assert deployment_level == 0.0
