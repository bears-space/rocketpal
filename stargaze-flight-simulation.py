#!/usr/bin/env python3

import argparse
import logging
import os
import typing as t

from core.flight_simulation import FlightSimulation

from core.location_library import LocationLibrary
from core.motor_library import MotorLibrary
from parsers.config import Config
from parsers.location import Location
from parsers.motor_config import MotorConfig
from parsers.nose_cone_config import NoseConeConfig
from parsers.parts_list_parser import PartsListParser
from parsers.rail_button_config import RailButtonConfig

CONFIG_FILENAME = "/configuration.yaml"
MOTOR_FOLDERNAME = "/motors"
RAIL_BUTTONS_FILENAME = "/rail_buttons.yaml"
NOSE_CONE_FILENAME = "/nose_cone.yaml"
POWER_OFF_DRAG_CURVE_FILENAME = "/power_off_drag_curve.csv"
POWER_ON_DRAG_CURVE_FILENAME = "/power_on_drag_curve.csv"
FINS_RADIANS_FILENAME = "/fins_radians.csv"
PARTS_LIST_FILENAME = "/parts_list.csv"
LOCATION_FOLDERNAME = "/locations"


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
        RAIL_BUTTONS_FILENAME,
        POWER_OFF_DRAG_CURVE_FILENAME,
        POWER_ON_DRAG_CURVE_FILENAME,
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
            exit(2)  # 2 means "No such file or directory"

    # Check that all expected folders are present in the config folder
    for foldername in [
        MOTOR_FOLDERNAME,
        LOCATION_FOLDERNAME,
    ]:
        file_path = config_folder + foldername
        if not os.path.isdir(file_path):
            logging.error(
                "StargazeFlightSimulation: Missing folder '"
                + str(foldername)
                + "' in specified config folder! Aborting ..."
            )
            exit(2)  # 2 means "No such file or directory"

    # Load config
    config: Config
    with open(config_folder + CONFIG_FILENAME, "r") as file:
        config = Config(file)
        logging.info(
            "StargazeFlightSimulation: Using Config with id '" + str(config.id) + "'"
        )

    # Load requested location from location library
    location_library: LocationLibrary = LocationLibrary(
        config_folder + LOCATION_FOLDERNAME
    )
    launch_location: t.Union[Location, None] = location_library.get(config.location_id)
    if launch_location == None:
        logging.error(
            "StargazeFlightSimulation: The location with the id '"
            + config.location_id
            + "' does not exist in the location library. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"
    else:
        logging.info(
            "StargazeFlightSimulation: Using Location with id '"
            + str(launch_location.id)
            + "'"
        )

    # Load requested motors from motor library
    motor_library: MotorLibrary = MotorLibrary(config_folder + MOTOR_FOLDERNAME)
    motors: t.List[MotorConfig] = []
    for id in config.motor_ids:
        motor: t.Union[MotorConfig, None] = motor_library.get(id)
        if motor == None:
            logging.warning(
                "StargazeFlightSimulation: The motor with the id '"
                + id
                + "' does not exist in the motor library. Skipping ..."
            )
        else:
            motors.append(motor)
            logging.info(
                "StargazeFlightSimulation: Loaded MotorConfig with id '"
                + str(motor.id)
                + "'"
            )

    # Ensure at least one motor is loaded
    if len(motors) == 0:
        logging.error(
            "StargazeFlightSimulation: No motors have been loaded. Aborting ..."
        )
        exit(2)  # 2 means "No such file or directory"

    # Use first motor from list
    # TODO Iterate over motors instead, allowing for comparison between different motors in one run
    motor_config = motors[0]
    logging.info(
        "StargazeFlightSimulation: Choosing MotorConfig with id '"
        + str(motor_config.id)
        + "'"
    )

    # Load rail button config
    rail_button_config: RailButtonConfig
    with open(config_folder + RAIL_BUTTONS_FILENAME, "r") as file:
        rail_button_config = RailButtonConfig(file)

    # Load rail button config
    nose_cone_config: NoseConeConfig
    with open(config_folder + NOSE_CONE_FILENAME, "r") as file:
        nose_cone_config = NoseConeConfig(file)

    # Parse parts list
    parts_list_parser: PartsListParser
    with open(config_folder + PARTS_LIST_FILENAME, "r") as file:
        parts_list_parser = PartsListParser(file)
    # TODO do something with the parts list

    # Initialize flight simulation
    sim: FlightSimulation = FlightSimulation(
        config=config,
        output_folder=output_folder,
        motor_file_path=config_folder
        + MOTOR_FOLDERNAME
        + "/"
        + motor_config.engine_filename,
        motor_config=motor_config,
        rail_button_config=rail_button_config,
        nose_cone_config=nose_cone_config,
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
