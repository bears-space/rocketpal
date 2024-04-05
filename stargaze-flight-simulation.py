#!/usr/bin/env python3

import argparse
import logging
import os
import typing as t

from core.flight_simulation import FlightSimulation
from parsers.motor_config import MotorConfig
from parsers.parts_list_parser import PartsListParser


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
    # TODO

    # Declare config variables
    motor_config: MotorConfig
    parts_list_parser: PartsListParser

    # Parse files
    with open(config_folder + "/motor_config.yaml", "r") as file:
        motor_config = MotorConfig(file)
    with open(config_folder + "/parts_list.csv", "r") as file:
        parts_list_parser = PartsListParser(file)

    # Initialize flight simulation
    # TODO Remove hardcoded motor file path
    sim: FlightSimulation = FlightSimulation(
        motor_file_path="data/motors/Cesaroni_M1670.eng",
        motor_config=motor_config,
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
