from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.utilities.config_calc import grainCom, grainDensity


class MotorConfig(LibraryEntry):
    # Engine file name
    engine_filename: str

    # Physical parameters
    dry_mass: float  # in kg
    dry_inertia: list[float]  # in kg/m²
    nozzle_radius: float  # in m
    throat_radius: float  # in m

    # Propellant parameters
    prop_mass: float  # in kg
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

    # Monte Carlo parameters
    total_impulse_standard_deviation_factor: float

    def __init__(self, data: dict) -> None:
        super().__init__(data)

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
        self.total_impulse_standard_deviation_factor = float(
            data["total_impulse_standard_deviation_factor"]
        )

        # Calculate grain density
        self.prop_mass = float(data["propMass"])
        self.grain_density = grainDensity(
            self.prop_mass,
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

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return MotorConfig(
            {
                "ID": id,
                "engFileName": "Cesaroni_6800M3700-P.eng",
                "dryMass": 2.760,
                "dryInertia": [0.0, 0.0, 0.0],
                "nozzleR": 33.0,
                "throatR": 11.0,
                "propMass": 3.019,
                "grainNumber": 6,
                "grainOR": 33.0,
                "grainIIR": 15.0,
                "grainIH": 120.0,
                "grainSep": 5.0,
                "burnT": 1.83,
                "nozzlePos": 0.0,
                "total_impulse_standard_deviation_factor": 0.1,
            }
        )

    def serialize(self) -> dict:
        return {
            "ID": self.id,
            "engFileName": self.engine_filename,
            "dryMass": self.dry_mass,
            "dryInertia": self.dry_inertia,
            "nozzleR": self.nozzle_radius * 1000.0,
            "throatR": self.throat_radius * 1000.0,
            "propMass": self.prop_mass,
            "grainNumber": self.grain_number,
            "grainOR": self.grain_outer_radius * 1000.0,
            "grainIIR": self.grain_initial_inner_radius * 1000.0,
            "grainIH": self.grain_initial_height * 1000.0,
            "grainSep": self.grain_separation * 1000.0,
            "burnT": self.burn_time,
            "nozzlePos": self.nozzle_position,
            "total_impulse_standard_deviation_factor": self.total_impulse_standard_deviation_factor,
        }
