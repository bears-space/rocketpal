# stargaze-flight-simulation

This is the [RocketPy](https://github.com/RocketPy-Team/RocketPy/)-based flight simulation for the STARGAZE rocket, built by [BEARS (Berlin Experimental Astronautics Research Student Team e.V.)](https://www.bears-space.de/).

## Usage

TODO

## Setup development environment

### Setup pyenv

First, we need to setup pyenv. This is required because we need to use a specific Python version, namely 3.8.0, and pyenv allows us to specify a Python version for this specific repository without affecting your system-wide Python installation.

Install pyenv on your system. This step varies based on your OS:

- **Linux**:
  - On **Arch**-based systems, run `sudo pacman -S pyenv`.
  - On **Ubuntu**-based systems, there is no package available. Install `pyenv` manually using `curl https://pyenv.run | bash`, as per [the instructions on their GitHub page](https://github.com/pyenv/pyenv#automatic-installer).
- **Windows**: Install `pyenv-win`. Follow the installation instructions on [pyenv-win's website](https://pyenv-win.github.io/pyenv-win/).
- **MacOS**: Install `pyenv` via [Homebrew](https://brew.sh/) using `brew install pyenv`.

If you are on **Linux** or **MacOS**, continue by setting up your shell environment for pyenv by following [their instructions on GitHub](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv).

Restart your computer after this.

Additionally, on **Linux** systems, it is recommended that you install typical build dependencies:

- On **Arch**-based systems, run `sudo pacman -S --needed base-devel`.
- On **Ubuntu**-based systems, run `sudo apt install build-essential`.

Now, install Python 3.8.0 using pyenv, like this:

```sh
pyenv install -v 3.8.0
```

Confirm Python 3.8.0 has been installed by checking the output of this command:

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
python3 -m venv venv

# Enter the virtual environment (VSCode can do this automatically if you activate it via the corresponding popup)
# This may vary slightly on Windows
source venv/bin/activate
```

Ensure you are in the venv, for example by checking that the output of the following command points into this repository:

```sh
pip -V
```

Before we install the required packages, update the local pip installation:

```sh
pip install --upgrade pip
```

Install the required packages using pip:

```sh
pip install --requirement requirements.txt
```
