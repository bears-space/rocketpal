from bears_flight_simulation.parsers.motor_config import MotorConfig


def test_serialize():
    serialized = {
        "ID": "example",
        "engFileName": "Cesaroni_6800M3700-P.eng",
        "dryMass": 2.760,
        "dryInertia": [0.0, 0.0, 0.0],
        "nozzleR": 33.0,
        "throatR": 11.0,
        "propMass": 3.019,
        "grainNumber": 6,
        "grainOR": 33.0,
        "grainIIR": 15.0,
        "grainIH": 120.0,
        "grainSep": 5.0,
        "burnT": 1.83,
        "nozzlePos": 0.0,
        "total_impulse_standard_deviation_factor": 0.1,
    }
    motor_config = MotorConfig(serialized)
    assert motor_config.serialize() == serialized
