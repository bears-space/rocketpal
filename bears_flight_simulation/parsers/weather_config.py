from bears_flight_simulation.core.library_entry import LibraryEntry


class WeatherConfig(LibraryEntry):
    wind_speeds: set[float]
    wind_directions: set[float]

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        wind_speed_in_m_per_s_min = float(data["wind_speed_in_m_per_s_min"])
        wind_speed_in_m_per_s_max = float(data["wind_speed_in_m_per_s_max"])
        wind_speed_in_m_per_s_step = float(data["wind_speed_in_m_per_s_step"])

        wind_direction_in_degrees_min = float(data["wind_direction_in_degrees_min"])
        wind_direction_in_degrees_max = float(
            data["wind_direction_in_degrees_max_non_inclusive"]
        )
        wind_direction_in_degrees_step = float(data["wind_direction_in_degrees_step"])

        # Generate set of wind speeds
        self.wind_speeds = set()
        wind_speed = wind_speed_in_m_per_s_min
        while wind_speed <= wind_speed_in_m_per_s_max:
            self.wind_speeds.add(wind_speed)
            wind_speed += wind_speed_in_m_per_s_step

        # Generate set of wind directions
        self.wind_directions = set()
        wind_direction = wind_direction_in_degrees_min
        while wind_direction < wind_direction_in_degrees_max:
            self.wind_directions.add(wind_direction)
            wind_direction += wind_direction_in_degrees_step
