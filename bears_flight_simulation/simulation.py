#!/usr/bin/env python3

import argparse
import logging
import os
import typing as t
from socket import gethostname
from datetime import datetime, timezone

from core.flight_simulation import FlightSimulation
from core.location_library import LocationLibrary
from core.motor_library import MotorLibrary
from core.parachute_library import ParachuteLibrary
from parsers.config import Config
from parsers.fins_config import FinsConfig
from parsers.location import Location
from parsers.motor_config import MotorConfig
from parsers.nose_cone_config import NoseConeConfig
from parsers.parachute_config import ParachuteConfig
from parsers.parts_list_parser import Part, parse_parts_list
from parsers.rail_button_config import RailButtonConfig

CONFIG_FILENAME = "/configuration.yaml"
MOTOR_FOLDERNAME = "/motors"
RAIL_BUTTONS_FILENAME = "/rail_buttons.yaml"
NOSE_CONE_FILENAME = "/nose_cone.yaml"
POWER_OFF_DRAG_CURVE_FILENAME = "/power_off_drag_curve.csv"
POWER_ON_DRAG_CURVE_FILENAME = "/power_on_drag_curve.csv"
FINS_CONFIG_FILENAME = "/fins.yaml"
FINS_RADIANS_FILENAME = "/fins_radians.csv"
PARTS_LIST_FILENAME = "/parts_list.csv"
LOCATION_FOLDERNAME = "/locations"
PARACHUTE_FOLDERNAME = "/parachutes"


def dir_path(path_to_dir: str) -> str:
    if os.path.isdir(path_to_dir):
        return path_to_dir
    else:
        raise NotADirectoryError(path_to_dir)


def _ensure_config_files_exist(config_folder: str) -> bool:
    # Check that all expected files are present in the config folder
    for filename in [
        CONFIG_FILENAME,
        RAIL_BUTTONS_FILENAME,
        NOSE_CONE_FILENAME,
        POWER_OFF_DRAG_CURVE_FILENAME,
        POWER_ON_DRAG_CURVE_FILENAME,
        FINS_CONFIG_FILENAME,
        FINS_RADIANS_FILENAME,
        PARTS_LIST_FILENAME,
    ]:
        file_path = config_folder + filename
        if not os.path.isfile(file_path):
            logging.error(
                "StargazeFlightSimulation: Missing file '"
                + str(filename)
                + "' in specified config folder! Aborting ..."
            )
            return False

    # Check that all expected folders are present in the config folder
    for foldername in [
        MOTOR_FOLDERNAME,
        LOCATION_FOLDERNAME,
        PARACHUTE_FOLDERNAME,
    ]:
        file_path = config_folder + foldername
        if not os.path.isdir(file_path):
            logging.error(
                "StargazeFlightSimulation: Missing folder '"
                + str(foldername)
                + "' in specified config folder! Aborting ..."
            )
            return False

    return True


def _load_motors_from_library(
    config_folder: str, motor_ids: t.List[str]
) -> t.List[MotorConfig]:
    motor_library: MotorLibrary = MotorLibrary(config_folder + MOTOR_FOLDERNAME)

    motors: t.List[MotorConfig] = []
    for id in motor_ids:
        motor = motor_library.get(id)
        if motor is None:
            logging.warning(
                f"StargazeFlightSimulation: The motor with the id '{id}' does not exist in the motor library. Skipping ..."
            )
        else:
            assert isinstance(motor, MotorConfig)
            motors.append(motor)
            logging.info(
                f"StargazeFlightSimulation: Loaded MotorConfig with id '{motor.id}'"
            )

    return motors


def _load_parachutes_from_library(
    config_folder: str, parachute_ids: t.List[str]
) -> t.List[ParachuteConfig]:
    parachute_library: ParachuteLibrary = ParachuteLibrary(
        config_folder + PARACHUTE_FOLDERNAME
    )
    parachutes: t.List[ParachuteConfig] = []
    for id in parachute_ids:
        parachute = parachute_library.get(id)
        if parachute is None:
            logging.warning(
                f"StargazeFlightSimulation: The parachute with the id '{id}' does not exist in the parachute library. Skipping ..."
            )
        else:
            assert isinstance(parachute, ParachuteConfig)
            parachutes.append(parachute)
            logging.info(
                f"StargazeFlightSimulation: Loaded ParachuteConfig with id '{parachute.id}'"
            )
    return parachutes


