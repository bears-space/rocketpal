@echo off

: Ensure the output folder exists
if not exist %cd%\output mkdir %cd%\output

: Run simulation and redirect terminal output to ./output/log.txt
python bears_flight_simulation\simulation.py sim .\template --output %cd%\output >> %cd%\output\log.txt 2>&1
