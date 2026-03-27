from bears_flight_simulation.parsers.location import Location


def test_serialize():
    serialized = {
        "ID": "example",
        "latitude": 42.0,
        "longitude": 73.0,
        "elevation": 1337.0,
    }
    location = Location(serialized)
    assert location.serialize() == serialized
