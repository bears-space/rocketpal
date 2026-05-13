# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod

from bears_flight_simulation.core.config import Config


class LibraryEntry(ABC, Config):
    def __init__(self, data: dict) -> None:
        self.extend_field_links([("id", str)])
        super().__init__(data)

    @classmethod
    @abstractmethod
    def new_default(cls, id: str) -> "LibraryEntry":
        raise NotImplementedError
