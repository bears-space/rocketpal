# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _read_project_version() -> str:
    pyproject_path = ROOT / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    return pyproject["project"]["version"]


def _read_commit_hash() -> str:
    commit_hash = os.environ.get("GIT_COMMIT_HASH") or os.environ.get("GITHUB_SHA")
    if commit_hash:
        return commit_hash[:12]

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError, subprocess.CalledProcessError:
        return "unknown"

    return result.stdout.strip() or "unknown"


project = "RocketPal"
author = "BEARS e.V. and contributors"
copyright = f"2023-{date.today().year}, BEARS e.V. and contributors"
version = _read_project_version()
release = version
commit_hash = _read_commit_hash()
rst_prolog = f"""
.. |docs_version| replace:: {release}
.. |docs_commit| replace:: {commit_hash}
"""

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_typehints = "description"
