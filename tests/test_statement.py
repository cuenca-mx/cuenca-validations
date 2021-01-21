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
    assert exc_info.value.errors()[0] == dict(
        loc=('month',),
        type='value_error',
        msg='month must be in 1..12',
    )


def test_invalid_current_month():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year + 1, month=1)
    assert exc_info.value.errors()[0] == dict(
        loc=('month',),
        type='value_error',
        msg=f'{date_now.year + 1}-1 is not a valid year-month pair',
    )


def test_invalid_future_month():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year, month=date_now.month)
    assert exc_info.value.errors()[0] == dict(
        loc=('month',),
        type='value_error',
        msg=f'{date_now.year}-{date_now.month} is not a valid year-month pair',
    )
