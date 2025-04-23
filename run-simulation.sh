#!/usr/bin/env bash

# Ensure the output folder exists
mkdir -p $PWD/output

# Run simulation and redirect terminal output to ./output/log.txt
python -m bears_flight_simulation ./template --output $PWD/output &> $PWD/output/log.txt
