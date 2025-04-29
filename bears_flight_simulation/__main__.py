#!/usr/bin/env python3

import click
import logging
import os

from bears_flight_simulation.simulation import load_configs_and_run_simulation


def dir_path(path_to_dir: str) -> str:
    if os.path.isdir(path_to_dir):
        return path_to_dir
    else:
        raise NotADirectoryError(path_to_dir)


@click.command()
@click.argument(
    "config_folder", type=click.Path(exists=True, file_okay=False, path_type=str)
)
@click.option(
    "-o",
    "--output",
    default="./output",
    type=click.Path(exists=False, file_okay=False, path_type=str),
    help="The output folder, by default './output'",
)
def run_bears_flight_simulation(config_folder, output):
    """Run the BEARS flight simulation using the given config_folder."""
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    load_configs_and_run_simulation(config_folder, output)


run_bears_flight_simulation()
