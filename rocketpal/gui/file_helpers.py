# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import subprocess
import sys
from pathlib import Path


def open_explorer(directory: Path) -> bool:
    if not directory.exists():
        print(f"The path {directory} does not exist.")
        return False

    # Convert to string for subprocess compatibility
    target = str(directory)

    # Open platform-specific file explorer
    try:
        if sys.platform == "win32":
            import os

            os.startfile(target)
        elif sys.platform == "darwin":
            subprocess.call(["open", target])
        else:
            subprocess.call(["xdg-open", target])
    except Exception as e:  # noqa: BLE001
        print(f"Failed to open file explorer: {e}")
        return False

    return True
