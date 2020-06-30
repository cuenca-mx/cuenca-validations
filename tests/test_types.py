import datetime as dt
import json
from dataclasses import dataclass
from enum import Enum

import pytest

from cuenca_validations import CJSONEncoder, QueryParams, SantizedDict, Status


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
