from pydantic import PositiveInt, StrictInt

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
