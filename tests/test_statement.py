import datetime as dt

import pytest
from pydantic import ValidationError

from cuenca_validations.types import StatementQuery

date_now = dt.date.today()


def test_invalid_year():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year + 1, month=1)
    assert exc_info.value.errors()[0] == dict(
        loc=('month',),
        type='value_error',
        msg='You cannot check the current year',
    )


def test_invalid_year_month():
    with pytest.raises(ValidationError) as exc_info:
        StatementQuery(year=date_now.year, month=date_now.month)
    assert exc_info.value.errors()[0] == dict(
        loc=('month',),
        type='value_error',
        msg='You cannot check the current month',
    )
