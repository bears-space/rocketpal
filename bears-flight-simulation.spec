# -*- mode: python ; coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import PySide6
from PyInstaller.utils.hooks import collect_all, collect_submodules

project_root = Path(SPECPATH)
pyside_dir = Path(PySide6.__file__).resolve().parent

pyside_datas, pyside_bins, pyside_hidden = collect_all("PySide6")
shiboken_datas, shiboken_bins, shiboken_hidden = collect_all("shiboken6")
rocketpy_datas, rocketpy_bins, rocketpy_hidden = collect_all("rocketpy")

# Ensure critical Qt runtime DLLs (including ICU) are colocated with Qt6Core.dll.
extra_qt_bins: list[tuple[str, str]] = []
for pattern in [
    "icu*.dll",
    "Qt6*.dll",
    "pyside6*.dll",
    "libEGL.dll",
    "libGLESv2.dll",
    "opengl32sw.dll",
]:
    for dll_path in pyside_dir.glob(pattern):
        extra_qt_bins.append((str(dll_path), "PySide6"))

binaries = pyside_bins + shiboken_bins + rocketpy_bins + extra_qt_bins
datas = pyside_datas + shiboken_datas + rocketpy_datas + [
    (str(project_root / "template"), "template"),
    (str(project_root / "img"), "img"),
]
hiddenimports = pyside_hidden + shiboken_hidden + rocketpy_hidden + collect_submodules("PySide6")


a = Analysis(
    ["bears_flight_simulation/simulation_gui.py"],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["scripts/pyinstaller_qt_runtime_hook.py"],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="bears-flight-simulation",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
