import typing as t
import yaml


class Config:
    # Identifier
    id: str

    # Input ids
    location_id: str
    motor_ids: t.List[str]
    drag_curve_power_on_file: str
    drag_curve_power_off_file: str

    # Simulation settings
    date_difference_days: int
    launch_rail_length: float
    inclination: float
    heading: float

    # Export options
    export_environment_info: bool
    export_motor_info: bool
    export_rocket_info: bool
    export_simulation_info_text: bool
    export_simulation_info_graphics: bool
    export_raw_flight_data: bool
    export_trajectory_for_google_earth: bool

    def __init__(self, config_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(config_file)

        # Parse identifier
        self.id = str(data["ID"])

        # Parse input ids
        self.location_id = str(data["location"])
        self.motor_ids = data["motors"]
        self.drag_curve_power_on_file = str(data["dragCurvePowerOnFile"])
        self.drag_curve_power_off_file = str(data["dragCurvePowerOffFile"])

        # Parse simulation settings
        self.date_difference_days = int(data["dateDiff"])
        self.launch_rail_length = float(data["railL"])
        self.inclination = float(data["inclination"])
        self.heading = float(data["heading"])

        # Parse export options
        self.export_environment_info = bool(data["exportEnvironmentInfo"])
        self.export_motor_info = bool(data["exportMotorInfo"])
        self.export_rocket_info = bool(data["exportRocketInfo"])
        self.export_simulation_info_text = bool(data["exportSimulationInfoText"])
        self.export_simulation_info_graphics = bool(
            data["exportSimulationInfoGraphics"]
        )
        self.export_raw_flight_data = bool(data["exportRawFlightData"])
        self.export_trajectory_for_google_earth = bool(
            data["exportTrajectoryForGoogleEarth"]
        )
