from cuenca_validations.types import uuid_field


def test_uuid_field_without_prefix():
    generator = uuid_field()
    uuid_str = generator()
    assert isinstance(uuid_str, str)
    assert len(uuid_str) == 22
    assert generator() != generator()


def test_uuid_field_with_prefix():
    prefix = 'AK'
    generator = uuid_field(prefix)
    uuid_str = generator()
    assert isinstance(uuid_str, str)
    assert uuid_str.startswith(prefix)
    assert len(uuid_str) == 22 + len(prefix)
    assert generator() != generator()


def test_multiple_generators():
    gen1 = uuid_field('CA')
    gen2 = uuid_field('TR')
    uuid1 = gen1()
    uuid2 = gen2()
    assert uuid1.startswith('CA')
    assert uuid2.startswith('TR')
    assert uuid1 != uuid2
