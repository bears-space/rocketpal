import typing as t

import yaml


class NoseConeConfig:
    kind: str
    bluffness: float
    power_if_using_powerseries_kind: t.Union[float, None]
    base_radius: t.Union[float, None]

    def __init__(self, nose_cone_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(nose_cone_file)

        # Load nose cone data
        self.kind = str(data["kind"])
        self.bluffness = float(data["bluffness"])
        self.power_if_using_powerseries_kind = data["power_if_using_powerseries_kind"]
        self.base_radius = data["base_radius"]

        # Ensure types for multi-type attributes
        assert type(self.power_if_using_powerseries_kind) in [float, type(None)]
        assert type(self.base_radius) in [float, type(None)]
