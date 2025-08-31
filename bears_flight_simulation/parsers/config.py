from datetime import datetime
import typing as t

import yaml


class Config:
    # Identifier
    id: str

    # Input ids
    location_id: str
    weather_config_id: str
    motor_ids: list[str]
    drag_curve_power_on_file: str
    drag_curve_power_off_file: str
    parachute_ids: list[str]
    airbrake_ids: list[str]

    # Simulation settings
    date_difference_days: int
    launch_rail_length: float
    inclination: float
    heading: float
    launch_date: datetime

    # Rocket settings
    diameter: float

    # Export options
    export_flight_data_time_step_seconds: float

    def __init__(self, config_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(config_file)

        # Parse identifier
        self.id = str(data["ID"])

        # Parse input ids
        self.location_id = str(data["location"])
        self.weather_config_id = str(data["weatherConfig"])
        self.motor_ids = data["motors"]
        self.drag_curve_power_on_file = str(data["dragCurvePowerOnFile"])
        self.drag_curve_power_off_file = str(data["dragCurvePowerOffFile"])
        self.parachute_ids = data["parachutes"]
        self.airbrake_ids = data["airbrakes"]

        # Parse simulation settings
        self.date_difference_days = int(data["dateDiff"])
        self.launch_rail_length = float(data["railL"])
        self.inclination = float(data["inclination"])
        self.heading = float(data["heading"])
        self.launch_date = datetime.strptime(
            str(data["launch_date"]), "%Y-%m-%d_%H-%M-%S"
        )

        # Parse rocket settings
        self.diameter = float(data["diameter"])

        # Parse export options
        self.export_flight_data_time_step_seconds = float(
            data["exportFlightDataTimeStepSeconds"]
        )
