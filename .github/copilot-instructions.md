# BEARS Flight Simulation Guidelines

## Build and Test
- Install and update dependencies with `uv sync` from the repository root.
- Run tests with `uv run python -m pytest`.
- Run lint and formatting checks with `pre-commit run --all-files`.
- Run the CLI simulation with `uv run python -m bears_flight_simulation sim ./input --output ./output`.
- Run the GUI with `uv run python -m bears_flight_simulation gui`.

## Resource Efficiency
- Prefer targeted file reads and searches over full-repo scans unless a task explicitly requires broad discovery.
- Reuse already collected context and avoid repeated tool calls for the same information.
- Make focused, minimal edits; avoid broad refactors unless requested.
- Validate changes with the smallest relevant command first (for example specific tests before full test suites).
- Avoid launching subagents for simple tasks that can be completed directly.
- Keep responses concise and implementation-oriented unless detailed explanations are explicitly requested.

## Architecture
- Main package: `bears_flight_simulation/`.
- CLI entrypoint is in `bears_flight_simulation/__main__.py` and exposes `sim` and `gui` commands.
- Runtime orchestration starts in `bears_flight_simulation/simulation.py`, then delegates to `bears_flight_simulation/core/flight_simulation.py`.
- `bears_flight_simulation/core/` contains simulation engine code and reusable library abstractions.
- `bears_flight_simulation/parsers/` parses YAML or CSV-backed config and parts data.
- `bears_flight_simulation/exporters/` writes plots and data outputs.
- `bears_flight_simulation/gui/` contains PySide6 widgets and GUI-specific behavior.

## Code Conventions
- Use modern Python typing syntax consistent with the codebase (for example `list[str]` and `Type | None`).
- Prefer `pathlib.Path` for new path-handling code.
- Keep parser and library boundaries clear.
- Parsing and data validation logic belongs in `parsers/`.
- Simulation orchestration belongs in `simulation.py` and `core/`.
- Library lookup behavior belongs in `core/*_library.py` classes.
- Use `yaml.safe_load` for YAML parsing.
- Follow existing logging style with `logging` module and explicit info or warning messages.

## Pitfalls and Gotchas
- RocketPy plotting behavior is patched via `bears_flight_simulation/hacks/matplotlib_hacks.py`; preserve this flow when changing plotting or export behavior.
- Simulation startup requires a strict configuration folder layout enforced by `_ensure_config_files_exist` in `bears_flight_simulation/simulation.py`.
- Motor files are expected in `.eng` (RASP) format.

## References
- Setup, usage, and operational workflows: `README.md`.
- Required configuration layout and loading flow: `bears_flight_simulation/simulation.py`.
- Core flight setup and simulation logic: `bears_flight_simulation/core/flight_simulation.py`.
- Pre-commit hooks and style checks: `.pre-commit-config.yaml`.
