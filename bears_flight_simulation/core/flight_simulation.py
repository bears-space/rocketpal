import logging
from pathlib import Path

from bears_flight_simulation.parsers.config import Config
from bears_flight_simulation.parsers.fins_config import FinsConfig
from bears_flight_simulation.parsers.location import Location
from bears_flight_simulation.parsers.motor_config import MotorConfig
from bears_flight_simulation.parsers.nose_cone_config import NoseConeConfig
from bears_flight_simulation.parsers.parachute_config import ParachuteConfig
from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig
from bears_flight_simulation.parsers.parts_list_parser import (
    Part,
    get_nosecone,
    get_nosecone_position,
    get_motor_position,
)
from bears_flight_simulation.parsers.rail_button_config import RailButtonConfig
from rocketpy import Environment, Flight, Rocket, SolidMotor

from bears_flight_simulation.utilities.rocket_calculations import (
    calculate_rocket_mass_without_motor_in_kg,
)
from bears_flight_simulation.utilities.config_calc import rocket_center_of_mass
from bears_flight_simulation.exporters.flight_data_export import (
    export_flight_data_to_csv,
    export_flight_data_to_csv_in_simulated_sensor_module_format,
)


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
        parachutes: list[ParachuteConfig],
        airbrakes: list[AirbrakeConfig],
        rail_button_config: RailButtonConfig,
        nose_cone_config: NoseConeConfig,
        power_off_drag_curve_file_path: str,
        power_on_drag_curve_file_path: str,
        fins_config: FinsConfig,
        launch_location: Location,
        parts: list[Part],
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
        self.environment.set_date(config.launch_date)
        # self.environment.set_atmospheric_model(type="Forecast", file="GFS")
        self.environment.set_atmospheric_model(type="standard_atmosphere")

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
        rocket_mass_without_motor = calculate_rocket_mass_without_motor_in_kg(parts)
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor) is {rocket_mass_without_motor}kg"
        )
        self.rocket = Rocket(
            radius=config.diameter / 2.0,  # 127 / 2000,
            mass=rocket_mass_without_motor,  # 14.426,
            inertia=(6.321, 6.321, 0.034),
            power_off_drag=power_off_drag_curve_file_path,
            power_on_drag=power_on_drag_curve_file_path,
            center_of_mass_without_motor=rocket_center_of_mass(parts)[2] / 1000.0,
            coordinate_system_orientation="tail_to_nose",
        )
        logging.info(
            f"FlightSimulation: ROCKET COM WITHOUT MOTOR is {rocket_center_of_mass(parts)}"
        )
        logging.info(
            f"FlightSimulation: ROCKET COM WITH MOTOR is {rocket_center_of_mass(parts, ignore_motor=False)}"
        )

        # Add motor to rocket
        self.rocket.add_motor(self.motor, position=get_motor_position(parts) / 1000.0)

        # Add rail guides
        self.rocket.set_rail_buttons(
            upper_button_position=rail_button_config.upper_button_position,
            lower_button_position=rail_button_config.lower_button_position,
            angular_position=rail_button_config.angular_position,
        )

        # Add aerodynamic components
        nosecone_length = get_nosecone(parts).length
        self.rocket.add_nose(
            length=nosecone_length / 1000.0,
            kind=nose_cone_config.kind,
            position=(
                get_nosecone_position(parts) + nosecone_length
            )  # HACK: offset nosecone by length
            / 1000.0,  # nose_cone_config.position,
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

        # Add airbrakes
        for airbrake in airbrakes:
            # TODO Add airbrakes to the rocket (including controller functions)
            # self.rocket.add_air_brakes()
            logging.info(
                f"FlightSimulation: ignoring configured airbrake '{airbrake.id}' (not implemented yet)"
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
        assert self.environment is not None
        assert self.motor is not None
        assert self.rocket is not None

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
        # print("ROCKET GRAPHICS START")
        if self.config.export_plot_static_margin:
            self.rocket.plots.static_margin(
                filename=self.output_folder + "/plots/rocket/static_margin.png"
            )
        if self.config.export_plot_rocket:
            self.rocket.draw(filename=self.output_folder + "/plots/rocket/rocket.png")
        # print("ROCKET GRAPHICS END")

    def show_results(self) -> None:
        assert self.simulation is not None

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
                assert parachute.name is not None and parachute.name != ""
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
                    filename=foldername + "noisy_pressure_signal_function.png"
                )
        print("RESULTS GRAPHICS END")

    def export_results(self) -> None:
        assert self.simulation is not None

        # Before export, ensure output folder exists
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

        # Export raw flight data
        if self.config.export_raw_flight_data:
            self.simulation.export_data(self.output_folder + "/raw_flight_data.csv")

        # Export flight data to csv
        if self.config.export_flight_data:
            export_flight_data_to_csv(
                self.simulation,
                self.output_folder + "/custom_flight_data.csv",
                self.config.export_flight_data_time_step_seconds,
            )

        # Export simulated sensor module data to csv
        if self.config.export_flight_data:
            export_flight_data_to_csv_in_simulated_sensor_module_format(
                self.simulation,
                self.output_folder + "/simulated_sensor_module_data.csv",
                self.environment,
                self.config.export_flight_data_time_step_seconds,
            )

        # Export trajectory for Google Earth visulization
        if self.config.export_trajectory_for_google_earth:
            self.simulation.export_kml(
                file_name=self.output_folder + "/trajectory.kml",
                extrude=True,
                altitude_mode="relative_to_ground",
            )
