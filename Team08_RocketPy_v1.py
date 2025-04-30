#!/usr/bin/env python3

import logging
from pathlib import Path

from bears_flight_simulation.simulation import load_configs_and_run_simulation

CONFIG_FOLDER = Path(__file__).parent / "template"
OUTPUT_FOLDER = Path(__file__).parent / "output"

# Set default logging level
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

load_configs_and_run_simulation(str(CONFIG_FOLDER), str(OUTPUT_FOLDER))
