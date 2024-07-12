import typing as t
import yaml


class RailButtonConfig:
    # Rail button data
    upper_button_position: float
    lower_button_position: float
    angular_position: float

    def __init__(self, rail_button_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(rail_button_file)

        # Load rail button data
        self.upper_button_position = float(data["upper_button_position"])
        self.lower_button_position = float(data["lower_button_position"])
        self.angular_position = float(data["angular_position"])
