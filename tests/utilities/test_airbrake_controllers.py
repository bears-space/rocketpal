import pytest

import math
from pathlib import Path
from rocketpy import Environment, AirBrakes

from bears_flight_simulation.utilities.airbrake_controllers import (
    stupid_full_extension_controller,
)

ZERO_DRAG_CURVE_PATH = (
    Path(__file__).parent.parent / "__assets__" / "airbrake_zero_drag_curve.csv"
)
REFERENCE_AREA = math.pi * ((0.1236 / 2.0) ** 2.0)  # A = πr²


@pytest.fixture
def standard_airbrakes() -> AirBrakes:
    return AirBrakes(
        drag_coefficient_curve=str(ZERO_DRAG_CURVE_PATH),
        reference_area=REFERENCE_AREA,
        clamp=True,
    )


def test_stupid_full_extension_controller__pad_no_history(standard_airbrakes):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
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


def test_stupid_full_extension_controller__pad_with_history(standard_airbrakes):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
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


def test_stupid_full_extension_controller__ascent_before_treshold(standard_airbrakes):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
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


def test_stupid_full_extension_controller__ascent_after_treshold(standard_airbrakes):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
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


def test_stupid_full_extension_controller__after_apogee(standard_airbrakes):
    _, deployment_level, _ = stupid_full_extension_controller(
        env=Environment(),
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
