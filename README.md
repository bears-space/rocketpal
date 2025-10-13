# stargaze-flight-simulation

[![Ruff](https://github.com/bears-space/stargaze-flight-simulation/actions/workflows/ruff.yaml/badge.svg)](https://github.com/bears-space/stargaze-flight-simulation/actions/workflows/ruff.yaml)

This is the [RocketPy](https://github.com/RocketPy-Team/RocketPy/)-based flight simulation for the STARGAZE rocket, built by [BEARS (Berlin Experimental Astronautics Research Student Team e.V.)](https://www.bears-space.de/).

NOTE: The GUI is currently unmaintained and broken, but is still included for future use.

## Instructions for EuRoC evaluators

To run the simulation, install Python and all requirements listend in the `requirements.txt` (refer ot the section [Setup development environment](#setup-development-environment)). Then, you should be able to run the simulation with the following command:

```sh
python Team08_RocketPy_v5.py
```

This will output the simulation results (graphics and other files) in the `./output` folder.

## Usage

### Setup / Installation

Before you can run the simulation, you need to install the correct version of Python (3.13.2) and the required packages from Pip. For this, please follow the instructions in the section [Setup development environment](#setup-development-environment).

### Basic usage

If you just want to run the simulation with default parameters, you can use one of the two provided scripts (assuming you installed Python and all required pip packages).

**On Windows**, run the following in a command prompt:

```bat
.\run-simulation.bat
```

**On Linux**, run the following in a terminal:

```sh
./run-simulation.sh
```

In both cases, the simulation uses the `./input` folder to read its configuration and the `./output` folder for output.

### Advanced usage

The package contains two commands: The simulation (`sim`) and the GUI (`gui`).

You can run the simulation from a terminal as follows:

```sh
python -m bears_flight_simulation sim ./input --output ./output
```

To see the available command line parameters, run one of the following (depending on what info you need):

```sh
python -m bears_flight_simulation --help
python -m bears_flight_simulation sim --help
python -m bears_flight_simulation gui --help
```

### Configuration

A file for the motor has to be provided in `.eng` format. On at least one website offering compatible files, this format has been referred to as "RASP" format. It is documented here: <https://www.thrustcurve.org/info/raspformat.html>

## Setup development environment

### Setup pyenv

First, we need to setup pyenv. This is required because we need to use a specific Python version, namely 3.13.2, and pyenv allows us to specify a Python version for this specific repository without affecting your system-wide Python installation.

Install pyenv on your system. This step varies based on your OS:

- **Linux**:
  - On **Arch**-based systems, run `sudo pacman -S pyenv`.
  - On **Ubuntu**-based systems, there is no package available. Install `pyenv` manually using `curl https://pyenv.run | bash`, as per [the instructions on their GitHub page](https://github.com/pyenv/pyenv#automatic-installer).
- **Windows**: Install `pyenv-win` using PowerShell by following the installation instructions on [pyenv-win's website](https://pyenv-win.github.io/pyenv-win/docs/installation.html#powershell). You do not need to follow their instructions for installing python versions, as this will be covered by the rest of this README.
- **MacOS**: Install `pyenv` via [Homebrew](https://brew.sh/) using `brew install pyenv`.

If you are on **Linux** or **MacOS**, continue by setting up your shell environment for pyenv by following [their instructions on GitHub](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv).

**Restart your computer after this.**

Additionally, on **Linux** systems, it is recommended that you install typical build dependencies:

- On **Arch**-based systems, run `sudo pacman -S --needed base-devel`.
- On **Ubuntu**-based systems, run `sudo apt install build-essential`.

If you are on a **Linux or MacOS** system, ensure Tk (for `tkinter`) is installed before you continue or you won't be able to see any graphical output. For example, on Arch-based systems, run `sudo pacman -S tk`.

Now, install Python 3.13.2 using pyenv, like this:

```sh
pyenv install 3.13.2
```

Confirm Python 3.13.2 has been installed by checking the output of this command:

```sh
pyenv versions
```

Now, ensure you are in the root folder of this repository.

The python version should be automatically selected thanks to the `.python-version` file in this repository's root. Ensure that this worked by checking the output of this command:

```sh
python --version
```

### Setup venv

Now, we need to setup a python virtual environment in which python libraries used by this project are managed.

Setup a python virtual environment by doing the following (from the root folder of the repository):

```sh
# Create the virtual environment
python -m venv venv

# Enter the virtual environment (VSCode can do this automatically if you activate it via the corresponding popup)
# for UNIX:
source venv/bin/activate
# for WINDOWS:
venv\Scripts\Activate.ps1
```

Ensure you are in the venv, for example by checking that the output of the following command points into this repository:

```sh
python -m pip -V
```

Before we install the required packages, update the local pip installation:

```sh
python -m pip install --upgrade pip
```

Install the required packages using pip:

```sh
python -m pip install --requirement requirements.txt
```

### Setup pre-commit

To ensure a consistent style in the repository, we use pre-commit hooks.

If you followed the venv installation steps from the previous section, `pre-commit` should have been installed automatically. Ensure this is the case by checking the output of this command:

```sh
pre-commit --version
```

If this **didn't** work, try installing the requirements again:

```sh
python -m pip install --requirement requirements.txt
```

In any case, finish by installing the pre-commit hooks to the local repository:

```sh
pre-commit install
```

The hooks are based on the configuration located in `.pre-commit-config.yaml` and will be run automatically before every git commit.

## How to import up-to-date parts list

The parts list is provided by BEARS in Excel (.xlsx) format. The following steps are used to convert it into a format usable by the flight simulation.

First, open the parts list Excel table online and store a local copy (*Datei -> Eine Kopie Erstellen -> Eine Kopie herunterladen*):

![Screenshot showing how to save a local copy in Excel Online](img/parts-list-conversion-step-1.png)

Second, open the local copy (.xlsx) in LibreOffice Calc and save it as a CSV file (.csv), accepting the warning dialogs about exporting to CSV:

![Screenshot showing how to access 'Save As' in LibreOffice](img/parts-list-conversion-step-2a.png)
![Screenshot showing the file saving dialog where you have to make sure the file ending is .csv](img/parts-list-conversion-step-2b.png)
![Screenshot showing a warning dialog about saving to .csv, where you have to confirm you want .csv](img/parts-list-conversion-step-2c.png)
![Screenshot showing the export configuration for the .csv file](img/parts-list-conversion-step-2d.png)
![Screenshot showing a warning dialog about only saving the currently opened table to .csv, where you have to press 'OK'](img/parts-list-conversion-step-2e.png)

Finally, open the CSV file (.csv) in a text editor, copy the contents and paste them into `template/parts_list.csv`, replacing the old file contents.

![Screenshot showing the .csv file opened in a text editor, where you have to copy the content](img/parts-list-conversion-step-3a.png)
![Screenshot showing the parts_list.csv opened in VSCode, where you have to replace the content by pasting](img/parts-list-conversion-step-3b.png)
