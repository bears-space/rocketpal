#!/usr/bin/env bash

# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

configDir="${1:-./template}"
outputDir="${2:-./output}"

# Ensure the output folder exists
mkdir -p "$outputDir"

# Run simulation and redirect terminal output to ./output/log.txt
uv run python -m rocketpal sim "$configDir" --output "$outputDir" 2>&1 | tee "$outputDir/log.txt"
