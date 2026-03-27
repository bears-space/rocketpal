from pathlib import Path

from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig


def test_serialize():
    serialized = {
        "ID": "example",
        "sampling_rate_hz": 10.0,
        "controller_function_name": "disabled_controller",
        "drag_curve_file": "stargaze_airbrake_drag_curve.csv",
        "drag_curve_standard_deviation_factor": 0.1,
    }
    airbrake_config = AirbrakeConfig(serialized, Path(""))
    assert airbrake_config.serialize() == serialized
