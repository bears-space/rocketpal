# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

param(
    [string]$ConfigDir = ".\template",
    [string]$OutputDir = ".\output"
)

# Ensure the output folder exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Run simulation and redirect output to ./output/log.txt
uv run python -m rocketpal sim $ConfigDir --output $OutputDir 2>&1 | Tee-Object -FilePath (Join-Path $OutputDir "log.txt")
