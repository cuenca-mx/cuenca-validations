from typing import Optional, Type

from pydantic import PositiveInt, StrictInt, constr

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


def digits(
    min_length: Optional[int] = None, max_length: Optional[int] = None
) -> Type[str]:
    return constr(regex=r'^\d+$', min_length=min_length, max_length=max_length)
