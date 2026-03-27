from bears_flight_simulation.parsers.parachute_config import ParachuteConfig


def test_serialize():
    serialized = {
        "ID": "example",
        "drag_coefficient_times_reference_area": 3.936710905,
        "drag_coefficient_times_reference_area_standard_deviation_factor": 0.1,
        "ejection_at_apogee": False,
        "ejection_altitude_meters_if_not_at_apogee": 300.0,
        "ejection_sampling_rate_hertz": 100.0,
        "opening_lag_seconds": 1.0,
        "opening_lag_seconds_standard_deviation_factor": 0.1,
        "noise_mean_pascal": 0.0,
        "noise_standard_deviation_pascal": 0.0,
        "noise_time_correlation_pascal": 0.0,
    }
    parachute_config = ParachuteConfig(serialized)
    assert parachute_config.serialize() == serialized
