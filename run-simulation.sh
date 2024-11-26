#!/usr/bin/env bash

# Ensure the output folder exists
mkdir -p ./output

# Run simulation and redirect terminal output to ./output/log.txt
python stargaze_flight_simulation.py ./input --output ./output &> ./output/log.txt
