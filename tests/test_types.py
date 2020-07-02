import datetime as dt
import json
from dataclasses import dataclass
from enum import Enum

import pytest
from pydantic import BaseModel

from cuenca_validations.types import (
    JSONEncoder,
    QueryParams,
    SantizedDict,
    Status,
    digits,
)


def test_sanitized_dict():
    now = dt.datetime.now()
    assert SantizedDict(
        status=Status.succeeded, time=now, hello='there'
    ) == dict(status='succeeded', time=now.isoformat() + 'Z', hello='there')


@pytest.mark.parametrize(
    'count, truth',
    [
        (1, True),
        ('1', True),
        (True, True),
        (False, False),
        (0, False),
        ('0', False),
    ],
)
def test_count(count, truth):
    q = QueryParams(count=count)
    assert q.count is truth


def test_dict():
    now = dt.datetime.utcnow()
    model = QueryParams(count=1, created_before=now)
    assert model.dict() == dict(count=1, created_before=now.isoformat() + 'Z')


class EnumTest(Enum):
    s, p, e, i, d = range(5)


@dataclass
class TestClass:
    uno: str

    def to_dict(self):
        return dict(uno=self.uno, dos='dos')


@pytest.mark.parametrize(
    'value, result',
    [
        (EnumTest.s, 0),
        (dt.date.today(), dt.date.today().isoformat() + 'Z'),
        (TestClass(uno='uno'), dict(uno='uno', dos='dos')),
    ],
)
def test_json_encoder(value, result):
    to_encode = dict(value=value)
    encoded = json.dumps(to_encode, cls=JSONEncoder)
    decoded = json.loads(encoded)

    assert decoded['value'] == result


def test_invalid_class():
    """
    For a class that doesn't have a `to_dict` method and it is not a type of
    `date` nor `Enum`, will use the default `json.JSONEncoder` method which
    raises a `TypeError`.
    """

    class ClassWithoutToDict:
        ...

    invalid_class = ClassWithoutToDict()
    with pytest.raises(TypeError):
        json.dumps(invalid_class, cls=JSONEncoder)


class Accounts(BaseModel):
    number: digits(5, 8)  # type: ignore


def test_only_digits():
    acc = Accounts(number='123456')
    assert acc.number == '123456'


@pytest.mark.parametrize(
    'number, error',
    [
        ('123', 'value_error.any_str.min_length'),
        ('1234567890', 'value_error.any_str.max_length'),
        ('no_123', 'value_error.digits'),
    ],
)
def test_invalid_digits(number, error):
    with pytest.raises(ValueError) as exception:
        Accounts(number=number)
    assert error in str(exception)
