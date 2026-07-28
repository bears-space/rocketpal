#!/usr/bin/env python3

# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging
import os
from pathlib import Path

import click

from rocketpal.simulation import load_configs_and_run_simulation


def dir_path(path_to_dir: str) -> str:
    if os.path.isdir(path_to_dir):
        return path_to_dir
    else:
        raise NotADirectoryError(path_to_dir)


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "config_folder", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option(
    "-o",
    "--output",
    default="./output",
    type=click.Path(exists=False, file_okay=False, path_type=Path),
    help="The output folder, by default './output'",
)
def sim(config_folder, output):
    """Run RocketPal using the given config_folder."""
    load_configs_and_run_simulation(config_folder, output)


@cli.command()
def gui():
    """Run the RocketPal GUI."""
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Import GUI module only when GUI command is invoked
    from rocketpal.simulation_gui import start_and_hand_over_to_simulation_gui

    start_and_hand_over_to_simulation_gui()


cli()
