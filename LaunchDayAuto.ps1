# Ensure the output folders exist
$folders = @(
    "$PWD/output-manual",
    "$PWD/output-airbrake",
    "$PWD/output-noairbrake",
    "$PWD/output-ballistic"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
    }
}

# Run simulations and redirect terminal outputs
python -m bears_flight_simulation sim ./template --output "$PWD/output-manual" *>&1 | Tee-Object "$PWD/output-manual/log.txt"
python -m bears_flight_simulation sim ./template-euroc25-scenario-airbrake --output "$PWD/output-airbrake" *>&1 | Tee-Object "$PWD/output-airbrake/log.txt"
python -m bears_flight_simulation sim ./template-euroc25-scenario-noairbrake --output "$PWD/output-noairbrake" *>&1 | Tee-Object "$PWD/output-noairbrake/log.txt"
python -m bears_flight_simulation sim ./template-euroc25-scenario-ballistic --output "$PWD/output-ballistic" *>&1 | Tee-Object "$PWD/output-ballistic/log.txt"