def _load_config(config_folder: str) -> Config:
    with open(config_folder + CONFIG_FILENAME, "r") as file:
        config = Config(file)
        logging.info(f"StargazeFlightSimulation: Using Config with id '{config.id}'")
        return config


def _load_launch_location_from_library(
    config_folder: str, location_id: str
) -> Location | None:
    location_library: LocationLibrary = LocationLibrary(
        config_folder + LOCATION_FOLDERNAME
    )
    library_entry = location_library.get(location_id)
    assert isinstance(library_entry, Location) or library_entry is None
    return library_entry


def _load_rail_button_config(config_folder: str) -> RailButtonConfig:
    with open(config_folder + RAIL_BUTTONS_FILENAME, "r") as file:
        return RailButtonConfig(file)


def _load_nose_cone_config(config_folder: str) -> NoseConeConfig:
    with open(config_folder + NOSE_CONE_FILENAME, "r") as file:
        return NoseConeConfig(file)


def _load_fins_config(config_folder: str) -> FinsConfig:
    with open(config_folder + FINS_CONFIG_FILENAME, "r") as file:
        return FinsConfig(file)


def load_configs_and_run_simulation(config_folder: str, output_folder: str) -> None:
    # Log current time and hostname for later reference
    logging.info(
        f"Running on {gethostname()} at {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} (UTC)"
    )

    if not _ensure_config_files_exist(config_folder):
        exit(2)  # 2 means "No such file or directory"

    config = _load_config(config_folder)

    launch_location = _load_launch_location_from_library(
        config_folder, config.location_id
    )
    if launch_location is None:
        logging.error(
            f"StargazeFlightSimulation: The location with the id '{config.location_id}'"
            f" does not exist in the location library. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"
    else:
        logging.info(
            f"StargazeFlightSimulation: Using Location with id '{launch_location.id}'"
        )

    motors = _load_motors_from_library(config_folder, config.motor_ids)
    if len(motors) == 0:
        logging.error(
            "StargazeFlightSimulation: No motors have been loaded. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"

    # Use first motor from list
    # TODO Iterate over motors instead, allowing for comparison between different motors in one run
    motor_config = motors[0]
    logging.info(
        f"StargazeFlightSimulation: Choosing MotorConfig with id '{motor_config.id}'"
    )

    parachutes = _load_parachutes_from_library(config_folder, config.parachute_ids)

    rail_button_config = _load_rail_button_config(config_folder)

    nose_cone_config = _load_nose_cone_config(config_folder)

    fins_config = _load_fins_config(config_folder)

    # Parse parts list
    parts_list: t.List[Part]
    with open(config_folder + PARTS_LIST_FILENAME, "r") as file:
        parts_list = parse_parts_list(file)

    # Initialize flight simulation
    sim: FlightSimulation = FlightSimulation(
        config=config,
        output_folder=output_folder,
        motor_file_path=config_folder
        + MOTOR_FOLDERNAME
        + "/"
        + motor_config.engine_filename,
        motor_config=motor_config,
        parachutes=parachutes,
        rail_button_config=rail_button_config,
        nose_cone_config=nose_cone_config,
        power_off_drag_curve_file_path=config_folder + POWER_OFF_DRAG_CURVE_FILENAME,
        power_on_drag_curve_file_path=config_folder + POWER_ON_DRAG_CURVE_FILENAME,
        fins_config=fins_config,
        fins_radians_file_path=config_folder + FINS_RADIANS_FILENAME,
        launch_location=launch_location,
        parts=parts_list,
    )

    # Show infos about configured flight
    sim.show_input_info()

    # Run simulation
    sim.simulate()

    # Show and save results
    sim.show_results()
    sim.export_results()


if __name__ == "__main__":
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Setup argparse
    argument_parser = argparse.ArgumentParser(prog="stargaze-flight-simulation")

    # Add arguments
    argument_parser.add_argument(
        "config_folder", type=dir_path, help="The input folder containing config files"
    )
    argument_parser.add_argument(
        "--output",
        type=str,
        help="The output folder, by default './output'",
        default="./output",
    )

    # Parse arguments
    args = argument_parser.parse_args()

    load_configs_and_run_simulation(
        config_folder=args.config_folder, output_folder=args.output
    )
