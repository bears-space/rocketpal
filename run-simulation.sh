#!/usr/bin/env bash

# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

# Ensure the output folder exists
mkdir -p $PWD/output

# Run simulation and redirect terminal output to ./output/log.txt
uv run python -m rocketpal sim ./template --output $PWD/output 2>&1 | tee $PWD/output/log.txt
