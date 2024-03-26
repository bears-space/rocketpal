#!/usr/bin/env python3

import argparse
import logging
import typing as t

from core.flight_simulation import FlightSimulation
from parsers.motor_config import MotorConfig
from parsers.parts_list_parser import PartsListParser


def main() -> None:
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Setup argparse
    argument_parser = argparse.ArgumentParser(prog="stargaze-flight-simulation")

    # Add arguments
    # TODO add help text
    argument_parser.add_argument("motor_config_yaml_file", type=argparse.FileType("r"))
    argument_parser.add_argument("parts_list_csv_file", type=argparse.FileType("r"))

    # Parse arguments
    args = argument_parser.parse_args()

    # Get variables from args
    motor_config_yaml_file: t.TextIO = args.motor_config_yaml_file
    parts_list_csv_file: t.TextIO = args.parts_list_csv_file

    # Parse files
    motor_config: MotorConfig = MotorConfig(motor_config_yaml_file)
    parts_list_parser: PartsListParser = PartsListParser(parts_list_csv_file)

    # Close files used by parsers
    motor_config_yaml_file.close()
    parts_list_csv_file.close()

    # Initialize flight simulation
    # TODO Pass and use data parsed from files
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
