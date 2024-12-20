import datetime as dt

import pytest
from pydantic import ValidationError

from cuenca_validations.types import StatementQuery

date_now = dt.date.today()


def test_valid_year_month():
    statement = StatementQuery(year=2020, month=12)
    assert statement.year == 2020
    assert statement.month == 12


def test_invalid_month():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year, month=13)
    assert exc_info.value.errors()[0]['type'] == 'value_error'
    assert exc_info.value.errors()[0]['loc'] == ('month',)
    assert 'month must be in 1..12' in exc_info.value.errors()[0]['msg']


def test_invalid_current_month():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year + 1, month=1)
    error = exc_info.value.errors()[0]
    assert error['loc'] == ('month',)
    assert error['type'] == 'value_error'
    assert (
        error['msg']
        == f'Value error, {date_now.year + 1}-1 is not a valid year-month pair'
    )


def test_invalid_future_month():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year, month=date_now.month)
    error = exc_info.value.errors()[0]
    assert error['loc'] == ('month',)
    assert error['type'] == 'value_error'
    assert error['msg'] == (
        f'Value error, '
        f'{date_now.year}-{date_now.month} '
        'is not a valid year-month pair'
    )
