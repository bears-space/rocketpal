import logging
from pathlib import Path
import math

from bears_flight_simulation.parsers.config import Config
from bears_flight_simulation.parsers.fins_config import FinsConfig
from bears_flight_simulation.parsers.location import Location
from bears_flight_simulation.parsers.motor_config import MotorConfig
from bears_flight_simulation.parsers.nose_cone_config import NoseConeConfig
from bears_flight_simulation.parsers.parachute_config import ParachuteConfig
from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig
from bears_flight_simulation.parsers.weather_config import WeatherConfig
from bears_flight_simulation.parsers.parts_list_parser import (
    Part,
    get_nosecone_total_length,
    get_nosecone_tip_position_plus_length,
    get_motor_position,
)
from bears_flight_simulation.parsers.rail_button_config import RailButtonConfig
from rocketpy import Environment, Flight, Rocket, SolidMotor, AirBrakes, MonteCarlo
from rocketpy.stochastic import (
    StochasticEnvironment,
    StochasticFlight,
    StochasticNoseCone,
    StochasticParachute,
    StochasticRailButtons,
    StochasticRocket,
    StochasticSolidMotor,
    StochasticTail,
    StochasticTrapezoidalFins,
)

from bears_flight_simulation.utilities.rocket_calculations import (
    calculate_rocket_mass_without_motor_in_kg,
    calculate_rocket_mass_in_kg,
)
from bears_flight_simulation.utilities.config_calc import rocket_center_of_mass
from bears_flight_simulation.exporters.flight_data_export import (
    export_flight_data_to_csv,
    export_flight_data_to_csv_in_simulated_sensor_module_format,
)
from bears_flight_simulation.exporters.airbrake_export import (
    plot_airbrake_deployment_over_time,
)
from bears_flight_simulation.exporters.altitude_plots import plot_altitude_over_time


def wind_speed_and_direction_to_east_and_north(
    wind_speed: float, wind_direction: float
) -> tuple[float, float]:
    # Convert from RocketPy direction convention to east-north-positive convention
    wind_direction = (-wind_direction) - 90.0

    wind_direction_rad = math.radians(wind_direction)
    east_component = math.cos(wind_direction_rad)
    north_component = math.sin(wind_direction_rad)
    return (east_component * wind_speed, north_component * wind_speed)


