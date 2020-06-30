import json
from typing import TYPE_CHECKING, Optional, Type

from pydantic import ConstrainedStr, NotDigitError, PositiveInt, StrictInt

from ..validators import sanitize_dict, sanitize_item

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class SantizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)


class CJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            encoded = sanitize_item(o)
        except AttributeError:
            encoded = super().default(o)
        return encoded


class StrictPositiveInt(StrictInt, PositiveInt):
    """
    - StrictInt: ensures a float isn't passed in by accident
    - PositiveInt: ensures the value is above 0
    """

    ...


def digits(
    min_length: Optional[int] = None, max_length: Optional[int] = None
) -> Type[str]:
    namespace = dict(min_length=min_length, max_length=max_length)
    return type('DigitsValue', (Digits,), namespace)


class Digits(ConstrainedStr):
    @classmethod
    def validate_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise NotDigitError
        return value

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate_digits
        yield cls
