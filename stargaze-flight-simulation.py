#!/usr/bin/env python3

import argparse
import logging
import os
import typing as t

from core.flight_simulation import FlightSimulation
from parsers.motor_config import MotorConfig
from parsers.parts_list_parser import PartsListParser

MOTOR_FILENAME = "/motor.eng"
POWER_OFF_DRAG_CURVE_FILENAME = "/power_off_drag_curve.csv"
POWER_ON_DRAG_CURVE_FILENAME = "/power_on_drag_curve.csv"
FINS_RADIANS_FILENAME = "/fins_radians.csv"


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
    # TODO add help text
    argument_parser.add_argument("config_folder", type=dir_path, default="./input")

    # Parse arguments
    args = argument_parser.parse_args()

    # Get variables from args
    config_folder: str = args.config_folder

    # Check that all expected files are present in the config folder
    for filename in [
        MOTOR_FILENAME,
        POWER_OFF_DRAG_CURVE_FILENAME,
        POWER_ON_DRAG_CURVE_FILENAME,
        FINS_RADIANS_FILENAME,
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
    motor_config: MotorConfig
    parts_list_parser: PartsListParser

    # Parse files
    with open(config_folder + "/motor_config.yaml", "r") as file:
        motor_config = MotorConfig(file)
    with open(config_folder + "/parts_list.csv", "r") as file:
        parts_list_parser = PartsListParser(file)

    # Initialize flight simulation
    sim: FlightSimulation = FlightSimulation(
        motor_file_path=config_folder + MOTOR_FILENAME,
        motor_config=motor_config,
        power_off_drag_curve_file_path=config_folder + POWER_OFF_DRAG_CURVE_FILENAME,
        power_on_drag_curve_file_path=config_folder + POWER_ON_DRAG_CURVE_FILENAME,
        fins_radians_file_path=config_folder + FINS_RADIANS_FILENAME,
    )

    # TODO Load flight parameters

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
