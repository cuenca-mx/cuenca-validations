import datetime as dt
import json
from dataclasses import dataclass
from enum import Enum

import pytest
from pydantic import BaseModel

from cuenca_validations import (
    CJSONEncoder,
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


def test_json_encoder():
    class EnumTest(Enum):
        s, p, e, i, d = range(5)

    @dataclass
    class TestClass:
        uno: str

        def to_dict(self):
            return dict(uno=self.uno, dos='dos')

    now = dt.datetime.utcnow()
    test_class = TestClass(uno='uno')

    to_encode = dict(enum=EnumTest.s, now=now, test_class=test_class,)

    encoded = json.dumps(to_encode, cls=CJSONEncoder)
    decoded = json.loads(encoded)

    assert decoded['enum'] == 0
    assert decoded['now'] == now.isoformat() + 'Z'
    assert decoded['test_class']['uno'] == 'uno'
    assert decoded['test_class']['dos'] == 'dos'


def test_invalid_class():
    class ClassWithoutToDict:
        ...

    invalid_class = ClassWithoutToDict()
    with pytest.raises(TypeError):
        json.dumps(invalid_class, cls=CJSONEncoder)


def test_only_digits():
    class Accounts(BaseModel):
        number: digits(5, 8)

    acc = Accounts(number='123456')
    assert acc.number == '123456'


@pytest.mark.parametrize(
    'number, error',
    [
        ('123', 'value_error.any_str.min_length'),
        ('1234567890', 'value_error.any_str.max_length'),
        ('no_123', 'value_error.payment_card_number.digits'),
    ],
)
def test_invalid_digits(number, error):
    class Accounts(BaseModel):
        number: digits(5, 8)

    with pytest.raises(ValueError) as exception:
        Accounts(number=number)
    assert error in str(exception)
