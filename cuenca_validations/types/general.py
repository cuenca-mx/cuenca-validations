from pydantic import ConstrainedStr, NotDigitError, PositiveInt, StrictInt

from ..validators import sanitize_dict


class SantizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)


class StrictPositiveInt(StrictInt, PositiveInt):
    """
    - StrictInt: ensures a float isn't passed in by accident
    - PositiveInt: ensures the value is above 0
    """

    ...


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
