# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# Ensure the output folder exists
$outputDir = Join-Path $PWD "output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Run simulation and redirect output to ./output/log.txt
uv run python -m bears_flight_simulation sim .\template --output $outputDir 2>&1 | Tee-Object -FilePath (Join-Path $outputDir "log.txt")
