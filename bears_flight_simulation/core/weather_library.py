# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from uuid import uuid4

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.parsers.weather_config import WeatherConfig


class WeatherLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return WeatherConfig(data)

    def new_entry(self) -> LibraryEntry:
        id = str(uuid4())
        entry = WeatherConfig.new_default(id)
        self.entries[id] = entry
        self.save()
        return entry
