from rocketpy import Environment, Rocket, SolidMotor, Flight
import datetime
from pathlib import Path

from parsers.motor_config_parser import MotorConfig


class FlightSimulation:
    rocket: Rocket
    simulation: Flight
    environment: Environment
    motor: SolidMotor

    def __init__(self, motor_file_path: str, motor_config: MotorConfig) -> None:
        # NOTE This is temporary test code based on RocketPy docs, see https://docs.rocketpy.org/en/latest/user/first_simulation.html

        # Setup environment
        self.environment = Environment(
            latitude=int(32.990254), longitude=int(-106.974998), elevation=1400
        )
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.environment.set_date(
            (tomorrow.year, tomorrow.month, tomorrow.day, 12), timezone="America/Denver"
        )
        self.environment.set_atmospheric_model(type="Forecast", file="GFS")

        # Setup motor
        self.motor = SolidMotor(
            thrust_source=motor_file_path,
            dry_mass=motor_config.dry_mass,
            dry_inertia=motor_config.dry_inertia,
            nozzle_radius=motor_config.nozzle_radius,
            grain_number=motor_config.grain_number,
            grain_density=motor_config.grain_density,
            grain_outer_radius=motor_config.grain_outer_radius,
            grain_initial_inner_radius=motor_config.grain_initial_inner_radius,
            grain_initial_height=motor_config.grain_initial_height,
            grain_separation=motor_config.grain_separation,
            grains_center_of_mass_position=motor_config.grains_center_of_mass_position,
            center_of_dry_mass_position=motor_config.center_of_dry_mass_position,
            nozzle_position=int(
                motor_config.nozzle_position
            ),  # TODO This really should be float, fix this typing issue on RocketPy's side
            burn_time=motor_config.burn_time,
            throat_radius=motor_config.throat_radius,
            coordinate_system_orientation="nozzle_to_combustion_chamber",
        )

        # Create rocket
        self.rocket = Rocket(
            radius=127 / 2000,
            mass=14.426,
            inertia=(6.321, 6.321, 0.034),
            power_off_drag="data/calisto/powerOffDragCurve.csv",
            power_on_drag="data/calisto/powerOnDragCurve.csv",
            center_of_mass_without_motor=0,
            coordinate_system_orientation="tail_to_nose",
        )

        # Add motor to rocket
        self.rocket.add_motor(self.motor, position=-1.255)

        # Add rail guides
        self.rocket.set_rail_buttons(
            upper_button_position=0.0818,
            lower_button_position=-0.6182,
            angular_position=45,
        )

        # Add aerodynamic components
        self.rocket.add_nose(length=0.55829, kind="von karman", position=1.278)
        self.rocket.add_trapezoidal_fins(
            n=4,
            root_chord=0.120,
            tip_chord=0.060,
            span=0.110,
            position=-1.04956,
            cant_angle=int(0.5),
            airfoil=("data/calisto/NACA0012-radians.csv", "radians"),
        )
        self.rocket.add_tail(
            top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
        )

        # Add parachutes
        self.rocket.add_parachute(
            name="main",
            cd_s=10.0,
            trigger=800,  # ejection altitude in meters
            sampling_rate=105,
            lag=int(1.5),
            noise=(0, 8.3, 0.5),
        )
        self.rocket.add_parachute(
            name="drogue",
            cd_s=1.0,
            trigger="apogee",  # ejection at apogee
            sampling_rate=105,
            lag=int(1.5),
            noise=(0, 8.3, 0.5),
        )

    def simulate(self) -> None:
        # Run the simulation
        self.simulation = Flight(
            rocket=self.rocket,
            environment=self.environment,
            rail_length=5.2,
            inclination=85,
            heading=0,
        )

    def show_input_info(self) -> None:
        assert self.environment != None
        assert self.motor != None
        assert self.rocket != None

        # Print environment info
        print("ENVIRONMENT INFO START")
        self.environment.info()
        print("ENVIRONMENT INFO END")

        # Print motor info
        print("MOTOR INFO START")
        self.motor.info()
        print("MOTOR INFO END")

        # Show graphics about the rocket
        print("ROCKET GRAPHICS START")
        self.rocket.plots.static_margin()
        self.rocket.draw()
        print("ROCKET GRAPHICS END")

    def show_results(self) -> None:
        assert self.simulation != None

        # Print simulation results
        print("RESULTS INFO START")
        self.simulation.info()
        print("RESULTS INFO END")

        # Show simulation results graphics
        print("RESULTS GRAPHICS START")
        self.simulation.all_info()
        print("RESULTS GRAPHICS END")

    def export_results(self) -> None:
        assert self.simulation != None

        # Before export, ensure output folder exists
        Path("output").mkdir(parents=True, exist_ok=True)

        # Export raw flight data
        self.simulation.export_data("output/calisto_flight_data.csv")

        # Export trajectory for Google Earth visulization
        self.simulation.export_kml(
            file_name="output/trajectory.kml",
            extrude=True,
            altitude_mode="relative_to_ground",
        )
