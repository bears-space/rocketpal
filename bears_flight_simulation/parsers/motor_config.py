from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.utilities.config_calc import grainCom, grainDensity


class MotorConfig(LibraryEntry):
    # Propellant parameters
    prop_mass: float  # in kg

    # Position parameters
    grains_center_of_mass_position: float  # in m
    center_of_dry_mass_position: float  # in m
    nozzle_position: float  # in m

    # Monte Carlo parameters
    total_impulse_standard_deviation_factor: float

    def __init__(self, data: dict) -> None:
        self.extend_field_links(
            [
                ("engine_filename", str),
                ("dry_mass", float),
                ("dry_inertia", list),
                ("nozzle_radius", float),
                ("throat_radius", float),
                ("prop_mass", float),
                ("grain_number", int),
                ("grain_outer_radius", float),
                ("grain_initial_inner_radius", float),
                ("grain_initial_height", float),
                ("grain_separation", float),
                ("burn_time", float),
                ("nozzle_position", float),
                ("total_impulse_standard_deviation_factor", float),
            ]
        )
        super().__init__(data)

        # Calculate grain density
        self.grain_density = grainDensity(
            self.prop_mass,  # type: ignore
            self.grain_number,  # type: ignore
            self.grain_initial_height,  # type: ignore
            self.grain_outer_radius,  # type: ignore
            self.grain_initial_inner_radius,  # type: ignore
        )

        # Calculate center of mass positions
        self.grains_center_of_mass_position = grainCom(
            self.grain_number,  # type: ignore
            self.grain_initial_height,  # type: ignore
            self.grain_separation,  # type: ignore
        )
        self.center_of_dry_mass_position = self.grains_center_of_mass_position

    @classmethod
    def new_default(cls, id: str) -> LibraryEntry:
        return MotorConfig(
            {
                "id": id,
                "engine_filename": "Cesaroni_6800M3700-P.eng",
                "dry_mass": 2.760,
                "dry_inertia": [0.0, 0.0, 0.0],
                "nozzle_radius": 33.0,
                "throat_radius": 11.0,
                "prop_mass": 3.019,
                "grain_number": 6,
                "grain_outer_radius": 0.033,
                "grain_initial_inner_radius": 0.015,
                "grain_initial_height": 0.120,
                "grain_separation": 0.005,
                "burn_time": 1.83,
                "nozzle_position": 0.0,
                "total_impulse_standard_deviation_factor": 0.1,
            }
        )
