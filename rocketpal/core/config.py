# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later


class Config:
    def __init__(self, data: dict) -> None:
        self.extend_field_links([])
        for field_name, field_type in self.field_links:
            self.__setattr__(field_name, field_type(data[field_name]))

    def serialize(self) -> dict:
        return {
            field_name: getattr(self, field_name) for field_name, _ in self.field_links
        }

    def extend_field_links(self, new_field_links: list[tuple[str, type]]) -> None:
        existing_field_links = getattr(self, "field_links", None)
        if existing_field_links is None:
            self.field_links = []
        self.field_links += new_field_links
