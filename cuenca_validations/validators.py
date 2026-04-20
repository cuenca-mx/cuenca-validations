import base64
import datetime as dt
import re
import unicodedata
from enum import Enum
from typing import Any, Callable, Optional, Union

SANITIZE_PHONE_NUMBER = re.compile(r'[+.()\-\s]')
STRIP_MX_MOBILE_PREFIX = re.compile(r'(52)(?:(?:044)|1)?(\d{10})$')
STRIP_US_DUPLICATE_PREFIX = re.compile(r'^11(\d{10})$')


def normalize_email(email: str) -> str:
    """Lowercase email and strip plus labels from the local part.

    mateohhr@Yahoo.com          -> mateohhr@yahoo.com
    guerradzul+cuenca@gmail.com -> guerradzul@gmail.com
    """
    local, _, domain = email.partition('@')
    return f'{local.split("+")[0]}@{domain}'.lower()


def normalize_phone_number(phone_number: str) -> str:
    """Sanitize and normalize phone numbers to E.164 format.

    Handles:
    - Special characters: +52 (55) 1234-5678 -> +525512345678
    - MX mobile prefix:   +5215512345678     -> +525512345678
    - MX 044 prefix:      +520445512345678   -> +525512345678
    - US duplicate prefix: +116504401222     -> +16504401222
    """
    pn = SANITIZE_PHONE_NUMBER.sub('', phone_number)
    pn = STRIP_MX_MOBILE_PREFIX.sub(r'\1\2', pn)
    pn = STRIP_US_DUPLICATE_PREFIX.sub(r'1\1', pn)
    return f'+{pn}'


def normalize_name(name: str) -> str:
    """Normalize names for search/index matching.

    Strips accents, lowercases, and collapses internal whitespace.

    Raúl  Andrés   -> raul andres
    MARÍA JOSÉ     -> maria jose
    """
    collapsed = ' '.join(name.split())
    nfkd = unicodedata.normalize('NFKD', collapsed)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower()


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
