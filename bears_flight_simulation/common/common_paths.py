import os
import sys
from pathlib import Path

import platformdirs

USER_BASE_FOLDER = Path(platformdirs.user_config_dir()) / "bears-flight-simulation"
USER_SIMULATION_CONFIG_BASE_FOLDER = USER_BASE_FOLDER / "simulations"
USER_LIBRARY_CONFIG_BASE_FOLDER = USER_BASE_FOLDER / "libraries"
USER_LOCATION_LIBRARY_FOLDER = USER_LIBRARY_CONFIG_BASE_FOLDER / "locations"
USER_MOTOR_LIBRARY_FOLDER = USER_LIBRARY_CONFIG_BASE_FOLDER / "motors"
USER_PARACHUTE_LIBRARY_FOLDER = USER_LIBRARY_CONFIG_BASE_FOLDER / "parachutes"

OUTPUT_FOLDER = Path.cwd() / "output"


def _get_project_base_path() -> Path:
    # PyInstaller one-file mode extracts bundled files to a temporary directory.
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parents[2]


PROJECT_BASE_PATH = _get_project_base_path()
TEMPLATE_FOLDER = PROJECT_BASE_PATH / "template"

LOGO_PATH = PROJECT_BASE_PATH / "img" / "BEARS_writing_with_motto.svg"
ICON_PATH = PROJECT_BASE_PATH / "img" / "BEARS_Logo_white_circle.png"


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
