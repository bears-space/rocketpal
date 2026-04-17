from bears_flight_simulation.parsers.location_config import LocationConfig


def test_serialize():
    serialized = {
        "id": "example",
        "latitude": 42.0,
        "longitude": 73.0,
        "elevation": 1337.0,
    }
    location = LocationConfig(serialized)
    assert location.serialize() == serialized
