#!/usr/bin/env bash

# Ensure the output folder exists
mkdir -p ./output

# Run simulation and redirect terminal output to ./output/log.txt
python simulation/simulation.py ./template --output ./output &> ./output/log.txt
