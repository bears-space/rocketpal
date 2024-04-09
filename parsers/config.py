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
    # TODO

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
        # TODO
