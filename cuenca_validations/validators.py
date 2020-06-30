__all__ = ['digits', 'sanitize_dict']

import datetime as dt
from enum import Enum
from typing import Optional, Type

from .types import Digits


def sanitize_dict(d: dict):
    for k, v in d.items():
        if isinstance(v, dt.date):
            d[k] = v.isoformat()
        elif isinstance(v, Enum):
            d[k] = v.value


def digits(
    min_length: Optional[int] = None, max_length: Optional[int] = None
) -> Type[str]:
    namespace = dict(min_length=min_length, max_length=max_length)
    return type('DigitsValue', (Digits,), namespace)
