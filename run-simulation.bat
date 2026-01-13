@echo off

: Ensure the output folder exists
if not exist %cd%\output mkdir %cd%\output

: Run simulation and redirect terminal output to ./output/log.txt
uv run python -m bears_flight_simulation sim .\template --output %cd%\output >> %cd%\output\log.txt 2>&1
