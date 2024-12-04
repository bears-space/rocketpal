import typing as t

import yaml


class FinsConfig:
    n: int
    root_chord: float
    tip_chord: float
    span: float
    position: float
    cant_angle: float
    sweep_length: t.Union[float, None]
    sweep_angle: t.Union[float, None]
    radius: t.Union[float, None]

    def __init__(self, fins_config_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(fins_config_file)

        # Load fins data
        self.n = int(data["n"])
        self.root_chord = float(data["root_chord"])
        self.tip_chord = float(data["tip_chord"])
        self.span = float(data["span"])
        self.position = float(data["position"])
        self.cant_angle = float(data["cant_angle"])
        self.sweep_length = data["sweep_length"]
        self.sweep_angle = data["sweep_angle"]
        self.radius = data["radius"]

        # Ensure types for multi-type attributes
        assert type(self.sweep_length) in [float, type(None)]
        assert type(self.sweep_angle) in [float, type(None)]
        assert type(self.radius) in [float, type(None)]
