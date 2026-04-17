#!/usr/bin/env python3

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from socket import gethostname

import yaml

from bears_flight_simulation.core.airbrake_library import AirbrakeLibrary
from bears_flight_simulation.core.flight_simulation import FlightSimulation
from bears_flight_simulation.core.location_library import LocationLibrary
from bears_flight_simulation.core.motor_library import MotorLibrary
from bears_flight_simulation.core.parachute_library import ParachuteLibrary
from bears_flight_simulation.core.weather_library import WeatherLibrary
from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig
from bears_flight_simulation.parsers.fins_config import FinsConfig
from bears_flight_simulation.parsers.location_config import LocationConfig
from bears_flight_simulation.parsers.motor_config import MotorConfig
from bears_flight_simulation.parsers.nose_cone_config import NoseConeConfig
from bears_flight_simulation.parsers.parachute_config import ParachuteConfig
from bears_flight_simulation.parsers.parts_list_parser import Part, parse_parts_list
from bears_flight_simulation.parsers.rail_button_config import RailButtonConfig
from bears_flight_simulation.parsers.simulation_config import SimulationConfig
from bears_flight_simulation.parsers.weather_config import WeatherConfig

CONFIG_FILENAME = "configuration.yaml"
MOTOR_FOLDERNAME = "motors"
RAIL_BUTTONS_FILENAME = "rail_buttons.yaml"
NOSE_CONE_FILENAME = "nose_cone.yaml"
POWER_OFF_DRAG_CURVE_FILENAME = "power_off_drag_curve.csv"
POWER_ON_DRAG_CURVE_FILENAME = "power_on_drag_curve.csv"
FINS_CONFIG_FILENAME = "fins.yaml"
PARTS_LIST_FILENAME = "parts_list.csv"
LOCATION_FOLDERNAME = "locations"
WEATHER_FOLDERNAME = "weathers"
PARACHUTE_FOLDERNAME = "parachutes"
AIRBRAKE_FOLDERNAME = "airbrakes"


def _ensure_config_files_exist(config_folder: Path) -> bool:
    # Check that all expected files are present in the config folder
    for filename in [
        CONFIG_FILENAME,
        RAIL_BUTTONS_FILENAME,
        NOSE_CONE_FILENAME,
        POWER_OFF_DRAG_CURVE_FILENAME,
        POWER_ON_DRAG_CURVE_FILENAME,
        FINS_CONFIG_FILENAME,
        PARTS_LIST_FILENAME,
    ]:
        file_path = config_folder / filename
        if not os.path.isfile(file_path):
            logging.error(
                "Missing file '"
                + str(filename)
                + "' in specified config folder! Aborting ..."
            )
            return False

    # Check that all expected folders are present in the config folder
    for foldername in [
        MOTOR_FOLDERNAME,
        LOCATION_FOLDERNAME,
        WEATHER_FOLDERNAME,
        PARACHUTE_FOLDERNAME,
        AIRBRAKE_FOLDERNAME,
    ]:
        file_path = config_folder / foldername
        if not os.path.isdir(file_path):
            logging.error(
                "Missing folder '"
                + str(foldername)
                + "' in specified config folder! Aborting ..."
            )
            return False

    return True


def _load_motor_from_library(config_folder: Path, motor_id: str) -> MotorConfig | None:
    motor_library: MotorLibrary = MotorLibrary(config_folder / MOTOR_FOLDERNAME)
    motor = motor_library.get(motor_id)
    assert isinstance(motor, MotorConfig) or motor is None
    return motor


def _load_parachutes_from_library(
    config_folder: Path, parachute_ids: list[str]
) -> list[ParachuteConfig]:
    parachute_library: ParachuteLibrary = ParachuteLibrary(
        config_folder / PARACHUTE_FOLDERNAME
    )
    parachutes: list[ParachuteConfig] = []
    for id in parachute_ids:
        parachute = parachute_library.get(id)
        if parachute is None:
            logging.warning(
                f"The parachute with the id '{id}' does not exist in the parachute library. Skipping ..."
            )
        else:
            assert isinstance(parachute, ParachuteConfig)
            parachutes.append(parachute)
            logging.info(f"Loaded ParachuteConfig with id '{parachute.id}'")  # type: ignore
    return parachutes


def _load_airbrakes_from_library(
    config_folder: Path, airbrake_ids: list[str]
) -> list[AirbrakeConfig]:
    airbrake_library: AirbrakeLibrary = AirbrakeLibrary(
        config_folder / AIRBRAKE_FOLDERNAME
    )
    airbrakes: list[AirbrakeConfig] = []
    for id in airbrake_ids:
        airbrake = airbrake_library.get(id)
        if airbrake is None:
            logging.warning(
                f"The airbrake with the id '{id}' does not exist in the airbrake library. Skipping ..."
            )
        else:
            assert isinstance(airbrake, AirbrakeConfig)
            airbrakes.append(airbrake)
            logging.info(f"Loaded AirbrakeConfig with id '{airbrake.id}'")  # type: ignore
    return airbrakes


