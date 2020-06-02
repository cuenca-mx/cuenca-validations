from typing import ClassVar

from pydantic import PositiveInt, StrictInt
from pydantic.types import PaymentCardNumber as PydanticPaymentCardNumber


class PaymentCardNumber(PydanticPaymentCardNumber):
    min_length: ClassVar[int] = 16
    max_length: ClassVar[int] = 16


class StrictPositiveInt(StrictInt, PositiveInt):
    """
    - StrictInt: ensures a float isn't passed in by accident
    - PositiveInt: ensures the value is above 0
    """

    ...
