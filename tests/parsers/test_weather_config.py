from bears_flight_simulation.parsers.weather_config import WeatherConfig


def test_serialize():
    serialized = {
        "ID": "example",
        "wind_speed_in_m_per_s": 5.0,
        "wind_direction_in_degrees": 90.0,
        "wind_x_y_factor_standard_deviation": 0.1,
    }
    weather_config = WeatherConfig(serialized)
    assert weather_config.serialize() == serialized
