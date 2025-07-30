import datetime as dt
import uuid
from base64 import urlsafe_b64encode
from typing import Callable, Optional, Union

from dateutil.relativedelta import relativedelta
from pydantic.fields import FieldInfo

from .general import LogConfig
from .identities import Curp


def uuid_field(prefix: str = '') -> Callable[[], str]:
    def base64_uuid_func() -> str:
        return prefix + urlsafe_b64encode(uuid.uuid4().bytes).decode()[:-2]

    return base64_uuid_func


def get_log_config(field: FieldInfo) -> Optional[LogConfig]:
    """Helper function to find LogConfig in field metadata"""
    try:
        return next(m for m in field.metadata if isinstance(m, LogConfig))
    except StopIteration:
        return None


def get_birth_date_from_curp(curp: Curp) -> dt.date:
    curp_date = curp[4:10]  # YYMMDD
    yy = int(curp_date[:2])
    current_yy = dt.date.today().year % 100
    century = '19' if yy > current_yy else '20'
    birth_date = dt.datetime.strptime(century + curp_date, '%Y%m%d').date()
    return birth_date


def validate_age_requirement(birth_date: Union[dt.date, Curp]) -> dt.date:
    if isinstance(birth_date, str):
        birth_date = get_birth_date_from_curp(birth_date)

    current_date = dt.date.today()
    if relativedelta(current_date, birth_date).years < 18:
        raise ValueError('User does not meet age requirement.')
    return birth_date
