@echo off

# Ensure the output folder exists
if not exist .\output mkdir .\output

# Run simulation and redirect terminal output to ./output/log.txt
python bears_flight_simulation\simulation.py .\template --output .\output >> .\output\log.txt 2>&1
