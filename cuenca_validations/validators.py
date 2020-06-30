import datetime as dt
from enum import Enum
from typing import Any

__all__ = ['sanitize_dict']


def sanitize_dict(d: dict):
    for k, v in d.items():
        try:
            d[k] = sanitize_item(v)
        except AttributeError:
            ...


def sanitize_item(item: Any) -> Any:
    if isinstance(item, dt.date):
        result = item.isoformat() + 'Z'  # Siempre usamos UTC
    elif isinstance(item, Enum):
        result = item.value
    else:
        result = item.to_dict()
    return result
