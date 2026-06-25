#!/usr/bin/env bash

# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

configDir="${1:-./template}"
outputDir="${2:-./output}"

# Ensure the output folder exists
mkdir -p "$outputDir"

# Run simulation
uv run -m rocketpal sim "$configDir" --output "$outputDir"
