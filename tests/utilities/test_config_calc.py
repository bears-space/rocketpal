from bears_flight_simulation.utilities.config_calc import rocket_center_of_mass


def test_rocket_center_of_mass__empty():
    assert rocket_center_of_mass([]) == (0.0, 0.0, 0.0)
