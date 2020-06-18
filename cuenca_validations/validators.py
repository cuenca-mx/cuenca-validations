__all__ = ['sanitize_dict']

import datetime as dt
from enum import Enum


def sanitize_dict(d: dict):
    for k, v in d.items():
        if isinstance(v, dt.date):
            d[k] = v.isoformat()
        elif isinstance(v, Enum):
            d[k] = v.value
