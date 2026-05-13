# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

import matplotlib.pyplot as plt

from bears_flight_simulation.hacks.matplotlib_hacks import (
    get_matplotlib_supported_file_endings,
    hack_override_matplotlib_show,
    hack_override_matplotlib_show_reset,
)

matplotlib_show_original = plt.show


def test_get_matplotlib_supported_file_endings():
    result = get_matplotlib_supported_file_endings()
    for filetype in plt.gcf().canvas.get_supported_filetypes().keys():
        assert f".{filetype}" in result


def test_hack_override_matplotlib_show__no_filename(tmp_path, monkeypatch):
    # Change current working directory to temporary directory
    monkeypatch.chdir(tmp_path)

    # Activate override
    hack_override_matplotlib_show()

    # Create some random plot
    plt.figure()
    plt.plot([1, 2, 3, 4, 5])
    plt.show()

    # Ensure a file is created
    assert Path("output").exists()
    assert Path("output/unnamed").exists()
    assert len(list(Path("output/unnamed").glob("*"))) == 1


def test_hack_override_matplotlib_show__no_filename_multiple(tmp_path, monkeypatch):
    # Change current working directory to temporary directory
    monkeypatch.chdir(tmp_path)

    # Activate override
    hack_override_matplotlib_show()

    for i in range(20):
        # Create some random plot
        plt.figure()
        plt.plot([1, 2, 3, 4, 5])
        plt.show()

    # Ensure a file is created
    assert Path("output").exists()
    assert Path("output/unnamed").exists()
    assert len(list(Path("output/unnamed").glob("*"))) == 20


def test_hack_override_matplotlib_show__with_filename(tmp_path, monkeypatch):
    # Change current working directory to temporary directory
    monkeypatch.chdir(tmp_path)

    # Activate override
    hack_override_matplotlib_show("my_specified_output_file.jpg")

    # Create some random plot
    plt.figure()
    plt.plot([1, 2, 3, 4, 5])
    plt.show()

    # Ensure the file is created
    assert Path("my_specified_output_file_0.jpg").exists()


def test_hack_override_matplotlib_show__with_filename_multiple(tmp_path, monkeypatch):
    # Change current working directory to temporary directory
    monkeypatch.chdir(tmp_path)

    # Activate override
    hack_override_matplotlib_show("my_specified_output_file.jpg")

    for i in range(20):
        # Create some random plot
        plt.figure()
        plt.plot([1, 2, 3, 4, 5])
        plt.show()

        # Ensure the file is created
        assert Path(f"my_specified_output_file_{i}.jpg").exists()


def test_hack_override_matplotlib_show_reset(tmp_path, monkeypatch):
    # Change current working directory to temporary directory
    monkeypatch.chdir(tmp_path)

    # First, activate override so we have something to reset from
    hack_override_matplotlib_show()
    assert plt.show != matplotlib_show_original

    # Then, reset the override
    hack_override_matplotlib_show_reset()
    assert plt.show == matplotlib_show_original
