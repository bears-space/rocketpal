#!/usr/bin/env bash

# Ensure the output folder exists
mkdir -p $PWD/output

# Run simulation and redirect terminal output to ./output/log.txt
uv run python -m bears_flight_simulation sim ./template --output $PWD/output 2>&1 | tee $PWD/output/log.txt
