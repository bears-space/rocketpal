"""PyInstaller runtime hook for robust Qt DLL loading on Windows/Wine."""

from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.platform.startswith("win"):
    meipass = Path(getattr(sys, "_MEIPASS", ""))
    if meipass:
        candidate_dirs = [
            meipass,
            meipass / "PySide6",
            meipass / "PySide6" / "Qt" / "bin",
        ]

        # Resolve dynamically to keep static type checkers happy on non-Windows.
        add_dll_directory = getattr(os, "add_dll_directory", None)

        # Ensure Windows DLL loader can resolve transitive Qt dependencies.
        for dll_dir in candidate_dirs:
            if not dll_dir.is_dir():
                continue

            if callable(add_dll_directory):
                add_dll_directory(str(dll_dir))

        existing_path = os.environ.get("PATH", "")
        prepended = os.pathsep.join(str(d) for d in candidate_dirs if d.is_dir())
        if prepended:
            os.environ["PATH"] = prepended + os.pathsep + existing_path
