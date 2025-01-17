import base64
import datetime as dt
from enum import Enum
from typing import Any, Callable, Optional, Union

from dateutil.relativedelta import relativedelta


def sanitize_dict(d: dict) -> dict:
    for k, v in d.items():
        d[k] = sanitize_item(v)
    return d


def sanitize_item(
    item: Any, default: Optional[Callable[..., Any]] = None
) -> Any:
    """
    :param item: item to be sanitized
    :param default: Optional function to be used when there is no case
    for this type of item, default `None` it returns the item as is.
    """
    rv: Union[str, list[Any]]
    if isinstance(item, dt.date):
        if isinstance(item, dt.datetime) and not item.tzinfo:
            rv = item.astimezone(dt.timezone.utc).isoformat()
        else:
            rv = item.isoformat()
    elif isinstance(item, list):
        rv = [
            sanitize_dict(e) if isinstance(e, dict) else sanitize_item(e)
            for e in item
        ]
    elif isinstance(item, bytes):
        rv = base64.b64encode(item).decode('utf-8')
    elif isinstance(item, Enum):
        rv = item.value
    elif hasattr(item, 'to_dict'):
        rv = item.to_dict()
    elif default:
        rv = default(item)
    else:
        rv = item
    return rv


def validate_age_requirement(birth_date: dt.date) -> dt.date:
    current_date = dt.date.today()
    if relativedelta(current_date, birth_date).years < 18:
        raise ValueError('User does not meet age requirement.')
    return birth_date
