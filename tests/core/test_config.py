# Copyright (C) 2023-2026  BEARS e.V. and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

from rocketpal.core.config import Config


def test_init__empty():
    """Test that empty Config initialization works."""
    config = Config({})
    assert isinstance(config.__dict__, dict)


def test_init__one_field():
    """Test Config with one required field present."""

    class OneFieldConfig(Config):
        field_links = [("field1", int)]

    config = OneFieldConfig({"field1": "42"})
    assert config.field1 == 42  # type: ignore


def test_init__multiple_fields():
    """Test Config with multiple required fields present."""

    class MultipleFieldsConfig(Config):
        field_links = [
            ("field1", int),
            ("field2", float),
            ("field3", str),
        ]

    config = MultipleFieldsConfig({"field1": "42", "field2": "3.14", "field3": "hello"})
    assert config.field1 == 42  # type: ignore
    assert config.field2 == 3.14  # type: ignore
    assert config.field3 == "hello"  # type: ignore


def test_init__missing_field_raises_error():
    """Test that missing fields in data dictionary raise a helpful error."""

    class MissingFieldConfig(Config):
        field_links = [("field1", float), ("field2", int)]

    try:
        config = MissingFieldConfig({"field1": "42.0"})  # Missing field2
        assert False, "Should have raised ValueError for missing field2"
    except ValueError as e:
        assert "Missing required field 'field2'" in str(e)
        assert "MissingFieldConfig" in str(e)


def test_init__empty_field_links_works():
    """Test that configs with no field links work (edge case)."""

    class EmptyConfig(Config):
        field_links = []

    config = EmptyConfig({})
    # Should work without any fields defined
    assert hasattr(config, "field_links")
    assert config.field_links == []


def test_init__wrong_type_field_raises_error():
    """Test that type conversion errors are caught."""

    class TypeCheckConfig(Config):
        field_links = [("field1", float)]  # Requires float

    try:
        config = TypeCheckConfig({"field1": "not_a_number"})
        assert False, "Should have raised error for invalid number"
    except ValueError, TypeError:
        # The error message includes the original conversion error
        pass  # This test just verifies the code handles bad input gracefully


def test_serialize__multiple_fields():
    """Test that serialization works after init with various field types."""

    class SerializeConfig(Config):
        field_links = [
            ("field1", int),
            ("field2", float),
            ("field3", str),
        ]

    config = SerializeConfig({"field1": "42", "field2": "3.14", "field3": "hello"})
    serialized = config.serialize()
    assert serialized == {"field1": 42, "field2": 3.14, "field3": "hello"}
