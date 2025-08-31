from bears_flight_simulation.core.library_entry import LibraryEntry


class WeatherConfig(LibraryEntry):
    wind_speed: float
    wind_direction: float
    wind_x_y_factor_standard_distribution: float

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.wind_speed = float(data["wind_speed_in_m_per_s"])
        self.wind_direction = float(data["wind_direction_in_degrees"])
        self.wind_x_y_factor_standard_distribution = float(
            data["wind_x_y_factor_standard_deviation"]
        )
