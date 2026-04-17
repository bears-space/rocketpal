from bears_flight_simulation.core.config import Config


def test_init__empty():
    config = Config({})
    assert isinstance(config.__dict__, dict)


def test_init__one_field():
    class OneFieldConfig(Config):
        field_links = [("field1", int)]

    config = OneFieldConfig({"field1": "42"})
    assert config.__dict__.get("field1") == 42


def test_init__multiple_fields():
    class MultipleFieldsConfig(Config):
        field_links = [
            ("field1", int),
            ("field2", float),
            ("field3", str),
        ]

    config = MultipleFieldsConfig({"field1": "42", "field2": "3.14", "field3": "hello"})
    assert config.__dict__.get("field1") == 42
    assert config.__dict__.get("field2") == 3.14
    assert config.__dict__.get("field3") == "hello"


def test_serialize__multiple_fields():
    class MultipleFieldsConfig(Config):
        field_links = [
            ("field1", int),
            ("field2", float),
            ("field3", str),
        ]

    config = MultipleFieldsConfig({"field1": "42", "field2": "3.14", "field3": "hello"})
    assert config.serialize() == {"field1": 42, "field2": 3.14, "field3": "hello"}
