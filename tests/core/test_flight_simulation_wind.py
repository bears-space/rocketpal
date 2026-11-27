# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Tests for wind speed and direction conversion in flight simulation."""

import math

from rocketpal.core.flight_simulation import wind_speed_and_direction_to_east_and_north


class TestWindConversion:
    """Test wind conversion with meteorological conventions."""

    def test_wind_from_north_gives_negative_north_component(self):
        """Wind from 0° (North) should give negative north component.

        Meteorologically, wind FROM North blows South, so the velocity vector points south:
        - East component = 0 (no east-west motion)
        - North component = -wind_speed (moving south/negative north direction)
        """
        east, north = wind_speed_and_direction_to_east_and_north(10.0, 0)

        assert abs(east) < 1e-9, f"East should be ~0 for wind from North, got {east}"
        assert math.isclose(north, -10.0, rel_tol=1e-9, abs_tol=1e-9), (
            f"North should be -10.0 for wind from North, got {north}"
        )

    def test_wind_from_east_gives_negative_east_component(self):
        """Wind from 90° (East) should give negative east component.

        Meteorologically, wind FROM East blows West, so the velocity vector
        points toward West:
        - East component = -wind_speed (moving west/negative east)
        - North component = 0 (no north-south motion)
        """
        east, north = wind_speed_and_direction_to_east_and_north(10.0, 90)

        assert math.isclose(east, -10.0, rel_tol=1e-9, abs_tol=1e-9), (
            f"East should be -10.0 for wind from East, got {east}"
        )
        assert abs(north) < 0.001, f"North should be ~0 for wind from East, got {north}"

    def test_wind_from_south_gives_positive_north_component(self):
        """Wind from 180° (South) should give positive north component.

        Meteorologically, wind FROM South blows North, so:
        - East component = 0 (no east-west motion)
        - North component = +wind_speed (moving north/positive north)
        """
        east, north = wind_speed_and_direction_to_east_and_north(10.0, 180)

        assert abs(east) < 0.001, f"East should be ~0 for wind from South, got {east}"
        assert math.isclose(north, 10.0, rel_tol=1e-9, abs_tol=1e-9), (
            f"North should be 10.0 for wind from South, got {north}"
        )

    def test_wind_from_west_gives_positive_east_component(self):
        """Wind from 270° (West) should give positive east component.

        Meteorologically, wind FROM West blows East, so:
        - East component = +wind_speed (moving east/positive east)
        - North component = 0 (no north-south motion)
        """
        east, north = wind_speed_and_direction_to_east_and_north(10.0, 270)

        assert math.isclose(east, 10.0, rel_tol=1e-9, abs_tol=1e-9), (
            f"East should be 10.0 for wind from West, got {east}"
        )
        assert abs(north) < 0.001, f"North should be ~0 for wind from West, got {north}"

    def test_wind_with_zero_speed_gives_zero_components(self):
        """Zero wind speed should give zero components regardless of direction."""
        east, north = wind_speed_and_direction_to_east_and_north(0.0, 45)

        assert east == 0.0, f"East should be 0 for zero wind speed, got {east}"
        assert north == 0.0, f"North should be 0 for zero wind speed, got {north}"

    def test_wind_with_arbitrary_direction(self):
        """Wind at 45° should give equal magnitude east and south components."""
        east, north = wind_speed_and_direction_to_east_and_north(10.0, 45)

        expected_magnitude = 10.0 * math.sqrt(2) / 2  # 10 / sqrt(2) ≈ 7.07
        assert math.isclose(
            abs(east), expected_magnitude, rel_tol=1e-9, abs_tol=1e-9
        ), f"East magnitude should be ~{expected_magnitude:.4f}, got {abs(east):.4f}"
        assert math.isclose(
            abs(north), expected_magnitude, rel_tol=1e-9, abs_tol=1e-9
        ), f"North magnitude should be ~{expected_magnitude:.4f}, got {abs(north):.4f}"

    def test_wind_with_315_degrees(self):
        """Wind from 315° (northeast) blows toward 135° (southeast), giving positive east component."""

        # Wind FROM 315° (NE quadrant) blows toward the opposite: 315° + 180° = 495° ≡ 135°
        # 135° in meteorological convention is SSE (SE-South), which in Cartesian coordinates
        # has positive east (toward SE) and negative north (toward S)
        east, north = wind_speed_and_direction_to_east_and_north(10.0, 315)

        expected_magnitude = 10.0 * math.sqrt(2) / 2  # ≈ 7.07

        assert math.isclose(
            abs(east), expected_magnitude, rel_tol=1e-9, abs_tol=1e-9
        ), f"East magnitude should be ~{expected_magnitude:.4f}, got {abs(east):.4f}"
        assert math.isclose(
            abs(north), expected_magnitude, rel_tol=1e-9, abs_tol=1e-9
        ), f"North magnitude should be ~{expected_magnitude:.4f}, got {abs(north):.4f}"

        # Wind from NE (315°) blows toward SE (135°), which has positive east component
        assert east > 0, f"East should be positive for wind from 315°, got {east}"
        assert north < 0, f"North should be negative for wind from 315°, got {north}"

    def test_wind_magnitude_preservation(self):
        """The magnitude of the wind vector should be preserved."""
        for direction in [0, 45, 90, 135, 180, 225, 270, 315, 360]:
            east, north = wind_speed_and_direction_to_east_and_north(10.0, direction)
            magnitude = math.sqrt(east**2 + north**2)
            assert math.isclose(magnitude, 10.0, rel_tol=1e-9, abs_tol=1e-9), (
                f"Magnitude at {direction}° should be 10.0, got {magnitude}"
            )
