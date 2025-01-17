__all__ = [
    '__version__',
    'types',
    'typing',
    'validators',
]

from pydantic_extra_types.phone_numbers import PhoneNumber

from . import types, typing, validators
from .version import __version__

PhoneNumber.phone_format = 'E164'
