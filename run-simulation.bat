@echo off

# Ensure the output folder exists
if not exist .\output mkdir .\output

# Run simulation and redirect terminal output to ./output/log.txt
python simulation\flight_simulation.py .\input --output .\output >> .\output\log.txt 2>&1
