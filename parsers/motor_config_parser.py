import typing as t
import yaml


class MotorConfigParser:
    # Physical parameters
    dry_mass: float  # in kg
    dry_inertia: t.List[float]  # in kg/m²
    nozzle_radius: float  # in mm
    throat_radius: float  # in mm

    # Propellant parameters
    grain_number: int
    grain_density: float  # in kg/m³
    grain_outer_radius: float  # in mm
    grain_initial_inner_radius: float  # in mm
    grain_initial_height: float  # in mm
    grain_separation: float  # in mm
    burn_time: float  # in seconds

    # Position parameters
    grains_center_of_mass_position: float  # in m
    center_of_dry_mass_position: float  # in m
    nozzle_position: float  # in m

    def __init__(self, motor_config_yaml_file) -> None:
        # Load yaml file
        data = yaml.safe_load(motor_config_yaml_file)

        # Parse data
        self.dry_mass = float(data["dry mass"])
        self.dry_inertia = data["dry inertia"]
        self.nozzle_radius = float(data["nozzle radius"])
        self.throat_radius = float(data["throat radius"])
        self.grain_number = int(data["grain number"])
        self.grain_density = float(data["grain density"])
        self.outer_radius = float(data["grain outer radius"])
        self.grain_initial_inner_radius = float(data["grain initial inner radius"])
        self.grain_initial_height = float(data["grain initial height"])
        self.grain_separation = float(data["grain separation"])
        self.burn_time = float(data["burn time"])
        self.grains_center_of_mass_position = float(
            data["grains center of mass position"]
        )
        self.center_of_dry_mass_position = float(data["center of dry mass position"])
        self.nozzle_position = float(data["nozzle position"])
