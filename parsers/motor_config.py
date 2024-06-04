import typing as t
import yaml

from utilities.ConfigCalc import grainDensity, grainCom


class MotorConfig:
    # Identifier
    id: str

    # Engine file name
    engine_filename: str

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

    def __init__(self, motor_config_yaml_file: t.TextIO) -> None:
        # Load yaml file
        data = yaml.safe_load(motor_config_yaml_file)

        # Parse identifier
        self.id = str(data["ID"])

        # Parse filename of engine
        self.engine_filename = str(data["engFileName"])

        # Parse data
        self.dry_mass = float(data["dryMass"])
        self.dry_inertia = data["dryInertia"]
        self.nozzle_radius = float(data["nozzleR"]) / 1000.0
        self.throat_radius = float(data["throatR"]) / 1000.0
        self.grain_number = int(data["grainNumber"])
        self.grain_outer_radius = float(data["grainOR"]) / 1000.0
        self.grain_initial_inner_radius = float(data["grainIIR"]) / 1000.0
        self.grain_initial_height = float(data["grainIH"]) / 1000.0
        self.grain_separation = float(data["grainSep"]) / 1000.0
        self.burn_time = float(data["burnT"])
        self.nozzle_position = float(data["nozzlePos"])

        # Calculate grain density
        prop_mass = float(data["propMass"])
        self.grain_density = grainDensity(
            prop_mass,
            self.grain_number,
            self.grain_initial_height,
            self.grain_outer_radius,
            self.grain_initial_inner_radius,
        )

        # Calculate center of mass positions
        self.grains_center_of_mass_position = grainCom(
            self.grain_number, self.grain_initial_height, self.grain_separation
        )
        self.center_of_dry_mass_position = self.grains_center_of_mass_position
