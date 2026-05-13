# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from uuid import uuid4

from bears_flight_simulation.core.library import Library
from bears_flight_simulation.core.library_entry import LibraryEntry
from bears_flight_simulation.parsers.airbrake_config import AirbrakeConfig


class AirbrakeLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return AirbrakeConfig(data, self.library_folder)

    def new_entry(self) -> LibraryEntry:
        id = str(uuid4())
        entry = AirbrakeConfig.new_default(id)
        self.entries[id] = entry
        self.save()
        return entry