class FlightSimulation:
    # Configs
    config: Config

    # Simulation stuff
    rocket: Rocket
    flight: Flight
    environment: Environment
    motor: SolidMotor
    stochastic_environment: StochasticEnvironment
    stochastic_motor: StochasticSolidMotor
    stochastic_rocket: StochasticRocket
    stochastic_flight: StochasticFlight

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
        weather_config: WeatherConfig,
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
        # self.environment.set_atmospheric_model(type="standard_atmosphere")
        (wind_east, wind_north) = wind_speed_and_direction_to_east_and_north(
            weather_config.wind_speed, weather_config.wind_direction
        )
        self.environment.set_atmospheric_model(
            type="custom_atmosphere",
            pressure=None,
            temperature=None,
            wind_u=[(0, wind_east)],  # type: ignore
            wind_v=[(0, wind_north)],  # type: ignore
        )
        # self.environment.set_atmospheric_model(type="Ensemble", file="GEFS")
        self.stochastic_environment = StochasticEnvironment(
            environment=self.environment,
            wind_velocity_x_factor=(
                1.0,
                weather_config.wind_x_y_factor_standard_distribution,
            ),
            wind_velocity_y_factor=(
                1.0,
                weather_config.wind_x_y_factor_standard_distribution,
            ),
        )

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
        self.stochastic_motor = StochasticSolidMotor(
            solid_motor=self.motor,
            burn_start_time=0.1,
            total_impulse=100,
        )

        # Create rocket
        rocket_mass_without_motor = calculate_rocket_mass_without_motor_in_kg(parts)
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor) is {rocket_mass_without_motor}kg"
        )
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor + motor drymass) is {rocket_mass_without_motor + motor_config.dry_mass}kg"
        )
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor + motor drymass + motor propmass) is {rocket_mass_without_motor + motor_config.dry_mass + motor_config.prop_mass}kg"
        )
        logging.info(
            f"FlightSimulation: calculated rocket mass (complete parts list) is {calculate_rocket_mass_in_kg(parts)}kg"
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
        self.stochastic_rocket = StochasticRocket(
            rocket=self.rocket,
            mass=0.05,
            center_of_mass_without_motor=0.05,
        )
        logging.info(
            f"FlightSimulation: ROCKET COM WITHOUT MOTOR is {rocket_center_of_mass(parts)}"
        )
        logging.info(
            f"FlightSimulation: ROCKET COM WITH MOTOR is {rocket_center_of_mass(parts, ignore_motor=False)}"
        )

        # Add motor to rocket
        self.rocket.add_motor(self.motor, position=get_motor_position(parts) / 1000.0)
        self.stochastic_rocket.add_motor(self.stochastic_motor)

        # Add rail guides
        self.rocket.set_rail_buttons(
            upper_button_position=rail_button_config.upper_button_position,
            lower_button_position=rail_button_config.lower_button_position,
            angular_position=rail_button_config.angular_position,
        )

        # Add aerodynamic components
        nosecone_length = get_nosecone_total_length(parts) / 1000.0
        nosecone_tip_upper_limit_position = (
            get_nosecone_tip_position_plus_length(parts) / 1000.0
        )
        logging.info(
            f"FlightSimulation: Configured nosecone with length={nosecone_length}m, upper_position_limit={nosecone_tip_upper_limit_position}m based on parts list"
        )
        self.rocket.add_nose(
            length=nosecone_length,
            kind=nose_cone_config.kind,
            position=nosecone_tip_upper_limit_position,
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
            # Create an airbrake controller function where the environment is pre-filled
            def airbrake_controller_function(
                time: float,
                sampling_rate: float,
                state_raw: list,
                state_history_raw: list,
                observed_variables: list,
                air_brakes: AirBrakes,
            ):
                return airbrake.controller_function(
                    self.environment,
                    self.rocket,
                    time,
                    sampling_rate,
                    state_raw,
                    state_history_raw,
                    observed_variables,
                    air_brakes,
                )

            # Actually add the controller function
            self.rocket.add_air_brakes(
                drag_coefficient_curve=airbrake.drag_curve_filepath,
                controller_function=airbrake_controller_function,
                sampling_rate=airbrake.sampling_rate_hz,
                clamp=True,
                name=airbrake.id,
            )

        logging.info(
            f"FlightSimulation: calculated rocket mass (rocket.evaluate_dry_mass) is {self.rocket.evaluate_dry_mass()}kg"
        )

        # Print uncertainties of the stochastic classes
        self.stochastic_environment.visualize_attributes()
        self.stochastic_motor.visualize_attributes()
        self.stochastic_rocket.visualize_attributes()

    def simulate(self) -> None:
        # Run the simulation
        self.flight = Flight(
            rocket=self.rocket,
            environment=self.environment,
            rail_length=self.config.launch_rail_length,  # rail length in meters
            inclination=self.config.inclination,  # inclination to ground in degrees
            heading=self.config.heading,  # launch heading relative to north in degrees
        )

        # Run the monte carlo (stochastic) simulation
        self.stochastic_flight = StochasticFlight(
            flight=self.flight,
            inclination=1.0,
            heading=2.0,
        )
        self.stochastic_flight.visualize_attributes()
        # ensure subfolder exists
        Path(self.output_folder + "/monte_carlo_analysis").mkdir(parents=True, exist_ok=True)
        self.monte_carlo_simulation = MonteCarlo(
            filename=self.output_folder + "/monte_carlo_analysis/monte_carlo_class",
            environment=self.stochastic_environment,
            rocket=self.stochastic_rocket,
            flight=self.stochastic_flight,
        )
        self.monte_carlo_simulation.simulate(
            number_of_simulations=self.config.number_of_simulations,
            append=False,
            include_function_data=False,
            parallel=self.config.parallel,
            n_workers=self.config.n_workers,
        )

    def show_input_info(self) -> None:
        assert self.environment is not None
        assert self.motor is not None
        assert self.rocket is not None

        # Print environment info
        print("ENVIRONMENT INFO START")
        self.environment.prints.all()
        self.environment.plots.info(
            filename=self.output_folder + "/plots/environment.png"
        )
        print("ENVIRONMENT INFO END")

        # Print motor info
        print("MOTOR INFO START")
        self.motor.prints.all()
        self.motor.plots.thrust(
            filename=self.output_folder + "/plots/rocket/motor_thrust.png"
        )
        print("MOTOR INFO END")

        # Show graphics about the rocket
        self.rocket.plots.static_margin(
            filename=self.output_folder + "/plots/rocket/static_margin.png"
        )
        self.rocket.draw(filename=self.output_folder + "/plots/rocket/rocket.png")

    def show_results(self) -> None:
        assert self.flight is not None

        # Print simulation results
        print("TRADITIONAL RESULTS INFO START")
        self.flight.prints.all()
        print("TRADITIONAL RESULTS INFO END")

        # Show simulation results graphics
        print("TRADITIONAL RESULTS GRAPHICS START")
        self.flight.plots.trajectory_3d(
            filename=self.output_folder + "/plots/results/trajectory_3d.png"
        )
        self.flight.plots.linear_kinematics_data(
            filename=self.output_folder + "/plots/results/linear_kinematics.png"
        )
        self.flight.plots.flight_path_angle_data(
            filename=self.output_folder + "/plots/results/flight_path_angle_data.png"
        )
        self.flight.plots.attitude_data(
            filename=self.output_folder + "/plots/results/attitude_data.png"
        )
        self.flight.plots.angular_kinematics_data(
            filename=self.output_folder + "/plots/results/angular_kinematics_data.png"
        )
        self.flight.plots.aerodynamic_forces(
            filename=self.output_folder + "/plots/results/aerodynamic_forces.png"
        )
        self.flight.plots.rail_buttons_forces(
            filename=self.output_folder + "/plots/results/rail_button_forces.png"
        )
        # NOTE: The energy data plot crashes when an airbrake is configured
        if len(self.config.airbrake_ids) == 0:
            self.flight.plots.energy_data(
                filename=self.output_folder + "/plots/results/energy_data.png"
            )
        self.flight.plots.fluid_mechanics_data(
            filename=self.output_folder + "/plots/results/fluid_mechanics_data.png"
        )
        self.flight.plots.stability_and_control_data(
            filename=self.output_folder
            + "/plots/results/stability_and_control_data.png"
        )
        self.flight.plots.pressure_rocket_altitude(
            filename=self.output_folder + "/plots/results/pressure_rocket_altitude.png"
        )
        for parachute in self.flight.rocket.parachutes:
            assert parachute.name is not None and parachute.name != ""
            foldername = (
                self.output_folder + "/plots/results/parachutes/" + parachute.name + "/"
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
        if len(self.config.airbrake_ids) > 0:
            plot_airbrake_deployment_over_time(
                self.flight,
                filename=self.output_folder + "/plots/results/airbrake_deployment.png",
            )
        plot_altitude_over_time(
            self.flight,
            filename=self.output_folder + "/plots/results/altitude_over_time.png",
        )
        print("TRADITIONAL RESULTS GRAPHICS END")

        print(f"number of loaded sims: {self.monte_carlo_simulation}")
        self.monte_carlo_simulation.prints.all()
        self.monte_carlo_simulation.plots.ellipses(save=True)
        self.monte_carlo_simulation.plots.all()

    def export_results(self) -> None:
        assert self.flight is not None

        # Before export, ensure output folder exists
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

        # Export raw flight data
        self.flight.export_data(self.output_folder + "/raw_flight_data.csv")

        # Export flight data to csv
        export_flight_data_to_csv(
            self.flight,
            self.output_folder + "/custom_flight_data.csv",
            self.config.export_flight_data_time_step_seconds,
        )

        # Export simulated sensor module data to csv
        export_flight_data_to_csv_in_simulated_sensor_module_format(
            self.flight,
            self.output_folder + "/simulated_sensor_module_data.csv",
            self.environment,
            self.config.export_flight_data_time_step_seconds,
        )

        # Export trajectory for Google Earth visulization
        self.flight.export_kml(
            file_name=self.output_folder + "/trajectory.kml",
            extrude=True,
            altitude_mode="relative_to_ground",
        )

        # Export monte carlo ellipses for Google Earth visualization
        self.monte_carlo_simulation.export_ellipses_to_kml(
            filename=self.output_folder + "/monte_carlo_analysis/monte_carlo_ellipses.kml",
            origin_lat=self.environment.latitude,
            origin_lon=self.environment.longitude,
        )
