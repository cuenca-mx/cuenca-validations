__all__ = ['sanitize_dict', 'sanitize_item']

import datetime as dt
from enum import Enum
from typing import Any

from .errors import NotDigitError


def sanitize_dict(d: dict):
    for k, v in d.items():
        d[k] = sanitize_item(v)


def sanitize_item(item: Any, default_function=None) -> Any:
    """
    :param item: item to be sanitized
    :param default_function: Optional function to be used when there is no case
    for this type of item, default `None` it returns the item as is.
    """
    result = item
    if isinstance(item, dt.date):
        result = item.isoformat() + 'Z'  # comply with iso8601
    elif isinstance(item, Enum):
        result = item.value
    else:
        try:
            result = item.to_dict()
        except AttributeError:
            if default_function:
                result = default_function(item)
    return result


def validate_digits(value: str) -> str:
    if not value.isdigit():
        raise NotDigitError
    return value
