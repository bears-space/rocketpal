# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from uuid import uuid4

from rocketpal.core.library import Library
from rocketpal.core.library_entry import LibraryEntry
from rocketpal.parsers.location_config import LocationConfig


class LocationLibrary(Library):
    def load_entry(self, data: dict) -> LibraryEntry:
        return LocationConfig(data)

    def new_entry(self) -> LibraryEntry:
        id = str(uuid4())
        entry = LocationConfig.new_default(id)
        self.entries[id] = entry
        self.save()
        return entry
