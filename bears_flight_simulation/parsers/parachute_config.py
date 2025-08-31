import typing as t

from bears_flight_simulation.core.library_entry import LibraryEntry


class ParachuteConfig(LibraryEntry):
    id: str
    drag_coefficient_times_reference_area: float
    drag_coefficient_times_reference_area_standard_deviation_factor: float
    ejection_altitude: t.Union[str, float]  # in meters or "apogee"
    ejection_sampling_rate_hertz: float
    opening_lag_seconds: float
    opening_lag_seconds_standard_deviation_factor: float
    noise_mean_pascal: float
    noise_standard_deviation_pascal: float
    noise_time_correlation_pascal: float

    def __init__(self, data: t.Dict) -> None:
        super().__init__(data)

        # Load parachute data
        self.id = str(data["ID"])
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
