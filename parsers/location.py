import typing as t
import yaml


class Location:
    latitude: float
    longitude: float
    elevation: float

    def __init__(self, launch_location_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(launch_location_file)

        self.latitude = float(data["latitude"])
        self.longitude = float(data["longitude"])
        self.elevation = float(data["elevation"])
