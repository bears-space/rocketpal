from rocketpy import Environment, Rocket, SolidMotor, Flight
import datetime
from pathlib import Path
import typing as t

from parsers.config import Config
from parsers.fins_config import FinsConfig
from parsers.location import Location
from parsers.motor_config import MotorConfig
from parsers.nose_cone_config import NoseConeConfig
from parsers.parachute_config import ParachuteConfig
from parsers.rail_button_config import RailButtonConfig


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
        parachutes: t.List[ParachuteConfig],
        rail_button_config: RailButtonConfig,
        nose_cone_config: NoseConeConfig,
        power_off_drag_curve_file_path: str,
        power_on_drag_curve_file_path: str,
        fins_config: FinsConfig,
        fins_radians_file_path: str,
        launch_location: Location,
    ) -> None:
        # Store configs / folders
        self.config = config
        self.output_folder = output_folder

        # Setup environment
        self.environment = Environment(
            latitude=launch_location.latitude,
            longitude=launch_location.longitude,
            elevation=launch_location.elevation,
        )
        launch_date = datetime.date.today() + datetime.timedelta(
            days=self.config.date_difference_days
        )
        self.environment.set_date(
            (launch_date.year, launch_date.month, launch_date.day, 12),
            timezone="America/Denver",
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
            nozzle_position=motor_config.nozzle_position,
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
            upper_button_position=rail_button_config.upper_button_position,
            lower_button_position=rail_button_config.lower_button_position,
            angular_position=rail_button_config.angular_position,
        )

        # Add aerodynamic components
        self.rocket.add_nose(
            length=nose_cone_config.length,
            kind=nose_cone_config.kind,
            position=nose_cone_config.position,
            bluffness=nose_cone_config.bluffness,
            power=nose_cone_config.power_if_using_powerseries_kind,
            base_radius=nose_cone_config.base_radius,
        )
        self.rocket.add_trapezoidal_fins(
            n=fins_config.n,
            root_chord=fins_config.root_chord,
            tip_chord=fins_config.tip_chord,
            span=fins_config.span,
            position=fins_config.position,
            cant_angle=fins_config.cant_angle,
            sweep_length=fins_config.sweep_length,
            sweep_angle=fins_config.sweep_angle,
            radius=fins_config.radius,
            airfoil=(fins_radians_file_path, "radians"),
        )

        # Add parachutes
        for parachute in parachutes:
            self.rocket.add_parachute(
                name=parachute.id,
                cd_s=parachute.drag_coefficient_times_reference_area,
                trigger=parachute.ejection_altitude,
                sampling_rate=parachute.ejection_sampling_rate_hertz,
                lag=parachute.opening_lag_seconds,
                noise=(
                    parachute.noise_mean_pascal,
                    parachute.noise_standard_deviation_pascal,
                    parachute.noise_time_correlation_pascal,
                ),
            )

    def simulate(self) -> None:
        # Run the simulation
        self.simulation = Flight(
            rocket=self.rocket,
            environment=self.environment,
            rail_length=self.config.launch_rail_length,  # rail length in meters
            inclination=self.config.inclination,  # inclination to ground in degrees
            heading=self.config.heading,  # launch heading relative to north in degrees
        )

    def show_input_info(self) -> None:
        assert self.environment != None
        assert self.motor != None
        assert self.rocket != None

        # Print environment info
        print("ENVIRONMENT INFO START")
        if self.config.export_text_environment:
            self.environment.prints.all()
        if self.config.export_plot_environment:
            self.environment.plots.info(
                filename=self.output_folder + "/plots/environment.png"
            )
        print("ENVIRONMENT INFO END")

        # Print motor info
        print("MOTOR INFO START")
        if self.config.export_text_motor:
            self.motor.prints.all()
        if self.config.export_plot_thrust:
            self.motor.plots.thrust(
                filename=self.output_folder + "/plots/rocket/motor_thrust.png"
            )
        print("MOTOR INFO END")

        # Show graphics about the rocket
        print("ROCKET GRAPHICS START")
        if self.config.export_plot_static_margin:
            self.rocket.plots.static_margin(
                filename=self.output_folder + "/plots/rocket/static_margin.png"
            )
        if self.config.export_plot_rocket:
            self.rocket.draw(filename=self.output_folder + "/plots/rocket/rocket.png")
        print("ROCKET GRAPHICS END")

    def show_results(self) -> None:
        assert self.simulation != None

        # Print simulation results
        print("RESULTS INFO START")
        if self.config.export_text_simulation:
            self.simulation.prints.all()
        print("RESULTS INFO END")

        # Show simulation results graphics
        print("RESULTS GRAPHICS START")
        if self.config.export_plot_trajectory_3d:
            self.simulation.plots.trajectory_3d(
                filename=self.output_folder + "/plots/results/trajectory_3d.png"
            )
        if self.config.export_plot_linear_kinematic_data:
            self.simulation.plots.linear_kinematics_data(
                filename=self.output_folder + "/plots/results/linear_kinematics.png"
            )
        if self.config.export_plot_flight_path_angle_data:
            self.simulation.plots.flight_path_angle_data(
                filename=self.output_folder
                + "/plots/results/flight_path_angle_data.png"
            )
        if self.config.export_plot_attitude_data:
            self.simulation.plots.attitude_data(
                filename=self.output_folder + "/plots/results/attitude_data.png"
            )
        if self.config.export_plot_angular_kinematics_data:
            self.simulation.plots.angular_kinematics_data(
                filename=self.output_folder
                + "/plots/results/angular_kinematics_data.png"
            )
        if self.config.export_plot_aerodynamic_forces:
            self.simulation.plots.aerodynamic_forces(
                filename=self.output_folder + "/plots/results/aerodynamic_forces.png"
            )
        if self.config.export_plot_rail_buttons_forces:
            self.simulation.plots.rail_buttons_forces(
                filename=self.output_folder + "/plots/results/rail_button_forces.png"
            )
        if self.config.export_plot_energy_data:
            self.simulation.plots.energy_data(
                filename=self.output_folder + "/plots/results/energy_data.png"
            )
        if self.config.export_plot_fluid_mechanics_data:
            self.simulation.plots.fluid_mechanics_data(
                filename=self.output_folder + "/plots/results/fluid_mechanics_data.png"
            )
        if self.config.export_plot_stability_and_control_data:
            self.simulation.plots.stability_and_control_data(
                filename=self.output_folder
                + "/plots/results/stability_and_control_data.png"
            )
        if self.config.export_plot_pressure_rocket_altitude:
            self.simulation.plots.pressure_rocket_altitude(
                filename=self.output_folder
                + "/plots/results/pressure_rocket_altitude.png"
            )
        if self.config.export_plot_pressure_signals:
            for parachute in self.simulation.rocket.parachutes:
                assert parachute.name != None and parachute.name != ""
                foldername = (
                    self.output_folder
                    + "/plots/results/parachutes/"
                    + parachute.name
                    + "/"
                )
                parachute.noise_signal_function(
                    filename=foldername + "noise_signal_function.png"
                )
                parachute.noisy_pressure_signal_function(
                    filename=foldername + "noisy_pressure_signal_function.png"
                )
                parachute.clean_pressure_signal_function(
                    filename=foldername + "clean_pressure_signal_function.png"
                )
        print("RESULTS GRAPHICS END")

    def export_results(self) -> None:
        assert self.simulation != None

        # Before export, ensure output folder exists
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

        # Export raw flight data
        if self.config.export_raw_flight_data:
            self.simulation.export_data(self.output_folder + "/calisto_flight_data.csv")

        # Export trajectory for Google Earth visulization
        if self.config.export_trajectory_for_google_earth:
            self.simulation.export_kml(
                file_name=self.output_folder + "/trajectory.kml",
                extrude=True,
                altitude_mode="relative_to_ground",
            )
