import platformdirs
from pathlib import Path
import os
import sys

SIMULATION_CONFIG_BASE_FOLDER = (
    platformdirs.user_config_dir() + "/bears-flight-simulation/simulations"
)
LIBRARY_CONFIG_BASE_FOLDER = (
    platformdirs.user_config_dir() + "/bears-flight-simulation/libraries"
)
LOCATION_LIBRARY_CONFIG_BASE_FOLDER = (
    platformdirs.user_config_dir() + "/bears-flight-simulation/libraries/locations"
)
MOTOR_LIBRARY_CONFIG_BASE_FOLDER = (
    platformdirs.user_config_dir() + "/bears-flight-simulation/libraries/motors"
)
PARACHUTE_LIBRARY_CONFIG_BASE_FOLDER = (
    platformdirs.user_config_dir() + "/bears-flight-simulation/libraries/parachutes"
)

OUTPUT_FOLDER = str(Path(os.path.realpath(sys.argv[0])).parent) + "/output"
TEMPLATE_FOLDER = str(Path(__file__).parent.parent.parent) + "/template"
LOGO_PATH = (
    str(Path(__file__).parent.parent.parent) + "/img/BEARS_writing_with_motto.svg"
)


def _get_config_folders(base_folder: str) -> set[str]:
    # Create the specified base config folder if it doesn't exist yet
    Path(base_folder).mkdir(parents=True, exist_ok=True)

    return set(os.listdir(base_folder))


def get_simulation_config_folders() -> set[str]:
    return _get_config_folders(SIMULATION_CONFIG_BASE_FOLDER)


def get_location_config_folders() -> set[str]:
    return _get_config_folders(LOCATION_LIBRARY_CONFIG_BASE_FOLDER)


def get_motor_config_folders() -> set[str]:
    return _get_config_folders(MOTOR_LIBRARY_CONFIG_BASE_FOLDER)


def get_parachute_config_folders() -> set[str]:
    return _get_config_folders(PARACHUTE_LIBRARY_CONFIG_BASE_FOLDER)
