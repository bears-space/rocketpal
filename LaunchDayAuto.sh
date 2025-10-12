#!/usr/bin/env bash

# Ensure the output folders exists
mkdir -p $PWD/output-manual
mkdir -p $PWD/output-airbrake
mkdir -p $PWD/output-noairbrake
mkdir -p $PWD/output-ballistic

# Run simulations and redirect terminal outputs
python -m bears_flight_simulation sim ./template --output $PWD/output-manual 2>&1 | tee $PWD/output-manual/log.txt
python -m bears_flight_simulation sim ./template-euroc25-scenario-airbrake --output $PWD/output-airbrake 2>&1 | tee $PWD/output-airbrake/log.txt
python -m bears_flight_simulation sim ./template-euroc25-scenario-noairbrake --output $PWD/output-noairbrake 2>&1 | tee $PWD/output-noairbrake/log.txt
python -m bears_flight_simulation sim ./template-euroc25-scenario-ballistic --output $PWD/output-ballistic 2>&1 | tee $PWD/output-ballistic/log.txt
