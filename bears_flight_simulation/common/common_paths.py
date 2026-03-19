import platformdirs
from pathlib import Path
import os
import sys

USER_BASE_FOLDER = Path(platformdirs.user_config_dir()) / "bears-flight-simulation"
USER_SIMULATION_CONFIG_BASE_FOLDER = USER_BASE_FOLDER / "simulations"
USER_LIBRARY_CONFIG_BASE_FOLDER = USER_BASE_FOLDER / "libraries"
USER_LOCATION_LIBRARY_FOLDER = USER_LIBRARY_CONFIG_BASE_FOLDER / "locations"
USER_MOTOR_LIBRARY_FOLDER = USER_LIBRARY_CONFIG_BASE_FOLDER / "motors"
USER_PARACHUTE_LIBRARY_FOLDER = USER_LIBRARY_CONFIG_BASE_FOLDER / "parachutes"

OUTPUT_FOLDER = Path(os.path.realpath(sys.argv[0])).parent / "output"
TEMPLATE_FOLDER = Path(__file__).parent.parent.parent / "template"

LOGO_PATH = Path(__file__).parent.parent.parent / "img" / "BEARS_writing_with_motto.svg"
ICON_PATH = Path(__file__).parent.parent.parent / "img" / "BEARS_Logo_white_circle.png"


def _get_config_folders(base_folder: Path) -> set[Path]:
    # Create the specified base config folder if it doesn't exist yet
    base_folder.mkdir(parents=True, exist_ok=True)

    return set(Path(entry) for entry in os.listdir(base_folder))


def get_simulation_entries() -> set[Path]:
    return _get_config_folders(USER_SIMULATION_CONFIG_BASE_FOLDER)


def get_location_entries() -> set[Path]:
    return _get_config_folders(USER_LOCATION_LIBRARY_FOLDER)


def get_motor_entries() -> set[Path]:
    return _get_config_folders(USER_MOTOR_LIBRARY_FOLDER)


def get_parachute_entries() -> set[Path]:
    return _get_config_folders(USER_PARACHUTE_LIBRARY_FOLDER)
