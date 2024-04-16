#!/usr/bin/env python3

import argparse
import logging
import os
import typing as t

from core.flight_simulation import FlightSimulation
from parsers.config import Config
from parsers.location import Location
from parsers.motor_config import MotorConfig
from parsers.parts_list_parser import PartsListParser

CONFIG_FILENAME = "/configuration.yaml"
MOTOR_FILENAME = "/motor.eng"
MOTOR_CONFIG_FILENAME = "/motor_config.yaml"
POWER_OFF_DRAG_CURVE_FILENAME = "/power_off_drag_curve.csv"
POWER_ON_DRAG_CURVE_FILENAME = "/power_on_drag_curve.csv"
FINS_RADIANS_FILENAME = "/fins_radians.csv"
PARTS_LIST_FILENAME = "/parts_list.csv"
LOCATION_FILENAME = "/location.yaml"


def dir_path(path_to_dir: str) -> str:
    if os.path.isdir(path_to_dir):
        return path_to_dir
    else:
        raise NotADirectoryError(path_to_dir)


def main() -> None:
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

    # Get variables from args
    config_folder: str = args.config_folder
    output_folder: str = args.output

    # Check that all expected files are present in the config folder
    for filename in [
        CONFIG_FILENAME,
        MOTOR_FILENAME,
        MOTOR_CONFIG_FILENAME,
        POWER_OFF_DRAG_CURVE_FILENAME,
        POWER_ON_DRAG_CURVE_FILENAME,
        FINS_RADIANS_FILENAME,
        PARTS_LIST_FILENAME,
        LOCATION_FILENAME,
    ]:
        file_path = config_folder + filename
        if not os.path.isfile(file_path):
            logging.error(
                "StargazeFlightSimulation: Missing file '"
                + str(filename)
                + "' in specified config folder! Aborting ..."
            )
            exit(2)  # 2 means "No such file or directory"

    # Declare config variables
    config: Config
    motor_config: MotorConfig
    parts_list_parser: PartsListParser
    launch_location: Location

    # Parse files
    with open(config_folder + CONFIG_FILENAME, "r") as file:
        config = Config(file)
        logging.info(
            "StargazeFlightSimulation: Using Config with id '" + str(config.id) + "'"
        )
    with open(config_folder + MOTOR_CONFIG_FILENAME, "r") as file:
        motor_config = MotorConfig(file)
        logging.info(
            "StargazeFlightSimulation: Using MotorConfig with id '"
            + str(motor_config.id)
            + "'"
        )
    with open(config_folder + PARTS_LIST_FILENAME, "r") as file:
        parts_list_parser = PartsListParser(file)
    with open(config_folder + LOCATION_FILENAME, "r") as file:
        launch_location = Location(file)
        logging.info(
            "StargazeFlightSimulation: Using Location with id '"
            + str(launch_location.id)
            + "'"
        )

    # Initialize flight simulation
    sim: FlightSimulation = FlightSimulation(
        config=config,
        output_folder=output_folder,
        motor_file_path=config_folder + MOTOR_FILENAME,
        motor_config=motor_config,
        power_off_drag_curve_file_path=config_folder + POWER_OFF_DRAG_CURVE_FILENAME,
        power_on_drag_curve_file_path=config_folder + POWER_ON_DRAG_CURVE_FILENAME,
        fins_radians_file_path=config_folder + FINS_RADIANS_FILENAME,
        launch_location=launch_location,
    )

    # Show infos about configured flight
    sim.show_input_info()

    # Run simulation
    sim.simulate()

    # Show and save results
    sim.show_results()
    sim.export_results()


# Run main if launched directly
if __name__ == "__main__":  # type: ignore
    main()
