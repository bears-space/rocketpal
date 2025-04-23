#!/usr/bin/env python3

import argparse
import logging
import os

from bears_flight_simulation.simulation import load_configs_and_run_simulation


def dir_path(path_to_dir: str) -> str:
    if os.path.isdir(path_to_dir):
        return path_to_dir
    else:
        raise NotADirectoryError(path_to_dir)


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
