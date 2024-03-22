from dataclasses import dataclass
import typing as t
import yaml


@dataclass
class MotorConfig:
    # Physical parameters
    dry_mass: float  # in kg
    dry_inertia: t.List[float]  # in kg/m²
    nozzle_radius: float  # in m
    throat_radius: float  # in m

    # Propellant parameters
    grain_number: int
    grain_density: float  # in kg/m³
    grain_outer_radius: float  # in m
    grain_initial_inner_radius: float  # in m
    grain_initial_height: float  # in m
    grain_separation: float  # in m
    burn_time: float  # in seconds

    # Position parameters
    grains_center_of_mass_position: float  # in m
    center_of_dry_mass_position: float  # in m
    nozzle_position: float  # in m


class MotorConfigParser:
    motor_config: MotorConfig

    def __init__(self, motor_config_yaml_file) -> None:
        # Load yaml file
        data = yaml.safe_load(motor_config_yaml_file)

        # Parse data
        self.motor_config = MotorConfig(
            dry_mass=float(data["dry mass"]),
            dry_inertia=data["dry inertia"],
            nozzle_radius=float(data["nozzle radius"]) / 1000.0,
            throat_radius=float(data["throat radius"]) / 1000.0,
            grain_number=int(data["grain number"]),
            grain_density=float(data["grain density"]),
            grain_outer_radius=float(data["grain outer radius"]) / 1000.0,
            grain_initial_inner_radius=float(data["grain initial inner radius"])
            / 1000.0,
            grain_initial_height=float(data["grain initial height"]) / 1000.0,
            grain_separation=float(data["grain separation"]) / 1000.0,
            burn_time=float(data["burn time"]),
            grains_center_of_mass_position=float(
                data["grains center of mass position"]
            ),
            center_of_dry_mass_position=float(data["center of dry mass position"]),
            nozzle_position=float(data["nozzle position"]),
        )
