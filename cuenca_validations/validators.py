import datetime as dt
from enum import Enum
from typing import Any

__all__ = ['sanitize_dict']


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
