from bears_flight_simulation.core.library_entry import LibraryEntry


class ParachuteConfig(LibraryEntry):
    drag_coefficient_times_reference_area: float
    drag_coefficient_times_reference_area_standard_deviation_factor: float
    ejection_altitude: str | float  # in meters or "apogee"
    ejection_sampling_rate_hertz: float
    opening_lag_seconds: float
    opening_lag_seconds_standard_deviation_factor: float
    noise_mean_pascal: float
    noise_standard_deviation_pascal: float
    noise_time_correlation_pascal: float

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        # Load parachute data
        self.drag_coefficient_times_reference_area = float(
            data["drag_coefficient_times_reference_area"]
        )
        self.drag_coefficient_times_reference_area_standard_deviation_factor = float(
            data["drag_coefficient_times_reference_area_standard_deviation_factor"]
        )
        self.ejection_sampling_rate_hertz = float(data["ejection_sampling_rate_hertz"])
        self.opening_lag_seconds = float(data["opening_lag_seconds"])
        self.opening_lag_seconds_standard_deviation_factor = float(
            data["opening_lag_seconds_standard_deviation_factor"]
        )
        self.noise_mean_pascal = float(data["noise_mean_pascal"])
        self.noise_standard_deviation_pascal = float(
            data["noise_standard_deviation_pascal"]
        )
        self.noise_time_correlation_pascal = float(
            data["noise_time_correlation_pascal"]
        )

        # Load ejection altitude data
        ejection_at_apogee = bool(data["ejection_at_apogee"])
        if ejection_at_apogee:
            self.ejection_altitude = "apogee"
        else:
            self.ejection_altitude = float(
                data["ejection_altitude_meters_if_not_at_apogee"]
            )

    @classmethod
    def new_default(cls, id: str) -> "ParachuteConfig":
        return ParachuteConfig(
            {
                "ID": id,
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
        )

    def serialize(self) -> dict:
        ejection_at_apogee = True
        ejection_altitude_meters_if_not_at_apogee = 0
        if self.ejection_altitude != "apogee":
            ejection_at_apogee = False
            assert not isinstance(self.ejection_altitude, str)
            ejection_altitude_meters_if_not_at_apogee = float(self.ejection_altitude)

        return {
            "ID": self.id,
            "drag_coefficient_times_reference_area": self.drag_coefficient_times_reference_area,
            "drag_coefficient_times_reference_area_standard_deviation_factor": self.drag_coefficient_times_reference_area_standard_deviation_factor,
            "ejection_at_apogee": ejection_at_apogee,
            "ejection_altitude_meters_if_not_at_apogee": ejection_altitude_meters_if_not_at_apogee,
            "ejection_sampling_rate_hertz": self.ejection_sampling_rate_hertz,
            "opening_lag_seconds": self.opening_lag_seconds,
            "opening_lag_seconds_standard_deviation_factor": self.opening_lag_seconds_standard_deviation_factor,
            "noise_mean_pascal": self.noise_mean_pascal,
            "noise_standard_deviation_pascal": self.noise_standard_deviation_pascal,
            "noise_time_correlation_pascal": self.noise_time_correlation_pascal,
        }
