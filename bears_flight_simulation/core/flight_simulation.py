import logging
import math
from pathlib import Path

from rocketpy import AirBrakes, Environment, Flight, MonteCarlo, Rocket, SolidMotor
from rocketpy.stochastic import (
    StochasticAirBrakes,
    StochasticEnvironment,
    StochasticFlight,
    StochasticParachute,
    StochasticRocket,
    StochasticSolidMotor,
)

from bears_flight_simulation.exporters.airbrake_export import (
    plot_airbrake_deployment_over_time,
)
from bears_flight_simulation.exporters.altitude_plots import plot_altitude_over_time
from bears_flight_simulation.exporters.flight_data_export import (
    export_flight_data_to_csv,
    export_flight_data_to_csv_in_simulated_sensor_module_format,
)
from bears_flight_simulation.hacks.matplotlib_hacks import (
    hack_override_matplotlib_show,
    hack_override_matplotlib_show_reset,
)
from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig
from bears_flight_simulation.parsers.fins_config import FinsConfig
from bears_flight_simulation.parsers.location_config import LocationConfig
from bears_flight_simulation.parsers.motor_config import MotorConfig
from bears_flight_simulation.parsers.nose_cone_config import NoseConeConfig
from bears_flight_simulation.parsers.parachute_config import ParachuteConfig
from bears_flight_simulation.parsers.parts_list_parser import (
    Part,
    get_motor_position,
    get_nosecone_tip_position_plus_length,
    get_nosecone_total_length,
)
from bears_flight_simulation.parsers.rail_button_config import RailButtonConfig
from bears_flight_simulation.parsers.simulation_config import SimulationConfig
from bears_flight_simulation.parsers.weather_config import WeatherConfig
from bears_flight_simulation.utilities.config_calc import rocket_center_of_mass
from bears_flight_simulation.utilities.rocket_calculations import (
    calculate_rocket_mass_in_kg,
    calculate_rocket_mass_without_motor_in_kg,
)


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
    config: SimulationConfig

    # Simulation stuff
    rocket: Rocket
    flight: Flight
    environment: Environment
    motor: SolidMotor
    stochastic_environment: StochasticEnvironment
    stochastic_motor: StochasticSolidMotor
    stochastic_rocket: StochasticRocket
    stochastic_flight: StochasticFlight
    stochastic_parachutes: list[StochasticParachute]
    stochastic_airbrakes: list[StochasticAirBrakes]

    # Folders
    output_folder: Path

    def __init__(
        self,
        config: SimulationConfig,
        output_folder: Path,
        motor_file_path: Path,
        motor_config: MotorConfig,
        parachutes: list[ParachuteConfig],
        airbrakes: list[AirbrakeConfig],
        rail_button_config: RailButtonConfig,
        nose_cone_config: NoseConeConfig,
        power_off_drag_curve_file_path: Path,
        power_on_drag_curve_file_path: Path,
        fins_config: FinsConfig,
        launch_location: LocationConfig,
        parts: list[Part],
        weather_config: WeatherConfig,
    ) -> None:
        # Store configs / folders
        self.config = config
        self.output_folder = output_folder

        # Setup environment
        self.environment = Environment(
            latitude=launch_location.latitude,  # type: ignore
            longitude=launch_location.longitude,  # type: ignore
            elevation=launch_location.elevation,  # type: ignore
        )
        self.environment.set_date(config.launch_date)
        if config.use_weather_forecast_instead_of_config:  # type: ignore
            self.environment.set_atmospheric_model(type="Forecast", file="GFS")
            if config.enable_monte_carlo_simulation:  # type: ignore
                logging.error(
                    "FlightSimulation: MonteCarlo simulation is not supported when using weather forecasts! Quitting..."
                )
                exit(1)
            # self.environment.set_atmospheric_model(type="Ensemble", file="GEFS")
            # self.environment.select_ensemble_member(3)
            # self.stochastic_environment = StochasticEnvironment(
            #    environment=self.environment,
            #    ensemble_member=range(0, self.environment.num_ensemble_members)
            # )
        else:
            (wind_east, wind_north) = wind_speed_and_direction_to_east_and_north(
                weather_config.wind_speed_in_m_per_s,  # type: ignore
                weather_config.wind_direction_in_degrees,  # type: ignore
            )
            self.environment.set_atmospheric_model(
                type="custom_atmosphere",
                pressure=None,
                temperature=None,
                wind_u=[(0, wind_east)],  # type: ignore
                wind_v=[(0, wind_north)],  # type: ignore
            )
            if config.enable_monte_carlo_simulation:  # type: ignore
                self.stochastic_environment = StochasticEnvironment(
                    environment=self.environment,
                    wind_velocity_x_factor=(
                        1.0,
                        weather_config.wind_x_y_factor_standard_deviation,  # type: ignore
                    ),
                    wind_velocity_y_factor=(
                        1.0,
                        weather_config.wind_x_y_factor_standard_deviation,  # type: ignore
                    ),
                )

        # Setup motor
        self.motor = SolidMotor(
            thrust_source=str(motor_file_path),
            dry_mass=motor_config.dry_mass,  # type: ignore
            dry_inertia=motor_config.dry_inertia,  # type: ignore
            nozzle_radius=motor_config.nozzle_radius,  # type: ignore
            grain_number=motor_config.grain_number,  # type: ignore
            grain_density=motor_config.grain_density,
            grain_outer_radius=motor_config.grain_outer_radius,  # type: ignore
            grain_initial_inner_radius=motor_config.grain_initial_inner_radius,  # type: ignore
            grain_initial_height=motor_config.grain_initial_height,  # type: ignore
            grain_separation=motor_config.grain_separation,  # type: ignore
            grains_center_of_mass_position=motor_config.grains_center_of_mass_position,
            center_of_dry_mass_position=motor_config.center_of_dry_mass_position,
            nozzle_position=motor_config.nozzle_position,
            burn_time=motor_config.burn_time,  # type: ignore
            throat_radius=motor_config.throat_radius,  # type: ignore
            coordinate_system_orientation="nozzle_to_combustion_chamber",
        )
        if config.enable_monte_carlo_simulation:  # type: ignore
            self.stochastic_motor = StochasticSolidMotor(
                solid_motor=self.motor,
                total_impulse=motor_config.total_impulse_standard_deviation_factor
                * self.motor.total_impulse,
            )

        # Create rocket
        rocket_mass_without_motor: float
        center_of_mass_without_motor: float
        if config.override_parts_list:  # type: ignore
            rocket_mass_without_motor = (
                config.override_parts_list_mass_without_motor_in_g / 1000.0  # type: ignore
            )
            center_of_mass_without_motor = (
                config.override_parts_list_center_of_mass_in_m  # type: ignore
            )
            logging.info(
                f"FlightSimulation: USING PARTS LIST OVERRIDE with mass_without_motor={rocket_mass_without_motor}kg and center_of_mass_without_motor={center_of_mass_without_motor}m"
            )
        else:
            rocket_mass_without_motor = calculate_rocket_mass_without_motor_in_kg(parts)
            center_of_mass_without_motor = rocket_center_of_mass(parts)[2] / 1000.0
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor) is {rocket_mass_without_motor}kg"
        )
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor + motor drymass) is {rocket_mass_without_motor + motor_config.dry_mass}kg"  # type: ignore
        )
        logging.info(
            f"FlightSimulation: calculated rocket mass (without motor + motor drymass + motor propmass) is {rocket_mass_without_motor + motor_config.dry_mass + motor_config.prop_mass}kg"  # type: ignore
        )
        logging.info(
            f"FlightSimulation: calculated rocket mass (complete parts list) is {calculate_rocket_mass_in_kg(parts)}kg"
        )
        self.rocket = Rocket(
            radius=config.diameter_in_m / 2.0,  # type: ignore
            mass=rocket_mass_without_motor,
            inertia=(
                self.config.inertia_11,  # type: ignore
                self.config.inertia_22,  # type: ignore
                self.config.inertia_33,  # type: ignore
            ),
            power_off_drag=str(power_off_drag_curve_file_path),
            power_on_drag=str(power_on_drag_curve_file_path),
            center_of_mass_without_motor=center_of_mass_without_motor,
            coordinate_system_orientation="tail_to_nose",
        )
        if config.enable_monte_carlo_simulation:  # type: ignore
            self.stochastic_rocket = StochasticRocket(
                rocket=self.rocket,
                mass=self.config.mass_standard_deviation_factor  # type: ignore
                * rocket_mass_without_motor,
                center_of_mass_without_motor=self.config.center_of_mass_standard_deviation_factor  # type: ignore
                * center_of_mass_without_motor,
                inertia_11=self.config.inertia_standard_deviation_factor  # type: ignore
                * self.config.inertia_11,  # type: ignore
                inertia_22=self.config.inertia_standard_deviation_factor  # type: ignore
                * self.config.inertia_22,  # type: ignore
                inertia_33=self.config.inertia_standard_deviation_factor  # type: ignore
                * self.config.inertia_33,  # type: ignore
                power_off_drag_factor=(
                    1.0,
                    self.config.power_off_drag_factor_standard_deviation,  # type: ignore
                ),
                power_on_drag_factor=(
                    1.0,
                    self.config.power_on_drag_factor_standard_deviation,  # type: ignore
                ),
            )
        logging.info(
            f"FlightSimulation: ROCKET COM WITHOUT MOTOR is {rocket_center_of_mass(parts)}"
        )
        logging.info(
            f"FlightSimulation: ROCKET COM WITH MOTOR is {rocket_center_of_mass(parts, ignore_motor=False)}"
        )

        # Add motor to rocket
        self.rocket.add_motor(self.motor, position=get_motor_position(parts) / 1000.0)
        if config.enable_monte_carlo_simulation:  # type: ignore
            self.stochastic_rocket.add_motor(self.stochastic_motor)

        # Add rail guides
        self.rocket.set_rail_buttons(
            upper_button_position=rail_button_config.upper_button_position,  # type: ignore
            lower_button_position=rail_button_config.lower_button_position,  # type: ignore
            angular_position=rail_button_config.angular_position,  # type: ignore
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
            kind=nose_cone_config.kind,  # type: ignore
            position=nosecone_tip_upper_limit_position,
            bluffness=nose_cone_config.bluffness,  # type: ignore
            power=nose_cone_config.power_if_using_powerseries_kind,
            base_radius=nose_cone_config.base_radius,
        )
        self.rocket.add_trapezoidal_fins(
            n=fins_config.n,  # type: ignore
            root_chord=fins_config.root_chord,  # type: ignore
            tip_chord=fins_config.tip_chord,  # type: ignore
            span=fins_config.span,  # type: ignore
            position=fins_config.position,  # type: ignore
            cant_angle=fins_config.cant_angle,  # type: ignore
            sweep_length=fins_config.sweep_length,
            sweep_angle=fins_config.sweep_angle,
            radius=fins_config.radius,
        )

        # Add parachutes
        self.stochastic_parachutes = []
        for parachute in parachutes:
            parachute_object = self.rocket.add_parachute(
                name=parachute.id,  # type: ignore
                cd_s=parachute.drag_coefficient_times_reference_area,  # type: ignore
                trigger=parachute.ejection_altitude,
                sampling_rate=parachute.ejection_sampling_rate_hertz,  # type: ignore
                lag=parachute.opening_lag_seconds,  # type: ignore
                noise=(
                    parachute.noise_mean_pascal,  # type: ignore
                    parachute.noise_standard_deviation_pascal,  # type: ignore
                    parachute.noise_time_correlation_pascal,  # type: ignore
                ),
            )
            if config.enable_monte_carlo_simulation:  # type: ignore
                stochastic_parachute = StochasticParachute(
                    parachute=parachute_object,
                    cd_s=parachute.drag_coefficient_times_reference_area_standard_deviation_factor  # type: ignore
                    * parachute.drag_coefficient_times_reference_area,  # type: ignore
                    lag=parachute.opening_lag_seconds_standard_deviation_factor  # type: ignore
                    * parachute.opening_lag_seconds,  # type: ignore
                )
                self.stochastic_parachutes.append(stochastic_parachute)
                self.stochastic_rocket.add_parachute(stochastic_parachute)

        # Add airbrakes
        self.stochastic_airbrakes = []
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
            airbrake_object, controller = self.rocket.add_air_brakes(
                drag_coefficient_curve=str(airbrake.drag_curve_filepath),
                controller_function=airbrake_controller_function,
                sampling_rate=airbrake.sampling_rate_hz,  # type: ignore
                clamp=True,
                name=airbrake.id,  # type: ignore
                return_controller=True,
            )  # type: ignore
            if config.enable_monte_carlo_simulation:  # type: ignore
                stochastic_airbrake = StochasticAirBrakes(
                    air_brakes=airbrake_object,
                    drag_coefficient_curve_factor=(
                        1.0,
                        airbrake.drag_curve_standard_deviation_factor,  # type: ignore
                    ),
                )
                self.stochastic_airbrakes.append(stochastic_airbrake)
                self.stochastic_rocket.add_air_brakes(stochastic_airbrake, controller)

        logging.info(
            f"FlightSimulation: calculated rocket mass (rocket.evaluate_dry_mass) is {self.rocket.evaluate_dry_mass()}kg"
        )

        # Print uncertainties of the stochastic classes
        if config.enable_monte_carlo_simulation:  # type: ignore
            self.stochastic_environment.visualize_attributes()
            self.stochastic_motor.visualize_attributes()
            self.stochastic_rocket.visualize_attributes()
            for stochastic_parachute in self.stochastic_parachutes:
                stochastic_parachute.visualize_attributes()
            for stochastic_airbrake in self.stochastic_airbrakes:
                stochastic_airbrake.visualize_attributes()

    def simulate(self) -> None:
        # Run the simulation
        self.flight = Flight(
            rocket=self.rocket,
            environment=self.environment,
            rail_length=self.config.rail_length_in_m,  # type: ignore
            inclination=self.config.inclination,  # type: ignore
            heading=self.config.heading,  # type: ignore
        )

        # Run the monte carlo (stochastic) simulation
        if self.config.enable_monte_carlo_simulation:  # type: ignore
            self.stochastic_flight = StochasticFlight(
                flight=self.flight,
                inclination=1.0,
                heading=2.0,
            )
            self.stochastic_flight.visualize_attributes()

            # ensure subfolder exists
            (self.output_folder / "monte_carlo_analysis").mkdir(
                parents=True, exist_ok=True
            )
            self.monte_carlo_simulation = MonteCarlo(
                filename=str(
                    self.output_folder / "monte_carlo_analysis" / "monte_carlo_class"
                ),
                environment=self.stochastic_environment,
                rocket=self.stochastic_rocket,
                flight=self.stochastic_flight,
            )
            self.monte_carlo_simulation.simulate(
                number_of_simulations=self.config.number_of_simulations,  # type: ignore
                append=False,
                include_function_data=False,
                parallel=self.config.parallel,  # type: ignore
                n_workers=self.config.n_workers,  # type: ignore
            )
        else:
            logging.info(
                "FlightSimulation: Monte Carlo simulation is disabled, skipping ..."
            )

    def show_input_info(self) -> None:
        assert self.environment is not None
        assert self.motor is not None
        assert self.rocket is not None

        # Print environment info
        print("ENVIRONMENT INFO START")
        self.environment.prints.all()
        self.environment.plots.info(
            filename=str(self.output_folder / "plots" / "environment.png")
        )
        print("ENVIRONMENT INFO END")

        # Print motor info
        print("MOTOR INFO START")
        self.motor.prints.all()
        self.motor.plots.thrust(
            filename=str(self.output_folder / "plots" / "rocket" / "motor_thrust.png")
        )
        print("MOTOR INFO END")

        # Show graphics about the rocket
        self.rocket.plots.static_margin(
            filename=str(self.output_folder / "plots" / "rocket" / "static_margin.png")
        )
        self.rocket.draw(
            filename=str(self.output_folder / "plots" / "rocket" / "rocket.png")
        )

    def show_results(self) -> None:
        assert self.flight is not None

        # Print simulation results
        print("TRADITIONAL RESULTS INFO START")
        self.flight.prints.all()
        print("TRADITIONAL RESULTS INFO END")

        # Show simulation results graphics
        print("TRADITIONAL RESULTS GRAPHICS START")
        self.flight.plots.trajectory_3d(
            filename=str(self.output_folder / "plots" / "results" / "trajectory_3d.png")
        )
        self.flight.plots.linear_kinematics_data(
            filename=str(
                self.output_folder / "plots" / "results" / "linear_kinematics.png"
            )
        )
        self.flight.plots.flight_path_angle_data(
            filename=str(
                self.output_folder / "plots" / "results" / "flight_path_angle_data.png"
            )
        )
        self.flight.plots.attitude_data(
            filename=str(self.output_folder / "plots" / "results" / "attitude_data.png")
        )
        self.flight.plots.angular_kinematics_data(
            filename=str(
                self.output_folder / "plots" / "results" / "angular_kinematics_data.png"
            )
        )
        self.flight.plots.aerodynamic_forces(
            filename=str(
                self.output_folder / "plots" / "results" / "aerodynamic_forces.png"
            )
        )
        self.flight.plots.rail_buttons_forces(
            filename=str(
                self.output_folder / "plots" / "results" / "rail_button_forces.png"
            )
        )
        # NOTE: The energy data plot crashes when an airbrake is configured
        if len(self.config.airbrake_ids) == 0:  # type: ignore
            self.flight.plots.energy_data(
                filename=str(
                    self.output_folder / "plots" / "results" / "energy_data.png"
                )
            )
        self.flight.plots.fluid_mechanics_data(
            filename=str(
                self.output_folder / "plots" / "results" / "fluid_mechanics_data.png"
            )
        )
        self.flight.plots.stability_and_control_data(
            filename=str(
                self.output_folder
                / "plots"
                / "results"
                / "stability_and_control_data.png"
            )
        )
        self.flight.plots.pressure_rocket_altitude(
            filename=str(
                self.output_folder
                / "plots"
                / "results"
                / "pressure_rocket_altitude.png"
            )
        )
        for parachute in self.flight.rocket.parachutes:
            assert parachute.name is not None and parachute.name != ""
            folder = (
                self.output_folder / "plots" / "results" / "parachutes" / parachute.name
            )
            parachute.noise_signal_function(
                filename=str(folder / "noise_signal_function.png")
            )
            parachute.noisy_pressure_signal_function(
                filename=str(folder / "noisy_pressure_signal_function.png")
            )
            parachute.clean_pressure_signal_function(
                filename=str(folder / "noisy_pressure_signal_function.png")
            )
        if len(self.config.airbrake_ids) > 0:  # type: ignore
            plot_airbrake_deployment_over_time(
                self.flight,
                filepath=self.output_folder
                / "plots"
                / "results"
                / "airbrake_deployment.png",
            )
        plot_altitude_over_time(
            self.flight,
            self.environment,
            filepath=self.output_folder
            / "plots"
            / "results"
            / "altitude_over_time.png",
        )
        print("TRADITIONAL RESULTS GRAPHICS END")

        if self.config.enable_monte_carlo_simulation:  # type: ignore
            print("MONTECARLO RESULTS START")
            print(f"number of loaded sims: {self.monte_carlo_simulation}")
            self.monte_carlo_simulation.prints.all()
            self.monte_carlo_simulation.plots.ellipses(save=True)
            hack_override_matplotlib_show(
                filename=str(
                    self.output_folder / "monte_carlo_analysis" / "histogram.png"
                )
            )
            self.monte_carlo_simulation.plots.all()
            hack_override_matplotlib_show_reset()
            print("MONTECARLO RESULTS END")

    def export_results(self) -> None:
        assert self.flight is not None

        # Before export, ensure output folder exists
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Export raw flight data
        self.flight.export_data(str(self.output_folder / "raw_flight_data.csv"))

        # Export flight data to csv
        export_flight_data_to_csv(
            self.flight,
            self.output_folder / "custom_flight_data.csv",
            self.config.export_flight_data_time_step_seconds,  # type: ignore
        )

        # Export simulated sensor module data to csv
        export_flight_data_to_csv_in_simulated_sensor_module_format(
            self.flight,
            self.output_folder / "simulated_sensor_module_data.csv",
            self.environment,
            self.config.export_flight_data_time_step_seconds,  # type: ignore
        )

        # Export trajectory for Google Earth visulization
        self.flight.export_kml(
            file_name=str(self.output_folder / "trajectory.kml"),
            extrude=True,
            altitude_mode="relative_to_ground",
        )

        # Export monte carlo ellipses for Google Earth visualization
        if self.config.enable_monte_carlo_simulation:  # type: ignore
            self.monte_carlo_simulation.export_ellipses_to_kml(
                filename=str(
                    self.output_folder
                    / "monte_carlo_analysis"
                    / "monte_carlo_ellipses.kml"
                ),
                origin_lat=self.environment.latitude,
                origin_lon=self.environment.longitude,
            )

        # Export more random stuff needed for Altimax calibration
        with open(self.output_folder / "altimax-calibration-data.txt", "w") as file:
            # Apogee time
            buffer = f"apogee_time: {self.flight.apogee_time}\n"

            # Find time to 400m and 300m descent
            found_400m = False
            for t in range(int(self.flight.apogee_time), int(self.flight.t_final)):
                if not found_400m:
                    if self.flight.altitude(t) < 400:  # type: ignore
                        buffer += f"time_to_400m_descent: {t}\n"
                        found_400m = True
                elif self.flight.altitude(t) < 300:  # type: ignore
                    buffer += f"time_to_300m_descent: {t}\n"
                    break

            file.write(buffer)
