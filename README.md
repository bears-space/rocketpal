# RocketPal

[![pre-commit](https://github.com/bears-space/rocketpal/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/bears-space/rocketpal/actions/workflows/pre-commit.yaml)
[![pytest](https://github.com/bears-space/rocketpal/actions/workflows/pytest.yaml/badge.svg)](https://github.com/bears-space/rocketpal/actions/workflows/pytest.yaml)
[![Ruff](https://github.com/bears-space/rocketpal/actions/workflows/ruff.yaml/badge.svg)](https://github.com/bears-space/rocketpal/actions/workflows/ruff.yaml)
[![docs](https://github.com/bears-space/rocketpal/actions/workflows/docs.yaml/badge.svg)](https://github.com/bears-space/rocketpal/actions/workflows/docs.yaml)

This is the [RocketPy](https://github.com/RocketPy-Team/RocketPy/)-based flight simulation for BEARS rockets, built by [BEARS (Berlin Experimental Astronautics Research Student Team e.V.)](https://www.bears-space.de/).

## Usage

### Setup / Installation

#### Setup uv

First, we need to install `uv`, a Python package manager.

- On Linux and macOS, use `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- On Windows, use `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.
- When in doubt, refer to the official setup instructions: <https://docs.astral.sh/uv/getting-started/installation/>

#### Sync dependencies with uv

To install or update the dependencies of this project, run this command from within the project root:

```sh
uv sync --dev
```

The `uv` package manager also automatically manages a separate Python installation for the project, so you do not have to think about your system-wide Python installation and pip packages.

#### Setup pre-commit

To ensure a consistent style in the repository, pre-commit hooks are used.

Within the project root, install the pre-commit hooks to the local repository:

```sh
pre-commit install
```

The hooks are based on the configuration located in `.pre-commit-config.yaml` and will be run automatically before every git commit.

### Basic usage

If you just want to run the simulation with default parameters, you can use one of the two provided scripts (assuming you installed Python and all required packages).

**On Windows**, run the following in a command prompt:

```ps
powershell -ExecutionPolicy Bypass -file .\run-simulation.ps1 .\template .\output
```

**On Linux**, run the following in a terminal:

```sh
bash ./run-simulation.sh ./template ./output
```

In both cases, if you do not pass arguments, the simulation uses the `./template` folder to read its configuration and the `./output` folder for output.

### Advanced usage

The package contains two commands: The simulation (`sim`) and the GUI (`gui`).

You can run the simulation from a terminal as follows:

```sh
uv run -m rocketpal sim ./input --output ./output
```

To see the available command line parameters, run one of the following (depending on what info you need):

```sh
uv run -m rocketpal --help
uv run -m rocketpal sim --help
uv run -m rocketpal gui --help
```

### Run unit tests

To run the provided unit tests, run this command from within the project root:

```sh
uv run -m pytest
```

### API documentation

The generated API documentation is published to GitHub Pages after each push to `main`.
You can find it at <https://bears-space.de/rocketpal/>.

### Configuration

A file for the motor has to be provided in `.eng` format. On at least one website offering compatible files, this format has been referred to as "RASP" format. It is documented here: <https://www.thrustcurve.org/info/raspformat.html>