def _load_config(config_folder: Path) -> SimulationConfig:
    with open(config_folder / CONFIG_FILENAME, "r") as file:
        data = yaml.safe_load(file)
        config = SimulationConfig(data)
        logging.info(f"Using Config with id '{config.id}'")  # type: ignore
        return config


def _load_launch_location_from_library(
    config_folder: Path, location_id: str
) -> LocationConfig | None:
    location_library: LocationLibrary = LocationLibrary(
        config_folder / LOCATION_FOLDERNAME
    )
    library_entry = location_library.get(location_id)
    assert isinstance(library_entry, LocationConfig) or library_entry is None
    return library_entry


def _load_weather_config_from_library(
    config_folder: Path, weather_config_id: str
) -> WeatherConfig | None:
    weather_library: WeatherLibrary = WeatherLibrary(config_folder / WEATHER_FOLDERNAME)
    library_entry = weather_library.get(weather_config_id)
    assert isinstance(library_entry, WeatherConfig) or library_entry is None
    return library_entry


def _load_rail_button_config(config_folder: Path) -> RailButtonConfig:
    with open(config_folder / RAIL_BUTTONS_FILENAME, "r") as file:
        data = yaml.safe_load(file)
        return RailButtonConfig(data)


def _load_nose_cone_config(config_folder: Path) -> NoseConeConfig:
    with open(config_folder / NOSE_CONE_FILENAME, "r") as file:
        data = yaml.safe_load(file)
        return NoseConeConfig(data)


def _load_fins_config(config_folder: Path) -> FinsConfig:
    with open(config_folder / FINS_CONFIG_FILENAME, "r") as file:
        data = yaml.safe_load(file)
        return FinsConfig(data)


def load_configs_and_run_simulation(config_folder: Path, output_folder: Path) -> None:
    # Log current time and hostname for later reference
    logging.info(
        f"Running on {gethostname()} at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} (UTC)"
    )

    if not _ensure_config_files_exist(config_folder):
        exit(2)  # 2 means "No such file or directory"

    config = _load_config(config_folder)

    launch_location = _load_launch_location_from_library(
        config_folder,
        config.location_id,  # type: ignore
    )
    if launch_location is None:
        logging.error(
            f"The location with the id '{config.location_id}'"  # type: ignore
            f" does not exist in the location library. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"
    else:
        logging.info(f"Using Location with id '{launch_location.id}'")  # type: ignore

    weather_config = _load_weather_config_from_library(
        config_folder,
        config.weather_config_id,  # type: ignore
    )
    if weather_config is None:
        logging.error(
            f"The weather config with the id '{config.weather_config_id}'"  # type: ignore
            f" does not exist in the weather config library. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"
    else:
        logging.info(f"Using WeatherConfig with id '{weather_config.id}'")  # type: ignore

    motor_config = _load_motor_from_library(config_folder, config.motor_id)  # type: ignore
    if motor_config is None:
        logging.error(
            f"The motor config with the id '{config.motor_id}'"  # type: ignore
            f" does not exist in the motor config library. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"
    else:
        logging.info(f"Using MotorConfig with id '{motor_config.id}'")  # type: ignore

    parachutes = _load_parachutes_from_library(config_folder, config.parachute_ids)  # type: ignore

    airbrakes = _load_airbrakes_from_library(config_folder, config.airbrake_ids)  # type: ignore

    rail_button_config = _load_rail_button_config(config_folder)

    nose_cone_config = _load_nose_cone_config(config_folder)

    fins_config = _load_fins_config(config_folder)

    # Parse parts list
    parts_list: list[Part]
    with open(config_folder / PARTS_LIST_FILENAME, "r") as file:
        parts_list = parse_parts_list(file)

        # Initialize flight simulation
        sim: FlightSimulation = FlightSimulation(
            config=config,
            output_folder=output_folder,
            motor_file_path=config_folder
            / MOTOR_FOLDERNAME
            / motor_config.engine_filename,  # type: ignore
            motor_config=motor_config,
            parachutes=parachutes,
            airbrakes=airbrakes,
            rail_button_config=rail_button_config,
            nose_cone_config=nose_cone_config,
            power_off_drag_curve_file_path=config_folder
            / POWER_OFF_DRAG_CURVE_FILENAME,
            power_on_drag_curve_file_path=config_folder / POWER_ON_DRAG_CURVE_FILENAME,
            fins_config=fins_config,
            launch_location=launch_location,
            parts=parts_list,
            weather_config=weather_config,
        )

        # Show infos about configured flight
        sim.show_input_info()

        # Run simulation
        sim.simulate()

        # Show and save results
        sim.show_results()
        sim.export_results()
