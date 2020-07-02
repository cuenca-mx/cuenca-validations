import datetime as dt
from enum import Enum
from typing import Any, Callable

from .errors import NotDigitError


def sanitize_dict(d: dict):
    for k, v in d.items():
        d[k] = sanitize_item(v)


def sanitize_item(item: Any, default: Callable = None) -> Any:
    """
    :param item: item to be sanitized
    :param default: Optional function to be used when there is no case
    for this type of item, default `None` it returns the item as is.
    """
    if isinstance(item, dt.date):
        if isinstance(item, dt.datetime) and not item.tzinfo:
            rv = item.astimezone(dt.timezone.utc).isoformat()
        else:
            rv = item.isoformat()
    elif isinstance(item, Enum):
        rv = item.value
    elif hasattr(item, 'to_dict'):
        rv = item.to_dict()
    elif default:
        rv = default(item)
    else:
        rv = item
    return rv


def validate_digits(value: str) -> str:
    if not value.isdigit():
        raise NotDigitError
    return value
