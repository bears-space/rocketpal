from rocketpy import Environment, Rocket, SolidMotor, Flight
import datetime
from pathlib import Path

from parsers.config import Config
from parsers.location import Location
from parsers.motor_config import MotorConfig


class FlightSimulation:
    # Configs
    config: Config

    # Simulation stuff
    rocket: Rocket
    simulation: Flight
    environment: Environment
    motor: SolidMotor

    # Folders
    output_folder: str

    def __init__(
        self,
        config: Config,
        output_folder: str,
        motor_file_path: str,
        motor_config: MotorConfig,
        power_off_drag_curve_file_path: str,
        power_on_drag_curve_file_path: str,
        fins_radians_file_path: str,
        launch_location: Location,
    ) -> None:
        # Store configs / folders
        self.config = config
        self.output_folder = output_folder

        # Setup environment
        self.environment = Environment(
            latitude=int(launch_location.latitude),
            longitude=int(launch_location.longitude),
            elevation=int(launch_location.elevation),
        )
        tomorrow = datetime.date.today() + datetime.timedelta(
            days=self.config.date_difference_days
        )
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
            power_off_drag=power_off_drag_curve_file_path,
            power_on_drag=power_on_drag_curve_file_path,
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
            airfoil=(fins_radians_file_path, "radians"),
        )

        # Add parachutes
        self.rocket.add_parachute(
            name="main",
            cd_s=4.0131,  # drag coefficient times reference area of parachute from matlab code
            trigger=300.0,  # ejection altitude in meters
            sampling_rate=100,  # sampling rate for check of parachute trigger in hertz
            lag=2,  # lag until parachute is fully opened after ejection system is triggered in s
            # noise=(0, 8.3, 0.5), # (mean,standard deviation,time-correlation) for noise of pressure signal (trigger function) in pascal
        )
        self.rocket.add_parachute(
            name="drogue",
            cd_s=0.1094,  # drag coefficient times reference area of parachute from matlab code
            trigger="apogee",  # ejection at apogee
            sampling_rate=100,  # sampling rate for check of parachute trigger in hertz
            lag=2,  # lag until parachute is fully opened after ejection system is triggered in s
            # noise=(0, 8.3, 0.5), # (mean,standard deviation,time-correlation) for noise of pressure signal (trigger function) in pascal
        )

    def simulate(self) -> None:
        # Run the simulation
        self.simulation = Flight(
            rocket=self.rocket,
            environment=self.environment,
            rail_length=self.config.launch_rail_length,  # rail length in meters
            inclination=int(
                self.config.inclination
            ),  # inclination to ground in degrees
            heading=int(
                self.config.heading
            ),  # launch heading relative to north in degrees
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
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

        # Export raw flight data
        self.simulation.export_data(self.output_folder + "/calisto_flight_data.csv")

        # Export trajectory for Google Earth visulization
        self.simulation.export_kml(
            file_name=self.output_folder + "/trajectory.kml",
            extrude=True,
            altitude_mode="relative_to_ground",
        )
